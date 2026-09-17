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

# Two-sided 95% Student's t critical values by degrees of freedom. The standard library has no t
# distribution, so this is a table rather than a computation. The critical value depends on n, and
# n comes from the input (harness.py takes N_PAIRS from the environment), so it is derived per run
# and the emitted key is named from the actual df. Outside the table this raises rather than
# approximating: a silently mislabelled interval is the defect this table exists to prevent.
T_95_BY_DF = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
    9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 21: 2.080, 22: 2.074,
    23: 2.069, 24: 2.064, 25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042,
}


def t_critical_95(df: int) -> float:
    """Two-sided 95% t critical value for df, or a loud failure."""
    try:
        return T_95_BY_DF[df]
    except KeyError:
        raise ValueError(
            "no tabulated two-sided 95%% t critical value for df=%d (table covers 1-30). "
            "Extend T_95_BY_DF rather than substituting a nearby value: an interval computed "
            "with the wrong critical value and labelled with the right df is worse than no "
            "interval." % df) from None


def aggregate(bundle: dict) -> dict:
    base, cand, diffs, indet_calls, indet_arms = [], [], [], 0, 0
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
                indet_arms += 1
            else:
                (base if arm == "baseline" else cand).append(s["total"])
                for k in CHECKS:
                    per_check[arm][k].append(s[k])
            # Two calls per arm: the generating call and its grader call. Count both, so the
            # name matches what is counted.
            for call in (rec, grading.get("grader_record")):
                if call is None:
                    indet_calls += 1
                    continue
                if call.get("status") != "completed":
                    indet_calls += 1
                cost += (call.get("result_json") or {}).get("total_cost_usd") or 0.0
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

    df = len(diffs) - 1
    t_crit = t_critical_95(df)
    t_key = "ci_95_student_t%d" % df
    # The cost of the defect this producer was committed to fix, measured rather than asserted.
    rounding_shift = max(abs(round(mean - k * se, 4) - round(mean - k * round(se, 4), 4))
                         for k in (Z_95, t_crit))

    return {
        "n_pairs": len(diffs),
        "indeterminate_calls": indet_calls,
        "indeterminate_arms": indet_arms,
        "baseline": arm_block(base),
        "candidate": arm_block(cand),
        "paired_difference_candidate_minus_baseline": {
            "mean": round(mean, 4),
            "sd": round(sd, 4),
            "standard_error": round(se, 4),
            "ci_95_normal_z": interval(Z_95),
            t_key: interval(t_crit),
            "t_degrees_of_freedom": df,
            "t_critical_value": t_crit,
            "both_intervals_span_zero": interval(Z_95)[0] < 0 < interval(Z_95)[1]
                                        and interval(t_crit)[0] < 0 < interval(t_crit)[1],
            "pairs_candidate_higher": sum(1 for d in diffs if d > 0),
            "pairs_tied": sum(1 for d in diffs if d == 0),
            "pairs_baseline_higher": sum(1 for d in diffs if d < 0),
            "interval_note": ("Both intervals are computed from the unrounded standard error "
                              f"({se:.9f}); the displayed sd and standard_error are that same "
                              "quantity rounded for reading. Multiplying the rounded SE instead "
                              f"would shift a bound by up to {rounding_shift:.1e}. The t critical "
                              f"value {t_crit} is the two-sided 95% value for df={df}, derived from "
                              "this input rather than fixed."),
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
