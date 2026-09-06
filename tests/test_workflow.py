"""Exercise the portable workflow gate; fixtures are retained without recursive cleanup."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'templates/workflow.py'
spec = importlib.util.spec_from_file_location('workflow', SCRIPT)
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix='houserules-workflow-'))
        (self.repo / 'code.txt').write_text('original', encoding='utf-8')

    def call(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), '--repo', str(self.repo), *args],
                              capture_output=True, text=True, encoding='utf-8')

    def start(self, *args):
        result = self.call('start', 'example', '--task', 'Verify fixture behavior',
                           '--target', 'code.txt', *args)
        self.assertEqual(result.returncode, 0, result.stderr)

    def run_code(self, code):
        return self.call('run', 'example', '--', sys.executable, '-c', code)

    def state(self):
        return json.loads((self.repo / 'work/example/workflow.json').read_text())

    def test_pass_then_reject_redundant_run(self):
        self.start()
        code = "print('checked')"
        self.assertEqual(self.run_code(code).returncode, 0)
        self.assertEqual(self.call('status', 'example').returncode, 0)
        summary = json.loads(self.call('status', 'example').stdout)
        self.assertNotIn('runs', summary)  # Full history stays on disk, not in routine agent context.
        self.assertEqual(summary['attempts'], 1)
        self.assertEqual(summary['latest_log'], 'work/example/run-001.log')
        before = self.state()
        self.assertEqual(self.run_code(code).returncode, 2)
        self.assertEqual(self.state(), before)
        self.assertIsNone(before['runs'][0]['usage'])

    def test_failed_run_consumes_budget_before_next_side_effect(self):
        self.start('--max-runs', '1')
        self.assertEqual(self.run_code('raise SystemExit(3)').returncode, 1)
        result = self.run_code("open('unwanted.txt', 'w').write('bad')")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.repo / 'unwanted.txt').exists())
        self.assertEqual(len(self.state()['runs']), 1)

    def test_changed_target_invalidates_pass_and_allows_recheck(self):
        self.start()
        self.assertEqual(self.run_code("print('check')").returncode, 0)
        (self.repo / 'code.txt').write_text('changed')
        status = self.call('status', 'example')
        self.assertEqual(status.returncode, 1)
        self.assertEqual(json.loads(status.stdout)['result'], 'stale')
        self.assertEqual(self.run_code("print('check')").returncode, 0)

    def test_changed_log_invalidates_pass(self):
        self.start()
        self.run_code("print('check')")
        (self.repo / 'work/example/run-001.log').write_text('replacement')
        self.assertEqual(self.call('status', 'example').returncode, 1)

    def test_command_changing_its_inputs_does_not_establish_stable_pass(self):
        self.start()
        result = self.run_code("open('code.txt', 'w').write('changed')")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['verified'])

    def test_missing_future_target_does_not_pass(self):
        result = self.call('start', 'example', '--task', 'New file', '--target', 'future.txt')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.run_code("print('not implemented')").returncode, 1)

    def test_timeout_retains_attempt_and_stops_next_run(self):
        self.start('--max-seconds', '0.05')
        self.assertEqual(self.run_code('import time; time.sleep(5)').returncode, 1)
        self.assertEqual(self.state()['runs'][0]['outcome'], 'timeout')
        self.assertEqual(self.run_code("print('retry')").returncode, 2)

    def test_invalid_ids_and_budget_are_read_only(self):
        for task, budget in [('../escape', '1'), ('valid', '0'), ('valid', 'nan')]:
            result = self.call('start', task, '--task', 'x', '--target', 'code.txt', '--max-seconds', budget)
            self.assertEqual(result.returncode, 2)
        self.assertFalse((self.repo / 'work').exists())

    def test_target_paths_reject_escape_directories_and_self_reference(self):
        for target in ['../escape', str(self.repo / 'code.txt'), '.', 'work/example/workflow.json',
                       'work/another/workflow.json', 'work/another/run-001.log']:
            result = self.call('start', 'example', '--task', 'x', '--target', target)
            self.assertEqual(result.returncode, 2, target)
        self.assertFalse((self.repo / 'work').exists())

    def test_cross_task_targets_preserve_existing_records(self):
        self.start()
        self.run_code("print('verified')")
        before = {p.relative_to(self.repo): p.read_bytes() for p in self.repo.rglob('*') if p.is_file()}
        for target in ['work/example/workflow.json', 'work/example/run-001.log']:
            result = self.call('start', 'other', '--task', 'x', '--target', target)
            self.assertEqual(result.returncode, 2)
            self.assertIn(target, result.stderr)
        self.assertEqual(before, {p.relative_to(self.repo): p.read_bytes()
                                 for p in self.repo.rglob('*') if p.is_file()})

    def test_existing_task_and_lock_are_preserved(self):
        self.start()
        original = self.state()
        self.assertEqual(self.call('start', 'example', '--task', 'replace', '--target', 'code.txt').returncode, 2)
        self.assertEqual(self.state(), original)
        lock = self.repo / 'work/example/.workflow.lock'
        lock.write_text('another worker')
        self.assertEqual(self.run_code("print('unexpected')").returncode, 2)
        self.assertEqual(lock.read_text(), 'another worker')

    def test_blocked_executable_is_recorded(self):
        self.start()
        self.assertEqual(self.call('run', 'example', '--', str(self.repo / 'absent-executable')).returncode, 1)
        self.assertEqual(self.state()['runs'][0]['outcome'], 'blocked')

    def test_interrupted_run_blocks_retry(self):
        self.start()
        path = self.repo / 'work/example/workflow.json'
        state = self.state()
        state['runs'] = [{'outcome': 'running', 'elapsed_seconds': None}]
        path.write_text(json.dumps(state))
        self.assertEqual(self.run_code("print('retry')").returncode, 2)

    def test_raw_usage_is_retained_without_adding_cached_subcounts(self):
        self.start()
        event = {'type': 'turn.completed', 'usage': {'input_tokens': 20, 'cached_input_tokens': 10, 'output_tokens': 3}}
        result = self.run_code('print(' + repr(json.dumps(event)) + ')')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.state()['runs'][0]['usage'], [event['usage']])


if __name__ == '__main__':
    unittest.main()
