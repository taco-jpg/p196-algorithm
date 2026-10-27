#!/usr/bin/env python3
"""Replay Agent6's P42 decimal center fixture using whole integers.

Source: PR361, commit0ac61037, reports/agent-6-T1-prefix3-D7.md.
Only the prescribed center/e/g/v data are retained.  No exterior-prefix
constraint from that projected witness is imposed on the new B search.
This center fixture alone is neither a cycleOK certificate nor a proof.
"""
from __future__ import annotations

import argparse
import json

from p24_center_target import integer_norm, require


BASE = 10
E = tuple(map(int, "010100010111000101010101011101000111010101"))
G = tuple(map(int, "101000101001001010100101000101001001010100"))
V = tuple(map(int, "000000010000200000010000000010000200000010"))
CENTERS = (
    (18, 13, 13, 18),
    (8, 13, 8, 13, 8),
    (18, 6, 18, 6, 18),
    (8, 15, 15, 15, 15, 8),
    (18, 11, 12, 12, 11, 18),
    (17, 4, 6, 6, 4, 17),
    (14, 9, 12, 12, 9, 14),
    (4, 5, 3, 6, 3, 5, 4),
    (10, 6, 12, 6, 10),
    (0, 7, 9, 9, 7, 0),
    (1, 14, 18, 18, 14, 1),
    (4, 9, 18, 18, 9, 4),
    (14, 14, 8, 18, 8, 14, 14),
    (18, 16, 18),
    (17, 14, 17),
    (7, 13, 13, 7),
    (16, 7, 7, 16),
    (6, 14, 14, 14, 6),
    (14, 9, 10, 9, 14),
    (4, 5, 1, 1, 5, 4),
    (10, 2, 2, 10),
    (0, 5, 5, 0),
    (10, 5, 10, 5, 10),
    (0, 12, 0, 12, 0),
    (10, 3, 3, 3, 3, 10),
    (0, 7, 6, 6, 7, 0),
    (1, 14, 12, 12, 14, 1),
    (4, 9, 6, 6, 9, 4),
    (14, 13, 15, 12, 15, 13, 14),
    (8, 12, 6, 12, 8),
    (18, 11, 9, 9, 11, 18),
    (17, 4, 0, 0, 4, 17),
    (14, 9, 0, 0, 9, 14),
    (4, 4, 10, 0, 10, 4, 4),
    (0, 2, 0),
    (1, 4, 1),
    (11, 5, 5, 11),
    (2, 11, 11, 2),
    (12, 4, 4, 4, 12),
    (4, 9, 8, 9, 4),
    (14, 13, 17, 17, 13, 14),
    (8, 16, 16, 8),
)


def replay_centers(full=False):
    require(len(CENTERS) == len(E) == len(G) == len(V) == 42, "fixture period")
    edges = []
    for t, center in enumerate(CENTERS):
        target = CENTERS[(t + 1) % len(CENTERS)]
        require(center == center[::-1] and all(type(c) is int and 0 <= c <= 18 for c in center),
                f"phase {t}: invalid source center")
        digits, carry = integer_norm(BASE, center, E[t])
        require(carry == 1 - E[t], f"phase {t}: carry does not flip")
        if G[t]:
            digits.append(9 * E[t])
        raw = [a + b for a, b in zip(digits, reversed(digits))]
        require(raw == [9] * V[t] + list(target) + [9] * V[t], f"phase {t}: raw image/trim identity")
        require(len(target) == len(center) + G[t] - 2 * V[t], f"phase {t}: width identity")
        edges.append({"t": t, "C": list(center), "C2": list(target), "e": E[t],
                      "e2": carry, "g": G[t], "v": V[t], "raw_C": raw})
    require(sum(G) == 2 * sum(V), "unbalanced center widths")
    result = {
        "status": "CENTER_CYCLE_VERIFIED", "classification": "COMPUTED",
        "discovered_by": "Agent6",
        "source": "https://github.com/taco-jpg/p196-algorithm/blob/0ac61037/reports/agent-6-T1-prefix3-D7.md",
        "base": BASE, "period": len(CENTERS), "e": list(E), "g": list(G), "v": list(V),
        "sum_g": sum(G), "sum_v": sum(V), "widths": list(map(len, CENTERS)),
        "min_width": min(map(len, CENTERS)), "max_width": max(map(len, CENTERS)),
        "half_period_complement": all(CENTERS[t + 21] == tuple(18 - x for x in CENTERS[t]) for t in range(21)),
        "exterior_prefix_constraint_imposed": False, "exterior_verified": False,
        "certificate_verified": False, "new_lean_verification": False,
    }
    if full:
        result["edges"] = edges
    return result


def assemble_candidate(words):
    """Accept only actual whole B words; then check every full edge in mirror."""
    from fixed_driver_verify import load_mirror, verify_exterior_words
    replay_centers()
    width = verify_exterior_words(BASE, E, G, words)
    edges = [(list(words[t]), list(CENTERS[t]), list(words[(t + 1) % 42]),
              list(CENTERS[(t + 1) % 42]), G[t], V[t]) for t in range(42)]
    mirror = load_mirror()
    require(mirror.cycleOK(BASE, edges, edges[0][0], edges[0][1]), "Python mirror rejected candidate")
    return {"status": "PYTHON_CERTIFICATE_CANDIDATE", "base": BASE, "period": 42,
            "width": width, "python_mirror_cycleOK": True, "edges": edges, "lean_verified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    print(json.dumps(replay_centers(args.full)))


if __name__ == "__main__":
    main()
