#!/usr/bin/env python3
"""Bound local verification commands and retain revision-bound evidence. Standard library only."""
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
import time


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


def targets(repo, names):
    return {name: digest(safe_path(repo, name)) for name in names}


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError('must be finite and positive')
    return number


@contextmanager
def locked(folder):
    lock = folder / '.workflow.lock'
    with lock.open('x', encoding='utf-8') as stream:
        stream.write(str(os.getpid()))
    try:
        yield
    finally:
        lock.unlink()  # One explicitly created lock, never a directory cleanup.


def write_state(path, state):
    temporary = path.with_suffix('.json.tmp')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(state, stream, indent=2, allow_nan=False)
        stream.write('\n')
    temporary.replace(path)


def read_state(path):
    state = json.loads(path.read_text(encoding='utf-8'))
    if (state.get('schema_version') != 1 or not isinstance(state.get('runs'), list)
            or not isinstance(state.get('targets'), list) or not state['targets']
            or any(not isinstance(p, str) for p in state['targets'])
            or type(state.get('max_runs')) is not int or state['max_runs'] < 1
            or not isinstance(state.get('max_seconds'), (int, float))
            or not math.isfinite(state['max_seconds']) or state['max_seconds'] <= 0):
        raise ValueError('Invalid workflow state; preserve the file and inspect it')
    for run in state['runs']:
        seconds = run.get('elapsed_seconds')
        if seconds is not None and (not isinstance(seconds, (int, float))
                                   or not math.isfinite(seconds) or seconds < 0):
            raise ValueError('Invalid elapsed time')
    return state


def allowance(state):
    if any(run.get('outcome') == 'running' for run in state['runs']):
        return 0, 0, 'An interrupted or active run must be inspected; do not retry blindly'
    # Each command receives all remaining time. Timeout exhausts that allocation even
    # when clock resolution reports a slightly shorter actual duration; keep usage honest.
    if any(run.get('outcome') == 'timeout' for run in state['runs']):
        return 0, 0, 'Budget exhausted by timeout'
    remaining_runs = state['max_runs'] - len(state['runs'])
    remaining_seconds = state['max_seconds'] - sum(r['elapsed_seconds'] for r in state['runs'])
    reason = 'Budget exhausted' if remaining_runs <= 0 or remaining_seconds <= 0 else None
    return remaining_runs, max(0, remaining_seconds), reason


def report(repo, state):
    count, seconds, reason = allowance(state)
    runs = state['runs']
    last = runs[-1] if runs else None
    stale = bool(last and (last.get('targets_before') != last.get('targets_after')
                          or targets(repo, state['targets']) != last.get('targets_after')
                          or any(digest(safe_path(repo, p)) != h
                                 for p, h in last.get('evidence', {}).items())))
    passed = bool(last and last.get('outcome') == 'pass' and not stale
                  and all(value is not None for value in last.get('targets_after', {}).values()))
    return {'task': state['task'], 'result': 'stale' if stale else
            (last.get('outcome') if last else 'not-run'), 'verified': passed,
            'remaining_runs': max(0, count), 'remaining_seconds': round(seconds, 3),
            'next': 'Review the recorded result; no rerun needed for unchanged inputs' if passed
            else reason or 'Run the relevant command within the remaining budget',
            'attempts': len(runs),
            'latest_log': next(iter(last.get('evidence', {})), None) if last else None}


def command_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest='action', required=True)
    start = sub.add_parser('start', help='Create work/<id>/workflow.json; existing work is never replaced')
    start.add_argument('id')
    start.add_argument('--task', required=True)
    start.add_argument('--target', action='append', required=True, help='Exact file to bind evidence to; repeat as needed')
    start.add_argument('--max-runs', type=int, default=3)
    start.add_argument('--max-seconds', type=positive, default=300)
    run = sub.add_parser('run', help='Run exact argv without a shell; preserve output, exit and target hashes')
    run.add_argument('id')
    run.add_argument('command', nargs=argparse.REMAINDER)
    status = sub.add_parser('status', help='Read-only evidence freshness and budget check; exit 0 only for a current pass')
    status.add_argument('id')
    return parser


def main(argv=None):
    parser = command_parser()
    args = parser.parse_args(argv)
    try:
        repo = args.repo.resolve(strict=True)
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', args.id):
            raise ValueError('Task id must be 1-64 lowercase letters/digits/hyphens')
        folder = safe_path(repo, f'work/{args.id}')
        state_path = safe_path(repo, f'work/{args.id}/workflow.json')
        if args.action == 'start':
            if args.max_runs < 1:
                raise ValueError('max-runs must be positive')
            if not args.task.strip():
                raise ValueError('Task must not be empty')
            if any(safe_path(repo, p).is_dir() for p in args.target):
                raise ValueError('Targets must be exact files, not directories')
            names = sorted(set(Path(p).as_posix() for p in args.target))
            for name in names:
                if safe_path(repo, name).is_relative_to(repo / 'work'):
                    raise ValueError(f'Workflow targets cannot use the work/ record area: {name}')
            initial = targets(repo, names)
            folder.mkdir(parents=True, exist_ok=True)
            with locked(folder):
                if state_path.exists():
                    raise ValueError('Task already exists; inspect status or choose a new task id')
                state = {'schema_version': 1, 'task': args.task, 'targets': names,
                         'initial_targets': initial, 'max_runs': args.max_runs,
                         'max_seconds': args.max_seconds, 'runs': []}
                write_state(state_path, state)
            print(f'Created {state_path.relative_to(repo)}; budget {args.max_runs} runs / {args.max_seconds:g}s')
            return 0
        if args.action == 'status':
            state = read_state(state_path)
            result = report(repo, state)
            print(json.dumps(result, indent=2))
            return 0 if result['verified'] else 1
        command = args.command
        if command and command[0] == '--':
            command = command[1:]
        if not command:
            raise ValueError('Provide an executable and arguments after --')
        with locked(folder):
            state = read_state(state_path)
            _, seconds, reason = allowance(state)
            if reason:
                raise ValueError(reason)
            if state['runs'] and state['runs'][-1].get('argv') == command and report(repo, state)['verified']:
                raise ValueError('This command already passed at unchanged targets; inspect status instead')
            index = len(state['runs']) + 1
            log = safe_path(repo, f'work/{args.id}/run-{index:03d}.log')
            # Claim the log before changing state; never overwrite a user file.
            with log.open('xb') as output:
                run = {'argv': command, 'outcome': 'running', 'elapsed_seconds': None,
                       'targets_before': targets(repo, state['targets']), 'usage': None}
                state['runs'].append(run)
                write_state(state_path, state)
                started = time.monotonic()
                try:
                    completed = subprocess.run(command, cwd=repo, stdout=output,
                                               stderr=subprocess.STDOUT, timeout=seconds)
                    run['exit_code'] = completed.returncode
                    run['outcome'] = 'pass' if completed.returncode == 0 else 'fail'
                except subprocess.TimeoutExpired:
                    run.update(outcome='timeout', exit_code=None)
                except OSError as exc:
                    output.write(str(exc).encode('utf-8'))
                    run.update(outcome='blocked', exit_code=None)
                finally:
                    run['elapsed_seconds'] = time.monotonic() - started
            run['targets_after'] = targets(repo, state['targets'])
            run['evidence'] = {log.relative_to(repo).as_posix(): digest(log)}
            # Preserve raw Codex per-turn counters only; do not infer bills or add subcounts.
            usage = []
            for line in log.read_text(encoding='utf-8', errors='replace').splitlines():
                try:
                    event = json.loads(line)
                    if isinstance(event, dict) and event.get('type') == 'turn.completed' and isinstance(event.get('usage'), dict):
                        usage.append(event['usage'])
                except ValueError:
                    pass
            run['usage'] = usage or None
            write_state(state_path, state)
            print(json.dumps(report(repo, state), indent=2))
            return 0 if report(repo, state)['verified'] else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Workflow stopped: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
