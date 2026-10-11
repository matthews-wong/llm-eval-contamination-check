"""Command line entry: python3 -m contamcheck CORPUS EVAL [--n N] [--threshold T]."""

import argparse
import sys

from .detector import DEFAULT_N, DEFAULT_THRESHOLD, build_index, score_item
from .loader import load_jsonl

EXIT_CLEAN = 0
EXIT_CONTAMINATED = 1
EXIT_USAGE = 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="contamcheck", description=__doc__)
    parser.add_argument("corpus", help="JSONL of texts the model may have seen")
    parser.add_argument("eval_set", help="JSONL of eval items to check")
    parser.add_argument("--n", type=int, default=DEFAULT_N, help="n-gram size in tokens")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help="overlap at or above this flags an item")
    args = parser.parse_args(argv)
    if args.n < 1 or not 0.0 < args.threshold <= 1.0:
        print(f"error: need n >= 1 and 0 < threshold <= 1, got n={args.n} threshold={args.threshold}",
              file=sys.stderr)
        return EXIT_USAGE

    try:
        corpus = load_jsonl(args.corpus)
        items = load_jsonl(args.eval_set)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    index = build_index([r["text"] for r in corpus], args.n)
    findings = [score_item(i["id"], i["text"], index, args.n, args.threshold) for i in items]

    print(f"{'id':<12} {'overlap':>7} {'shared/total':>13}  verdict")
    for f in findings:
        verdict = "CONTAMINATED" if f.contaminated else "ok"
        print(f"{f.item_id:<12} {f.overlap:>7.2f} {f'{f.shared}/{f.total}':>13}  {verdict}")
    flagged = sum(f.contaminated for f in findings)
    print(f"\n{flagged}/{len(findings)} eval items flagged "
          f"(n={args.n}, threshold={args.threshold}, corpus docs={len(corpus)})")
    return EXIT_CONTAMINATED if flagged else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
