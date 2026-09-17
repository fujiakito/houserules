#!/usr/bin/env python3
"""Derive the `aggregate` block of the replication record from a harness bundle.

Standard library only. Reads the `bundle.json` that `harness.py` writes and emits the exact
block stored under `aggregate` in attempt-20260917-replication.json, so the derived figures
have a committed producer and a committed input rather than only being recomputable.

Every statistic is computed from the raw per-pair scores with NO intermediate rounding; the
displayed sd and standard_error are the same quantities rounded once for reading, and both
intervals are computed from the unrounded standard error. An earlier, uncommitted aggregation
step rounded sd before deriving the SE and then multiplied that rounded SE, which shifted both
interval bounds by about 9.3e-5. That defect is the reason this step is committed.

Usage: python aggregate.py <bundle.json>
"""
from __future__ import annotations

import json
import statistics as st
import sys

CHECKS = ("check_1", "check_2", "check_3", "check_4")
Z_95 = 1.96
T9_95 = 2.262


def aggregate(bundle: dict) -> dict:
    base, cand, diffs, indet = [], [], [], 0
    per_check = {"baseline": {k: [] for k in CHECKS}, "candidate": {k: [] for k in CHECKS}}
    cost = 0.0

    for pair in bundle["pairs"]:
        scores = {}
        for arm in ("baseline", "candidate"):
            rec = pair["arms"][arm]
            grading = pair["grading"][arm]
            s = grading["scores"]
            scores[arm] = s
            if s is None:
                indet += 1
            else:
                (base if arm == "baseline" else cand).append(s["total"])
                for k in CHECKS:
                    per_check[arm][k].append(s[k])
            cost += (rec.get("result_json") or {}).get("total_cost_usd") or 0.0
            grec = grading.get("grader_record")
            if grec:
                cost += (grec.get("result_json") or {}).get("total_cost_usd") or 0.0
        if scores["baseline"] and scores["candidate"]:
            diffs.append(round(scores["candidate"]["total"] - scores["baseline"]["total"], 2))

    def arm_block(vals: list) -> dict:
        return {"mean": round(sum(vals) / len(vals), 4),
                "sd": round(st.stdev(vals), 4) if len(vals) > 1 else 0.0,
                "min": min(vals), "max": max(vals), "observed_values": sorted(set(vals))}

    mean = sum(diffs) / len(diffs)
    sd = st.stdev(diffs) if len(diffs) > 1 else 0.0
    se = sd / (len(diffs) ** 0.5)          # unrounded; intervals use this value
    interval = lambda k: [round(mean - k * se, 4), round(mean + k * se, 4)]

    return {
        "n_pairs": len(diffs),
        "indeterminate_calls": indet,
        "baseline": arm_block(base),
        "candidate": arm_block(cand),
        "paired_difference_candidate_minus_baseline": {
            "mean": round(mean, 4),
            "sd": round(sd, 4),
            "standard_error": round(se, 4),
            "ci_95_normal_z": interval(Z_95),
            "ci_95_student_t9": interval(T9_95),
            "both_intervals_span_zero": interval(Z_95)[0] < 0 < interval(Z_95)[1]
                                        and interval(T9_95)[0] < 0 < interval(T9_95)[1],
            "pairs_candidate_higher": sum(1 for d in diffs if d > 0),
            "pairs_tied": sum(1 for d in diffs if d == 0),
            "pairs_baseline_higher": sum(1 for d in diffs if d < 0),
            "interval_note": ("Both intervals are computed from the unrounded standard error "
                              f"({se:.9f}); the displayed sd and standard_error are that same "
                              "quantity rounded for reading. Multiplying the rounded SE instead "
                              "shifts the bounds by 1e-4."),
        },
        "per_check_mean": {k: {arm: round(sum(per_check[arm][k]) / len(per_check[arm][k]), 4)
                               for arm in ("baseline", "candidate")} for k in CHECKS},
        "total_cost_usd": round(cost, 4),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        raise SystemExit(2)
    with open(sys.argv[1], encoding="utf-8") as fh:
        print(json.dumps(aggregate(json.load(fh)), indent=2))
