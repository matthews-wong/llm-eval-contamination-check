"""Score eval items by how much of their text already appears in a corpus."""

from dataclasses import dataclass

from .text import ngrams, tokenize

DEFAULT_N = 8
DEFAULT_THRESHOLD = 0.5


@dataclass(frozen=True)
class Finding:
    item_id: str
    overlap: float
    shared: int
    total: int
    contaminated: bool


def build_index(corpus_texts: list[str], n: int = DEFAULT_N) -> set[tuple[str, ...]]:
    index: set[tuple[str, ...]] = set()
    for text in corpus_texts:
        index |= ngrams(tokenize(text), n)
    return index


def score_item(
    item_id: str,
    text: str,
    index: set[tuple[str, ...]],
    n: int = DEFAULT_N,
    threshold: float = DEFAULT_THRESHOLD,
) -> Finding:
    """Overlap is the share of the item's distinct n-grams found in the index.

    Items too short to form one n-gram score 0 rather than raising: a short
    question cannot be judged by long n-grams, and the caller sees total=0.
    """
    grams = ngrams(tokenize(text), n)
    if not grams:
        return Finding(item_id, 0.0, 0, 0, False)
    shared = len(grams & index)
    overlap = shared / len(grams)
    return Finding(item_id, overlap, shared, len(grams), overlap >= threshold)
