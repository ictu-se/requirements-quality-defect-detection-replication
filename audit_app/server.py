#!/usr/bin/env python3
import csv
import json
import shutil
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


APP_DIR = Path(__file__).resolve().parent
PROJECT = APP_DIR.parent
DEFAULT_CSV = PROJECT / "data" / "manual_audit_full613_stratified120_sheet.csv"
SNAPSHOT_JSON = PROJECT / "data" / "manual_audit_full613_stratified120_progress.json"
TRANSLATION_CACHE = PROJECT / "data" / "manual_audit_full613_statement_vi_cache.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
TRANSLATION_MODEL = "gemma3:4b"

DEFECT_TYPES = [
    "ambiguous_term",
    "missing_actor",
    "missing_trigger",
    "missing_expected_outcome",
    "missing_constraint",
    "not_testable",
    "overly_broad_requirement",
    "inconsistent_condition",
    "unsupported_external_assumption",
]

SEVERITIES = ["none", "minor", "major", "critical"]
AGREEMENTS = ["agree", "partial", "disagree"]

CSV_FIELDS = [
    "audit_id",
    "task_id",
    "source_type",
    "gold_label_source",
    "repo",
    "language",
    "statement",
    "silver_has_defect",
    "silver_defect_types",
    "silver_severity",
    "review_has_defect",
    "review_defect_types",
    "review_severity",
    "label_agreement",
    "review_notes",
]


def read_rows():
    with DEFAULT_CSV.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(rows):
    backup = DEFAULT_CSV.with_suffix(DEFAULT_CSV.suffix + ".bak")
    if not backup.exists():
        shutil.copy2(DEFAULT_CSV, backup)

    tmp = DEFAULT_CSV.with_suffix(DEFAULT_CSV.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in CSV_FIELDS})
    tmp.replace(DEFAULT_CSV)

    with SNAPSHOT_JSON.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "updated_at": datetime.now().isoformat(timespec="seconds"),
                "csv_path": str(DEFAULT_CSV),
                "rows": rows,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )


def progress(rows):
    completed = sum(1 for row in rows if row.get("review_has_defect") in {"TRUE", "FALSE"})
    agreed = sum(1 for row in rows if row.get("label_agreement") == "agree")
    partial = sum(1 for row in rows if row.get("label_agreement") == "partial")
    disagreed = sum(1 for row in rows if row.get("label_agreement") == "disagree")
    return {
        "total": len(rows),
        "completed": completed,
        "remaining": len(rows) - completed,
        "agree": agreed,
        "partial": partial,
        "disagree": disagreed,
    }


def read_translation_cache():
    if not TRANSLATION_CACHE.exists():
        return {}
    with TRANSLATION_CACHE.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_translation_cache(cache):
    with TRANSLATION_CACHE.open("w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def translate_statement(audit_id, statement):
    cache = read_translation_cache()
    if (
        audit_id in cache
        and cache[audit_id].get("model") == TRANSLATION_MODEL
        and cache[audit_id].get("vi_statement")
    ):
        return cache[audit_id]["vi_statement"]

    prompt = (
        "Dịch nội dung requirement/software statement sau sang tiếng Việt tự nhiên, "
        "giữ nguyên tên hàm, tên biến, đường dẫn, API, số liệu, ký hiệu toán học và thuật ngữ kỹ thuật quan trọng. "
        "Chỉ trả về bản dịch tiếng Việt, không giải thích, không thêm nhận xét.\n\n"
        f"STATEMENT:\n{statement}"
    )
    payload = {
        "model": TRANSLATION_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.0, "num_predict": 700},
    }
    req = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))
    translation = (data.get("response") or "").strip()
    if not translation:
        raise RuntimeError("Ollama returned an empty translation")

    cache[audit_id] = {
        "model": TRANSLATION_MODEL,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "vi_statement": translation,
    }
    write_translation_cache(cache)
    return translation


def json_response(handler, payload, status=200):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def static_response(handler, path, content_type):
    body = path.read_bytes()
    handler.send_response(200)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class AuditHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index.html"}:
            return static_response(self, APP_DIR / "static" / "index.html", "text/html; charset=utf-8")
        if parsed.path == "/static/app.js":
            return static_response(self, APP_DIR / "static" / "app.js", "application/javascript; charset=utf-8")
        if parsed.path == "/static/style.css":
            return static_response(self, APP_DIR / "static" / "style.css", "text/css; charset=utf-8")
        if parsed.path == "/api/items":
            rows = read_rows()
            translations = read_translation_cache()
            for row in rows:
                row["vi_statement"] = translations.get(row.get("audit_id", ""), {}).get("vi_statement", "")
            return json_response(
                self,
                {
                    "csv_path": str(DEFAULT_CSV),
                    "defect_types": DEFECT_TYPES,
                    "severities": SEVERITIES,
                    "agreements": AGREEMENTS,
                    "progress": progress(rows),
                    "items": rows,
                },
            )
        if parsed.path == "/api/export":
            rows = read_rows()
            return json_response(self, {"progress": progress(rows), "items": rows})
        json_response(self, {"error": "not found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/translate":
            length = int(self.headers.get("Content-Length", "0"))
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
            except json.JSONDecodeError:
                return json_response(self, {"error": "invalid JSON"}, status=400)

            audit_id = payload.get("audit_id", "")
            rows = read_rows()
            row = next((item for item in rows if item.get("audit_id") == audit_id), None)
            if not row:
                return json_response(self, {"error": f"audit_id not found: {audit_id}"}, status=404)
            try:
                translation = translate_statement(audit_id, row.get("statement", ""))
            except Exception as exc:
                return json_response(self, {"error": f"translation failed: {exc}"}, status=500)
            return json_response(self, {"audit_id": audit_id, "vi_statement": translation})

        if parsed.path != "/api/save":
            return json_response(self, {"error": "not found"}, status=404)

        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError:
            return json_response(self, {"error": "invalid JSON"}, status=400)

        audit_id = payload.get("audit_id", "")
        if not audit_id:
            return json_response(self, {"error": "missing audit_id"}, status=400)

        review_has_defect = payload.get("review_has_defect", "")
        review_types = payload.get("review_defect_types", [])
        review_severity = payload.get("review_severity", "")
        agreement = payload.get("label_agreement", "")
        notes = payload.get("review_notes", "")

        if review_has_defect not in {"TRUE", "FALSE", ""}:
            return json_response(self, {"error": "review_has_defect must be TRUE or FALSE"}, status=400)
        if any(item not in DEFECT_TYPES for item in review_types):
            return json_response(self, {"error": "unknown defect type"}, status=400)
        if review_severity and review_severity not in SEVERITIES:
            return json_response(self, {"error": "unknown severity"}, status=400)
        if agreement and agreement not in AGREEMENTS:
            return json_response(self, {"error": "unknown agreement"}, status=400)
        if review_has_defect == "FALSE" and review_types:
            return json_response(self, {"error": "no-defect rows cannot have defect types"}, status=400)
        if review_has_defect == "FALSE" and review_severity not in {"", "none"}:
            return json_response(self, {"error": "no-defect rows must use severity none"}, status=400)
        if review_has_defect == "TRUE" and review_severity == "none":
            return json_response(self, {"error": "defect rows should use minor, major, or critical"}, status=400)

        rows = read_rows()
        found = False
        for row in rows:
            if row.get("audit_id") == audit_id:
                row["review_has_defect"] = review_has_defect
                row["review_defect_types"] = "|".join(review_types)
                row["review_severity"] = review_severity
                row["label_agreement"] = agreement
                row["review_notes"] = notes
                found = True
                break

        if not found:
            return json_response(self, {"error": f"audit_id not found: {audit_id}"}, status=404)

        write_rows(rows)
        return json_response(self, {"ok": True, "progress": progress(rows)})


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    if not DEFAULT_CSV.exists():
        raise SystemExit(f"CSV not found: {DEFAULT_CSV}")

    server = ThreadingHTTPServer((args.host, args.port), AuditHandler)
    print(f"Audit app: http://{args.host}:{args.port}")
    print(f"CSV: {DEFAULT_CSV}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
