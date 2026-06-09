import argparse
import json
import subprocess
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[2]
PROJECT_DATA = ROOT / "datasets" / "04_requirements_quality_defect_detection__data"
DEFAULT_CONDITIONS = ["zero_shot", "rubric_guided"]


def safe_model_name(model):
    return model.replace(":", "_").replace("/", "_")


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


def count_jsonl(path):
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def installed_ollama_models():
    try:
        proc = subprocess.run(
            ["ollama", "list"],
            cwd=PROJECT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return set()
    names = set()
    for line in proc.stdout.splitlines()[1:]:
        parts = line.split()
        if parts:
            names.add(parts[0])
    return names


def run(cmd):
    print(" ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=PROJECT).returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", default="configs/model_roster_12.json")
    parser.add_argument("--tasks", default="data/defect_detection_pilot90.jsonl")
    parser.add_argument("--out-dir", default="results/model_matrix_pilot90")
    parser.add_argument("--conditions", nargs="*", default=DEFAULT_CONDITIONS)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--score", action="store_true")
    parser.add_argument("--summarize", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()

    roster_path = PROJECT / args.roster
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    task_path = resolve_tasks_path(args.tasks)
    expected = args.limit or count_jsonl(task_path)
    out_dir = PROJECT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    installed = installed_ollama_models()
    models = [row["name"] for row in roster["models"]]
    missing = [model for model in models if installed and model not in installed]
    if missing and not args.allow_missing:
        print("missing Ollama models:", ", ".join(missing), file=sys.stderr)
        print("Install them first with `ollama pull <model>` or pass --allow-missing.", file=sys.stderr)
        return 2

    jobs = []
    for model in models:
        if missing and model in missing and args.allow_missing:
            print(f"skip missing model {model}", flush=True)
            continue
        for condition in args.conditions:
            out_path = out_dir / f"{safe_model_name(model)}_{condition}_outputs.jsonl"
            jobs.append((model, condition, out_path))

    print(f"matrix jobs: {len(jobs)}; expected rows/job: {expected}", flush=True)
    metric_paths = []
    for index, (model, condition, out_path) in enumerate(jobs, start=1):
        existing = count_jsonl(out_path)
        if existing >= expected and not args.force:
            print(f"[{index}/{len(jobs)}] skip complete {out_path.name}", flush=True)
        else:
            if existing and not args.force:
                print(f"[{index}/{len(jobs)}] rerun partial {out_path.name}: {existing}/{expected}", flush=True)
            else:
                print(f"[{index}/{len(jobs)}] run {model} {condition}", flush=True)
            rc = run([
                sys.executable,
                "scripts/run_ollama_defect_detection.py",
                "--model", model,
                "--tasks", str(task_path),
                "--condition", condition,
                "--limit", str(args.limit),
                "--timeout", str(args.timeout),
                "--out", str(out_path.relative_to(PROJECT)),
            ])
            if rc != 0:
                return rc

        if args.score:
            metrics_path = out_path.with_name(out_path.stem + "_metrics.csv")
            metric_paths.append(metrics_path)
            if args.force or not metrics_path.exists():
                rc = run([
                    sys.executable,
                    "scripts/score_defect_outputs.py",
                    str(out_path.relative_to(PROJECT)),
                    "--tasks", str(task_path),
                    "--out", str(metrics_path.relative_to(PROJECT)),
                ])
                if rc != 0:
                    return rc

    if args.summarize and metric_paths:
        existing_metrics = [str(path.relative_to(PROJECT)) for path in metric_paths if path.exists()]
        if existing_metrics:
            rc = run([
                sys.executable,
                "scripts/summarize_defect_results.py",
                *existing_metrics,
                "--out-prefix",
                str((out_dir / "defect_detection_model_matrix_summary").relative_to(PROJECT)),
            ])
            if rc != 0:
                return rc
            rc = run([
                sys.executable,
                "scripts/rank_model_matrix.py",
                *existing_metrics,
                "--roster",
                args.roster,
                "--out-prefix",
                str((out_dir / "defect_detection_model_ranking").relative_to(PROJECT)),
            ])
            if rc != 0:
                return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
