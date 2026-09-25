#!/usr/bin/env python3
"""Frozen v2 paired trial - replication with counterbalancing and isolated blind grading.

Differences from the 2026-09-16 single-pair harness (attempt-20260916-outputs/harness.py):
  1. N repetitions of the same frozen pair, to estimate run-to-run variation.
  2. Arm execution order is counterbalanced per pair (baseline-first / candidate-first).
  3. Each arm output is graded in its OWN grader process, seeing only the rubric and that one
     output. The 2026-09-16 run graded both outputs in a single call, so the grader could compare
     them against each other; that confound is removed here.
  4. The grader emits a machine-readable SCORES_JSON line, so per-check scores are parsed rather
     than hand-transcribed. The verbatim prose remains the authority and is preserved.

Unchanged: stdlib only, 300s per-process deadline, no retries, empty non-repository cwd per call,
partial streams retained on timeout, unparseable or timed-out results recorded INDETERMINATE.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time

REPO = "/home/user/houserules"
PACKET_DIR = os.path.join(REPO, "tests", "workflows", "prior-art", "v2")
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out")

TIMEOUT_SECONDS = 300
CLAUDE = "/opt/node22/bin/claude"
N_PAIRS = int(os.environ.get("N_PAIRS", "10"))

FROZEN = {
    "baseline-prompt.md": "de5f3d7354351f8d4857ae297eb5cff0e99409d04e50efcbd875eee236cdbab5",
    "candidate-prompt.md": "c55af38a425d6c35863c5382495f8422a051505c3516cc7bd1fdee8c7b4ae12c",
    "rubric.md": "4a2126bdd5d96ff469c1c3a39b2530c820fa3ca4c7846efb66a7bac9436cba67",
}

GRADER_INSTRUCTION = (
    "\n\n---\nBelow is ONE candidate output produced for the scenario above. You are grading it on "
    "its own; you have not been shown any other output and must not assume one exists. Grade "
    "SEMANTICALLY against the four numbered outcomes above. Do not score by keyword match, by "
    "quoting of the protocol, by use of template headings, or by invocation of any skill. Award "
    "1, 0.5 or 0 per check.\n\n"
    "Give a per-check score for checks 1-4 with a one-line reason each. Then, as the FINAL line "
    "and nothing after it, emit exactly:\n"
    'SCORES_JSON: {"check_1": <n>, "check_2": <n>, "check_3": <n>, "check_4": <n>, "total": <n>}\n\n'
    "=== OUTPUT ===\n"
)


def utcnow() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def progress(msg: str) -> None:
    """Progress reporting, deliberately outside the per-process deadline."""
    print("[%s] %s" % (utcnow(), msg), file=sys.stderr, flush=True)


def read_bytes(name: str) -> bytes:
    with open(os.path.join(PACKET_DIR, name), "rb") as fh:
        return fh.read()


def measure_hashes() -> dict:
    return {n: hashlib.sha256(read_bytes(n)).hexdigest() for n in FROZEN}


def run_one(label: str, prompt_text: str, cwd: str) -> dict:
    """Run a single headless process. Returns a record; never retries."""
    os.makedirs(cwd, exist_ok=True)
    if os.listdir(cwd):
        raise RuntimeError("cwd is not empty: %s" % cwd)

    argv = [CLAUDE, "-p", prompt_text, "--output-format", "json",
            "--strict-mcp-config", "--tools", ""]
    env = dict(os.environ)
    env.pop("CLAUDE_CODE_SSE_PORT", None)

    stdout_path = os.path.join(OUT, "%s.stdout.txt" % label)
    stderr_path = os.path.join(OUT, "%s.stderr.txt" % label)

    start_wall = utcnow()
    t0 = time.monotonic()
    timed_out = False
    exit_code = None
    try:
        cp = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                            timeout=TIMEOUT_SECONDS)
        out_b, err_b, exit_code = cp.stdout, cp.stderr, cp.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        out_b = exc.stdout or b""
        err_b = exc.stderr or b""
    elapsed = round(time.monotonic() - t0, 3)
    end_wall = utcnow()

    with open(stdout_path, "wb") as fh:
        fh.write(out_b)
    with open(stderr_path, "wb") as fh:
        fh.write(err_b)

    parsed = None
    if not timed_out:
        try:
            parsed = json.loads(out_b.decode("utf-8", "replace"))
        except (ValueError, UnicodeError):
            parsed = None

    status = "INDETERMINATE" if timed_out else (
        "completed" if (exit_code == 0 and parsed is not None) else "INDETERMINATE")
    progress("  %s: %s in %ss (exit=%s, timed_out=%s)"
             % (label, status, elapsed, exit_code, timed_out))

    return {
        "label": label, "argv": argv, "working_directory": cwd,
        "timeout_seconds": TIMEOUT_SECONDS, "utc_start": start_wall, "utc_end": end_wall,
        "elapsed_seconds": elapsed, "timed_out": timed_out, "exit_code": exit_code,
        "status": status, "stdout_path": stdout_path, "stderr_path": stderr_path,
        "result_json": parsed,
    }


def result_text(rec: dict):
    res = rec.get("result_json") or {}
    text = res.get("result")
    return text if isinstance(text, str) and text.strip() else None


def parse_scores(text: str):
    """Parse the final SCORES_JSON line. Returns (scores_dict_or_None, note)."""
    if not text:
        return None, "no grader text"
    matches = re.findall(r"SCORES_JSON:\s*(\{.*?\})", text, re.DOTALL)
    if not matches:
        return None, "SCORES_JSON line absent"
    try:
        obj = json.loads(matches[-1])
    except ValueError:
        return None, "SCORES_JSON not valid JSON"
    keys = ("check_1", "check_2", "check_3", "check_4")
    if not all(k in obj for k in keys):
        return None, "SCORES_JSON missing a check key"
    try:
        vals = [float(obj[k]) for k in keys]
    except (TypeError, ValueError):
        return None, "SCORES_JSON check value not numeric"
    if any(v not in (0.0, 0.5, 1.0) for v in vals):
        return None, "SCORES_JSON check value outside {0, 0.5, 1}"
    return {"check_1": vals[0], "check_2": vals[1], "check_3": vals[2],
            "check_4": vals[3], "total": round(sum(vals), 2)}, "parsed"


def main() -> int:
    os.makedirs(OUT, exist_ok=True)

    measured = measure_hashes()
    mismatch = {k: (FROZEN[k], measured[k]) for k in FROZEN if FROZEN[k] != measured[k]}
    if mismatch:
        print(json.dumps({"stop": "frozen input hash mismatch", "detail": mismatch}, indent=2))
        return 2
    progress("frozen inputs verified against v2/README.md")

    version = subprocess.run([CLAUDE, "--version"], capture_output=True, text=True,
                             timeout=60).stdout.strip()
    progress("surface: %s ; N_PAIRS=%d" % (version, N_PAIRS))

    rubric = read_bytes("rubric.md").decode("utf-8")
    prompts = {n: read_bytes("%s-prompt.md" % n).decode("utf-8")
               for n in ("baseline", "candidate")}

    rng = random.SystemRandom()
    pairs = []

    for i in range(1, N_PAIRS + 1):
        # Counterbalance execution order: odd pairs baseline-first, even candidate-first.
        order = ["baseline", "candidate"] if i % 2 == 1 else ["candidate", "baseline"]
        progress("pair %d/%d: order=%s" % (i, N_PAIRS, "/".join(order)))

        arms = {}
        for arm in order:
            lab = "p%02d-%s" % (i, arm)
            rec = run_one(lab, prompts[arm], os.path.join(BASE, "cwd", lab))
            rec["arm"] = arm
            rec["pair"] = i
            rec["prompt_file"] = "%s-prompt.md" % arm
            arms[arm] = rec

        # Blind labels, independent of execution order.
        labels = ["A", "B"]
        rng.shuffle(labels)
        mapping = {labels[0]: "baseline", labels[1]: "candidate"}

        graded = {}
        for lab, arm in mapping.items():
            text = result_text(arms[arm])
            arms[arm]["blind_label"] = lab
            if text is None:
                graded[arm] = {"scores": None, "note": "arm output unavailable",
                               "grader_record": None}
                progress("  grading %s skipped: arm output unavailable" % lab)
                continue
            blind_path = os.path.join(OUT, "blind", "p%02d-output-%s.txt" % (i, lab))
            os.makedirs(os.path.dirname(blind_path), exist_ok=True)
            with open(blind_path, "w", encoding="utf-8") as fh:
                fh.write(text)
            arms[arm]["blind_output_path"] = blind_path

            gprompt = rubric + GRADER_INSTRUCTION + text + "\n"
            glab = "p%02d-grader-%s" % (i, lab)
            grec = run_one(glab, gprompt, os.path.join(BASE, "cwd", glab))
            gtext = result_text(grec)
            scores, note = parse_scores(gtext)
            with open(os.path.join(OUT, "%s-prompt.txt" % glab), "w", encoding="utf-8") as fh:
                fh.write(gprompt)
            graded[arm] = {"scores": scores, "note": note, "grader_record": grec,
                           "graded_as_label": lab}
            progress("  grade %s (%s): %s [%s]"
                     % (lab, "hidden", scores["total"] if scores else "INDETERMINATE", note))

        # Mapping is written outside the grader's input and cwd.
        with open(os.path.join(BASE, "label-mapping-p%02d.json" % i), "w",
                  encoding="utf-8") as fh:
            json.dump(mapping, fh, indent=2)

        pairs.append({"pair": i, "execution_order": order, "label_mapping": mapping,
                      "arms": arms, "grading": graded})

        with open(os.path.join(OUT, "bundle.json"), "w", encoding="utf-8") as fh:
            json.dump({"surface_version": version, "n_pairs_requested": N_PAIRS,
                       "input_hashes_measured": measured, "pairs": pairs}, fh, indent=2)

    progress("all pairs done; bundle written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
