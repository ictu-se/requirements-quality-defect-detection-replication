import argparse
import csv
import json
import re
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[2]
PROJECT_DATA = ROOT / "datasets" / "04_requirements_quality_defect_detection__data"
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
DEFECT_TYPE_SET = set(DEFECT_TYPES)
SEVERITY_WEIGHT = {"none": 0, "minor": 1, "major": 2, "critical": 3}


def resolve_tasks_path(value):
    path = Path(value)
    if path.is_absolute() and path.exists():
        return path
    project_path = PROJECT / path
    if project_path.exists():
        return project_path
    data_path = PROJECT_DATA / path.name
    if data_path.exists():
        return data_path
    return project_path


def extract_json(text):
    if not text:
        return None
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            return None
    return None


def load_tasks(path):
    tasks = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            tasks[row["task_id"]] = row
    return tasks


def predicted_types(parsed):
    if not isinstance(parsed, dict):
        return set()
    defects = parsed.get("defects", [])
    found = set()
    if isinstance(defects, list):
        for item in defects:
            if isinstance(item, dict):
                label = str(item.get("type", "")).strip()
            else:
                label = str(item).strip()
            if label in DEFECT_TYPE_SET:
                found.add(label)
    return found


def predicted_has_defect(parsed, pred_types):
    if isinstance(parsed, dict) and isinstance(parsed.get("has_defect"), bool):
        return parsed["has_defect"]
    return bool(pred_types)


def clamp01(value, default=""):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if number < 0:
        return 0.0
    if number > 1:
        return 1.0
    return number


def normalized_text(text):
    return re.sub(r"\s+", " ", str(text or "")).strip().lower()


def defect_items(parsed):
    if not isinstance(parsed, dict):
        return []
    items = parsed.get("defects", [])
    return items if isinstance(items, list) else []


def max_pred_severity(items):
    max_weight = 0
    max_label = "none"
    for item in items:
        if not isinstance(item, dict):
            continue
        label = str(item.get("severity", "")).strip().lower()
        weight = SEVERITY_WEIGHT.get(label, 0)
        if weight > max_weight:
            max_weight = weight
            max_label = label
    return max_label, max_weight


def span_support(items, statement):
    statement_norm = normalized_text(statement)
    checked = 0
    supported = 0
    unsupported_labels = []
    copied_chars = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        label = str(item.get("type", "")).strip()
        if label not in DEFECT_TYPE_SET:
            continue
        span = normalized_text(item.get("span", ""))
        if not span:
            continue
        checked += 1
        copied_chars += len(span)
        if span in statement_norm:
            supported += 1
        else:
            unsupported_labels.append(label)
    rate = supported / checked if checked else ""
    return checked, supported, rate, unsupported_labels, copied_chars


def confidence_values(parsed, items, pred_has):
    top = ""
    if isinstance(parsed, dict):
        top = clamp01(parsed.get("confidence", ""), "")
    defect_conf = []
    for item in items:
        if isinstance(item, dict):
            value = clamp01(item.get("confidence", ""), "")
            if value != "":
                defect_conf.append(value)
    if top == "" and defect_conf:
        top = sum(defect_conf) / len(defect_conf)
    if top == "":
        top = 1.0 if pred_has else 0.0
    return top, defect_conf


def calibration_bin(confidence):
    if confidence == "":
        return ""
    index = min(9, int(float(confidence) * 10))
    low = index / 10
    high = low + 0.1
    return f"{low:.1f}-{high:.1f}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("outputs_jsonl")
    parser.add_argument("--tasks", default="data/defect_detection_pilot90.jsonl")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    tasks = load_tasks(resolve_tasks_path(args.tasks))
    in_path = Path(args.outputs_jsonl)
    out_path = Path(args.out) if args.out else PROJECT / "results" / (in_path.stem + "_metrics.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    with in_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            task = tasks.get(record.get("task_id"), {})
            parsed = extract_json(record.get("stdout", ""))
            pred = predicted_types(parsed)
            gold = set(task.get("gold_defect_types", []))
            pred_has = predicted_has_defect(parsed, pred)
            gold_has = bool(task.get("gold_has_defect", False))
            items = defect_items(parsed)
            pred_severity, pred_severity_weight = max_pred_severity(items)
            gold_severity = str(task.get("gold_severity", "none") or "none").lower()
            gold_severity_weight = SEVERITY_WEIGHT.get(gold_severity, 0)
            span_checked, span_supported, span_supported_rate, unsupported_span_labels, copied_chars = span_support(
                items, task.get("statement", "")
            )
            confidence, defect_conf = confidence_values(parsed, items, pred_has)
            any_correct = int(gold_has == pred_has)
            brier = (float(confidence) - float(gold_has)) ** 2 if confidence != "" else ""
            needs_human_review = ""
            if isinstance(parsed, dict) and isinstance(parsed.get("needs_human_review"), bool):
                needs_human_review = int(parsed["needs_human_review"])
            tp = len(pred & gold)
            fp = len(pred - gold)
            fn = len(gold - pred)
            weighted_tp = sum(gold_severity_weight for label in pred & gold)
            weighted_fp = sum(max(1, pred_severity_weight) for label in pred - gold)
            weighted_fn = sum(gold_severity_weight for label in gold - pred)
            per_type = {}
            for defect_type in DEFECT_TYPES:
                per_type[f"{defect_type}_gold"] = int(defect_type in gold)
                per_type[f"{defect_type}_pred"] = int(defect_type in pred)
                per_type[f"{defect_type}_tp"] = int(defect_type in gold and defect_type in pred)
                per_type[f"{defect_type}_fp"] = int(defect_type not in gold and defect_type in pred)
                per_type[f"{defect_type}_fn"] = int(defect_type in gold and defect_type not in pred)
            rows.append({
                "task_id": record.get("task_id", ""),
                "source_type": record.get("source_type", task.get("source_type", "")),
                "repo": record.get("repo", task.get("repo", "")),
                "language": record.get("language", task.get("language", "")),
                "condition": record.get("condition", ""),
                "model": record.get("model", ""),
                "returncode": record.get("returncode", ""),
                "elapsed_sec": record.get("elapsed_sec", ""),
                "parse_ok": int(parsed is not None),
                "gold_has_defect": int(gold_has),
                "pred_has_defect": int(pred_has),
                "any_defect_correct": any_correct,
                "gold_defect_types": "|".join(sorted(gold)),
                "pred_defect_types": "|".join(sorted(pred)),
                "type_tp": tp,
                "type_fp": fp,
                "type_fn": fn,
                "weighted_type_tp": weighted_tp,
                "weighted_type_fp": weighted_fp,
                "weighted_type_fn": weighted_fn,
                "type_exact_match": int(pred == gold),
                "false_alarm": int((not gold_has) and pred_has),
                "missed_defect": int(gold_has and (not pred_has)),
                "over_report_count": max(0, len(pred) - len(gold)),
                "under_report_count": max(0, len(gold) - len(pred)),
                "pred_defect_count": len(pred),
                "gold_label_source": task.get("gold_label_source", ""),
                "gold_severity": gold_severity,
                "pred_severity": pred_severity,
                "gold_severity_weight": gold_severity_weight,
                "pred_severity_weight": pred_severity_weight,
                "severity_abs_error": abs(pred_severity_weight - gold_severity_weight),
                "missed_major_or_critical": int(gold_severity_weight >= 2 and not pred_has),
                "unsupported_span_count": max(0, span_checked - span_supported),
                "span_checked_count": span_checked,
                "span_supported_count": span_supported,
                "span_supported_rate": span_supported_rate,
                "unsupported_span_labels": "|".join(sorted(set(unsupported_span_labels))),
                "copied_span_chars": copied_chars,
                "confidence": confidence,
                "mean_defect_confidence": (sum(defect_conf) / len(defect_conf)) if defect_conf else "",
                "brier_any_defect": brier,
                "confidence_bin": calibration_bin(confidence),
                "high_confidence_wrong": int(confidence != "" and float(confidence) >= 0.8 and not any_correct),
                "low_confidence_correct": int(confidence != "" and float(confidence) <= 0.6 and any_correct),
                "needs_human_review": needs_human_review,
                **per_type,
            })

    fields = list(rows[0].keys()) if rows else []
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} metric rows to {out_path}")


if __name__ == "__main__":
    main()
