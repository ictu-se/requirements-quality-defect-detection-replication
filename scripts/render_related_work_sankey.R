args <- commandArgs(trailingOnly = TRUE)
cmd_args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", cmd_args, value = TRUE)
script_path <- if (length(file_arg) > 0) sub("^--file=", "", file_arg[[1]]) else "scripts/render_related_work_sankey.R"
project_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
root_script <- file.path(project_dir, "figure_1_related_work_map.R")
input_file <- if (length(args) >= 1) args[[1]] else file.path(project_dir, "docs", "related_work_sankey_input.csv")
output_file <- if (length(args) >= 2) args[[2]] else file.path(project_dir, "SUBMISSION_BAI4", "latex_source", "figures", "fig_bai4_related_work_map.pdf")

system2(
  "Rscript",
  c(shQuote(root_script), shQuote(input_file), shQuote(output_file)),
  stdout = "",
  stderr = ""
)
