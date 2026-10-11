"""Text normalisation and n-gram extraction."""

import re

_WORD = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lower-case alphanumeric tokens; punctuation and spacing never defeat a match."""
    return _WORD.findall(text.lower())


def ngrams(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    """Distinct contiguous n-grams. Texts shorter than n yield an empty set."""
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}
