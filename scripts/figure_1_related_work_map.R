suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(ggsankey)
})

project_dir <- normalizePath(getwd(), mustWork = TRUE)
default_input <- file.path(project_dir, "data", "related_work_sankey_input.csv")
default_output <- file.path(project_dir, "figures", "fig_bai4_related_work_map.pdf")

args <- commandArgs(trailingOnly = TRUE)
input_file <- if (length(args) >= 1) args[[1]] else default_input
output_file <- if (length(args) >= 2) args[[2]] else default_output

input_file <- normalizePath(input_file, mustWork = TRUE)
output_file <- normalizePath(output_file, mustWork = FALSE)
dir.create(dirname(output_file), recursive = TRUE, showWarnings = FALSE)

chart_data <- read.csv(input_file, stringsAsFactors = FALSE, check.names = FALSE) |>
  mutate(
    time = factor(time, levels = sort(unique(time))),
    group = factor(group),
    label = case_when(
      group == "Quality criteria and ambiguity" ~ "Quality / ambiguity",
      group == "Requirements smells" ~ "Req. smells",
      group == "NLP/ML for RE" ~ "NLP/ML for RE",
      group == "LLMs for SE" ~ "LLMs for SE",
      group == "LLMs for RE" ~ "LLMs for RE",
      group == "Evaluation and oracle validity" ~ "Eval. / oracle validity",
      TRUE ~ group
    ),
    value = as.numeric(value)
  ) |>
  filter(!is.na(time), !is.na(group), !is.na(value), value > 0)

highlight_groups <- c(
  "Quality criteria and ambiguity",
  "Requirements smells",
  "NLP/ML for RE",
  "LLMs for SE",
  "LLMs for RE",
  "Evaluation and oracle validity"
)

colors <- c(
  "Quality criteria and ambiguity" = "#7B61A8",
  "Requirements smells" = "#D18B2C",
  "NLP/ML for RE" = "#517F54",
  "LLMs for SE" = "#2F6F9F",
  "LLMs for RE" = "#B54E4E",
  "Evaluation and oracle validity" = "#4F6F85"
)
neutral_color <- "#C8C1C8"
min_time <- min(as.numeric(chart_data$time))

label_data <- chart_data |>
  group_by(group) |>
  arrange(time, .by_group = TRUE) |>
  mutate(side = case_when(
    row_number() == 1 ~ "start",
    row_number() == n() ~ "end",
    TRUE ~ "middle"
  )) |>
  filter(side %in% c("start", "end")) |>
  ungroup() |>
  mutate(
    label = as.character(label),
    label_color = if_else(as.character(group) %in% highlight_groups, as.character(group), NA_character_),
    label_y = case_when(
      side == "start" ~ value,
      group == "Evaluation and oracle validity" ~ 4.65,
      group == "LLMs for RE" ~ 3.60,
      group == "Requirements smells" ~ 2.85,
      group == "NLP/ML for RE" ~ 2.15,
      group == "LLMs for SE" ~ 1.45,
      group == "Quality criteria and ambiguity" ~ 0.75,
      TRUE ~ value
    )
  ) |>
  filter(side == "end" | as.numeric(time) == min_time)

p <- ggplot(
  chart_data,
  aes(
    x = time,
    node = group,
    value = value,
    group = group,
    fill = if_else(as.character(group) %in% highlight_groups, as.character(group), NA_character_)
  )
) +
  geom_sankey_bump(
    color = "grey99",
    smooth = 7,
    linewidth = 0.18,
    alpha = 0.92
  ) +
  geom_label(
    data = label_data,
    aes(
      x = time,
      y = label_y,
      label = label,
      color = label_color,
      hjust = if_else(side == "start", 1, 0)
    ),
    inherit.aes = FALSE,
    nudge_x = if_else(label_data$side == "start", -0.34, 0.34),
    linewidth = 0,
    fill = "grey99",
    fontface = "bold",
    size = 2.45
  ) +
  scale_fill_manual(values = colors, na.value = neutral_color, guide = "none") +
  scale_color_manual(values = colors, na.value = neutral_color, guide = "none") +
  coord_cartesian(clip = "off") +
  labs(
    title = "Evolution of Literature Streams in Requirements-Quality Research",
    subtitle = "Ribbon thickness represents cited-source emphasis at each publication year.",
    caption = NULL,
    x = NULL,
    y = NULL
  ) +
  theme_minimal(base_size = 11) +
  theme(
    legend.position = "none",
    plot.background = element_rect(fill = "grey99", color = NA),
    panel.background = element_rect(fill = "grey99", color = NA),
    axis.title = element_blank(),
    axis.text.y = element_blank(),
    axis.text.x = element_text(face = "bold", color = "#475467", size = 8),
    panel.grid.major.y = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_line(color = "#e5e7eb", linewidth = 0.35),
    plot.title = element_text(face = "bold", size = 16, color = "#101828"),
    plot.subtitle = element_text(lineheight = 1.08, color = "#475467", margin = margin(b = 10)),
    plot.caption = element_blank(),
    plot.margin = margin(16, 158, 10, 142)
  )

suppressWarnings(
  ggsave(
    output_file,
    plot = p,
    width = 12.2,
    height = 5.7,
    bg = "grey99"
  )
)

message("wrote ", output_file)
