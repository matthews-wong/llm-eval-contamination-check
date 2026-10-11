import unittest

from contamcheck.text import ngrams, tokenize


class TokenizeTests(unittest.TestCase):
    def test_ignores_case_and_punctuation(self):
        self.assertEqual(tokenize("Hello,  World!"), ["hello", "world"])

    def test_empty_text(self):
        self.assertEqual(tokenize(""), [])


class NgramTests(unittest.TestCase):
    def test_bigrams(self):
        self.assertEqual(ngrams(["a", "b", "c"], 2), {("a", "b"), ("b", "c")})

    def test_short_text_has_no_ngrams(self):
        self.assertEqual(ngrams(["a", "b"], 3), set())

    def test_rejects_non_positive_n(self):
        with self.assertRaisesRegex(ValueError, "got 0"):
            ngrams(["a"], 0)


if __name__ == "__main__":
    unittest.main()
