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
        base = ['run', '--case', self.case, '--runner', 'claude', '--model', 'pinned-1', '--effort', 'medium',
                '--trials', '1', '--attempt', 'attempt-t', '--max-usd', '5']
        for flag, value in over.items():
            base.extend([flag] if value is True else [flag, str(value)])
        return base

    def record(self, attempt='attempt-t'):
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
        self.assertFalse((self.case_dir / 'attempt-t').exists())

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
        code, _, _ = self.call('grade', '--case', self.case, '--attempt', 'attempt-t')
        self.assertEqual(code, 0)
        blind = self.case_dir / 'attempt-t' / 'blind'
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
        args = ['run', '--case', self.case, '--runner', 'claude', '--model', 'pinned-1', '--effort', 'medium',
                '--trials', '1', '--attempt', 'attempt-t']
        out, err = io.StringIO(), io.StringIO()
        with patch.object(runner.subprocess, 'run') as spawn:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = runner.main(['--repo', str(self.repo), *args])
            spawn.assert_not_called()
        self.assertEqual(code, 2)
        self.assertIn('--max-usd', err.getvalue())
        self.assertFalse((self.case_dir / 'attempt-t').exists())

    def test_unpinned_model_is_refused(self):
        with self.assertRaises(ValueError):
            runner.build_argv('claude', '')

    def test_raised_deadline_above_the_case_is_refused(self):
        code, _, err = self.call(*self.run_args(**{'--timeout-seconds': 600}), cells=[])
        self.assertEqual(code, 2)
        self.assertIn('exceeds the deadline recorded', err)
        self.assertFalse((self.case_dir / 'attempt-t').exists())

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
        before = (self.case_dir / 'attempt-t' / 'attempt.json').read_bytes()
        code, _, err = self.call(*self.run_args(), cells=[completed(payload())])
        self.assertEqual(code, 2)
        self.assertIn('--resume', err)
        self.assertEqual((self.case_dir / 'attempt-t' / 'attempt.json').read_bytes(), before)

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
        stored = self.case_dir / 'attempt-t' / entry['output_path']
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
        kept = (self.case_dir / 'attempt-t' / 'cell-baseline-1.out').read_bytes()
        before = self.record()['arms'][0]
        code, _, _ = self.call(*self.run_args(**{'--resume': True}),
                               cells=[completed(payload('second')),
                                      completed(payload('third'))])
        self.assertEqual(code, 0)
        record = self.record()
        self.assertEqual(len(record['arms']), 3)
        self.assertEqual((self.case_dir / 'attempt-t' / 'cell-baseline-1.out').read_bytes(), kept)
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
                                     '--model', 'pinned-1', '--effort', 'medium', '--trials', '2')
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
        before = (self.case_dir / 'attempt-t' / 'attempt.json').read_bytes()
        scores = self.repo / 'scores.json'
        scores.write_text(json.dumps({'1': {'A': 70.0}}), encoding='utf-8')
        code, _, err = self.call('grade', '--case', self.case, '--attempt', 'attempt-t',
                                 '--scores', 'scores.json')
        self.assertEqual(code, 2)
        self.assertIn('Incomplete scores', err)
        self.assertEqual((self.case_dir / 'attempt-t' / 'attempt.json').read_bytes(), before)

    def test_grade_unblinds_each_score_onto_the_arm_the_permutation_names(self):
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        record = self.record()
        mapping = runner.blind_labels(f"demo|1|claude|{record['model']}",
                                      [e['arm'] for e in record['arms']])
        by_label = {'A': 10.0, 'B': 20.0, 'C': 30.0}
        (self.repo / 'scores.json').write_text(json.dumps({'1': by_label}), encoding='utf-8')
        code, _, _ = self.call('grade', '--case', self.case, '--attempt', 'attempt-t',
                               '--scores', 'scores.json', '--grader', 'tester', '--blinded')
        self.assertEqual(code, 0)
        graded = self.record()
        for entry in graded['arms']:
            self.assertEqual(entry['score'], by_label[mapping[entry['arm']]])
        self.assertTrue(graded['blinding']['revealed'])
        self.assertEqual(graded['grading']['grader'], 'tester')
        self.assertTrue(graded['grading']['blinded'])
        self.assertTrue(any('project participant' in n for n in graded['limitations']))


    # -- review 2026-09-25 findings ----------------------------------------

    def test_resume_refuses_a_changed_model_and_leaves_the_record_untouched(self):
        self.call(*self.run_args(**{'--arm': 'baseline'}), cells=[completed(payload('first'))])
        before = (self.case_dir / 'attempt-t' / 'attempt.json').read_bytes()
        args = self.run_args(**{'--resume': True})
        args[args.index('pinned-1')] = 'pinned-2'
        code, _, err = self.call(*args, cells=[])
        self.assertEqual(code, 2)
        self.assertIn('model', err)
        self.assertIn('argv', err)
        self.assertEqual((self.case_dir / 'attempt-t' / 'attempt.json').read_bytes(), before)

    def test_resume_refuses_a_changed_budget_deadline_or_trial_count(self):
        self.call(*self.run_args(**{'--arm': 'baseline'}), cells=[completed(payload('first'))])
        for flag, value, field in (('--max-usd', 50, 'budget.max_usd'),
                                   ('--timeout-seconds', 10, 'timeout_seconds'),
                                   ('--trials', 2, 'plan.trials')):
            with self.subTest(flag=flag):
                args = self.run_args(**{'--resume': True})
                if flag in args:
                    args[args.index(flag) + 1] = str(value)
                else:
                    args.extend([flag, str(value)])
                code, _, err = self.call(*args, cells=[])
                self.assertEqual(code, 2)
                self.assertIn(field, err)

    def test_one_arm_run_is_indeterminate_against_the_recorded_plan(self):
        code, out, _ = self.call(*self.run_args(**{'--arm': 'baseline'}),
                                 cells=[completed(payload('only'))])
        self.assertEqual(code, 1)
        record = self.record()
        self.assertEqual(record['plan'], {'arms': ['baseline', 'candidate', 'control'], 'trials': 1})
        self.assertEqual(record['status'], 'indeterminate')
        self.assertEqual(json.loads(out)['cells_planned'], 3)

    def test_grade_refuses_an_output_changed_after_execution(self):
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        (self.case_dir / 'attempt-t' / 'cell-candidate-1.out').write_bytes(payload('edited'))
        code, _, err = self.call('grade', '--case', self.case, '--attempt', 'attempt-t')
        self.assertEqual(code, 2)
        self.assertIn('cell-candidate-1.out', err)
        self.assertFalse((self.case_dir / 'attempt-t' / 'blind').exists())

    def test_grade_refuses_out_of_range_scores_and_never_regrades(self):
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        scores = self.repo / 'scores.json'
        scores.write_text(json.dumps({'1': {'A': 101, 'B': 1, 'C': 1}}), encoding='utf-8')
        code, _, err = self.call('grade', '--case', self.case, '--attempt', 'attempt-t',
                                 '--scores', 'scores.json')
        self.assertEqual(code, 2)
        self.assertIn('between 0 and 100', err)
        scores.write_text(json.dumps({'1': {'A': 1, 'B': 2, 'C': 3}}), encoding='utf-8')
        self.assertEqual(self.call('grade', '--case', self.case, '--attempt', 'attempt-t',
                                   '--scores', 'scores.json')[0], 0)
        graded = (self.case_dir / 'attempt-t' / 'attempt.json').read_bytes()
        code, _, err = self.call('grade', '--case', self.case, '--attempt', 'attempt-t',
                                 '--scores', 'scores.json')
        self.assertEqual(code, 2)
        self.assertIn('already graded', err)
        self.assertEqual((self.case_dir / 'attempt-t' / 'attempt.json').read_bytes(), graded)

    def test_codex_jsonl_yields_the_last_agent_message_and_turn_usage(self):
        # Event shape per openai/codex codex-rs/exec/src/exec_events.rs (main, retrieved 2026-09-25).
        stream = '\n'.join(json.dumps(event) for event in [
            {'type': 'thread.started', 'thread_id': 't'},
            {'type': 'item.completed', 'item': {'id': 'i0', 'type': 'reasoning', 'text': 'thinking'}},
            {'type': 'item.completed', 'item': {'id': 'i1', 'type': 'agent_message', 'text': 'draft'}},
            {'type': 'item.completed', 'item': {'id': 'i2', 'type': 'agent_message', 'text': 'final'}},
            {'type': 'turn.completed', 'usage': {'input_tokens': 7, 'output_tokens': 3}},
        ])
        usage, cost, response = runner.parse_payload(stream)
        self.assertEqual(response, 'final')
        self.assertEqual(usage, {'input_tokens': 7, 'output_tokens': 3})
        self.assertIsNone(cost)

    def test_cells_run_in_a_fresh_empty_directory_outside_the_repository(self):
        seen = []
        replies = [completed(payload()) for _ in range(3)]

        def spawn(argv, **kwargs):
            if argv[-1] == '--version':
                return subprocess.CompletedProcess(argv, 0, b'2.1.272\n', b'')
            cwd = Path(kwargs['cwd'])
            seen.append((cwd, sorted(cwd.iterdir())))
            return replies.pop(0)

        out, err = io.StringIO(), io.StringIO()
        with patch.object(runner.subprocess, 'run', side_effect=spawn), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = runner.main(['--repo', str(self.repo), *self.run_args()])
        self.assertEqual(code, 0, err.getvalue())
        self.assertEqual(len({cwd for cwd, _ in seen}), 3, 'cells shared a working directory')
        for cwd, contents in seen:
            self.assertEqual(contents, [])
            self.assertNotIn(self.repo, [cwd, *cwd.parents])
            for word in ('baseline', 'candidate', 'control', 'demo', 'eval'):
                self.assertNotIn(word, cwd.name)
            self.assertFalse(cwd.exists(), 'working directory was not removed')
        self.assertNotIn(str(self.repo), json.dumps(self.record()))

    def test_attempt_names_outside_the_attempt_prefix_are_refused(self):
        for bad in ('att', 'attempt-a/b', '../attempt-x'):
            with self.subTest(attempt=bad):
                args = self.run_args()
                args[args.index('attempt-t')] = bad
                code, _, err = self.call(*args, cells=[])
                self.assertEqual(code, 2)
                self.assertIn('attempt-', err)

    # -- review 2026-09-26 findings ----------------------------------------

    def test_resume_refuses_a_changed_cli_version_and_leaves_the_record_untouched(self):
        self.call(*self.run_args(**{'--arm': 'baseline'}), cells=[completed(payload('first'))],
                  version=b'2.1.272\n')
        before = (self.case_dir / 'attempt-t' / 'attempt.json').read_bytes()
        for probed in (b'2.1.273\n', None):
            with self.subTest(version=probed):
                code, _, err = self.call(*self.run_args(**{'--resume': True}), cells=[],
                                         version=probed)
                self.assertEqual(code, 2)
                self.assertIn('version changed', err)
                self.assertEqual((self.case_dir / 'attempt-t' / 'attempt.json').read_bytes(),
                                 before)

    def test_resume_under_the_same_cli_version_proceeds(self):
        self.call(*self.run_args(**{'--arm': 'baseline'}), cells=[completed(payload('first'))])
        code, _, err = self.call(*self.run_args(**{'--resume': True}),
                                 cells=[completed(payload()), completed(payload())])
        self.assertEqual(code, 0, err)
        self.assertEqual(self.record()['surface_version'], '2.1.272')

    def test_manifest_without_a_hash_for_a_declared_input_is_refused(self):
        manifest = self.case_dir / 'case.json'
        case = json.loads(manifest.read_text(encoding='utf-8'))
        del case['frozen_sha256']['arm-candidate.md']
        manifest.write_text(json.dumps(case, indent=2), encoding='utf-8')
        for argv in (('verify', '--case', self.case),
                     ('plan', '--case', self.case, '--runner', 'claude', '--model', 'pinned-1'),
                     tuple(self.run_args())):
            with self.subTest(action=argv[0]):
                code, _, err = self.call(*argv, cells=[])
                self.assertEqual(code, 2)
                self.assertIn('arm-candidate.md', err)
        self.assertFalse((self.case_dir / 'attempt-t').exists())

    def test_grade_refuses_while_a_run_holds_the_lock(self):
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        folder = self.case_dir / 'attempt-t'
        before = (folder / 'attempt.json').read_bytes()
        (folder / '.eval.lock').write_text('4242', encoding='utf-8')
        (self.repo / 'scores.json').write_text(json.dumps({'1': {'A': 1, 'B': 2, 'C': 3}}),
                                               encoding='utf-8')
        for extra in ((), ('--scores', 'scores.json')):
            with self.subTest(scores=bool(extra)):
                code, _, err = self.call('grade', '--case', self.case, '--attempt', 'attempt-t',
                                         *extra)
                self.assertEqual(code, 2)
                self.assertIn('.eval.lock', err)
        self.assertFalse((folder / 'blind').exists())
        self.assertEqual((folder / 'attempt.json').read_bytes(), before)
        self.assertTrue((folder / '.eval.lock').exists(), 'grade removed a lock it did not own')

    # -- review 2026-09-26 second pass -------------------------------------

    def test_grade_refuses_after_a_rubric_edit_on_both_paths(self):
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        folder = self.case_dir / 'attempt-t'
        before = (folder / 'attempt.json').read_bytes()
        (self.case_dir / 'rubric.md').write_text(RUBRIC.replace('60', '50'), encoding='utf-8')
        (self.repo / 'scores.json').write_text(json.dumps({'1': {'A': 1, 'B': 2, 'C': 3}}),
                                               encoding='utf-8')
        for extra in ((), ('--scores', 'scores.json')):
            with self.subTest(scores=bool(extra)):
                code, _, err = self.call('grade', '--case', self.case, '--attempt', 'attempt-t',
                                         *extra)
                self.assertEqual(code, 2)
                self.assertIn('rubric', err)
        self.assertFalse((folder / 'blind').exists())
        self.assertEqual((folder / 'attempt.json').read_bytes(), before)

    def test_grade_refuses_when_the_manifest_is_rehashed_after_the_run(self):
        """Re-freezing case.json to match an edit must not launder it past the attempt record."""
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        (self.case_dir / 'rubric.md').write_text(RUBRIC.replace('60', '50'), encoding='utf-8')
        manifest = self.case_dir / 'case.json'
        case = json.loads(manifest.read_text(encoding='utf-8'))
        case['frozen_sha256']['rubric.md'] = hashlib.sha256(
            (self.case_dir / 'rubric.md').read_bytes()).hexdigest()
        manifest.write_text(json.dumps(case, indent=2), encoding='utf-8')
        code, _, err = self.call('grade', '--case', self.case, '--attempt', 'attempt-t')
        self.assertEqual(code, 2)
        self.assertIn('rubric', err)
        self.assertFalse((self.case_dir / 'attempt-t' / 'blind').exists())

    def test_manifest_hashing_an_undeclared_name_is_refused(self):
        manifest = self.case_dir / 'case.json'
        case = json.loads(manifest.read_text(encoding='utf-8'))
        case['frozen_sha256']['notes.md'] = '0' * 64
        manifest.write_text(json.dumps(case, indent=2), encoding='utf-8')
        code, _, err = self.call('verify', '--case', self.case)
        self.assertEqual(code, 2)
        self.assertIn('notes.md', err)


    # -- explicit configuration and honest campaign accounting ------------

    def test_effort_is_required_and_cannot_select_an_implicit_default(self):
        for effort in (None, '', 'auto', 'default', 'medium extra'):
            with self.subTest(effort=effort), self.assertRaises(ValueError):
                runner.build_argv('claude', 'pinned-1', effort)
        args = self.run_args()
        index = args.index('--effort')
        del args[index:index + 2]
        with patch.object(runner.subprocess, 'run') as spawn:
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                runner.main(['--repo', str(self.repo), *args])
            self.assertEqual(exc.exception.code, 2)
            spawn.assert_not_called()
        self.assertFalse((self.case_dir / 'attempt-t').exists())

    def test_effort_uses_surface_specific_argv_and_is_recorded(self):
        claude = runner.build_argv('claude', 'pinned-1', 'medium')
        self.assertEqual(claude[claude.index('--effort') + 1], 'medium')
        codex = runner.build_argv('codex', 'gpt-6-sol', 'high')
        self.assertEqual(codex[codex.index('--config') + 1], 'model_reasoning_effort="high"')
        self.assertEqual(codex[-1], '-')
        self.call(*self.run_args(), cells=[completed(payload()) for _ in range(3)])
        self.assertEqual(self.record()['effort'], 'medium')
        self.assertEqual(self.record()['effort_source'], 'requested-not-runtime-attested')

    def test_resume_refuses_a_changed_effort_before_rewriting_evidence(self):
        self.call(*self.run_args(**{'--arm': 'baseline'}), cells=[completed(payload())])
        before = (self.case_dir / 'attempt-t' / 'attempt.json').read_bytes()
        code, _, err = self.call(*self.run_args(**{'--resume': True, '--effort': 'high'}),
                                 cells=[])
        self.assertEqual(code, 2)
        self.assertIn('effort', err)
        self.assertEqual((self.case_dir / 'attempt-t' / 'attempt.json').read_bytes(), before)

    def test_unmetered_permission_needs_a_reason_before_creating_an_attempt(self):
        code, _, err = self.call(*self.run_args(**{'--allow-unmetered-cells': 3}), cells=[])
        self.assertEqual(code, 2)
        self.assertIn('--unmetered-reason', err)
        self.assertFalse((self.case_dir / 'attempt-t').exists())

    def test_codex_refuses_without_explicit_cost_permission_before_spawning(self):
        args = self.run_args()
        args[args.index('claude')] = 'codex'
        with patch.object(runner.subprocess, 'run') as spawn:
            code, _, err = self.call(*args)
            spawn.assert_not_called()
        self.assertEqual(code, 2)
        self.assertIn('Codex has no supported cost report', err)
        self.assertFalse((self.case_dir / 'attempt-t').exists())

    def test_codex_stops_before_exceeding_its_known_unmetered_allowance(self):
        args = self.run_args(**{'--allow-unmetered-cells': 1,
                                '--unmetered-reason': 'approved token-only pilot'})
        args[args.index('claude')] = 'codex'
        code, _, _ = self.call(*args, cells=[completed(payload(cost=None))])
        self.assertEqual(code, 1)
        self.assertEqual(len(self.record()['arms']), 1)
        self.assertEqual(self.record()['budget']['unmetered_cells'], 1)
        self.assertEqual(self.record()['budget']['unmetered_reason'], 'approved token-only pilot')

    def test_partial_cost_is_not_presented_as_the_campaign_total(self):
        code, _, _ = self.call(*self.run_args(**{'--allow-unmetered-cells': 1,
                                                '--unmetered-reason': 'known telemetry gap'}),
                               cells=[completed(payload(cost=0.2)),
                                      completed(payload(cost=None)), completed(payload(cost=0.3))])
        self.assertEqual(code, 0)
        budget = self.record()['budget']
        self.assertIsNone(budget['spent_usd'])
        self.assertAlmostEqual(budget['reported_cost_usd'], 0.5)
        self.assertEqual(budget['cost_source'], 'partial')
        before = (self.case_dir / 'attempt-t' / 'attempt.json').read_bytes()
        code, _, err = self.call(*self.run_args(**{
            '--resume': True, '--allow-unmetered-cells': 1, '--unmetered-reason': 'different'}),
            cells=[])
        self.assertEqual(code, 2)
        self.assertIn('budget.unmetered_reason', err)
        self.assertEqual((self.case_dir / 'attempt-t' / 'attempt.json').read_bytes(), before)

    def test_unreported_timeout_stops_campaign_and_resume_keeps_the_observation(self):
        expired = subprocess.TimeoutExpired(['claude'], 300, output=b'partial', stderr=b'')
        code, _, _ = self.call(*self.run_args(), cells=[expired])
        self.assertEqual(code, 1)
        self.assertEqual(len(self.record()['arms']), 1)
        self.assertEqual(self.record()['budget']['unmetered_cells'], 1)
        entry = self.record()['arms'][0]
        before = (self.case_dir / 'attempt-t' / entry['output_path']).read_bytes()
        code, _, _ = self.call(*self.run_args(**{'--resume': True}), cells=[])
        self.assertEqual(code, 1)
        self.assertEqual(self.record()['arms'][0], entry)
        self.assertEqual((self.case_dir / 'attempt-t' / entry['output_path']).read_bytes(), before)

    def test_failed_cell_is_never_retried_or_overwritten_on_resume(self):
        self.call(*self.run_args(**{'--arm': 'baseline'}),
                  cells=[completed(payload('failed observation'), code=1)])
        entry = self.record()['arms'][0]
        before = (self.case_dir / 'attempt-t' / entry['output_path']).read_bytes()
        code, _, _ = self.call(*self.run_args(**{'--resume': True}),
                               cells=[completed(payload()), completed(payload())])
        self.assertEqual(code, 1)
        self.assertEqual(next(e for e in self.record()['arms'] if e['arm'] == 'baseline'), entry)
        self.assertEqual((self.case_dir / 'attempt-t' / entry['output_path']).read_bytes(), before)

    def test_reported_spend_stops_subsequent_cells_not_the_running_cell(self):
        code, _, _ = self.call(*self.run_args(**{'--max-usd': 0.1}),
                               cells=[completed(payload(cost=0.2))])
        self.assertEqual(code, 1)
        self.assertEqual(len(self.record()['arms']), 1)
        self.assertEqual(self.record()['budget']['spent_usd'], 0.2)

    def test_invalid_cost_is_unknown_not_a_free_or_negative_charge(self):
        for cost in (-1, True, float('nan'), float('inf')):
            with self.subTest(cost=cost):
                self.assertIsNone(runner.parse_payload(payload(cost=cost).decode())[1])
        self.assertEqual(runner.parse_payload(payload(cost=0).decode())[1], 0)

    def test_plan_reports_drift_with_a_nonzero_exit(self):
        (self.case_dir / 'task.md').write_text('changed', encoding='utf-8')
        with patch.object(runner.subprocess, 'run') as spawn:
            code, out, _ = self.call('plan', '--case', self.case, '--runner', 'claude',
                                     '--model', 'pinned-1', '--effort', 'medium')
            spawn.assert_not_called()
        self.assertEqual(code, 1)
        self.assertIn('task.md', json.loads(out)['frozen_drift'])

    def test_pilot_matrix_plans_offline_without_creating_attempts(self):
        pilot = json.loads((ROOT / 'tests/eval/pilot.json').read_text(encoding='utf-8'))
        self.assertFalse(pilot['execution_authorized'])
        case_dir = ROOT / pilot['case']
        before = sorted(p.name for p in case_dir.iterdir())
        for profile in pilot['profiles']:
            out = io.StringIO()
            with self.subTest(profile=profile['id']), patch.object(runner.subprocess, 'run') as spawn:
                with contextlib.redirect_stdout(out):
                    code = runner.main(['--repo', str(ROOT), 'plan', '--case', pilot['case'],
                                        '--runner', profile['runner'], '--model', profile['model'],
                                        '--effort', profile['effort'],
                                        '--trials', str(pilot['trials'])])
                spawn.assert_not_called()
                self.assertEqual(code, 0)
                plan = json.loads(out.getvalue())
                self.assertEqual(len(plan['cells']), 4)
                self.assertEqual(plan['effort'], profile['effort'])
                self.assertEqual(plan['frozen_drift'], [])
        self.assertEqual(sorted(p.name for p in case_dir.iterdir()), before)

if __name__ == '__main__':
    unittest.main()
