#!/usr/bin/env python3
"""Run a frozen baseline-vs-candidate skill evaluation and record revision-bound evidence.

Implements the requirements written in tests/workflows/prior-art/v2/README.md as one reusable
runner, in place of the per-attempt harness scripts recorded beside the prior-art attempts.
Standard library only; distribution-only, never an installed asset.

Bounding attempts, deadlines and spend is a usage control, not a sandbox. This runner does not
restrict what the provider CLI it spawns may do, and it cannot prove that CLI honoured the
isolation flags it was given.

The runner refuses rather than degrades. It stops when a frozen input no longer matches its
recorded hash, when a runner would execute without an explicit model pin, when no spend ceiling is
given, when a deadline is raised above the one the case recorded, when a resumed attempt would
run under settings other than the ones it recorded, and when a recorded output no longer hashes to
its record at grading time. Each refusal exists because an arm that differs from another arm in more
than the declared variable produces a number that looks like a result and is not one.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

SCHEMA_VERSION = 2
LABELS = ('A', 'B', 'C', 'D', 'E', 'F')

# Isolation is fixed per runner and deliberately not caller-settable. houserules installs an
# always-on AGENTS.md workflow block; without these flags the operator's own project, user and
# plugin configuration reaches the baseline arm and the comparison measures the skill against
# itself. Upstream ponytail published exactly that bug, and this repository's own R-003/F-001
# finding is the same failure class. See research/PRIOR-ART-EVAL-HARNESSES.md section 4.
RUNNERS = {
    'claude': {
        'profile': 'claude-isolated-v1',
        'base': ['claude', '--print', '--output-format', 'json'],
        'isolation': ['--setting-sources', '', '--strict-mcp-config', '--tools', ''],
        'model_flag': '--model',
        'tail': [],
        'version_argv': ['claude', '--version'],
    },
    'codex': {
        'profile': 'codex-isolated-v1',
        'base': ['codex', 'exec', '--json'],
        'isolation': ['--ignore-user-config', '--ephemeral', '--sandbox', 'read-only',
                      '--skip-git-repo-check'],
        'model_flag': '--model',
        'tail': ['-'],
        'version_argv': ['codex', '--version'],
    },
}

# A single path segment, so every attempt directory is covered by the -text rule in .gitattributes.
ATTEMPT_NAME = re.compile(r'attempt-[A-Za-z0-9._-]{1,120}')

JUDGE_BEGIN = '<!-- judge:begin -->'
JUDGE_END = '<!-- judge:end -->'


# safe_path and digest mirror templates/workflow.py. They are copied rather than imported:
# that file is an installed-asset source whose digests are manifest-tracked, and it binds state
# to work/, which .gitignore excludes while evaluation records must be committed.
def safe_path(repo, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise ValueError('Use a repository-relative path without ..')
    result = repo / path
    if not result.resolve().is_relative_to(repo):
        raise ValueError('Path leaves the repository')
    if any(p.is_symlink() for p in [result, *result.parents] if p != repo and repo in p.parents):
        raise ValueError('Symlink paths are not accepted')
    return result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError('must be finite and positive')
    return number


@contextmanager
def locked(folder):
    lock = folder / '.eval.lock'
    try:
        stream = lock.open('x', encoding='utf-8')
    except FileExistsError:
        raise ValueError(f'{lock} exists: another run holds this attempt. If no run is active, '
                         'a previous one crashed; delete the lock file and pass --resume') from None
    with stream:
        stream.write(str(os.getpid()))
    try:
        yield
    finally:
        lock.unlink()  # One explicitly created lock, never a directory cleanup.


def write_record(path, record):
    # Callers hold the attempt lock, so a leftover temporary is from a crashed run, never a live one.
    temporary = path.with_suffix('.json.tmp')
    with temporary.open('w', encoding='utf-8') as stream:
        json.dump(record, stream, indent=2, allow_nan=False)
        stream.write('\n')
    temporary.replace(path)


def read_case(repo, case_dir):
    """Load and validate case.json. Every declared input must exist and be a file."""
    manifest = safe_path(repo, f'{case_dir}/case.json')
    case = json.loads(manifest.read_text(encoding='utf-8'))
    if case.get('schema_version') != 1:
        raise ValueError('Unsupported case schema_version')
    for field in ('case', 'task', 'rubric', 'arms', 'frozen_sha256'):
        if field not in case:
            raise ValueError(f'case.json is missing {field}')
    if not isinstance(case['arms'], dict) or not case['arms']:
        raise ValueError('case.json must declare at least one arm')
    if len(case['arms']) > len(LABELS):
        raise ValueError(f'At most {len(LABELS)} arms are supported')
    if not isinstance(case.get('score_max'), (int, float)) or case['score_max'] <= 0:
        raise ValueError('case.json must declare a positive score_max')
    seconds = case.get('timeout_seconds')
    if not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or seconds <= 0:
        raise ValueError('case.json must declare a positive timeout_seconds')
    for name in frozen_names(case):
        if not safe_path(repo, f'{case_dir}/{name}').is_file():
            raise ValueError(f'Declared input is missing: {name}')
    # Drift is checked over recorded hashes, so an input with no recorded hash could change freely.
    unhashed = sorted(set(frozen_names(case)) - set(case['frozen_sha256']))
    if unhashed:
        raise ValueError(f"frozen_sha256 has no hash for declared input(s): {', '.join(unhashed)}")
    return case


def frozen_names(case):
    """Every file whose bytes must not change between the recorded run and a later one."""
    names = [case['task'], case['rubric']]
    names.extend(case['arms'][arm] for arm in sorted(case['arms']))
    names.extend(case.get('extra_inputs', []))
    return sorted(set(names))


def input_hashes(repo, case_dir, case):
    hashes = {name: digest(safe_path(repo, f'{case_dir}/{name}')) for name in frozen_names(case)}
    span, marker = extract_judge_section(
        safe_path(repo, f"{case_dir}/{case['rubric']}").read_text(encoding='utf-8'))
    hashes['rubric.judge-span'] = hashlib.sha256(span.encode('utf-8')).hexdigest()
    hashes['case.json'] = digest(safe_path(repo, f'{case_dir}/case.json'))
    return hashes, marker


def frozen_drift(repo, case_dir, case, expected):
    """Names whose current bytes differ from expected. Naming the file is the point."""
    current, _ = input_hashes(repo, case_dir, case)
    return sorted(name for name, value in expected.items()
                  if name in current and current[name] != value)


def extract_judge_section(text):
    """Return the region a grader may see, and whether markers delimited it.

    Release-gate wording names the arms, so sending a whole rubric to a blind grader would leak
    the vocabulary the blinding exists to hide. A rubric without markers returns whole and records
    judge_marker false: the existing prior-art rubrics are frozen bytes and are not retrofitted.
    """
    start = text.find(JUDGE_BEGIN)
    end = text.find(JUDGE_END)
    if start == -1 or end == -1 or end < start:
        return text, False
    return text[start + len(JUDGE_BEGIN):end].strip() + '\n', True


def blind_labels(group_key, arms):
    """Deterministic permutation of arm -> label, derived from a digest of the group key.

    Not random: a resumed run must reproduce the labels it used the first time. The mapping is
    never written to the record before grading; only group_key is, so a grader can hold the packet
    and the record without holding the answer.
    """
    ranked = sorted(arms, key=lambda arm: hashlib.sha256(
        group_key.encode('utf-8') + b'\x00' + arm.encode('utf-8')).hexdigest())
    ordering = [hashlib.sha256(group_key.encode('utf-8') + b'\x00' + arm.encode('utf-8')).hexdigest()
                for arm in ranked]
    if len(set(ordering)) != len(ordering):
        raise ValueError('Digest collision while blinding; rename an arm')
    return {arm: LABELS[index] for index, arm in enumerate(ranked)}


def isolation_flags(runner):
    if runner not in RUNNERS:
        raise ValueError(f'Unknown runner: {runner}')
    return list(RUNNERS[runner]['isolation'])


def build_argv(runner, model):
    """Assemble the exact argv. A model pin is structural, not a default."""
    spec = RUNNERS[runner]
    if not model or not str(model).strip():
        raise ValueError('An explicit --model pin is required; an unpinned model is not a control')
    return (list(spec['base']) + isolation_flags(runner)
            + [spec['model_flag'], model] + list(spec['tail']))


def parse_payload(text):
    """Return (usage, cost, response_text) without inferring any missing value.

    Unknown stays None. Never 0: a zero cost reads as free, and an absent cost is not free.
    """
    usage, cost, response = None, None, None
    try:
        payload = json.loads(text)
    except ValueError:
        payload = None
    if isinstance(payload, dict):
        usage = payload.get('usage') if isinstance(payload.get('usage'), dict) else None
        cost = payload.get('total_cost_usd')
        response = payload.get('result') if isinstance(payload.get('result'), str) else None
        return usage, cost if isinstance(cost, (int, float)) else None, response
    events = []
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict):
            events.append(event)
    for event in events:
        if isinstance(event.get('usage'), dict):
            usage = event['usage']
        if isinstance(event.get('total_cost_usd'), (int, float)):
            cost = event['total_cost_usd']
        # codex exec --json: {"type": "item.completed", "item": {"type": "agent_message",
        # "text": ...}}. The last agent message is the answer; reasoning and tool items are not.
        item = event.get('item')
        if (event.get('type') == 'item.completed' and isinstance(item, dict)
                and item.get('type') == 'agent_message' and isinstance(item.get('text'), str)):
            response = item['text']
    return usage, cost, response


def planned_cells(case, arms, trials):
    return [(arm, trial) for trial in range(1, trials + 1) for arm in arms]


def recorded_plan(record):
    """The campaign an attempt committed to when it was created: every case arm, every trial."""
    plan = record.get('plan')
    if not isinstance(plan, dict) or not plan.get('arms') or not plan.get('trials'):
        raise ValueError('The attempt record carries no campaign plan')
    return planned_cells(None, plan['arms'], plan['trials'])


def resume_conflicts(record, expected):
    """Recorded settings the resumed invocation would change. Any of them splits the attempt."""
    recorded = {
        'surface': record.get('surface'),
        'model': record.get('model'),
        'argv': record.get('argv'),
        'timeout_seconds': record.get('timeout_seconds'),
        'budget.max_usd': (record.get('budget') or {}).get('max_usd'),
        'budget.allow_unmetered_cells': (record.get('budget') or {}).get('allow_unmetered_cells'),
        'harness.sha256': (record.get('harness') or {}).get('sha256'),
        'plan.trials': (record.get('plan') or {}).get('trials'),
    }
    return sorted(name for name, value in expected.items() if recorded.get(name) != value)


def pending_cells(record, cells):
    done = {(entry['arm'], entry['trial']) for entry in record.get('arms', [])
            if entry.get('status') == 'completed'}
    return [cell for cell in cells if cell not in done]


def attempt_status(record, cells):
    """Completed only when every planned cell completed. Anything else is indeterminate.

    A timeout is an indeterminate outcome, not a diagnosed defect, and not a failure to score.
    """
    done = {(entry['arm'], entry['trial']): entry.get('status') for entry in record.get('arms', [])}
    if any(done.get(cell) != 'completed' for cell in cells):
        return 'indeterminate'
    return 'completed'


def budget_gate(spent, max_usd, unmetered, allow_unmetered):
    """Refusals are pre-execution. An unreportable cost is unknown, and unknown is not free."""
    if max_usd is None:
        return 'A spend ceiling is required; pass --max-usd'
    if spent is not None and spent >= max_usd:
        return f'Spend ceiling reached: {spent} >= {max_usd}'
    if unmetered > allow_unmetered:
        return (f'{unmetered} cell(s) reported no cost and --allow-unmetered-cells is '
                f'{allow_unmetered}; an unmetered campaign has no ceiling')
    return None


def probe_version(runner):
    try:
        completed = subprocess.run(RUNNERS[runner]['version_argv'], shell=False,
                                   capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.decode('utf-8', errors='replace').strip() or None


def new_record(case, case_dir, runner, model, timeout_seconds, budget, hashes, marker, argv,
               harness_sha, trials):
    return {
        'schema_version': SCHEMA_VERSION,
        'status': 'indeterminate',
        'recorded_date': time.strftime('%Y-%m-%d', time.gmtime()),
        'case': case['case'],
        'case_dir': case_dir,
        'harness': {'path': 'tests/eval/runner.py', 'sha256': harness_sha},
        # argv stays a top-level field, as in the v2 attempt record this schema extends.
        'argv': argv,
        'surface': runner,
        'surface_version': None,
        'surface_version_source': 'measured',
        'model': model,
        'provider': None,
        'utc_start': None,
        'utc_end': None,
        'timeout_seconds': timeout_seconds,
        # A fresh empty directory per cell, outside the repository and named by the system, not
        # by the arm: the headless CLI shows the model its cwd, and a repository cwd loads the
        # project's own context file into every arm.
        'working_directory': 'fresh-empty-system-temp-per-cell',
        'plan': {'arms': sorted(case['arms']), 'trials': trials},
        'isolation': {'profile': RUNNERS[runner]['profile'], 'flags': isolation_flags(runner)},
        'budget': budget,
        'input_hashes_current': hashes,
        'blinding': {'method': 'sha256-rank', 'group_key_template': '{case}|{trial}|{runner}|{model}',
                     'judge_marker': marker, 'revealed': False},
        'arms': [],
        'grading': {'grader': None, 'blinded': None, 'rubric_sha256': hashes.get('rubric.judge-span'),
                    'graded_utc': None},
        'limitations': [
            'The candidate arm supplies the skill body as prompt text. This measures the '
            'instruction text, not skill discovery or native invocation; files on disk are not '
            'evidence of a loaded capability.',
            'Isolation flags are recorded as passed, not verified as honoured. No offline check '
            'can prove the provider CLI applied them.',
            'Bounded attempts, deadlines and spend are usage control, not a sandbox.',
            'Each cell runs in an empty temporary directory, so no project context file is '
            'discovered. User-level context (for example a user memory file) is not proven '
            'excluded by the recorded flags.',
        ],
    }


def cmd_verify(repo, args):
    case = read_case(repo, args.case)
    drift = frozen_drift(repo, args.case, case, case['frozen_sha256'])
    current, marker = input_hashes(repo, args.case, case)
    missing = sorted(set(case['frozen_sha256']) - set(current))
    print(json.dumps({'case': case['case'], 'judge_marker': marker,
                      'drift': drift, 'unrecognised_recorded_names': missing,
                      'hashes': current}, indent=2))
    if drift:
        print(f"Frozen input drift: {', '.join(drift)}", file=sys.stderr)
        return 1
    return 0


def cmd_plan(repo, args):
    case = read_case(repo, args.case)
    arms = resolve_arms(case, args.arm)
    cells = planned_cells(case, arms, args.trials)
    argv = build_argv(args.runner, args.model)
    hashes, marker = input_hashes(repo, args.case, case)
    print(json.dumps({
        'case': case['case'], 'runner': args.runner, 'model': args.model,
        'isolation': {'profile': RUNNERS[args.runner]['profile'],
                      'flags': isolation_flags(args.runner)},
        'argv': argv, 'judge_marker': marker,
        'timeout_seconds': case['timeout_seconds'],
        'cells': [{'arm': arm, 'trial': trial,
                   'group_key': group_key(case, trial, args.runner, args.model)}
                  for arm, trial in cells],
        'frozen_drift': frozen_drift(repo, args.case, case, case['frozen_sha256']),
        'input_hashes': hashes,
    }, indent=2))
    return 0


def group_key(case, trial, runner, model):
    return f"{case['case']}|{trial}|{runner}|{model}"


def resolve_arms(case, requested):
    arms = sorted(case['arms'])
    if not requested:
        return arms
    unknown = sorted(set(requested) - set(arms))
    if unknown:
        raise ValueError(f"Unknown arm(s): {', '.join(unknown)}")
    return sorted(set(requested))


def cmd_run(repo, args):
    case = read_case(repo, args.case)
    arms = resolve_arms(case, args.arm)
    # The attempt is planned over every case arm; --arm only selects which cells run now. Status
    # is judged against the whole plan, so running one arm can never report a completed attempt.
    plan = planned_cells(case, sorted(case['arms']), args.trials)
    cells = [cell for cell in plan if cell[0] in arms]
    timeout_seconds = args.timeout_seconds or case['timeout_seconds']
    if timeout_seconds > case['timeout_seconds']:
        raise ValueError(
            f"--timeout-seconds {timeout_seconds:g} exceeds the deadline recorded for this case "
            f"({case['timeout_seconds']:g}); raising a deadline to obtain a score is not a control")
    argv = build_argv(args.runner, args.model)
    drift = frozen_drift(repo, args.case, case, case['frozen_sha256'])
    if drift:
        raise ValueError(f"Frozen input drift, refusing to run: {', '.join(drift)}")
    reason = budget_gate(None, args.max_usd, 0, args.allow_unmetered_cells)
    if reason:
        raise ValueError(reason)

    hashes, marker = input_hashes(repo, args.case, case)
    attempt_dir = args.attempt or f"attempt-{time.strftime('%Y%m%d', time.gmtime())}-{args.runner}"
    if not ATTEMPT_NAME.fullmatch(attempt_dir):
        raise ValueError('--attempt must be a single directory name starting with attempt-')
    folder = safe_path(repo, f'{args.case}/{attempt_dir}')
    record_path = safe_path(repo, f'{args.case}/{attempt_dir}/attempt.json')

    if args.dry_run:
        print(json.dumps({'dry_run': True, 'argv': argv, 'attempt_dir': attempt_dir,
                          'cells': [{'arm': a, 'trial': t} for a, t in cells],
                          'isolation': isolation_flags(args.runner),
                          'timeout_seconds': timeout_seconds,
                          'input_hashes': hashes}, indent=2))
        return 0

    harness_sha = digest(Path(__file__).resolve())
    folder.mkdir(parents=True, exist_ok=True)
    with locked(folder):
        if record_path.exists() and not args.resume:
            raise ValueError('An attempt record already exists; pass --resume or choose --attempt')
        if record_path.exists():
            record = json.loads(record_path.read_text(encoding='utf-8'))
            if record.get('schema_version') != SCHEMA_VERSION:
                raise ValueError('Unsupported attempt schema_version')
            stale = frozen_drift(repo, args.case, case, record.get('input_hashes_current', {}))
            if stale:
                raise ValueError(f"Inputs changed since this attempt: {', '.join(stale)}")
            conflicts = resume_conflicts(record, {
                'surface': args.runner, 'model': args.model, 'argv': argv,
                'timeout_seconds': timeout_seconds, 'budget.max_usd': args.max_usd,
                'budget.allow_unmetered_cells': args.allow_unmetered_cells,
                'harness.sha256': harness_sha, 'plan.trials': args.trials})
            if conflicts:
                raise ValueError('Resume would change what this attempt recorded: '
                                 f"{', '.join(conflicts)}. Start a new --attempt instead")
            if record.get('blinding', {}).get('revealed'):
                raise ValueError('This attempt is already graded; start a new --attempt')
        else:
            budget = {'max_usd': args.max_usd, 'spent_usd': None, 'cost_source': None,
                      'allow_unmetered_cells': args.allow_unmetered_cells}
            record = new_record(case, args.case, args.runner, args.model, timeout_seconds,
                                budget, hashes, marker, argv, harness_sha, args.trials)
            record['utc_start'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            write_record(record_path, record)

        plan = recorded_plan(record)
        cells = [cell for cell in plan if cell[0] in arms]
        version = probe_version(args.runner)
        recorded_version = record.get('surface_version')
        if recorded_version is not None and version != recorded_version:
            # Checked before any write, so the record keeps naming the version its cells ran on.
            raise ValueError(f'{args.runner} CLI version changed since this attempt '
                             f'({recorded_version!r} -> {version!r}); start a new --attempt')
        record['surface_version'] = version
        if version is None:
            record['status'] = 'indeterminate'
            record['limitations'].append(
                f'The {args.runner} CLI could not be probed for a version; no cell was executed.')
            write_record(record_path, record)
            print(json.dumps({'status': 'indeterminate',
                              'reason': f'{args.runner} CLI unavailable'}, indent=2))
            return 1

        spent = record['budget'].get('spent_usd')
        # Only a completed cell can have failed to report a cost. A blocked or timed-out cell
        # produced no billable turn, so counting it would refuse a campaign for the wrong reason.
        unmetered = sum(1 for e in record['arms']
                        if e.get('status') == 'completed' and e.get('cost_source') == 'unavailable')
        for arm, trial in pending_cells(record, cells):
            reason = budget_gate(spent, args.max_usd, unmetered, args.allow_unmetered_cells)
            if reason:
                record['limitations'].append(f'Campaign stopped before all cells ran: {reason}')
                break
            entry = run_cell(repo, args, case, folder, arm, trial, argv, timeout_seconds)
            record['arms'] = [e for e in record['arms']
                              if (e['arm'], e['trial']) != (arm, trial)] + [entry]
            record['arms'].sort(key=lambda e: (e['trial'], e['arm']))
            if entry.get('billed_cost') is not None:
                spent = (spent or 0) + entry['billed_cost']
            elif entry.get('status') == 'completed':
                unmetered += 1
            record['budget']['spent_usd'] = spent
            record['budget']['cost_source'] = 'unavailable' if spent is None else 'reported'
            record['status'] = attempt_status(record, plan)
            record['utc_end'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            write_record(record_path, record)

        record['status'] = attempt_status(record, plan)
        record['utc_end'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        write_record(record_path, record)

    print(json.dumps({'status': record['status'], 'attempt': attempt_dir,
                      'cells_recorded': len(record['arms']), 'cells_planned': len(plan),
                      'spent_usd': record['budget']['spent_usd']}, indent=2))
    return 0 if record['status'] == 'completed' else 1


def run_cell(repo, args, case, folder, arm, trial, argv, timeout_seconds):
    prompt = safe_path(repo, f"{args.case}/{case['arms'][arm]}").read_bytes()
    out_path = folder / f'cell-{arm}-{trial}.out'
    err_path = folder / f'cell-{arm}-{trial}.err'
    entry = {'arm': arm, 'trial': trial, 'status': 'blocked', 'exit_code': None,
             'timed_out': False, 'elapsed_seconds': None,
             'output_path': out_path.name, 'output_sha256': None,
             'diagnostic_path': err_path.name, 'usage': None, 'billed_cost': None,
             'cost_source': 'unavailable', 'score': None,
             'score_max': case['score_max'], 'score_breakdown': None}
    started = time.monotonic()
    stdout, stderr = b'', b''
    workdir = Path(tempfile.mkdtemp())  # System-named: no arm, case or repository word in it.
    try:
        completed = subprocess.run(argv, shell=False, cwd=workdir, input=prompt,
                                   capture_output=True, timeout=timeout_seconds)
        stdout, stderr = completed.stdout, completed.stderr
        entry['exit_code'] = completed.returncode
        entry['status'] = 'completed' if completed.returncode == 0 else 'failed'
    except subprocess.TimeoutExpired as exc:
        # Retain whatever the process produced; a deadline is an indeterminate outcome.
        stdout = exc.stdout or b''
        stderr = exc.stderr or b''
        entry.update(status='timeout', timed_out=True)
    except OSError as exc:
        stderr = str(exc).encode('utf-8')
        entry['status'] = 'blocked'
    finally:
        entry['elapsed_seconds'] = time.monotonic() - started
        try:
            workdir.rmdir()  # Only ever an empty directory; anything left in it stays for review.
        except OSError:
            entry['workdir_left_nonempty'] = True
    out_path.write_bytes(stdout)
    err_path.write_bytes(stderr)
    entry['output_sha256'] = digest(out_path)
    usage, cost, _ = parse_payload(stdout.decode('utf-8', errors='replace'))
    entry['usage'] = usage
    entry['billed_cost'] = cost
    entry['cost_source'] = 'reported' if cost is not None else 'unavailable'
    return entry


def cmd_grade(repo, args):
    case = read_case(repo, args.case)
    if not ATTEMPT_NAME.fullmatch(args.attempt):
        raise ValueError('--attempt must be a single directory name starting with attempt-')
    record_path = safe_path(repo, f'{args.case}/{args.attempt}/attempt.json')
    if not record_path.is_file():
        raise ValueError(f'No attempt record at {args.attempt}')
    # The same lock run holds: a grade overlapping a campaign would read a transient cell set,
    # and the two writers would overwrite each other's record.
    with locked(record_path.parent):
        return grade_locked(repo, args, case, record_path)


def grade_locked(repo, args, case, record_path):
    folder = record_path.parent
    record = json.loads(record_path.read_text(encoding='utf-8'))
    if record.get('blinding', {}).get('revealed'):
        raise ValueError('This attempt is already graded; a recorded grade is not overwritten')
    completed = [e for e in record.get('arms', []) if e.get('status') == 'completed']
    if not completed:
        raise ValueError('No completed cell to grade')
    changed = sorted(entry['output_path'] for entry in completed
                     if digest(folder / entry['output_path']) != entry.get('output_sha256'))
    if changed:
        raise ValueError(f"Recorded output no longer matches its hash: {', '.join(changed)}")
    groups = {}
    for entry in completed:
        groups.setdefault(entry['trial'], []).append(entry['arm'])

    if args.scores is None:
        blind = folder / 'blind'
        blind.mkdir(exist_ok=True)
        span, _ = extract_judge_section(
            safe_path(repo, f"{args.case}/{case['rubric']}").read_text(encoding='utf-8'))
        (blind / 'rubric-judge.md').write_text(span, encoding='utf-8')
        for trial, arms in sorted(groups.items()):
            mapping = blind_labels(group_key(case, trial, record['surface'], record['model']), arms)
            for arm in arms:
                raw = (folder / f'cell-{arm}-{trial}.out').read_text(encoding='utf-8',
                                                                    errors='replace')
                _, _, response = parse_payload(raw)
                target = blind / f'trial-{trial}-response-{mapping[arm]}.md'
                target.write_text(response if response is not None else raw, encoding='utf-8')
        print(json.dumps({'blind_packet': str(blind.relative_to(repo)),
                          'trials': sorted(groups), 'next':
                          'Score each labelled response against rubric-judge.md, then pass '
                          '--scores with {"<trial>": {"<label>": <number>}}'}, indent=2))
        return 0

    scores = json.loads(safe_path(repo, args.scores).read_text(encoding='utf-8'))
    graded, missing = {}, []
    for trial, arms in sorted(groups.items()):
        mapping = blind_labels(group_key(case, trial, record['surface'], record['model']), arms)
        supplied = scores.get(str(trial), scores.get(trial, {}))
        for arm in arms:
            label = mapping[arm]
            if label not in supplied:
                missing.append(f'trial {trial} label {label}')
                continue
            value = supplied[label]
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(value) or not 0 <= value <= case['score_max']):
                raise ValueError(f'Score for trial {trial} label {label} is not a number '
                                 f"between 0 and {case['score_max']:g}")
            graded[(arm, trial)] = float(value)
    if missing:
        raise ValueError(f"Incomplete scores, nothing written: {', '.join(missing)}")

    for entry in record['arms']:
        key = (entry['arm'], entry['trial'])
        if key in graded:
            entry['score'] = graded[key]
    record['blinding']['revealed'] = True
    record['grading'] = {'grader': args.grader, 'blinded': args.blinded,
                         'rubric_sha256': record['input_hashes_current'].get('rubric.judge-span'),
                         'graded_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    if not args.blinded:
        record['limitations'].append('Grading was not structurally blinded.')
    record['limitations'].append(
        f'Grader {args.grader} is a project participant; structural blinding is not independence.')
    write_record(record_path, record)
    print(json.dumps({'graded_cells': len(graded), 'revealed': True}, indent=2))
    return 0


def command_parser():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest='action', required=True)

    verify = sub.add_parser('verify', help='Recompute frozen input hashes; exit 1 on drift')
    verify.add_argument('--case', required=True)

    plan = sub.add_parser('plan', help='Print exact argv and the cell list; write nothing')
    plan.add_argument('--case', required=True)
    plan.add_argument('--runner', required=True, choices=sorted(RUNNERS))
    plan.add_argument('--model', required=True)
    plan.add_argument('--arm', action='append')
    plan.add_argument('--trials', type=int, default=3)

    run = sub.add_parser('run', help='Execute pending cells and append to the attempt record')
    run.add_argument('--case', required=True)
    run.add_argument('--runner', required=True, choices=sorted(RUNNERS))
    run.add_argument('--model', required=True)
    run.add_argument('--attempt')
    run.add_argument('--arm', action='append')
    run.add_argument('--trials', type=int, default=3)
    run.add_argument('--timeout-seconds', type=positive)
    run.add_argument('--max-usd', type=positive)
    run.add_argument('--allow-unmetered-cells', type=int, default=0)
    run.add_argument('--resume', action='store_true')
    run.add_argument('--dry-run', action='store_true')

    grade = sub.add_parser('grade', help='Emit a blind packet, or ingest scores and unblind')
    grade.add_argument('--case', required=True)
    grade.add_argument('--attempt', required=True)
    grade.add_argument('--scores')
    grade.add_argument('--grader', default='unnamed')
    grade.add_argument('--blinded', action='store_true')
    return parser


def main(argv=None):
    parser = command_parser()
    args = parser.parse_args(argv)
    try:
        repo = args.repo.resolve(strict=True)
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]{0,255}', args.case):
            raise ValueError('Case must be a simple repository-relative directory path')
        if args.action == 'verify':
            return cmd_verify(repo, args)
        if args.action == 'plan':
            if args.trials < 1:
                raise ValueError('trials must be positive')
            return cmd_plan(repo, args)
        if args.action == 'run':
            if args.trials < 1:
                raise ValueError('trials must be positive')
            if args.allow_unmetered_cells < 0:
                raise ValueError('allow-unmetered-cells must not be negative')
            return cmd_run(repo, args)
        return cmd_grade(repo, args)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Evaluation stopped: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
