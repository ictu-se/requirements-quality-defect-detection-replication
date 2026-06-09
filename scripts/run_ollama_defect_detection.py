import argparse
import json
import socket
import time
import urllib.error
import urllib.request
from pathlib import Path

from render_prompts import load_template, render


PROJECT = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[2]
PROJECT_DATA = ROOT / "datasets" / "04_requirements_quality_defect_detection__data"


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


def call_ollama(model, prompt, timeout):
    started = time.time()
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "top_p": 0.9,
        },
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8", errors="replace"))
    return {
        "returncode": 0,
        "stdout": data.get("response", ""),
        "stderr": "",
        "elapsed_sec": round(time.time() - started, 3),
        "eval_count": data.get("eval_count", ""),
        "prompt_eval_count": data.get("prompt_eval_count", ""),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--tasks", default="data/defect_detection_pilot90.jsonl")
    parser.add_argument("--condition", default="rubric_guided", choices=["zero_shot", "rubric_guided"])
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    tasks_path = resolve_tasks_path(args.tasks)
    template = load_template(PROJECT / "prompts/defect_detection_prompt.md")
    safe_model_name = args.model.replace(":", "_").replace("/", "_")
    out_path = PROJECT / args.out if args.out else PROJECT / "results" / f"{safe_model_name}_{args.condition}_outputs.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with tasks_path.open("r", encoding="utf-8") as f, out_path.open("w", encoding="utf-8", newline="\n") as out:
        for line in f:
            if not line.strip():
                continue
            task = json.loads(line)
            prompt = render(template, task, args.condition)
            try:
                result = call_ollama(args.model, prompt, args.timeout)
            except (TimeoutError, socket.timeout):
                result = {
                    "returncode": -1,
                    "stdout": "",
                    "stderr": "timeout",
                    "elapsed_sec": args.timeout,
                    "eval_count": "",
                    "prompt_eval_count": "",
                }
            except urllib.error.URLError as exc:
                result = {
                    "returncode": -2,
                    "stdout": "",
                    "stderr": str(exc),
                    "elapsed_sec": round(time.time(), 3),
                    "eval_count": "",
                    "prompt_eval_count": "",
                }
            record = {
                "task_id": task["task_id"],
                "source_type": task.get("source_type", ""),
                "repo": task.get("repo", ""),
                "language": task.get("language", ""),
                "condition": args.condition,
                "model": args.model,
                **result,
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            out.flush()
            count += 1
            print(f"{count}: {task['task_id']} rc={record['returncode']} elapsed={record['elapsed_sec']}")
            if args.limit and count >= args.limit:
                break
    print(f"wrote {count} outputs to {out_path}")


if __name__ == "__main__":
    raise SystemExit(main())
