# Artifact Manifest

This package supports the paper "Requirements-Quality Defect Screening with Local Large Language Models over Heterogeneous Software Artifacts." It is intended to let reviewers inspect the benchmark, classifier runner, prompt template, raw model outputs, scoring scripts, audit sheet, and analysis files used for the reported results.

## Top-Level Files

- `README.md`: entry point with environment notes and common reproduction commands.
- `ARTIFACT_MANIFEST.md`: this file.
- `REPRODUCIBILITY_CHECKLIST.md`: ordered verification and reproduction checklist.
- `CHECKSUMS_SHA256.txt`: SHA-256 checksums for package files.
- `requirements.txt`: Python dependency note. The core Python pipeline uses the standard library.
- `R-packages.txt`: R packages used by the optional figure-generation scripts.
- `.gitignore`: excludes caches, local logs, and manuscript/build artifacts.

## Data

- `data/defect_detection_dataset.jsonl`: 613 requirement-like artifacts used in the full model matrix.
- `data/defect_detection_dataset.csv`: CSV view of the same 613-row benchmark.
- `data/defect_detection_summary.csv`: source/type summary of the benchmark.
- `data/manual_audit_full613_stratified120_sheet.csv`: completed 120-row blinded audit sheet.
- `data/related_work_sankey_input.csv`: input for the related-work figure.

## Configuration And Prompts

- `configs/model_roster_12.json`: the 12 local models used in the reported full run.
- `configs/model_roster_10.json`: earlier 10-model roster retained for traceability.
- `configs/model_roster_additional_2.json`: two additional models that complete the 12-model roster.
- `prompts/defect_detection_prompt.md`: zero-shot and rubric-guided prompt template.

## Scripts

- `scripts/run_ollama_defect_detection.py`: local-model runner for one model and one prompt condition.
- `scripts/run_model_matrix.py`: matrix runner for all models and conditions.
- `scripts/score_defect_outputs.py`: parser and scoring script for model outputs.
- `scripts/summarize_defect_results.py`: summary tables by model, source, defect type, and calibration bin.
- `scripts/rank_model_matrix.py`: model ranking and operating-point selection.
- `scripts/statistical_analysis.py`: bootstrap confidence intervals and paired statistical tests.
- `scripts/verify_replication_package.py`: package integrity and expected-count check.
- `scripts/plot_manuscript_figures.py`: Python figure-generation script.
- `scripts/plot_manuscript_figures.R`, `scripts/figure_1_related_work_map.R`, `scripts/render_related_work_sankey.R`: optional R figure scripts.
- `scripts/render_prompts.py`: prompt-rendering helper.

## Results

`results/model_matrix_full613/` contains the raw outputs, metrics, summaries, rankings, calibration tables, statistical tests, and audit-subset records used by the paper.

Expected full-run files:

- 24 `*_outputs.jsonl` files: one per model--condition job, each with 613 rows.
- 24 `*_outputs_metrics.csv` files: scored outputs, each with 613 data rows.
- `defect_detection_model_matrix_summary_12models.csv` and `.md`: full 12-model summary.
- `defect_detection_model_ranking_12models.csv` and `.md`: full 12-model ranking.
- `defect_detection_model_matrix_summary_12models_by_source.csv`: source-specific results.
- `defect_detection_model_matrix_summary_12models_by_defect_type.csv`: defect-type results.
- `defect_detection_model_matrix_summary_12models_calibration.csv`: confidence/calibration summary.
- `statistical_bootstrap_ci.csv`: bootstrap intervals.
- `statistical_paired_tests.csv`: paired statistical tests.
- `audit120_review_label_tasks.jsonl`: model-output subset aligned with manual audit rows.

## Manual-Audit App

`audit_app/` contains a local browser interface used for blinded inspection of the 120-row audit sample. It is included so reviewers can inspect the audit workflow and, if desired, continue or repeat an audit locally.

## Exclusions

The package excludes article drafts, LaTeX sources, PDFs, local terminal logs, cache files, and private notes. These files are not needed to reproduce the reported metrics and would make the package less suitable for review.
