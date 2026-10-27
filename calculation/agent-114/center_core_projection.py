#!/usr/bin/env python3
"""Exact witnesses for the limitation of finite centered-window abstractions.

This program constructs closed PROJECTED paths, never full center cycles.
Each projected edge has its own full-word witness.  The report proves the
construction for every finite radius; the checks below audit its arithmetic.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True)
class Mode:
    e: int
    g: int
    enext: int
    trim: int
    shell: tuple[int, ...]


MODES = (
    Mode(0, 0, 0, 0, (15, 5)),
    Mode(0, 0, 1, 0, (10, 0)),
    Mode(1, 0, 0, 0, (5, 6)),
    Mode(1, 0, 1, 0, (0, 1)),
    Mode(0, 0, 0, 1, (14, 15, 0)),
    Mode(0, 0, 1, 1, (14, 10, 6)),
    Mode(1, 0, 0, 1, (4, 5, 0)),
    Mode(1, 0, 1, 1, (4, 0, 6)),
    Mode(0, 1, 1, 0, (10, 0)),
    Mode(1, 1, 0, 0, (0, 1)),
)
MODE_MAP = {(q.e, q.g, q.enext, q.trim): q for q in MODES}
STREAMS = {
    "p11": ("10100110011", "11100010000"),
    "p12": ("101010010101", "100010001000"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def normalize(word: tuple[int, ...], entry: int):
    digits, carries = [], [entry]
    for coefficient in word:
        total = coefficient + carries[-1]
        digits.append(total % 10)
        carries.append(total // 10)
    return tuple(digits), tuple(carries)


def raw_center(word: tuple[int, ...], e: int, g: int):
    digits, carries = normalize(word, e)
    require(carries[-1] == 1 - e, "source center does not flip its carry")
    extended = digits + ((9 * e,) if g else ())
    return tuple(a + b for a, b in zip(extended, reversed(extended)))


def maximal_trim(word: tuple[int, ...]):
    count = 0
    while len(word) >= 2 and word[0] == word[-1] == 9:
        word = word[1:-1]
        count += 1
    return word, count


def alternating_sum(word: tuple[int, ...]) -> int:
    return sum(x if i % 2 == 0 else -x for i, x in enumerate(word))


def make_source(mode: Mode, length: int, residue: int):
    middle_length = length - 2 * len(mode.shell) - 8
    require(middle_length >= 4, "source is too short for the guarded filler")
    digit = (7 * (residue - 2 * sum(mode.shell))) % 9
    half = mode.shell + (0, digit, digit, 0)
    return half + (0,) * middle_length + half[::-1]


def project(word: tuple[int, ...], e: int, radius: int):
    require(radius >= 1, "radius must be positive")
    require(word == word[::-1] and all(0 <= x <= 18 for x in word),
            "invalid symmetric center")
    require(bool(word) and word[0] != 9, "center must be normalized")
    digits, carries = normalize(word, e)
    require(carries[-1] == 1 - e, "target/source carry flip fails")
    width = 2 * radius + len(word) % 2
    require(width <= len(word), "window exceeds full center")
    start = (len(word) - width) // 2
    alt = alternating_sum(word) % 11 if len(word) % 2 else 0
    if len(word) % 2:
        require(word[len(word) // 2] % 2 == 0 and alt == 9,
                "odd-center invariant fails")
    return (e, len(word), word[start:start + width],
            digits[start:start + width], carries[start:start + width + 1],
            sum(word) % 9, alt)


def check_edge(mode: Mode, length: int, residue: int, radius: int):
    source = make_source(mode, length, residue)
    raw = raw_center(source, mode.e, mode.g)
    target, trim = maximal_trim(raw)
    require(trim == mode.trim, "unexpected maximal trim")
    p, q = project(source, mode.e, radius), project(target, mode.enext, radius)
    require(q[1] == length + mode.g - 2 * trim, "length identity fails")
    require(p[5] == residue, "filler did not realize the requested residue")
    require(q[5] == (2 * residue + 4 * mode.e - 2) % 9,
            "center residue recurrence fails")
    require(all(all(x == 0 for x in state[i]) for state in (p, q)
                for i in (2, 3, 4)), "central coefficients/digits/carries are not zero")
    return source, target, p, q


def residue_cycles(es: list[int]):
    result = []
    for initial in range(9):
        residues, s = [], initial
        for e in es:
            residues.append(s)
            s = (2 * s + 4 * e - 2) % 9
        if s == initial:
            result.append(residues)
    return result


def projected_loop(name: str, repetitions: int, radius: int):
    ebits, gbits = STREAMS[name]
    es = [int(c) for c in ebits * repetitions]
    gs = [int(c) for c in gbits * repetitions]
    total_g = sum(gs)
    require(total_g % 2 == 0, "odd total overflow: prior length-parity obstruction")
    require(all(not g or es[(i + 1) % len(es)] == 1 - es[i]
                for i, g in enumerate(gs)), "overflow carry itinerary fails")
    available = [i for i, g in enumerate(gs) if not g]
    require(len(available) >= total_g // 2, "insufficient nonoverflow trim phases")
    trims = [0] * len(es)
    for i in available[:total_g // 2]:
        trims[i] = 1
    offsets = [0]
    for g, v in zip(gs, trims):
        offsets.append(offsets[-1] + g - 2 * v)
    require(offsets[-1] == 0, "length schedule does not close")
    residues = residue_cycles(es)
    require(bool(residues), "no closed mod-9 residue itinerary")
    lengths = [2 * radius + 24 - min(offsets) + x for x in offsets[:-1]]
    edges = []
    for i, (e, g, v, n, s) in enumerate(zip(es, gs, trims, lengths, residues[0])):
        mode = MODE_MAP[e, g, es[(i + 1) % len(es)], v]
        edges.append(check_edge(mode, n, s, radius))
    require(all(edges[i][3] == edges[(i + 1) % len(edges)][2]
                for i in range(len(edges))), "projected path does not close")
    full_mismatches = sum(edges[i][1] != edges[(i + 1) % len(edges)][0]
                          for i in range(len(edges)))
    require(full_mismatches > 0, "unexpected full center return: investigate immediately")
    return {"stream": name, "repetitions": repetitions, "radius": radius,
            "period": len(es), "sum_g": total_g, "sum_v": sum(trims),
            "min_length": min(lengths), "max_length": max(lengths),
            "initial_residue": residues[0][0], "full_word_mismatches": full_mismatches,
            "status": "PROJECTED_LOOP_ONLY"}


def selftest(max_radius: int):
    count = 0
    for radius in range(1, max_radius + 1):
        for parity in (0, 1):
            for mode in MODES:
                for residue in range(9):
                    check_edge(mode, 2 * radius + 24 + parity, residue, radius)
                    count += 1
    # An external mirror cross-check verifies actual center blocks against the
    # repository's exact checker.  This is not the independent integer audit.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    examples = {(0, 0, 0): [1], (0, 0, 1): [5],
                (1, 0, 0): [1, 10], (1, 0, 1): [1, 15],
                (0, 1, 1): [10, 0], (1, 1, 0): [10]}
    mirror_count = 0
    for mode in MODES:
        for residue in range(9):
            source, target, _, _ = check_edge(mode, 45, residue, 8)
            B = examples[mode.e, mode.g, mode.enext]
            Bnext = mirror.nextB(10, B, list(source))
            edge = (B, list(source), Bnext, list(target), 0, mode.trim)
            require(mirror.edgeOK(10, edge), "repository mirror rejects witness edge")
            require(mirror.hyp(10, Bnext, list(target)), "mirror target Hyp fails")
            require(mirror.gam(10, B, list(source)) == mode.g, "mirror overflow mismatch")
            mirror_count += 1
    print(f"LOCAL_WITNESSES={count} MIRROR_EDGES={mirror_count} PASS")
    loop_count = 0
    for radius in (1, max_radius):
        for name, reps in (("p11", (1, 2, 3, 4)), ("p12", (2, 4, 6))):
            for repetition in reps:
                print(projected_loop(name, repetition, radius))
                loop_count += 1
    print(f"PROJECTED_LOOPS={loop_count} FULL_CENTER_CYCLE_CLAIM=False PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-radius", type=int, default=32)
    args = parser.parse_args()
    require(1 <= args.max_radius <= 256, "max radius must be in 1..256")
    selftest(args.max_radius)


if __name__ == "__main__":
    main()
