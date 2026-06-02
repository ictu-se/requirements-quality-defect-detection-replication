import argparse
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[2]
PROJECT_DATA = ROOT / "datasets" / "04_requirements_quality_defect_detection__data"


def load_template(path):
    return path.read_text(encoding="utf-8")


def safe(value):
    if value is None:
        return ""
    return str(value)


def render(template, task, condition):
    values = {
        "repo": safe(task.get("repo", "")),
        "source_type": safe(task.get("source_type", "")),
        "language": safe(task.get("language", "")),
        "condition": condition,
        "statement": safe(task.get("statement", "")),
    }
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{" + key + "}", value)
    return rendered


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", default="data/defect_detection_pilot90.jsonl")
    parser.add_argument("--condition", default="rubric_guided", choices=["zero_shot", "rubric_guided"])
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    tasks_path = resolve_tasks_path(args.tasks)
    template = load_template(PROJECT / "prompts/defect_detection_prompt.md")
    out_dir = PROJECT / "prompts" / "rendered" / args.condition
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    with tasks_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            task = json.loads(line)
            prompt = render(template, task, args.condition)
            with (out_dir / f"{task['task_id']}.md").open("w", encoding="utf-8", newline="\n") as out:
                out.write(prompt)
            count += 1
            if args.limit and count >= args.limit:
                break
    print(f"rendered {count} prompts to {out_dir}")


if __name__ == "__main__":
    main()
