#!/usr/bin/env python3
"""Independent finite arithmetic control for the two exact zero-gap bounds.

This is a finite control, not a Lean proof. It imports no theorem generator,
normalizer, carry code, or predecessor code. Every admissible symmetric word
of widths 1..8 is generated directly. Its next word is computed by the ordinary
decimal expansion of sum(q[i] * 10**i), followed by reflection and addition.

The tests use the strongest possible supplied budgets: M is the exact old
mass and K is the exact longest old zero interval. Larger valid budgets only
increase the proposed upper bounds. Source fingerprints bind this experiment
to the separately reviewed statement; they do not turn it into a proof.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import sys
import time


EXACT_SOURCE_SHA256 = 'f8187cafd7210bdf63e360694d875b278b174516d81270ab47d2170a0b1d46bc'
EXPECTED_COUNTS = {1: 9, 2: 18, 3: 180, 4: 342, 5: 3420,
                   6: 6498, 7: 64980, 8: 123462}


def require(condition: bool, context: object) -> None:
    if not condition:
        raise AssertionError(context)


def longest_zero_interval(word: tuple[int, ...]) -> int:
    best = run = 0
    for coefficient in word:
        run = run + 1 if coefficient == 0 else 0
        best = max(best, run)
    return best


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
                        default=Path(__file__).resolve().parents[4] / 'Agent104ExactZeroGap.lean')
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    started = time.monotonic()
    source_bytes = args.source.read_bytes()
    source_sha = hashlib.sha256(source_bytes).hexdigest()
    require(source_sha == EXACT_SOURCE_SHA256, ('source fingerprint changed', source_sha))
    counts: dict[int, int] = {}
    branch_counts = [0, 0]
    positive_zero_run_counts = [0, 0]
    small_budget_examples: dict[str, object] = {}
    equality_examples: dict[str, object] = {}
    short_width_zero_runs: dict[int, int] = {}
    for width in range(1, 9):
        count = 0
        zero_cases = 0
        for left in product(range(19), repeat=(width + 1) // 2):
            if left[0] == 0 or (width % 2 and left[-1] % 2):
                continue
            old = left + left[:width // 2][::-1]
            require(len(old) == width and old == old[::-1], old)
            weighted_value = sum(coefficient * 10 ** i for i, coefficient in enumerate(old))
            digits = tuple(map(int, str(weighted_value)[::-1]))
            overflow = len(digits) - width
            require(overflow in (0, 1), ('unexpected width', old, digits))
            new = tuple(a + b for a, b in zip(digits, digits[::-1]))
            mass = sum(old)
            old_gap = longest_zero_interval(old)
            new_gap = longest_zero_interval(new)
            if overflow == 0:
                bound = max(old_gap, 1, mass // 9)
            else:
                bound = max(max(old_gap - 1, 0), 2, mass // 9 + 1)
            require(new_gap <= bound,
                    {'old': old, 'new': new, 'mass': mass, 'old_gap': old_gap,
                     'new_gap': new_gap, 'overflow': overflow, 'bound': bound})
            count += 1
            branch_counts[overflow] += 1
            if new_gap:
                positive_zero_run_counts[overflow] += 1
                zero_cases += 1
            if old_gap <= 1 and new_gap:
                small_budget_examples.setdefault(str((overflow, old_gap, new_gap)),
                    {'old': old, 'new': new, 'mass': mass, 'bound': bound})
            if new_gap == bound and new_gap >= 2:
                equality_examples.setdefault(str((overflow, new_gap)),
                    {'old': old, 'new': new, 'mass': mass, 'old_gap': old_gap})
        require(count == EXPECTED_COUNTS[width], ('universe count', width, count))
        counts[width] = count
        if width <= 2:
            short_width_zero_runs[width] = zero_cases
    require(sum(counts.values()) == 198909, 'total universe count')
    require(branch_counts == [93931, 104978], ('branch counts', branch_counts))
    require(args.source.read_bytes() == source_bytes, 'source changed during control')
    result = {
        'schema_version': 1,
        'status': 'PASS_FINITE_ARITHMETIC_CONTROL_ONLY',
        'evidence_level': 'Independent exhaustive finite arithmetic control; not a Lean theorem proof.',
        'reviewer': 'real subagent /root/strategy_review',
        'executed_at_utc': datetime.now(timezone.utc).isoformat(),
        'python_version': platform.python_version(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_path': str(args.source.resolve()),
        'source_sha256': source_sha,
        'widths': [1, 8],
        'admissible_counts_by_width': counts,
        'total_admissible_words': sum(counts.values()),
        'nooverflow_count': branch_counts[0],
        'overflow_count': branch_counts[1],
        'nonempty_new_zero_runs_by_branch': positive_zero_run_counts,
        'new_zero_run_cases_at_widths_1_and_2': short_width_zero_runs,
        'mass_budget': 'exact sum of all old coefficients',
        'zero_budget': 'exact longest old zero interval; zero if none',
        'arithmetic_method': 'integer weighted value -> decimal digits -> reflected pair sums',
        'bounds': {'nooverflow': 'max(K, 1, M//9)',
                   'overflow': 'max(max(K-1, 0), 2, M//9+1)'},
        'small_old_gap_examples': small_budget_examples,
        'equality_examples': equality_examples,
        'elapsed_seconds': round(time.monotonic() - started, 6),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'total_admissible_words',
                      'nooverflow_count', 'overflow_count', 'elapsed_seconds']}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
