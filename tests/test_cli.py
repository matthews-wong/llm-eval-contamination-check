import contextlib
import io
import unittest

from contamcheck.cli import EXIT_CLEAN, EXIT_CONTAMINATED, EXIT_USAGE, main

CORPUS = "fixtures/corpus.jsonl"


def run(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_leaky_set_exits_nonzero_and_names_items(self):
        code, out, _ = run(CORPUS, "fixtures/eval_leaky.jsonl")
        self.assertEqual(code, EXIT_CONTAMINATED)
        self.assertIn("q-leak-1", out)
        self.assertIn("2/4 eval items flagged", out)

    def test_clean_set_exits_zero(self):
        code, out, _ = run(CORPUS, "fixtures/eval_clean.jsonl")
        self.assertEqual(code, EXIT_CLEAN)
        self.assertIn("0/2 eval items flagged", out)

    def test_missing_file_is_usage_error(self):
        code, _, err = run(CORPUS, "fixtures/nope.jsonl")
        self.assertEqual(code, EXIT_USAGE)
        self.assertIn("nope.jsonl", err)

    def test_bad_threshold_is_usage_error(self):
        code, _, err = run(CORPUS, "fixtures/eval_clean.jsonl", "--threshold", "0")
        self.assertEqual(code, EXIT_USAGE)
        self.assertIn("threshold=0.0", err)


if __name__ == "__main__":
    unittest.main()
