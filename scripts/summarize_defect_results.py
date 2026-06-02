import argparse
import csv
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


def read_rows(paths):
    rows = []
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as f:
            rows.extend(csv.DictReader(f))
    return rows


def as_float(row, key):
    try:
        return float(row.get(key, 0) or 0)
    except ValueError:
        return 0.0


def mean_present(rows, key):
    values = []
    for row in rows:
        value = row.get(key, "")
        if value == "":
            continue
        values.append(as_float(row, key))
    return sum(values) / len(values) if values else 0.0


def binary_f1(tp, fp, fn):
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def macro_type_scores(rows):
    f1s = []
    precisions = []
    recalls = []
    support_types = 0
    for defect_type in DEFECT_TYPES:
        tp = sum(as_float(r, f"{defect_type}_tp") for r in rows)
        fp = sum(as_float(r, f"{defect_type}_fp") for r in rows)
        fn = sum(as_float(r, f"{defect_type}_fn") for r in rows)
        if tp + fp + fn == 0:
            continue
        support_types += 1
        precision, recall, f1 = binary_f1(tp, fp, fn)
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
    return {
        "macro_type_precision": sum(precisions) / len(precisions) if precisions else 0.0,
        "macro_type_recall": sum(recalls) / len(recalls) if recalls else 0.0,
        "macro_type_f1": sum(f1s) / len(f1s) if f1s else 0.0,
        "supported_defect_types": support_types,
    }


def calibration_ece(rows):
    bins = defaultdict(list)
    for row in rows:
        key = row.get("confidence_bin", "")
        if not key:
            continue
        bins[key].append(row)
    total = sum(len(group) for group in bins.values())
    if not total:
        return 0.0
    ece = 0.0
    for group in bins.values():
        avg_conf = mean_present(group, "confidence")
        accuracy = sum(as_float(r, "any_defect_correct") for r in group) / len(group)
        ece += (len(group) / total) * abs(avg_conf - accuracy)
    return ece


def summarize_group(rows):
    n = len(rows)
    if not n:
        return {}
    tp = sum(as_float(r, "type_tp") for r in rows)
    fp = sum(as_float(r, "type_fp") for r in rows)
    fn = sum(as_float(r, "type_fn") for r in rows)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    wtp = sum(as_float(r, "weighted_type_tp") for r in rows)
    wfp = sum(as_float(r, "weighted_type_fp") for r in rows)
    wfn = sum(as_float(r, "weighted_type_fn") for r in rows)
    weighted_precision, weighted_recall, weighted_f1 = binary_f1(wtp, wfp, wfn)
    macro = macro_type_scores(rows)
    return {
        "n": n,
        "parse_rate": sum(as_float(r, "parse_ok") for r in rows) / n,
        "any_defect_accuracy": sum(as_float(r, "any_defect_correct") for r in rows) / n,
        "type_exact_match_rate": sum(as_float(r, "type_exact_match") for r in rows) / n,
        "type_precision": precision,
        "type_recall": recall,
        "type_f1": f1,
        **macro,
        "severity_weighted_precision": weighted_precision,
        "severity_weighted_recall": weighted_recall,
        "severity_weighted_f1": weighted_f1,
        "false_alarm_rate": sum(as_float(r, "false_alarm") for r in rows) / n,
        "missed_defect_rate": sum(as_float(r, "missed_defect") for r in rows) / n,
        "missed_major_or_critical_rate": sum(as_float(r, "missed_major_or_critical") for r in rows) / n,
        "mean_over_report_count": sum(as_float(r, "over_report_count") for r in rows) / n,
        "mean_under_report_count": sum(as_float(r, "under_report_count") for r in rows) / n,
        "mean_severity_abs_error": sum(as_float(r, "severity_abs_error") for r in rows) / n,
        "span_support_rate": mean_present(rows, "span_supported_rate"),
        "unsupported_span_rate": sum(as_float(r, "unsupported_span_count") for r in rows) / max(1, sum(as_float(r, "span_checked_count") for r in rows)),
        "mean_confidence": mean_present(rows, "confidence"),
        "brier_any_defect": mean_present(rows, "brier_any_defect"),
        "ece_any_defect": calibration_ece(rows),
        "high_confidence_wrong_rate": sum(as_float(r, "high_confidence_wrong") for r in rows) / n,
        "low_confidence_correct_rate": sum(as_float(r, "low_confidence_correct") for r in rows) / n,
        "needs_human_review_rate": mean_present(rows, "needs_human_review"),
        "mean_pred_defect_count": sum(as_float(r, "pred_defect_count") for r in rows) / n,
        "mean_elapsed_sec": sum(as_float(r, "elapsed_sec") for r in rows) / n,
    }


def per_type_rows(rows):
    out = []
    groups = defaultdict(list)
    for row in rows:
        groups[(row.get("model", ""), row.get("condition", ""))].append(row)
    for (model, condition), group in sorted(groups.items()):
        for defect_type in DEFECT_TYPES:
            tp = sum(as_float(r, f"{defect_type}_tp") for r in group)
            fp = sum(as_float(r, f"{defect_type}_fp") for r in group)
            fn = sum(as_float(r, f"{defect_type}_fn") for r in group)
            support = sum(as_float(r, f"{defect_type}_gold") for r in group)
            predicted = sum(as_float(r, f"{defect_type}_pred") for r in group)
            precision, recall, f1 = binary_f1(tp, fp, fn)
            out.append({
                "model": model,
                "condition": condition,
                "defect_type": defect_type,
                "gold_support": support,
                "predicted_count": predicted,
                "tp": tp,
                "fp": fp,
                "fn": fn,
                "precision": precision,
                "recall": recall,
                "f1": f1,
            })
    return out


def calibration_rows(rows):
    out = []
    groups = defaultdict(list)
    for row in rows:
        groups[(row.get("model", ""), row.get("condition", ""), row.get("confidence_bin", ""))].append(row)
    for (model, condition, bin_name), group in sorted(groups.items()):
        if not bin_name:
            continue
        out.append({
            "model": model,
            "condition": condition,
            "confidence_bin": bin_name,
            "n": len(group),
            "mean_confidence": mean_present(group, "confidence"),
            "accuracy": sum(as_float(r, "any_defect_correct") for r in group) / len(group),
            "brier_any_defect": mean_present(group, "brier_any_defect"),
        })
    return out


def fmt(value):
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics_csv", nargs="+")
    parser.add_argument("--out-prefix", default="results/defect_detection_summary")
    args = parser.parse_args()

    paths = [Path(p) for p in args.metrics_csv]
    rows = read_rows(paths)
    groups = defaultdict(list)
    source_groups = defaultdict(list)
    for row in rows:
        groups[(row.get("model", ""), row.get("condition", ""))].append(row)
        source_groups[(
            row.get("model", ""),
            row.get("condition", ""),
            row.get("source_type", ""),
            row.get("gold_label_source", ""),
        )].append(row)

    summary_rows = []
    for (model, condition), group in sorted(groups.items()):
        row = {"model": model, "condition": condition}
        row.update(summarize_group(group))
        summary_rows.append(row)

    out_prefix = PROJECT / args.out_prefix
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    csv_path = out_prefix.with_suffix(".csv")
    md_path = out_prefix.with_suffix(".md")
    fields = list(summary_rows[0].keys()) if summary_rows else []
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary_rows)

    with md_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("# Defect Detection Summary\n\n")
        if summary_rows:
            f.write("| Model | Condition | N | Parse | Any acc | Micro F1 | Macro F1 | Sev F1 | False alarm | Missed major | Span support | Brier | ECE | Mean sec |\n")
            f.write("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n")
            for row in summary_rows:
                f.write(
                    f"| {row['model']} | {row['condition']} | {row['n']} | {fmt(row['parse_rate'])} | "
                    f"{fmt(row['any_defect_accuracy'])} | {fmt(row['type_f1'])} | "
                    f"{fmt(row['macro_type_f1'])} | {fmt(row['severity_weighted_f1'])} | "
                    f"{fmt(row['false_alarm_rate'])} | {fmt(row['missed_major_or_critical_rate'])} | "
                    f"{fmt(row['span_support_rate'])} | {fmt(row['brier_any_defect'])} | "
                    f"{fmt(row['ece_any_defect'])} | "
                    f"{fmt(row['mean_elapsed_sec'])} |\n"
                )
            f.write("\n## By Source Type\n\n")
            f.write("| Model | Condition | Source type | Label source | N | Parse | Any-defect acc | Type F1 | False alarm | Missed defect |\n")
            f.write("| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |\n")
            for key, group in sorted(source_groups.items()):
                model, condition, source_type, label_source = key
                source_row = summarize_group(group)
                f.write(
                    f"| {model} | {condition} | {source_type} | {label_source} | {source_row['n']} | "
                    f"{fmt(source_row['parse_rate'])} | {fmt(source_row['any_defect_accuracy'])} | "
                    f"{fmt(source_row['type_f1'])} | {fmt(source_row['false_alarm_rate'])} | "
                    f"{fmt(source_row['missed_defect_rate'])} |\n"
                )

    source_csv_path = out_prefix.with_name(out_prefix.name + "_by_source").with_suffix(".csv")
    source_rows = []
    for key, group in sorted(source_groups.items()):
        model, condition, source_type, label_source = key
        row = {
            "model": model,
            "condition": condition,
            "source_type": source_type,
            "gold_label_source": label_source,
        }
        row.update(summarize_group(group))
        source_rows.append(row)
    if source_rows:
        with source_csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(source_rows[0].keys()))
            writer.writeheader()
            writer.writerows(source_rows)
    type_csv_path = out_prefix.with_name(out_prefix.name + "_by_defect_type").with_suffix(".csv")
    type_rows = per_type_rows(rows)
    if type_rows:
        with type_csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(type_rows[0].keys()))
            writer.writeheader()
            writer.writerows(type_rows)
    calibration_csv_path = out_prefix.with_name(out_prefix.name + "_calibration").with_suffix(".csv")
    cal_rows = calibration_rows(rows)
    if cal_rows:
        with calibration_csv_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(cal_rows[0].keys()))
            writer.writeheader()
            writer.writerows(cal_rows)
    print(f"wrote {csv_path}, {md_path}, {source_csv_path}, {type_csv_path}, and {calibration_csv_path}")


if __name__ == "__main__":
    main()
