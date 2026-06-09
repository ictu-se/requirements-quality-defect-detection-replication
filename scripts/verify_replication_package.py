import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "model_matrix_full613"


def count_jsonl(path):
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def count_csv_rows(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return max(sum(1 for _ in csv.reader(handle)) - 1, 0)


def check(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK: {message}")


def main():
    dataset = ROOT / "data" / "defect_detection_dataset.jsonl"
    audit = ROOT / "data" / "manual_audit_full613_stratified120_sheet.csv"
    roster_path = ROOT / "configs" / "model_roster_12.json"
    prompt = ROOT / "prompts" / "defect_detection_prompt.md"

    check(dataset.exists(), "benchmark JSONL exists")
    check(count_jsonl(dataset) == 613, "benchmark has 613 rows")
    check(audit.exists(), "manual audit sheet exists")
    check(count_csv_rows(audit) == 120, "manual audit sheet has 120 rows")
    check(roster_path.exists(), "12-model roster exists")
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    check(len(roster.get("models", [])) == 12, "model roster has 12 models")
    check(prompt.exists(), "prompt template exists")

    output_files = sorted(RESULTS.glob("*_outputs.jsonl"))
    metric_files = sorted(RESULTS.glob("*_outputs_metrics.csv"))
    check(len(output_files) == 24, "24 full-run raw output files exist")
    check(len(metric_files) == 24, "24 full-run metric files exist")

    for path in output_files:
        check(count_jsonl(path) == 613, f"{path.name} has 613 output rows")
    for path in metric_files:
        check(count_csv_rows(path) == 613, f"{path.name} has 613 metric rows")

    required = [
        "defect_detection_model_matrix_summary_12models.csv",
        "defect_detection_model_matrix_summary_12models.md",
        "defect_detection_model_matrix_summary_12models_by_source.csv",
        "defect_detection_model_matrix_summary_12models_by_defect_type.csv",
        "defect_detection_model_matrix_summary_12models_calibration.csv",
        "defect_detection_model_ranking_12models.csv",
        "defect_detection_model_ranking_12models.md",
        "defect_detection_model_ranking_12models_best_per_model.csv",
        "statistical_bootstrap_ci.csv",
        "statistical_paired_tests.csv",
        "audit120_review_label_tasks.jsonl",
    ]
    for name in required:
        check((RESULTS / name).exists(), f"{name} exists")

    total_outputs = sum(count_jsonl(path) for path in output_files)
    total_metrics = sum(count_csv_rows(path) for path in metric_files)
    check(total_outputs == 14712, "total raw outputs equal 14,712")
    check(total_metrics == 14712, "total metric rows equal 14,712")
    print("Replication package verification complete.")


if __name__ == "__main__":
    main()
