# Requirements-Quality Defect Detection Replication Package

This repository contains the code, prompts, benchmark data, manual-audit sheet, and experiment outputs for the study on local LLM screening of requirements-quality defects.

## Quick Verification

Run the package self-check first:

```bash
python3 scripts/verify_replication_package.py
```

The script verifies that the package contains the 613-row benchmark, the 120-row audit sheet, the 12-model roster, 24 full-run output files, 24 metric files, complete 613-row outputs for every model--condition job, and the summary/statistical files used by the manuscript.

## Contents

- `data/`: the 613-row benchmark, dataset summary, related-work figure input, and 120-row manual-audit sheet.
- `configs/`: the 12-model Ollama roster used in the full experiment.
- `prompts/`: the zero-shot and rubric-guided prompt template.
- `scripts/`: experiment runners, scoring scripts, summary/ranking scripts, statistical analysis, and figure-generation scripts.
- `results/model_matrix_full613/`: full model outputs, per-run metrics, summary tables, rankings, calibration tables, and statistical test outputs.
- `audit_app/`: local browser interface used for blinded manual audit.
- `docs/`: defect taxonomy and evaluation framework.
- `ARTIFACT_MANIFEST.md`: file-by-file description of the package contents.
- `REPRODUCIBILITY_CHECKLIST.md`: ordered commands for verifying, re-scoring, re-summarizing, and re-running experiments.
- `CHECKSUMS_SHA256.txt`: SHA-256 checksums for package files.

The repository intentionally excludes manuscript drafts, LaTeX build artifacts, local logs, caches, exploratory smoke/probe runs, and private workspace notes.

## Environment

Python scripts use only the Python standard library. Use Python 3.9 or newer.

The full model matrix requires [Ollama](https://ollama.com/) running locally and the model names listed in `configs/model_roster_12.json`.

The figure scripts require R with these packages:

```r
install.packages(c("ggplot2", "dplyr", "tidyr", "scales", "ggrepel", "colorspace", "ggsankey"))
```

## Reproduce Existing Tables

From the repository root:

```bash
python3 scripts/verify_replication_package.py

python3 scripts/summarize_defect_results.py \
  results/model_matrix_full613/*_outputs_metrics.csv \
  --out-prefix results/model_matrix_full613/defect_detection_model_matrix_summary

python3 scripts/rank_model_matrix.py \
  results/model_matrix_full613/*_outputs_metrics.csv \
  --roster configs/model_roster_12.json \
  --out-prefix results/model_matrix_full613/defect_detection_model_ranking

python3 scripts/statistical_analysis.py \
  --results-dir results/model_matrix_full613 \
  --out-dir results/model_matrix_full613
```

These commands regenerate the summary, ranking, bootstrap-confidence, and paired-test CSV files used in the manuscript.

## Reproduce Figures

```bash
python3 scripts/plot_manuscript_figures.py \
  --results-dir results/model_matrix_full613 \
  --out-dir figures

Rscript scripts/figure_1_related_work_map.R \
  data/related_work_sankey_input.csv \
  figures/fig_bai4_related_work_map.pdf
```

The generated PDFs appear in `figures/`.

## Rerun a Small Experiment

First start Ollama and pull at least one model, for example:

```bash
ollama pull gemma3:4b
```

Then run a short zero-shot check:

```bash
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

## Rerun the Full Model Matrix

Install all models listed in `configs/model_roster_12.json`, then run:

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

The full run evaluates 12 models under two prompt conditions over 613 artifacts, producing 14,712 deterministic generations.

## Manual-Audit Interface

The completed audit sheet is in `data/manual_audit_full613_stratified120_sheet.csv`. To inspect or continue an audit locally:

```bash
python3 audit_app/server.py --host 127.0.0.1 --port 8765
```

Then open `http://127.0.0.1:8765`.

## Expected Artifact Counts

- Benchmark rows: 613.
- Manual-audit rows: 120 plus CSV header.
- Model roster: 12 local models.
- Prompt conditions: zero-shot and rubric-guided.
- Full-run jobs: 24 model--condition rows.
- Raw full-run generations: 14,712.
- Per-output metric rows: 14,712.

These counts are checked by `scripts/verify_replication_package.py`.
