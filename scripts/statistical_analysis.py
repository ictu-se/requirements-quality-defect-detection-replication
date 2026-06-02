import argparse
import csv
import random
from pathlib import Path


DEFECT_TYPES = [
    "ambiguous_term",
    "missing_actor",
    "missing_trigger",
    "missing_expected_outcome",
    "missing_constraint",
    "not_testable",
    "overly_broad_requirement",
    "inconsistent_condition",
    "unsupported_external_assumption",
]

FOCUS = [
    ("gemma3:4b", "zero_shot"),
    ("gemma3:4b", "rubric_guided"),
    ("qwen3:4b", "zero_shot"),
    ("qwen2.5-coder:14b", "rubric_guided"),
    ("qwen2.5-coder:1.5b", "zero_shot"),
]

PAIRS = [
    ("gemma3:4b", "zero_shot", "gemma3:4b", "rubric_guided"),
    ("gemma3:4b", "zero_shot", "qwen2.5-coder:14b", "rubric_guided"),
    ("qwen2.5-coder:14b", "rubric_guided", "qwen2.5-coder:14b", "zero_shot"),
    ("qwen2.5-coder:1.5b", "zero_shot", "qwen2.5-coder:1.5b", "rubric_guided"),
]


def model_file_stem(model):
    return model.replace(":", "_").replace("/", "_")


def read_metrics(path):
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda row: row["task_id"])
    return rows


def as_float(row, key):
    value = row.get(key, "")
    return float(value) if value != "" else 0.0


def f1(tp, fp, fn):
    denom = (2 * tp) + fp + fn
    return (2 * tp / denom) if denom else 0.0


def aggregate(rows):
    n = len(rows)
    tp = sum(as_float(row, "type_tp") for row in rows)
    fp = sum(as_float(row, "type_fp") for row in rows)
    fn = sum(as_float(row, "type_fn") for row in rows)
    wtp = sum(as_float(row, "weighted_type_tp") for row in rows)
    wfp = sum(as_float(row, "weighted_type_fp") for row in rows)
    wfn = sum(as_float(row, "weighted_type_fn") for row in rows)
    macro = []
    for defect_type in DEFECT_TYPES:
        macro.append(
            f1(
                sum(as_float(row, f"{defect_type}_tp") for row in rows),
                sum(as_float(row, f"{defect_type}_fp") for row in rows),
                sum(as_float(row, f"{defect_type}_fn") for row in rows),
            )
        )
    return {
        "n": n,
        "any_acc": sum(as_float(row, "any_defect_correct") for row in rows) / n,
        "micro_f1": f1(tp, fp, fn),
        "macro_f1": sum(macro) / len(macro),
        "severity_f1": f1(wtp, wfp, wfn),
        "false_alarm": sum(as_float(row, "false_alarm") for row in rows) / n,
        "missed_major": sum(as_float(row, "missed_major_or_critical") for row in rows) / n,
        "span_support": (
            sum(as_float(row, "span_supported_count") for row in rows)
            / max(1.0, sum(as_float(row, "span_checked_count") for row in rows))
        ),
        "brier": sum(as_float(row, "brier_any_defect") for row in rows) / n,
        "mean_sec": sum(as_float(row, "elapsed_sec") for row in rows) / n,
    }


def percentile(values, q):
    if not values:
        return 0.0
    values = sorted(values)
    pos = (len(values) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(values) - 1)
    frac = pos - lo
    return values[lo] * (1 - frac) + values[hi] * frac


def bootstrap_ci(rows, rng, iterations):
    n = len(rows)
    samples = {key: [] for key in aggregate(rows) if key != "n"}
    for _ in range(iterations):
        draw = [rows[rng.randrange(n)] for _ in range(n)]
        agg = aggregate(draw)
        for key in samples:
            samples[key].append(agg[key])
    return {
        key: (percentile(values, 0.025), percentile(values, 0.975))
        for key, values in samples.items()
    }


def paired_permutation(rows_a, rows_b, metric, rng, iterations):
    by_a = {row["task_id"]: row for row in rows_a}
    by_b = {row["task_id"]: row for row in rows_b}
    task_ids = sorted(set(by_a) & set(by_b))
    diffs = [as_float(by_a[task_id], metric) - as_float(by_b[task_id], metric) for task_id in task_ids]
    observed = sum(diffs) / len(diffs)
    count = 0
    for _ in range(iterations):
        sampled = sum(diff if rng.random() < 0.5 else -diff for diff in diffs) / len(diffs)
        if abs(sampled) >= abs(observed) - 1e-12:
            count += 1
    return observed, (count + 1) / (iterations + 1), len(task_ids)


def fmt_ci(value, ci):
    return f"{value:.3f} [{ci[0]:.3f}, {ci[1]:.3f}]"


def write_ci_table(path, rows):
    fields = [
        "model",
        "condition",
        "n",
        "any_acc_ci",
        "micro_f1_ci",
        "macro_f1_ci",
        "severity_f1_ci",
        "false_alarm_ci",
        "missed_major_ci",
        "brier_ci",
        "mean_sec_ci",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_pair_table(path, rows):
    fields = [
        "comparison",
        "n",
        "any_acc_delta",
        "any_acc_p",
        "false_alarm_delta",
        "false_alarm_p",
        "missed_major_delta",
        "missed_major_p",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results/model_matrix_full613")
    parser.add_argument("--out-dir", default="results/model_matrix_full613")
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--permutations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260602)
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)

    data = {}
    for model, condition in set(FOCUS + [(a, b) for a, b, _, _ in PAIRS] + [(c, d) for _, _, c, d in PAIRS]):
        path = results_dir / f"{model_file_stem(model)}_{condition}_outputs_metrics.csv"
        if path.exists():
            data[(model, condition)] = read_metrics(path)

    ci_rows = []
    for model, condition in FOCUS:
        rows = data[(model, condition)]
        agg = aggregate(rows)
        ci = bootstrap_ci(rows, rng, args.bootstrap)
        ci_rows.append(
            {
                "model": model,
                "condition": condition,
                "n": agg["n"],
                "any_acc_ci": fmt_ci(agg["any_acc"], ci["any_acc"]),
                "micro_f1_ci": fmt_ci(agg["micro_f1"], ci["micro_f1"]),
                "macro_f1_ci": fmt_ci(agg["macro_f1"], ci["macro_f1"]),
                "severity_f1_ci": fmt_ci(agg["severity_f1"], ci["severity_f1"]),
                "false_alarm_ci": fmt_ci(agg["false_alarm"], ci["false_alarm"]),
                "missed_major_ci": fmt_ci(agg["missed_major"], ci["missed_major"]),
                "brier_ci": fmt_ci(agg["brier"], ci["brier"]),
                "mean_sec_ci": fmt_ci(agg["mean_sec"], ci["mean_sec"]),
            }
        )

    pair_rows = []
    for a_model, a_condition, b_model, b_condition in PAIRS:
        rows_a = data[(a_model, a_condition)]
        rows_b = data[(b_model, b_condition)]
        any_delta, any_p, n = paired_permutation(rows_a, rows_b, "any_defect_correct", rng, args.permutations)
        fa_delta, fa_p, _ = paired_permutation(rows_a, rows_b, "false_alarm", rng, args.permutations)
        mm_delta, mm_p, _ = paired_permutation(rows_a, rows_b, "missed_major_or_critical", rng, args.permutations)
        pair_rows.append(
            {
                "comparison": f"{a_model} {a_condition} minus {b_model} {b_condition}",
                "n": n,
                "any_acc_delta": f"{any_delta:.3f}",
                "any_acc_p": f"{any_p:.4f}",
                "false_alarm_delta": f"{fa_delta:.3f}",
                "false_alarm_p": f"{fa_p:.4f}",
                "missed_major_delta": f"{mm_delta:.3f}",
                "missed_major_p": f"{mm_p:.4f}",
            }
        )

    ci_path = out_dir / "statistical_bootstrap_ci.csv"
    pair_path = out_dir / "statistical_paired_tests.csv"
    write_ci_table(ci_path, ci_rows)
    write_pair_table(pair_path, pair_rows)
    print(f"wrote {ci_path}")
    print(f"wrote {pair_path}")


if __name__ == "__main__":
    main()
