import argparse
import subprocess
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
RESULTS = PROJECT / "results" / "model_matrix_full613"
OUT_DIR = PROJECT / "SUBMISSION_BAI4" / "latex_source" / "figures"
R_SCRIPT = PROJECT / "scripts" / "plot_manuscript_figures.R"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default=RESULTS)
    parser.add_argument("--out-dir", default=OUT_DIR)
    args = parser.parse_args()

    subprocess.run(
        [
            "Rscript",
            str(R_SCRIPT),
            str(PROJECT),
            str(Path(args.results_dir)),
            str(Path(args.out_dir)),
        ],
        cwd=PROJECT,
        check=True,
    )


if __name__ == "__main__":
    main()
