"""JSONL loading for corpus and eval files."""

import json
from pathlib import Path

ID_FIELD = "id"
TEXT_FIELD = "text"


def load_jsonl(path: str | Path) -> list[dict[str, str]]:
    """Read records that each carry string `id` and `text` fields.

    Errors name the file and line so a bad fixture is easy to find.
    """
    records = []
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON: {exc.msg}") from exc
            for field in (ID_FIELD, TEXT_FIELD):
                if not isinstance(rec, dict) or not isinstance(rec.get(field), str):
                    raise ValueError(f"{path}:{lineno}: missing string field {field!r}")
            records.append(rec)
    return records
