#!/usr/bin/env python3
"""Independently replay Agent101's 24-edge decimal CENTER cycle.

Discovery: https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433181110
This is not an exterior B cycle, a certificate, or a Lychrel-number proof.
The arithmetic below normalizes whole integers and imports no search code.

Usage: python3 calculation/agent-117/p24_center_target.py [--full]
"""
from __future__ import annotations

import argparse
import json


BASE = 10
E = tuple(map(int, "010100110100101011001011"))
G = tuple(map(int, "110001001000110001001000"))
V = tuple(map(int, "100001000000100001000000"))
CENTERS = (
    (9, 14, 13, 18, 13, 14, 9),
    (4, 9, 13, 13, 9, 4),
    (14, 14, 3, 8, 3, 14, 14),
    (9, 9, 7, 16, 7, 9, 9),
    (9, 9, 16, 12, 16, 9, 9),
    (9, 9, 13, 6, 13, 9, 9),
    (9, 3, 10, 10, 3, 9),
    (9, 8, 1, 1, 8, 9),
    (9, 17, 2, 2, 17, 9),
    (9, 7, 10, 4, 10, 7, 9),
    (9, 16, 0, 10, 0, 16, 9),
    (9, 12, 2, 0, 2, 12, 9),
    (9, 4, 5, 0, 5, 4, 9),
    (14, 9, 5, 5, 9, 14),
    (4, 4, 15, 10, 15, 4, 4),
    (9, 9, 11, 2, 11, 9, 9),
    (9, 9, 2, 6, 2, 9, 9),
    (9, 9, 5, 12, 5, 9, 9),
    (9, 15, 8, 8, 15, 9),
    (9, 10, 17, 17, 10, 9),
    (9, 1, 16, 16, 1, 9),
    (9, 11, 8, 14, 8, 11, 9),
    (9, 2, 18, 8, 18, 2, 9),
    (9, 6, 16, 18, 16, 6, 9),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer_norm(base, word, incoming):
    """Digit extraction from one integer, not the incremental carry routine."""
    value = incoming + sum(coefficient * base ** i for i, coefficient in enumerate(word))
    power = base ** len(word)
    carry, residue = divmod(value, power)
    digits = [(residue // base ** i) % base for i in range(len(word))]
    return digits, carry


def replay_centers(full=False):
    require(len(CENTERS) == len(E) == len(G) == len(V) == 24, "fixture period")
    edges = []
    for t, center in enumerate(CENTERS):
        target = CENTERS[(t + 1) % len(CENTERS)]
        require(center == center[::-1] and all(0 <= c <= 18 for c in center),
                f"phase {t}: invalid source center")
        digits, carry = integer_norm(BASE, center, E[t])
        require(carry == 1 - E[t], f"phase {t}: carry does not flip")
        if G[t]:
            digits.append(9 * E[t])
        raw = [a + b for a, b in zip(digits, reversed(digits))]
        require(raw == [9] * V[t] + list(target) + [9] * V[t],
                f"phase {t}: image/trim identity")
        require(len(target) == len(center) + G[t] - 2 * V[t],
                f"phase {t}: width identity")
        edges.append({"t": t, "C": list(center), "C2": list(target),
                      "e": E[t], "e2": carry, "g": G[t], "v": V[t],
                      "normalized_digits_with_overflow": digits, "raw_C": raw})
    require(sum(G) == 2 * sum(V), "unbalanced widths")
    complement = all(CENTERS[t + 12] == tuple(18 - c for c in CENTERS[t])
                     for t in range(12))
    result = {
        "status": "CENTER_CYCLE_VERIFIED", "classification": "COMPUTED",
        "discovered_by": "Agent101",
        "source": "https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433181110",
        "base": BASE, "period": len(CENTERS), "e": list(E), "g": list(G), "v": list(V),
        "sum_g": sum(G), "sum_v": sum(V), "widths": list(map(len, CENTERS)),
        "min_width": min(map(len, CENTERS)), "max_width": max(map(len, CENTERS)),
        "half_period_complement": complement,
        "exterior_verified": False, "certificate_verified": False,
        "new_lean_verification": False,
    }
    if full:
        result["edges"] = edges
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="include every center and raw edge")
    args = parser.parse_args()
    print(json.dumps(replay_centers(args.full)))


if __name__ == "__main__":
    main()
