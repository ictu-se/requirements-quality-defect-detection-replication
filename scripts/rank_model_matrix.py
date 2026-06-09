import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
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


def as_float(row, key):
    try:
        return float(row.get(key, 0) or 0)
    except ValueError:
        return 0.0


def read_rows(paths):
    rows = []
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as f:
            rows.extend(csv.DictReader(f))
    return rows


def mean_present(rows, key):
    values = [as_float(row, key) for row in rows if row.get(key, "") != ""]
    return sum(values) / len(values) if values else 0.0


def binary_f1(tp, fp, fn):
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def macro_f1(rows):
    f1s = []
    for defect_type in DEFECT_TYPES:
        tp = sum(as_float(r, f"{defect_type}_tp") for r in rows)
        fp = sum(as_float(r, f"{defect_type}_fp") for r in rows)
        fn = sum(as_float(r, f"{defect_type}_fn") for r in rows)
        if tp + fp + fn:
            f1s.append(binary_f1(tp, fp, fn)[2])
    return sum(f1s) / len(f1s) if f1s else 0.0


def calibration_ece(rows):
    bins = defaultdict(list)
    for row in rows:
        if row.get("confidence_bin", ""):
            bins[row["confidence_bin"]].append(row)
    total = sum(len(group) for group in bins.values())
    if not total:
        return 0.0
    ece = 0.0
    for group in bins.values():
        avg_conf = mean_present(group, "confidence")
        accuracy = sum(as_float(r, "any_defect_correct") for r in group) / len(group)
        ece += (len(group) / total) * abs(avg_conf - accuracy)
    return ece


def summarize(rows):
    n = len(rows)
    if not n:
        return {}
    tp = sum(as_float(r, "type_tp") for r in rows)
    fp = sum(as_float(r, "type_fp") for r in rows)
    fn = sum(as_float(r, "type_fn") for r in rows)
    precision, recall, f1 = binary_f1(tp, fp, fn)
    wtp = sum(as_float(r, "weighted_type_tp") for r in rows)
    wfp = sum(as_float(r, "weighted_type_fp") for r in rows)
    wfn = sum(as_float(r, "weighted_type_fn") for r in rows)
    weighted_f1 = binary_f1(wtp, wfp, wfn)[2]
    macro = macro_f1(rows)
    parse_rate = sum(as_float(r, "parse_ok") for r in rows) / n
    any_acc = sum(as_float(r, "any_defect_correct") for r in rows) / n
    false_alarm = sum(as_float(r, "false_alarm") for r in rows) / n
    missed = sum(as_float(r, "missed_defect") for r in rows) / n
    missed_major = sum(as_float(r, "missed_major_or_critical") for r in rows) / n
    exact = sum(as_float(r, "type_exact_match") for r in rows) / n
    elapsed = sum(as_float(r, "elapsed_sec") for r in rows) / n
    span_support = mean_present(rows, "span_supported_rate")
    brier = mean_present(rows, "brier_any_defect")
    ece = calibration_ece(rows)
    score = (
        24.0 * f1
        + 16.0 * macro
        + 15.0 * weighted_f1
        + 18.0 * any_acc
        + 12.0 * parse_rate
        + 8.0 * exact
        + 4.0 * span_support
        - 7.5 * false_alarm
        - 7.5 * missed
        - 10.0 * missed_major
        - 4.0 * brier
        - 4.0 * ece
    )
    return {
        "n": n,
        "parse_rate": parse_rate,
        "any_defect_accuracy": any_acc,
        "type_precision": precision,
        "type_recall": recall,
        "type_f1": f1,
        "macro_type_f1": macro,
        "severity_weighted_f1": weighted_f1,
        "type_exact_match_rate": exact,
        "false_alarm_rate": false_alarm,
        "missed_defect_rate": missed,
        "missed_major_or_critical_rate": missed_major,
        "span_support_rate": span_support,
        "brier_any_defect": brier,
        "ece_any_defect": ece,
        "mean_elapsed_sec": elapsed,
        "selection_score": score,
    }


def load_roster(path):
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {row["name"]: row for row in data.get("models", [])}


def reason_for(row, roster_row):
    reasons = []
    if row["type_f1"] >= 0.45:
        reasons.append("strong defect-type F1")
    elif row["type_f1"] <= 0.10:
        reasons.append("weak defect-type discrimination")
    if row["macro_type_f1"] >= 0.35:
        reasons.append("broad coverage across defect types")
    elif row["macro_type_f1"] <= 0.10:
        reasons.append("poor minority-defect coverage")
    if row["severity_weighted_f1"] >= row["type_f1"] + 0.05:
        reasons.append("better on higher-severity labels")
    if row["any_defect_accuracy"] >= 0.70:
        reasons.append("good any-defect accuracy")
    if row["false_alarm_rate"] <= 0.10:
        reasons.append("low false-alarm rate")
    elif row["false_alarm_rate"] >= 0.30:
        reasons.append("high false-alarm rate")
    if row["missed_defect_rate"] <= 0.10:
        reasons.append("low missed-defect rate")
    elif row["missed_defect_rate"] >= 0.30:
        reasons.append("misses many defects")
    if row["parse_rate"] < 0.95:
        reasons.append("JSON robustness risk")
    if row["span_support_rate"] >= 0.80:
        reasons.append("well-grounded spans")
    if row["brier_any_defect"] <= 0.15:
        reasons.append("well-calibrated confidence")
    elif row["brier_any_defect"] >= 0.30:
        reasons.append("poor confidence calibration")
    if row["mean_elapsed_sec"] <= 3.0:
        reasons.append("fast runtime")
    elif row["mean_elapsed_sec"] >= 10.0:
        reasons.append("slow runtime")
    role = roster_row.get("role", "")
    if role:
        reasons.append(role)
    return "; ".join(reasons) if reasons else "balanced profile"


def fmt(value):
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics_csv", nargs="+")
    parser.add_argument("--roster", default="configs/model_roster_12.json")
    parser.add_argument("--out-prefix", default="results/defect_detection_model_ranking")
    args = parser.parse_args()

    paths = [Path(p) for p in args.metrics_csv]
    rows = read_rows(paths)
    roster = load_roster(PROJECT / args.roster)

    groups = defaultdict(list)
    model_groups = defaultdict(list)
    for row in rows:
        groups[(row.get("model", ""), row.get("condition", ""))].append(row)
        model_groups[row.get("model", "")].append(row)

    ranked_rows = []
    for (model, condition), group in sorted(groups.items()):
        row = {"model": model, "condition": condition}
        row.update(summarize(group))
        row["family"] = roster.get(model, {}).get("family", "")
        row["type"] = roster.get(model, {}).get("type", "")
        row["reason"] = reason_for(row, roster.get(model, {}))
        ranked_rows.append(row)
    ranked_rows.sort(key=lambda r: r["selection_score"], reverse=True)

    best_per_model = []
    by_model = defaultdict(list)
    for row in ranked_rows:
        by_model[row["model"]].append(row)
    for model, model_rows in by_model.items():
        best_per_model.append(max(model_rows, key=lambda r: r["selection_score"]))
    best_per_model.sort(key=lambda r: r["selection_score"], reverse=True)

    out_prefix = PROJECT / args.out_prefix
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    csv_path = out_prefix.with_suffix(".csv")
    best_csv_path = out_prefix.with_name(out_prefix.name + "_best_per_model").with_suffix(".csv")
    md_path = out_prefix.with_suffix(".md")

    fields = [
        "model", "condition", "family", "type", "n", "selection_score",
        "parse_rate", "any_defect_accuracy", "type_f1", "macro_type_f1",
        "severity_weighted_f1", "type_precision", "type_recall",
        "type_exact_match_rate", "false_alarm_rate", "missed_defect_rate",
        "missed_major_or_critical_rate", "span_support_rate",
        "brier_any_defect", "ece_any_defect", "mean_elapsed_sec", "reason",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(ranked_rows)
    with best_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(best_per_model)

    with md_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("# Defect Detection Model Ranking\n\n")
        f.write("Selection score combines micro-F1, macro-F1, severity-weighted F1, any-defect accuracy, parse rate, exact match, span support, false alarms, missed defects, missed major/critical defects, Brier score, and ECE.\n\n")
        f.write("## Best Condition Per Model\n\n")
        f.write("| Rank | Model | Best condition | Family | Type | Score | Micro F1 | Macro F1 | Sev F1 | Any acc | False alarm | Missed major | Brier | Mean sec | Why |\n")
        f.write("| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |\n")
        for index, row in enumerate(best_per_model, start=1):
            f.write(
                f"| {index} | {row['model']} | {row['condition']} | {row['family']} | {row['type']} | "
                f"{fmt(row['selection_score'])} | {fmt(row['type_f1'])} | {fmt(row['macro_type_f1'])} | "
                f"{fmt(row['severity_weighted_f1'])} | {fmt(row['any_defect_accuracy'])} | "
                f"{fmt(row['false_alarm_rate'])} | {fmt(row['missed_major_or_critical_rate'])} | "
                f"{fmt(row['brier_any_defect'])} | "
                f"{fmt(row['mean_elapsed_sec'])} | {row['reason']} |\n"
            )
        f.write("\n## All Model-Condition Rows\n\n")
        f.write("| Rank | Model | Condition | Score | Parse | Micro F1 | Macro F1 | Sev F1 | Any acc | False alarm | Missed major | Brier | Mean sec |\n")
        f.write("| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n")
        for index, row in enumerate(ranked_rows, start=1):
            f.write(
                f"| {index} | {row['model']} | {row['condition']} | {fmt(row['selection_score'])} | "
                f"{fmt(row['parse_rate'])} | {fmt(row['type_f1'])} | {fmt(row['macro_type_f1'])} | "
                f"{fmt(row['severity_weighted_f1'])} | {fmt(row['any_defect_accuracy'])} | "
                f"{fmt(row['false_alarm_rate'])} | {fmt(row['missed_major_or_critical_rate'])} | "
                f"{fmt(row['brier_any_defect'])} | "
                f"{fmt(row['mean_elapsed_sec'])} |\n"
            )
    print(f"wrote {csv_path}, {best_csv_path}, and {md_path}")


if __name__ == "__main__":
    main()
