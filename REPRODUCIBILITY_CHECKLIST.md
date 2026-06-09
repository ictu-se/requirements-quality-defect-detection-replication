# Reproducibility Checklist

Run all commands from the package root.

## 1. Verify Package Integrity

```bash
python3 scripts/verify_replication_package.py
```

Expected result: all checks pass. The script verifies benchmark size, audit size, model roster size, full-output files, metric files, and key summary/statistical files.

## 2. Recompute Summary Tables From Existing Metrics

```bash
python3 scripts/summarize_defect_results.py \
  results/model_matrix_full613/*_outputs_metrics.csv \
  --out-prefix results/model_matrix_full613/defect_detection_model_matrix_summary
```

Main regenerated outputs:

- `results/model_matrix_full613/defect_detection_model_matrix_summary.csv`
- `results/model_matrix_full613/defect_detection_model_matrix_summary.md`
- `results/model_matrix_full613/defect_detection_model_matrix_summary_by_source.csv`
- `results/model_matrix_full613/defect_detection_model_matrix_summary_by_defect_type.csv`
- `results/model_matrix_full613/defect_detection_model_matrix_summary_calibration.csv`

## 3. Recompute Model Ranking

```bash
python3 scripts/rank_model_matrix.py \
  results/model_matrix_full613/*_outputs_metrics.csv \
  --roster configs/model_roster_12.json \
  --out-prefix results/model_matrix_full613/defect_detection_model_ranking
```

Main regenerated outputs:

- `results/model_matrix_full613/defect_detection_model_ranking.csv`
- `results/model_matrix_full613/defect_detection_model_ranking.md`
- `results/model_matrix_full613/defect_detection_model_ranking_best_per_model.csv`

## 4. Recompute Statistical Tests

```bash
python3 scripts/statistical_analysis.py \
  --results-dir results/model_matrix_full613 \
  --out-dir results/model_matrix_full613
```

Main regenerated outputs:

- `results/model_matrix_full613/statistical_bootstrap_ci.csv`
- `results/model_matrix_full613/statistical_paired_tests.csv`

## 5. Re-score Raw Outputs

To verify the classifier/parser/scorer against raw outputs, re-score any full-output file:

```bash
python3 scripts/score_defect_outputs.py \
  results/model_matrix_full613/qwen2.5-coder_32b_rubric_guided_outputs.jsonl \
  --tasks data/defect_detection_dataset.jsonl \
  --out /tmp/qwen32_rubric_rescore.csv
```

The output should contain 613 scored rows plus the CSV header.

## 6. Run A Small Fresh Experiment

This step requires Ollama and at least one local model.

```bash
ollama pull gemma3:4b

python3 scripts/run_ollama_defect_detection.py \
  --model gemma3:4b \
  --tasks data/defect_detection_dataset.jsonl \
  --condition zero_shot \
  --limit 5 \
  --out results/model_matrix_full613/gemma3_4b_zero_shot_smoke_outputs.jsonl

python3 scripts/score_defect_outputs.py \
  results/model_matrix_full613/gemma3_4b_zero_shot_smoke_outputs.jsonl \
  --tasks data/defect_detection_dataset.jsonl \
  --out results/model_matrix_full613/gemma3_4b_zero_shot_smoke_outputs_metrics.csv
```

This checks that the runner, prompt renderer, output parser, and scorer work in the reviewer's local environment.

## 7. Re-run The Full Model Matrix

This step requires all models listed in `configs/model_roster_12.json` and substantial local runtime.

```bash
python3 scripts/run_model_matrix.py \
  --roster configs/model_roster_12.json \
  --tasks data/defect_detection_dataset.jsonl \
  --out-dir results/model_matrix_full613 \
  --conditions zero_shot rubric_guided \
  --timeout 240 \
  --score \
  --summarize
```

Expected scale: 12 models x 2 prompt conditions x 613 artifacts = 14,712 generations.

## 8. Inspect Manual Audit

The completed audit sheet is:

```text
data/manual_audit_full613_stratified120_sheet.csv
```

To inspect the browser-based audit workflow:

```bash
python3 audit_app/server.py --host 127.0.0.1 --port 8765
```

Then open `http://127.0.0.1:8765`.
