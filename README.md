# llm-eval-contamination-check

A benchmark score means little if the eval questions were already in the
training data or the prompt context. This tool flags eval items whose text
overlaps a reference corpus, using plain n-gram matching. Pure standard-library
Python, no model and no network.

## Usage

```
python3 -m contamcheck CORPUS.jsonl EVAL.jsonl [--n 8] [--threshold 0.5]
```

Both files are JSONL with string `id` and `text` fields. Text is lower-cased and
reduced to alphanumeric tokens, so case and punctuation do not hide a copy. An
item's overlap is the share of its distinct n-grams that also appear in the
corpus; at or above `--threshold` it is flagged. Exit codes: `0` clean,
`1` something flagged, `2` bad input.

Example on the bundled fixtures (3 corpus docs, 4 eval items):

```
$ python3 -m contamcheck fixtures/corpus.jsonl fixtures/eval_leaky.jsonl
id           overlap  shared/total  verdict
q-leak-1        1.00           4/4  CONTAMINATED
q-para-1        0.71           5/7  CONTAMINATED
q-clean-1       0.00           0/7  ok
q-clean-2       0.00           0/0  ok

2/4 eval items flagged (n=8, threshold=0.5, corpus docs=3)
```

These are fixture results, not a measurement of any real benchmark.

## Design notes

- **Item-level, not corpus-level.** Overlap is measured over the eval item's
  n-grams, so a short question buried in a long document still scores 1.0.
- **Short items.** An item with fewer than `n` tokens has no n-grams and is
  reported as `0/0`, not flagged. Lower `--n` for short-form questions, at the
  cost of more false positives on common phrases.
- **Limits.** Exact n-gram overlap misses paraphrases and translations. A clean
  result means "no verbatim leakage found", not "uncontaminated".

## Validation

```
python3 -m unittest -v
```
