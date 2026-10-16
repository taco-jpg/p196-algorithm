#!/usr/bin/env python3
"""Independent finite arithmetic control; not a Lean proof or all-time result.

Enumerate every positive input with one through five decimal digits.  Group
by the exact mirrored digit-sum word and compare the proposed splitting
formula with actual integer multiplicities.  The reverse-add implementation
here uses decimal strings independently of the Lean positional definitions.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def factor(s: int, outer: bool = False) -> int:
    if s < 0 or s > 18:
        return 0
    if s <= 9:
        return s if outer else s + 1
    return 19 - s


def proposed_count(q: tuple[int, ...]) -> int:
    length = len(q)
    if length == 0:
        return 0
    if length == 1:
        return int(2 <= q[0] <= 18 and q[0] % 2 == 0)
    count = factor(q[0], True)
    for s in q[1:length // 2]:
        count *= factor(s)
    if length % 2:
        count *= int(0 <= q[length // 2] <= 18 and q[length // 2] % 2 == 0)
    return count


def run(max_digits: int = 5) -> dict:
    rows = []
    for length in range(1, max_digits + 1):
        counts = Counter()
        pal_counts = Counter()
        targets = {}
        target_counts = Counter()
        sample = defaultdict(list)
        for n in range(10 ** (length - 1), 10 ** length):
            text = str(n)
            ds = tuple(map(int, text[::-1]))
            q = tuple(a + b for a, b in zip(ds, ds[::-1]))
            target = n + int(text[::-1])
            counts[q] += 1
            target_counts[target] += 1
            pal_counts[q] += int(text == text[::-1])
            if q in targets:
                assert targets[q] == target
            targets[q] = target
            if len(sample[q]) < 10:
                sample[q].append(n)
        assert len(targets) == len(set(targets.values()))
        for q, actual in counts.items():
            assert proposed_count(q) == actual, (length, q, actual)
            assert pal_counts[q] == int(all(s % 2 == 0 for s in q))
        max_count = max(counts.values())
        first_max = min((targets[q], q) for q, count in counts.items() if count == max_count)
        target, q = first_max
        rows.append({
            "width": length,
            "inputs_enumerated": 9 * 10 ** (length - 1),
            "distinct_pair_words": len(counts),
            "all_profile_counts_match": True,
            "all_palindromic_member_counts_match": True,
            "maximum_fixed_width_numeric_fiber": max_count,
            "smallest_target_attaining_maximum": target,
            "its_pair_word_lsd_first": q,
            "sample_inputs": sample[q],
        })
    return {
        "evidence_level": "FINITE_PYTHON_CONTROL_ONLY",
        "no_lean_or_infinite_time_claim": True,
        "utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "max_digits": max_digits,
        "rows": rows,
    }


if __name__ == "__main__":
    result = run()
    output = Path(__file__).with_name("multiplicity_probe.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
