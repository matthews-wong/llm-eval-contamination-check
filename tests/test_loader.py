import tempfile
import unittest
from pathlib import Path

from contamcheck.loader import load_jsonl


def write(content: str) -> Path:
    tmp = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8")
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


class LoadJsonlTests(unittest.TestCase):
    def test_loads_records_and_skips_blank_lines(self):
        path = write('{"id": "a", "text": "x"}\n\n{"id": "b", "text": "y"}\n')
        self.addCleanup(path.unlink)
        self.assertEqual([r["id"] for r in load_jsonl(path)], ["a", "b"])

    def test_bad_json_reports_line(self):
        path = write('{"id": "a", "text": "x"}\n{oops\n')
        self.addCleanup(path.unlink)
        with self.assertRaisesRegex(ValueError, ":2: invalid JSON"):
            load_jsonl(path)

    def test_missing_field_reports_field(self):
        path = write('{"id": "a"}\n')
        self.addCleanup(path.unlink)
        with self.assertRaisesRegex(ValueError, "'text'"):
            load_jsonl(path)


if __name__ == "__main__":
    unittest.main()
