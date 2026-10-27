#!/usr/bin/env python3
"""Independent arithmetic audit of neutral-B padding and prefix projection.

The all-width argument is in reports/agent-106-T2.md.  This program checks
its local identities against the unchanged Python mirror, including empty
and short exterior words.  It does not search for a decimal certificate.
"""

from itertools import product
from pathlib import Path
import random
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "calculation"))
import neutral_band_search as mirror


def normalize(word, incoming):
    digits = []
    carry = incoming
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, 10)
        digits.append(digit)
    return digits, carry


def raw_exterior(word):
    low, outgoing = normalize(word, 0)
    high, overflow = normalize(word[::-1], 1 - outgoing)
    if overflow:
        low += [9 * (1 - outgoing)]
        high = [1] + high[::-1]
    else:
        high.reverse()
    return [a + b for a, b in zip(low, high)], outgoing, overflow


def prefix_advance(prefix, incoming):
    """Exact generalization of the existing PrefixModel.advance arithmetic."""
    low, _ = normalize(prefix, 0)
    high, overflow = normalize(prefix[::-1], incoming)
    high.reverse()
    if overflow:
        high = [1] + high[:-1]
    return tuple(a + b for a, b in zip(low, high)), overflow


def audit_word(word):
    raw, outgoing, overflow = raw_exterior(word)
    center = [10] if outgoing == 0 else [0]
    assert mirror.hyp(10, word, center)
    assert raw == mirror.nextB(10, word, center)
    assert overflow == mirror.gam(10, word, center)
    assert len(raw) == len(word) + overflow
    checks = 0
    for extra in (0, 1, 3):
        width = max(3, len(word)) + extra
        padded = word + [9] * (width - len(word))
        padded_raw, padded_e, padded_g = raw_exterior(padded)
        assert (padded_e, padded_g) == (outgoing, overflow)
        assert padded_raw == raw + [9] * (width - len(word))
        inner = normalize(padded[3:][::-1], 1 - outgoing)[1]
        projected, projected_g = prefix_advance(padded[:3], inner)
        assert projected == tuple(padded_raw[:3])
        assert projected_g == overflow
        # For every permitted exterior trim, common-width targets agree.
        run = 0
        while run < len(raw) and raw[-run - 1] == 9:
            run += 1
        for trim in range(run + 1):
            target = raw[:len(raw) - trim] if trim else raw
            if len(target) <= width:
                target_padded = target + [9] * (width - len(target))
                assert padded_raw == target_padded + [9] * overflow
        checks += 1
    return checks


def source_skeleton():
    source = ROOT / "lean/P196/Agent2SaturatedProfile/Saturated8CycleProfile.lean"
    text = source.read_text(encoding="utf-8")
    definition = text.split("def cycleState :", 1)[1].split("theorem edge0", 1)[0]
    rows = re.findall(r"[|]\s*(?:[0-6]|_)\s*=>\s*\u27e8(\d+),(\d+),(\d+)\u27e9", definition)
    assert len(rows) == 8
    return tuple(tuple(map(int, row)) for row in rows)


def main():
    exhaustive_words = checks = 0
    checks += audit_word([])
    exhaustive_words += 1
    for width in range(1, 4):
        for first in range(1, 19):
            for suffix in product(range(19), repeat=width - 1):
                checks += audit_word([first, *suffix])
                exhaustive_words += 1
    rng = random.Random(106)
    for _ in range(5000):
        width = rng.randrange(4, 65)
        word = [rng.randrange(1, 19)] + [rng.randrange(19) for _ in range(width - 1)]
        checks += audit_word(word)
    skeleton = source_skeleton()
    accepted = []
    for phase, prefix in enumerate(skeleton):
        for inward in (0, 1):
            successor, overflow = prefix_advance(prefix, inward)
            if successor == skeleton[(phase + 1) % 8]:
                assert overflow == phase % 2
                accepted.append((phase, inward))
    assert accepted == [(0, 1), (1, 0), (1, 1), (2, 0), (3, 0), (3, 1),
                        (4, 0), (5, 0), (5, 1), (6, 1), (7, 0), (7, 1)]
    print("PREFIX_BRIDGE_CHECK PASSED")
    print(f"exhaustive_words={exhaustive_words} random_words=5000 padded_checks={checks}")
    print(f"source_skeleton={skeleton}")
    print(f"admissible_skeleton_inputs={accepted}")
    print("scope: arithmetic bridge audit; existing 8-phase theorem is credited, not reproved")


if __name__ == "__main__":
    main()
