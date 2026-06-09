suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
  library(tidyr)
  library(scales)
  library(ggrepel)
  library(colorspace)
})

args <- commandArgs(trailingOnly = TRUE)
project_dir <- if (length(args) >= 1) args[[1]] else getwd()
results_dir <- if (length(args) >= 2) args[[2]] else file.path(project_dir, "results", "model_matrix_full613")
out_dir <- if (length(args) >= 3) args[[3]] else file.path(project_dir, "SUBMISSION_BAI4", "latex_source", "figures")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

read_csv_base <- function(path) {
  read.csv(path, stringsAsFactors = FALSE, check.names = FALSE)
}

short_model <- function(x) {
  x <- gsub("qwen2.5-coder:", "qwen2.5-c:", x)
  x <- gsub("deepseek-coder:", "deepseek-c:", x)
  x <- gsub("granite3.2-vision:latest", "granite3.2-v", x)
  x <- gsub("llama3.2:", "llama3.2:", x)
  x
}

condition_label <- function(x) {
  ifelse(x == "zero_shot", "zero-shot", "rubric-guided")
}

ink <- "#222831"
muted <- "#66717A"
grid_col <- "#E7EBEF"
blue <- "#0072B2"
vermillion <- "#D55E00"
teal <- "#009E73"
amber <- "#E69F00"
purple <- "#6A4C93"

condition_palette <- c("zero-shot" = blue, "rubric-guided" = vermillion)
metric_palette <- c(
  "Any-defect accuracy" = blue,
  "Type F1" = teal,
  "False-alarm rate" = amber
)
score_palette <- c("#B8C2CC", purple, blue, teal)
rate_palette <- c("#F7F9FA", "#D7E8EA", "#8BBEC4", blue)

theme_manuscript <- function(base_size = 9) {
  theme_minimal(base_size = base_size, base_family = "Helvetica") +
    theme(
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(linewidth = 0.22, colour = grid_col),
      axis.line = element_line(linewidth = 0.32, colour = "#A8B0B8"),
      plot.title = element_text(face = "bold", size = base_size + 1.4, colour = ink, hjust = 0),
      plot.subtitle = element_text(size = base_size, colour = muted, hjust = 0, margin = margin(t = 2, b = 7)),
      axis.title = element_text(size = base_size, colour = ink),
      axis.text = element_text(size = base_size - 0.6, colour = "#414A52"),
      legend.title = element_text(size = base_size - 0.8, colour = ink),
      legend.text = element_text(size = base_size - 1, colour = ink),
      legend.position = "bottom",
      legend.key.height = unit(0.22, "in"),
      plot.margin = margin(7, 10, 7, 10),
      plot.background = element_rect(fill = "white", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA)
    )
}

save_pdf <- function(plot, filename, width, height) {
  ggsave(
    file.path(out_dir, filename),
    plot = plot,
    width = width,
    height = height,
    units = "in",
    device = cairo_pdf,
    bg = "white"
  )
}

ranking_base <- if (file.exists(file.path(results_dir, "defect_detection_model_ranking_12models.csv"))) {
  "defect_detection_model_ranking_12models"
} else {
  "defect_detection_model_ranking"
}
summary_base <- if (file.exists(file.path(results_dir, "defect_detection_model_matrix_summary_12models.csv"))) {
  "defect_detection_model_matrix_summary_12models"
} else {
  "defect_detection_model_matrix_summary"
}

best <- read_csv_base(file.path(results_dir, paste0(ranking_base, "_best_per_model.csv")))
ranking <- read_csv_base(file.path(results_dir, paste0(ranking_base, ".csv")))
defect_type <- read_csv_base(file.path(results_dir, paste0(summary_base, "_by_defect_type.csv")))
source <- read_csv_base(file.path(results_dir, paste0(summary_base, "_by_source.csv")))
calibration <- read_csv_base(file.path(results_dir, paste0(summary_base, "_calibration.csv")))

best <- best |>
  mutate(
    model_short = short_model(model),
    condition_clean = condition_label(condition)
  )

cat("Figure data checks\n")
cat(sprintf(
  "- best model: %s / %s; score %.3f; macro F1 %.3f; missed major %.3f; false alarm %.3f; sec %.3f\n",
  best$model[which.max(best$selection_score)],
  best$condition[which.max(best$selection_score)],
  max(best$selection_score),
  best$macro_type_f1[which.max(best$selection_score)],
  best$missed_major_or_critical_rate[which.max(best$selection_score)],
  best$false_alarm_rate[which.max(best$selection_score)],
  best$mean_elapsed_sec[which.max(best$selection_score)]
))

model_order <- best |>
  arrange(selection_score) |>
  pull(model_short)

p_score <- best |>
  mutate(model_short = factor(model_short, levels = model_order)) |>
  ggplot(aes(x = selection_score, y = model_short, fill = condition_clean)) +
  geom_col(width = 0.64, colour = "white", linewidth = 0.15) +
  geom_text(aes(label = sprintf("%.1f", selection_score)), hjust = -0.18, size = 2.45, colour = ink) +
  scale_fill_manual(values = condition_palette) +
  scale_x_continuous(expand = expansion(mult = c(0, 0.10))) +
  labs(
    title = "Best condition per model",
    x = "Selection score",
    y = NULL,
    fill = "Prompt"
  ) +
  theme_manuscript() +
  theme(panel.grid.major.y = element_blank())

p_runtime <- best |>
  ggplot(aes(x = mean_elapsed_sec, y = selection_score, colour = condition_clean, shape = condition_clean, label = model_short)) +
  geom_point(size = 3.0, stroke = 0.75, alpha = 0.95) +
  ggrepel::geom_label_repel(
    size = 2.35,
    label.size = 0,
    label.padding = unit(0.08, "lines"),
    fill = alpha("white", 0.92),
    colour = ink,
    min.segment.length = 0,
    segment.size = 0.22,
    box.padding = 0.28,
    max.overlaps = Inf
  ) +
  scale_x_log10(labels = label_number(), breaks = c(0.7, 1, 3, 10, 30, 50)) +
  scale_colour_manual(values = condition_palette) +
  scale_shape_manual(values = c("zero-shot" = 16, "rubric-guided" = 17)) +
  labs(
    title = "Runtime-quality trade-off",
    x = "Mean seconds per sample (log scale)",
    y = "Selection score",
    colour = "Prompt",
    shape = "Prompt"
  ) +
  theme_manuscript()

save_pdf(p_score, "fig_bai4_model_score.pdf", 7.4, 4.8)
save_pdf(p_runtime, "fig_bai4_runtime_tradeoff.pdf", 7.4, 4.8)

p_operating <- best |>
  ggplot(aes(
    x = false_alarm_rate,
    y = missed_major_or_critical_rate,
    size = macro_type_f1,
    fill = selection_score,
    shape = condition_clean,
    label = model_short
  )) +
  geom_hline(yintercept = 0.05, linewidth = 0.35, linetype = "dashed", colour = "#B8C2CC") +
  geom_vline(xintercept = 0.10, linewidth = 0.35, linetype = "dashed", colour = "#B8C2CC") +
  geom_point(colour = "white", stroke = 0.45, alpha = 0.97) +
  ggrepel::geom_label_repel(
    size = 2.35,
    label.size = 0,
    label.padding = unit(0.10, "lines"),
    fill = alpha("white", 0.92),
    colour = ink,
    min.segment.length = 0,
    segment.size = 0.20,
    box.padding = 0.30,
    point.padding = 0.18,
    max.overlaps = Inf
  ) +
  scale_shape_manual(values = c("zero-shot" = 21, "rubric-guided" = 24)) +
  scale_fill_gradientn(colours = score_palette) +
  scale_size_continuous(range = c(3.2, 8.0), breaks = c(0.05, 0.10, 0.15)) +
  scale_x_continuous(labels = label_number(accuracy = 0.01), limits = c(-0.02, max(best$false_alarm_rate) + 0.06)) +
  scale_y_continuous(labels = label_number(accuracy = 0.01), limits = c(-0.006, max(best$missed_major_or_critical_rate) + 0.04)) +
  labs(
    title = "Screening vs. conservative operating points",
    x = "False-alarm rate",
    y = "Missed major/critical rate",
    fill = "Selection score",
    size = "Macro F1",
    shape = NULL
  ) +
  theme_manuscript() +
  guides(
    shape = guide_legend(title = "Prompt", override.aes = list(size = 4, fill = "#F7F9FA", colour = ink)),
    size = guide_legend(title = "Macro F1", override.aes = list(shape = 21, fill = "#6F8FB7")),
    fill = guide_colourbar(title = "Selection score", barwidth = 6, barheight = 0.45)
  ) +
  theme(
    legend.position = "bottom",
    legend.title = element_text(size = 8),
    panel.grid.minor = element_blank()
  )

save_pdf(p_operating, "fig_bai4_operating_points.pdf", 7.8, 5.4)

focus_defect <- defect_type |>
  filter(model == "qwen2.5-coder:32b", condition == "rubric_guided") |>
  mutate(
    defect_label = recode(
      defect_type,
      unsupported_external_assumption = "Unsupported external\nassumption",
      overly_broad_requirement = "Overly broad\nrequirement",
      missing_expected_outcome = "Missing expected\noutcome",
      inconsistent_condition = "Inconsistent\ncondition",
      missing_constraint = "Missing\nconstraint",
      missing_trigger = "Missing\ntrigger",
      ambiguous_term = "Ambiguous\nterm",
      missing_actor = "Missing\nactor",
      not_testable = "Not\ntestable"
    ),
    defect_label = factor(defect_label, levels = defect_label[order(f1)])
  )

cat(sprintf(
  "- qwen2.5-coder:32b rubric-guided strongest defect-type F1: %s %.3f (n=%d)\n",
  focus_defect$defect_type[which.max(focus_defect$f1)],
  max(focus_defect$f1),
  as.integer(focus_defect$gold_support[which.max(focus_defect$f1)])
))

p_defect <- focus_defect |>
  ggplot(aes(x = f1, y = defect_label)) +
  geom_segment(aes(x = 0, xend = f1, yend = defect_label), colour = "#CCD5DD", linewidth = 1.05, lineend = "round") +
  geom_point(aes(size = gold_support), colour = "white", fill = teal, shape = 21, stroke = 0.45) +
  geom_text(
    aes(label = sprintf("%.2f", f1)),
    hjust = -0.35,
    size = 2.6,
    colour = ink
  ) +
  geom_text(
    aes(label = paste0("n=", as.integer(gold_support))),
    x = 0.55,
    hjust = 1,
    size = 2.45,
    colour = muted
  ) +
  scale_size_continuous(range = c(2.2, 7.5), guide = "none") +
  scale_x_continuous(limits = c(0, max(0.65, max(focus_defect$f1) + 0.06)), labels = label_number(accuracy = 0.01), expand = expansion(mult = c(0, 0))) +
  labs(
    title = "Defect-type F1 for qwen2.5-coder:32b rubric-guided",
    subtitle = "Point size and right-side labels report gold support.",
    x = "F1",
    y = NULL
  ) +
  theme_manuscript() +
  theme(
    panel.grid.major.y = element_blank(),
    panel.grid.minor = element_blank()
  )

save_pdf(p_defect, "fig_bai4_defect_type_f1.pdf", 7.8, 5.2)

focus_source <- source |>
  filter(model == "qwen2.5-coder:32b", condition == "rubric_guided") |>
  mutate(
    source_label = recode(
      source_type,
      synthetic_defect = "Synthetic\ndefect",
      function_spec = "Function\nspec",
      issue_statement = "Issue\nstatement",
      layout_change_spec = "Layout-change\nspec",
      testing_rule_spec = "Testing-rule\nspec",
      acceptance_criterion = "Acceptance\ncriterion"
    ),
    source_label = factor(source_label, levels = source_label[order(any_defect_accuracy, decreasing = TRUE)])
  ) |>
  select(source_label, any_defect_accuracy, type_f1, false_alarm_rate) |>
  pivot_longer(
    cols = c(any_defect_accuracy, type_f1, false_alarm_rate),
    names_to = "metric",
    values_to = "value"
  ) |>
  mutate(metric = recode(
    metric,
    any_defect_accuracy = "Any-defect accuracy",
    type_f1 = "Type F1",
    false_alarm_rate = "False-alarm rate"
  )) |>
  mutate(metric = factor(metric, levels = c("Any-defect accuracy", "Type F1", "False-alarm rate")))

p_source <- focus_source |>
  ggplot(aes(x = metric, y = source_label, fill = value)) +
  geom_tile(colour = "white", linewidth = 1.2) +
  geom_text(aes(label = sprintf("%.2f", value)), size = 2.85, colour = ink) +
  scale_fill_gradientn(
    colours = rate_palette,
    limits = c(0, 1),
    labels = label_number(accuracy = 0.1)
  ) +
  labs(
    title = "Source-specific behavior for qwen2.5-coder:32b rubric-guided",
    x = NULL,
    y = NULL,
    fill = "Rate"
  ) +
  theme_manuscript() +
  theme(
    panel.grid = element_blank(),
    axis.text.x = element_text(size = 8.2),
    legend.position = "right",
    legend.title = element_text(size = 8),
    axis.line = element_blank()
  )

save_pdf(p_source, "fig_bai4_source_behavior.pdf", 7.6, 4.8)

keep_cal <- calibration |>
  filter(
    (model == "qwen2.5-coder:32b" & condition == "rubric_guided") |
    (model == "gemma3:4b" & condition == "zero_shot") |
      (model == "qwen2.5-coder:14b" & condition == "rubric_guided")
  ) |>
  mutate(series = paste(short_model(model), condition_label(condition), sep = " / "))

p_calibration <- ggplot(keep_cal, aes(x = mean_confidence, y = accuracy, colour = series)) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", colour = "#8D99A6", linewidth = 0.45) +
  geom_line(linewidth = 0.75) +
  geom_point(size = 2.4, stroke = 0.25) +
  scale_colour_manual(values = c(blue, vermillion, teal)) +
  scale_x_continuous(limits = c(0, 1), labels = label_number(accuracy = 0.1)) +
  scale_y_continuous(limits = c(0, 1), labels = label_number(accuracy = 0.1)) +
  labs(
    title = "Confidence calibration by bin",
    x = "Mean confidence",
    y = "Empirical any-defect accuracy",
    colour = "Model / prompt"
  ) +
  theme_manuscript()

save_pdf(p_calibration, "fig_bai4_calibration.pdf", 6.5, 5.0)

related_script <- file.path(project_dir, "scripts", "render_related_work_sankey.R")
related_input <- file.path(project_dir, "docs", "related_work_sankey_input.csv")
related_output <- file.path(out_dir, "fig_bai4_related_work_map.pdf")
if (file.exists(related_script)) {
  status <- system2("Rscript", c(related_script, related_input, related_output))
  if (!identical(status, 0L)) {
    warning("related-work Sankey rendering failed with status ", status)
  }
}

cat(sprintf("- wrote manuscript figures to %s\n", out_dir))
