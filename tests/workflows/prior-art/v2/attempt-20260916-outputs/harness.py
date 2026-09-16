#!/usr/bin/env python3
"""Frozen v2 paired trial harness. Standard library only.

One attempt per arm, sequential, baseline first, 300s per-arm process deadline.
Each arm runs as its own process with cwd set to its own EMPTY scratch directory so
that no repository context file (CLAUDE.md / AGENTS.md) is loaded.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import random
import subprocess
import sys
import time

REPO = "/home/user/houserules"
PACKET_DIR = os.path.join(REPO, "tests", "workflows", "prior-art", "v2")
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out")

TIMEOUT_SECONDS = 300
CLAUDE = "/opt/node22/bin/claude"

FROZEN = {
    "baseline-prompt.md": "de5f3d7354351f8d4857ae297eb5cff0e99409d04e50efcbd875eee236cdbab5",
    "candidate-prompt.md": "c55af38a425d6c35863c5382495f8422a051505c3516cc7bd1fdee8c7b4ae12c",
    "rubric.md": "4a2126bdd5d96ff469c1c3a39b2530c820fa3ca4c7846efb66a7bac9436cba67",
}


def utcnow() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def progress(msg: str) -> None:
    """Progress reporting, deliberately outside the per-arm process deadline."""
    print("[%s] %s" % (utcnow(), msg), file=sys.stderr, flush=True)


def read_bytes(name: str) -> bytes:
    with open(os.path.join(PACKET_DIR, name), "rb") as fh:
        return fh.read()


def measure_hashes() -> dict:
    return {n: hashlib.sha256(read_bytes(n)).hexdigest() for n in FROZEN}


def run_one(label: str, prompt_text: str, cwd: str) -> dict:
    """Run a single arm. Returns a record; never retries."""
    os.makedirs(cwd, exist_ok=True)
    if os.listdir(cwd):
        raise RuntimeError("arm cwd is not empty: %s" % cwd)

    argv = [CLAUDE, "-p", prompt_text, "--output-format", "json",
            "--strict-mcp-config", "--tools", ""]

    env = dict(os.environ)
    # Keep the arm's environment free of this harness's own session context.
    env.pop("CLAUDE_CODE_SSE_PORT", None)

    stdout_path = os.path.join(OUT, "%s.stdout.txt" % label)
    stderr_path = os.path.join(OUT, "%s.stderr.txt" % label)

    progress("arm %s: launching (deadline %ss)" % (label, TIMEOUT_SECONDS))
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

    # Partial streams are retained on timeout.
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

    progress("arm %s: %s in %ss (exit=%s, timed_out=%s)"
             % (label, status, elapsed, exit_code, timed_out))

    return {
        "label": label,
        "argv": argv,
        "working_directory": cwd,
        "timeout_seconds": TIMEOUT_SECONDS,
        "utc_start": start_wall,
        "utc_end": end_wall,
        "elapsed_seconds": elapsed,
        "timed_out": timed_out,
        "exit_code": exit_code,
        "status": status,
        "stdout_path": stdout_path,
        "stderr_path": stderr_path,
        "result_json": parsed,
    }


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
    progress("surface: %s" % version)

    arms = []
    for arm_name, fname in (("baseline", "baseline-prompt.md"),
                            ("candidate", "candidate-prompt.md")):
        prompt_text = read_bytes(fname).decode("utf-8")
        cwd = os.path.join(BASE, "cwd-%s" % arm_name)
        rec = run_one(arm_name, prompt_text, cwd)
        rec["arm"] = arm_name
        rec["prompt_file"] = fname
        arms.append(rec)

    # ---- blinding -------------------------------------------------------
    blind_dir = os.path.join(OUT, "blind")
    os.makedirs(blind_dir, exist_ok=True)
    labels = ["A", "B"]
    rng = random.SystemRandom()
    rng.shuffle(labels)
    mapping = {}
    texts = {}
    for lab, rec in zip(labels, arms):
        mapping[lab] = rec["arm"]
        res = rec["result_json"] or {}
        text = res.get("result")
        if not isinstance(text, str) or not text.strip():
            text = None
        texts[lab] = text
        path = os.path.join(blind_dir, "output-%s.txt" % lab)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text if text is not None else "[OUTPUT UNAVAILABLE - INDETERMINATE]\n")
        rec["blind_label"] = lab
        rec["blind_output_path"] = path

    # Mapping is written where the grader process never reads it.
    map_path = os.path.join(BASE, "label-mapping.json")  # deliberately outside OUT/blind
    with open(map_path, "w", encoding="utf-8") as fh:
        json.dump(mapping, fh, indent=2)
    progress("blind labels assigned; mapping withheld from grader")

    # ---- grading --------------------------------------------------------
    grade_rec = None
    if all(texts[lab] is not None for lab in ("A", "B")):
        rubric = read_bytes("rubric.md").decode("utf-8")
        grader_prompt = (
            rubric
            + "\n\n---\nBelow are two candidate outputs, labelled A and B, produced for the same "
              "scenario. You do not know which arm produced which. Grade SEMANTICALLY against the "
              "four numbered outcomes above; do not score by keyword match, by quoting of the "
              "protocol, by use of template headings, or by invocation of any skill. Award 1, 0.5 "
              "or 0 per check.\n\nFor EACH of A and B, give a per-check score for checks 1-4 with "
              "a one-line reason each, then a total out of 4. End with one line naming which label "
              "scored higher, or 'tie'.\n\n"
            + "=== OUTPUT A ===\n" + texts["A"]
            + "\n\n=== OUTPUT B ===\n" + texts["B"] + "\n"
        )
        gcwd = os.path.join(BASE, "cwd-grader")
        grade_rec = run_one("grader", grader_prompt, gcwd)
        grade_rec["arm"] = "grader"
        with open(os.path.join(OUT, "grader-prompt.txt"), "w", encoding="utf-8") as fh:
            fh.write(grader_prompt)
    else:
        progress("grading skipped: at least one arm output unavailable (indeterminate)")

    bundle = {
        "surface_version": version,
        "input_hashes_measured": measured,
        "arms": arms,
        "label_mapping": mapping,
        "label_mapping_path": map_path,
        "grader": grade_rec,
    }
    with open(os.path.join(OUT, "bundle.json"), "w", encoding="utf-8") as fh:
        json.dump(bundle, fh, indent=2)
    progress("bundle written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
