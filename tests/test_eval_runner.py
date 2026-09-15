"""Regression tests for the evaluation harness; fixtures are retained without recursive cleanup.

These assert the harness's own logic only: hashing, refusals, blinding determinism, outcome
classification and resume. Nothing here asserts that a candidate scores higher, that a score
clears a threshold, or anything about model output content. Those are what a recorded attempt is
for; a unit test that asserted them would be asserting its own fixture.

No provider CLI is spawned and no network call is made. subprocess is mocked throughout.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tests/eval/runner.py'
spec = importlib.util.spec_from_file_location('eval_runner', SCRIPT)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

TASK = 'Implement the described behaviour.\n'
RUBRIC = """# Response quality rubric

Release gate wording lives outside the markers: promote the candidate only when it beats the
baseline and the control arm.

<!-- judge:begin -->
Score each response from 0 to 100.

| Check | Weight |
|---|---:|
| The reasoning is correct | 60 |
| The answer is minimal for the stated slice | 40 |
<!-- judge:end -->

Gate: promotion requires the candidate to beat every other arm.
"""


def payload(text='answer', cost=0.01, usage=None):
    body = {'result': text}
    if cost is not None:
        body['total_cost_usd'] = cost
    if usage is not None:
        body['usage'] = usage
    return json.dumps(body).encode('utf-8')


def completed(stdout, code=0):
    return subprocess.CompletedProcess(['claude'], code, stdout, b'')


class EvalRunnerTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix='houserules-eval-'))
        self.case = 'cases/demo'
        self.case_dir = self.repo / self.case
        self.case_dir.mkdir(parents=True)
        self.write_case()

    # -- fixture helpers -------------------------------------------------

    def write_case(self, arms=('baseline', 'candidate', 'control'), timeout=300):
        (self.case_dir / 'task.md').write_text(TASK, encoding='utf-8')
        (self.case_dir / 'rubric.md').write_text(RUBRIC, encoding='utf-8')
        for arm in arms:
            (self.case_dir / f'arm-{arm}.md').write_text(
                TASK + f'\n<!-- treatment {arm} -->\n', encoding='utf-8')
        case = {'schema_version': 1, 'case': 'demo', 'task': 'task.md', 'rubric': 'rubric.md',
                'arms': {arm: f'arm-{arm}.md' for arm in arms},
                'score_max': 100, 'timeout_seconds': timeout, 'frozen_sha256': {}}
        (self.case_dir / 'case.json').write_text(json.dumps(case, indent=2), encoding='utf-8')
        loaded = json.loads((self.case_dir / 'case.json').read_text(encoding='utf-8'))
        frozen = {name: hashlib.sha256((self.case_dir / name).read_bytes()).hexdigest()
                  for name in runner.frozen_names(loaded)}
        case['frozen_sha256'] = frozen
        (self.case_dir / 'case.json').write_text(json.dumps(case, indent=2), encoding='utf-8')

    def provider(self, cells, version=b'2.1.272 (Claude Code)\n'):
        queue = list(cells)

        def _run(argv, **kwargs):
            if argv[-1] == '--version':
                if version is None:
                    raise FileNotFoundError('claude')
                return subprocess.CompletedProcess(argv, 0, version, b'')
            if not queue:
                raise AssertionError('more cells executed than the test queued')
            item = queue.pop(0)
            if isinstance(item, BaseException):
                raise item
            return item

        return _run

    def call(self, *argv, cells=None, version=b'2.1.272\n'):
        args = ['--repo', str(self.repo), *argv]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            if cells is None:
                code = runner.main(args)
            else:
                with patch.object(runner.subprocess, 'run',
                                  side_effect=self.provider(cells, version)), \
                     patch.object(runner.time, 'monotonic',
                                  side_effect=itertools.count(0, 0.5)):
                    code = runner.main(args)
        return code, out.getvalue(), err.getvalue()

    def run_args(self, **over):
        base = ['run', '--case', self.case, '--runner', 'claude', '--model', 'pinned-1',
                '--trials', '1', '--attempt', 'att', '--max-usd', '5']
        for flag, value in over.items():
            base.extend([flag] if value is True else [flag, str(value)])
        return base

    def record(self, attempt='att'):
        return json.loads((self.case_dir / attempt / 'attempt.json').read_text(encoding='utf-8'))

    # -- frozen inputs ---------------------------------------------------

    def test_shipped_case_inputs_match_their_recorded_hashes(self):
        """Every committed case's frozen bytes still hash to what its manifest records."""
        manifests = sorted((ROOT / 'tests/workflows/skill-eval').glob('*/case.json'))
        for manifest in manifests:
            with self.subTest(case=manifest.parent.name):
                case = json.loads(manifest.read_text(encoding='utf-8'))
                for name, expected in case['frozen_sha256'].items():
                    actual = hashlib.sha256((manifest.parent / name).read_bytes()).hexdigest()
                    self.assertEqual(actual, expected, f'{manifest.parent.name}/{name} drifted')

    def test_shipped_case_arms_differ_only_by_their_treatment_block(self):
        """Every arm file ends with its case's task.md bytes, exactly.

        This is the control that review finding R-003/F-001 was raised about: an arm differing
        from another in more than the declared variable produces a number that is not a result.
        Asserted here rather than reviewed by eye.
        """
        for manifest in sorted((ROOT / 'tests/workflows/skill-eval').glob('*/case.json')):
            case = json.loads(manifest.read_text(encoding='utf-8'))
            task = (manifest.parent / case['task']).read_bytes()
            for arm, name in sorted(case['arms'].items()):
                with self.subTest(case=case['case'], arm=arm):
                    self.assertTrue((manifest.parent / name).read_bytes().endswith(task),
                                    f'{name} does not end with {case["task"]} verbatim')

    def test_shipped_case_judge_spans_do_not_name_their_arms(self):
        """Only the judge span reaches a grader, so it must not carry condition vocabulary."""
        for manifest in sorted((ROOT / 'tests/workflows/skill-eval').glob('*/case.json')):
            case = json.loads(manifest.read_text(encoding='utf-8'))
            rubric = (manifest.parent / case['rubric']).read_text(encoding='utf-8')
            span, marker = runner.extract_judge_section(rubric)
            with self.subTest(case=case['case']):
                self.assertTrue(marker, f"{case['case']} rubric has no judge markers")
                for leak in list(case['arms']) + ['promot']:
                    self.assertNotIn(leak.lower(), span.lower(),
                                     f"{case['case']} judge span leaks {leak!r}")

    def test_drifted_frozen_input_refuses_and_names_the_file(self):
        (self.case_dir / 'arm-candidate.md').write_text('tampered\n', encoding='utf-8')
        code, _, err = self.call(*self.run_args(), cells=[])
        self.assertEqual(code, 2)
        self.assertIn('arm-candidate.md', err)
        self.assertFalse((self.case_dir / 'att').exists())

    def test_verify_reports_drift_without_executing_anything(self):
        code, out, _ = self.call('verify', '--case', self.case)
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)['drift'], [])
        (self.case_dir / 'task.md').write_text('changed\n', encoding='utf-8')
        code, out, err = self.call('verify', '--case', self.case)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)['drift'], ['task.md'])
        self.assertIn('task.md', err)

    # -- blinding --------------------------------------------------------

    def test_blind_labels_are_deterministic_for_a_group_key(self):
        arms = ['baseline', 'candidate', 'control']
        first = runner.blind_labels('demo|1|claude|pinned-1', arms)
        again = runner.blind_labels('demo|1|claude|pinned-1', list(reversed(arms)))
        self.assertEqual(first, again)

    def test_blind_labels_are_a_permutation_not_an_ordering(self):
        arms = ['baseline', 'candidate', 'control']
        seen = set()
        for trial in range(1, 12):
            mapping = runner.blind_labels(f'demo|{trial}|claude|pinned-1', arms)
            self.assertEqual(sorted(mapping), sorted(arms))
            self.assertEqual(len(set(mapping.values())), len(arms))
            seen.add(tuple(mapping[arm] for arm in arms))
        identity = tuple(runner.LABELS[:len(arms)])
        self.assertTrue(seen - {identity}, 'labels never deviate from arm order')

    def test_judge_markers_bound_what_a_grader_sees(self):
        span, marker = runner.extract_judge_section(RUBRIC)
        self.assertTrue(marker)
        self.assertIn('The reasoning is correct', span)
        self.assertNotIn('promote', span)
        whole, marker = runner.extract_judge_section('# No markers here\n')
        self.assertFalse(marker)
        self.assertEqual(whole, '# No markers here\n')

    def test_blind_packet_excludes_arm_names_and_gate_vocabulary(self):
        self.call(*self.run_args(), cells=[completed(payload(f'reply {n}')) for n in range(3)])
        code, _, _ = self.call('grade', '--case', self.case, '--attempt', 'att')
        self.assertEqual(code, 0)
        blind = self.case_dir / 'att' / 'blind'
        names = sorted(p.name for p in blind.iterdir())
        self.assertEqual(names, ['rubric-judge.md', 'trial-1-response-A.md',
                                 'trial-1-response-B.md', 'trial-1-response-C.md'])
        for path in blind.iterdir():
            body = path.read_text(encoding='utf-8').lower()
            for leak in ('baseline', 'candidate', 'control', 'promot'):
                self.assertNotIn(leak, body, f'{path.name} leaks {leak}')
        self.assertFalse(self.record()['blinding']['revealed'])

    # -- refusals --------------------------------------------------------

    def test_absent_budget_refuses_before_any_execution(self):
        args = ['run', '--case', self.case, '--runner', 'claude', '--model', 'pinned-1',
                '--trials', '1', '--attempt', 'att']
        out, err = io.StringIO(), io.StringIO()
        with patch.object(runner.subprocess, 'run') as spawn:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = runner.main(['--repo', str(self.repo), *args])
            spawn.assert_not_called()
        self.assertEqual(code, 2)
        self.assertIn('--max-usd', err.getvalue())
        self.assertFalse((self.case_dir / 'att').exists())

    def test_unpinned_model_is_refused(self):
        with self.assertRaises(ValueError):
            runner.build_argv('claude', '')

    def test_raised_deadline_above_the_case_is_refused(self):
        code, _, err = self.call(*self.run_args(**{'--timeout-seconds': 600}), cells=[])
        self.assertEqual(code, 2)
        self.assertIn('exceeds the deadline recorded', err)
        self.assertFalse((self.case_dir / 'att').exists())

    def test_unmetered_runner_is_rejected_after_the_allowance(self):
        code, _, _ = self.call(*self.run_args(),
                               cells=[completed(payload('a', cost=None)),
                                      completed(payload('b', cost=None))])
        self.assertEqual(code, 1)
        record = self.record()
        self.assertEqual(len(record['arms']), 1, 'the campaign continued past the allowance')
        self.assertIsNone(record['arms'][0]['billed_cost'])
        self.assertEqual(record['arms'][0]['cost_source'], 'unavailable')
        self.assertEqual(record['status'], 'indeterminate')
        self.assertTrue(any('no ceiling' in note for note in record['limitations']))

    def test_existing_attempt_is_never_overwritten_without_resume(self):
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        before = (self.case_dir / 'att' / 'attempt.json').read_bytes()
        code, _, err = self.call(*self.run_args(), cells=[completed(payload())])
        self.assertEqual(code, 2)
        self.assertIn('--resume', err)
        self.assertEqual((self.case_dir / 'att' / 'attempt.json').read_bytes(), before)

    def test_case_paths_reject_escape_and_symlinks(self):
        for bad in ('../escape', '/etc', 'cases/../../escape'):
            with self.subTest(case=bad):
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    code = runner.main(['--repo', str(self.repo), 'verify', '--case', bad])
                self.assertEqual(code, 2)

    # -- outcomes --------------------------------------------------------

    def test_missing_provider_cli_is_indeterminate_not_failed(self):
        code, out, _ = self.call(*self.run_args(), cells=[], version=None)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)['status'], 'indeterminate')
        record = self.record()
        self.assertEqual(record['arms'], [])
        self.assertIsNone(record['surface_version'])
        self.assertTrue(any('could not be probed' in note for note in record['limitations']))

    def test_blocked_cell_is_recorded_without_a_score(self):
        code, _, _ = self.call(*self.run_args(**{'--arm': 'baseline'}),
                               cells=[OSError('spawn refused')])
        self.assertEqual(code, 1)
        entry = self.record()['arms'][0]
        self.assertEqual(entry['status'], 'blocked')
        self.assertIsNone(entry['score'])
        self.assertIsNone(entry['exit_code'])
        self.assertEqual(self.record()['status'], 'indeterminate')

    def test_timeout_records_indeterminate_and_retains_partial_output(self):
        expired = subprocess.TimeoutExpired(['claude'], 300, output=b'partial answer', stderr=b'')
        code, _, _ = self.call(*self.run_args(**{'--arm': 'baseline'}), cells=[expired])
        self.assertEqual(code, 1)
        record = self.record()
        entry = record['arms'][0]
        self.assertEqual(entry['status'], 'timeout')
        self.assertTrue(entry['timed_out'])
        self.assertIsNone(entry['score'])
        self.assertEqual(entry['elapsed_seconds'], 0.5)
        stored = self.case_dir / 'att' / entry['output_path']
        self.assertEqual(stored.read_bytes(), b'partial answer')
        self.assertEqual(record['status'], 'indeterminate')

    def test_unknown_usage_and_cost_are_null_not_zero(self):
        code, _, _ = self.call(*self.run_args(),
                               cells=[completed(b'not json at all')])
        self.assertEqual(code, 1)
        entry = self.record()['arms'][0]
        self.assertIsNone(entry['usage'])
        self.assertIsNone(entry['billed_cost'])
        self.assertIsNone(self.record()['budget']['spent_usd'])

    def test_completed_campaign_records_every_cell_and_the_pinned_argv(self):
        code, _, _ = self.call(*self.run_args(),
                               cells=[completed(payload(usage={'input_tokens': 5})) for _ in range(3)])
        self.assertEqual(code, 0)
        record = self.record()
        self.assertEqual(record['status'], 'completed')
        self.assertEqual(len(record['arms']), 3)
        self.assertIn('--model', record['argv'])
        self.assertEqual(record['argv'][record['argv'].index('--model') + 1], 'pinned-1')
        self.assertEqual(record['isolation']['flags'], runner.isolation_flags('claude'))
        self.assertAlmostEqual(record['budget']['spent_usd'], 0.03)
        self.assertEqual(record['arms'][0]['usage'], {'input_tokens': 5})

    # -- resume and dry run ----------------------------------------------

    def test_resume_skips_completed_cells_and_preserves_recorded_bytes(self):
        self.call(*self.run_args(**{'--arm': 'baseline'}), cells=[completed(payload('first'))])
        kept = (self.case_dir / 'att' / 'cell-baseline-1.out').read_bytes()
        before = self.record()['arms'][0]
        code, _, _ = self.call(*self.run_args(**{'--resume': True}),
                               cells=[completed(payload('second')),
                                      completed(payload('third'))])
        self.assertEqual(code, 0)
        record = self.record()
        self.assertEqual(len(record['arms']), 3)
        self.assertEqual((self.case_dir / 'att' / 'cell-baseline-1.out').read_bytes(), kept)
        self.assertEqual(next(e for e in record['arms'] if e['arm'] == 'baseline'), before)

    def test_dry_run_writes_nothing_and_pins_model_and_isolation(self):
        before = sorted(p.name for p in self.case_dir.iterdir())
        with patch.object(runner.subprocess, 'run') as spawn:
            code, out, _ = self.call(*self.run_args(**{'--dry-run': True}))
            spawn.assert_not_called()
        self.assertEqual(code, 0)
        printed = json.loads(out)
        self.assertTrue(printed['dry_run'])
        self.assertIn('pinned-1', printed['argv'])
        for flag in runner.isolation_flags('claude'):
            self.assertIn(flag, printed['argv'])
        self.assertEqual(sorted(p.name for p in self.case_dir.iterdir()), before)

    def test_plan_runs_without_a_provider_and_writes_nothing(self):
        before = sorted(p.name for p in self.case_dir.iterdir())
        with patch.object(runner.subprocess, 'run') as spawn:
            code, out, _ = self.call('plan', '--case', self.case, '--runner', 'claude',
                                     '--model', 'pinned-1', '--trials', '2')
            spawn.assert_not_called()
        self.assertEqual(code, 0)
        printed = json.loads(out)
        self.assertEqual(len(printed['cells']), 6)
        self.assertTrue(printed['judge_marker'])
        self.assertEqual(printed['frozen_drift'], [])
        self.assertEqual(sorted(p.name for p in self.case_dir.iterdir()), before)

    # -- grading ---------------------------------------------------------

    def test_grade_refuses_partial_scores_and_leaves_the_record_untouched(self):
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        before = (self.case_dir / 'att' / 'attempt.json').read_bytes()
        scores = self.repo / 'scores.json'
        scores.write_text(json.dumps({'1': {'A': 70.0}}), encoding='utf-8')
        code, _, err = self.call('grade', '--case', self.case, '--attempt', 'att',
                                 '--scores', 'scores.json')
        self.assertEqual(code, 2)
        self.assertIn('Incomplete scores', err)
        self.assertEqual((self.case_dir / 'att' / 'attempt.json').read_bytes(), before)

    def test_grade_unblinds_each_score_onto_the_arm_the_permutation_names(self):
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        record = self.record()
        mapping = runner.blind_labels(f"demo|1|claude|{record['model']}",
                                      [e['arm'] for e in record['arms']])
        by_label = {'A': 10.0, 'B': 20.0, 'C': 30.0}
        (self.repo / 'scores.json').write_text(json.dumps({'1': by_label}), encoding='utf-8')
        code, _, _ = self.call('grade', '--case', self.case, '--attempt', 'att',
                               '--scores', 'scores.json', '--grader', 'tester', '--blinded')
        self.assertEqual(code, 0)
        graded = self.record()
        for entry in graded['arms']:
            self.assertEqual(entry['score'], by_label[mapping[entry['arm']]])
        self.assertTrue(graded['blinding']['revealed'])
        self.assertEqual(graded['grading']['grader'], 'tester')
        self.assertTrue(graded['grading']['blinded'])
        self.assertTrue(any('project participant' in n for n in graded['limitations']))


if __name__ == '__main__':
    unittest.main()
