# Evaluation Framework for BAI4

This document defines the expanded evaluation protocol for requirement quality
defect detection. The goal is to support a paper-scale analysis rather than a
single accuracy table.

## Metric Families

### 1. Detection Effectiveness

These metrics answer whether a model detects the right defect labels.

- `any_defect_accuracy`: binary correctness for defect vs no defect.
- `type_precision`, `type_recall`, `type_f1`: micro-averaged multi-label
  defect-type performance.
- `macro_type_precision`, `macro_type_recall`, `macro_type_f1`: equal-weighted
  defect-type performance, useful for rare labels.
- `type_exact_match_rate`: strict match of the full defect-type set.
- per-type precision, recall, and F1 in `*_by_defect_type.csv`.

### 2. Risk and Severity

These metrics answer whether a model misses defects that matter operationally.

- `false_alarm_rate`: model reports a defect for a no-defect statement.
- `missed_defect_rate`: model reports no defect for a defective statement.
- `missed_major_or_critical_rate`: missed defect where the silver severity is
  major or critical.
- `severity_weighted_precision`, `severity_weighted_recall`,
  `severity_weighted_f1`: defect-type score weighted by severity.
- `mean_severity_abs_error`: distance between predicted and silver severity.
- `mean_over_report_count`: excess predicted defect labels.
- `mean_under_report_count`: missing gold defect labels.

### 3. Grounding and Evidence Support

These metrics answer whether the model can justify defect labels from the text.

- `span_checked_count`: number of predicted defect spans provided.
- `span_supported_count`: predicted spans that appear in the statement.
- `span_supported_rate`: supported predicted spans divided by checked spans.
- `unsupported_span_rate`: unsupported spans over all checked spans.
- `unsupported_span_labels`: labels whose evidence spans are not grounded.
- `copied_span_chars`: rough proxy for how much evidence the model quotes.

These are automatic proxies. Human review should still assess explanation
adequacy and rewrite correctness.

### 4. Calibration and Uncertainty

These metrics answer whether the model knows when it is uncertain.

- `confidence`: top-level confidence in the binary defect decision.
- `mean_defect_confidence`: average confidence over predicted defect items.
- `brier_any_defect`: Brier score for the binary defect decision.
- `ece_any_defect`: expected calibration error over confidence bins.
- `high_confidence_wrong_rate`: wrong decisions with confidence >= 0.8.
- `low_confidence_correct_rate`: correct decisions with confidence <= 0.6.
- `needs_human_review_rate`: how often the model explicitly asks for review.
- `*_calibration.csv`: per-bin confidence vs accuracy table.

### 5. Robustness and Reproducibility

These metrics answer whether results are stable and reproducible.

- `parse_rate`: JSON/schema extraction success.
- `mean_elapsed_sec`: runtime cost proxy.
- `by_source` breakdown: source-specific robustness across issue statements,
  generated acceptance criteria, function specifications, testing-rule
  specifications, layout-change specifications, and synthetic defects.
- `zero_shot` vs `rubric_guided` delta: prompt sensitivity.
- Future repeat-run metric: run-to-run consistency over a smaller repeated
  subset.

## Model Ranking

`scripts/rank_model_matrix.py` produces:

- `defect_detection_model_ranking.csv`
- `defect_detection_model_ranking_best_per_model.csv`
- `defect_detection_model_ranking.md`

The ranking score combines:

- micro defect-type F1;
- macro defect-type F1;
- severity-weighted F1;
- any-defect accuracy;
- parse rate;
- exact type match;
- span support;
- false-alarm penalty;
- missed-defect penalty;
- missed major/critical penalty;
- Brier score penalty;
- ECE penalty.

The ranking is a screening tool, not a final scientific claim. The paper should
also discuss per-source and per-defect-type failures.

## Human Review Metrics

The pilot manual review sheet should be used to estimate:

- agreement between silver labels and reviewer labels;
- defect-type label correction rate;
- severity correction rate;
- explanation adequacy;
- explanation usefulness;
- rewrite correctness;
- rewrite minimality.

Recommended human-review dimensions for model outputs:

- `label_correctness`: whether the predicted defect type is correct.
- `evidence_adequacy`: whether the span/explanation supports the label.
- `rewrite_correctness`: whether the rewrite fixes the defect.
- `rewrite_minimality`: whether the rewrite avoids unnecessary new assumptions.
- `practical_usefulness`: whether an RE/test engineer would act on the output.

## Decision Gate Before Full Run

Do not run the full 613-row x 12-model x 2-condition matrix from smoke tests
alone. Run the 90-row pilot matrix first. Move to full run only if:

- parse rate is close to 1.0 for most model-condition pairs;
- micro and macro defect-type F1 are non-trivial;
- false-alarm and missed-major rates are acceptable;
- no major source type collapses completely;
- confidence calibration is at least interpretable;
- human review does not show systematic silver-label failure.
