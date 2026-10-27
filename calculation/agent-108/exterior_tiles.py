#!/usr/bin/env python3
"""Independent exact audit of decimal exterior overflow blocks of lengths 1..5.

A block has g=(1,0,...,0).  At a spatial cut its symbol is (L,H,Y),
encoded as L + 2**r H + 2**(2*r) Y, with r-bit carry masks and a digit Y.
For an output symbol (L',H',Y'), the coefficient trace x_0,...,x_r obeys

    x_0 = 10 H_0 + Y' - H'_0,
    10 L'_j <= x_j + L_j <= 10 L'_j + 9,
    10 H_j  <= x_j + H'_j <= 10 H_j  + 9,
    x_1 = x_0 + L_0 - 10 L'_0 + Y,
    x_(j+1) = 2 x_j + L_j + H'_j - 10(L'_j + H_j), j>0.

All x_j are in 0..18.  Thus a symbol pair determines its trace uniquely.
The two horizontal ports are x_0 and x_r; adjacent temporal blocks share
these ports, with cyclic closure.  First-column tiles additionally require
x_0,...,x_(r-1)>0.  Generic columns do not impose that condition.

The physical initial symbol is 2**r + 2**(2*r).  A terminal symbol satisfies
H = ((1<<r)-1) xor L and Y = 9*(L&1); precisely these symbols have an
unchanged-symbol tile with all coefficients and ports equal to neutral 9.

The primary builder reconstructs coefficients from quotient inequalities.
A separately organized complete enumeration chooses x_0,L,H',Y and uses
ordinary quotient/remainder normalization, computing H,L',Y' afterwards.
It has 19 * 10 * 4**r choices, each a distinct (source,target) tile, giving
an independent exact count.  Every r=1..5 table is compared in full.
With --mdd, every exported C++ row is also compared, including positivity.

This is a local transition audit, not an all-width search or a certificate.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
from typing import NamedTuple


class Tile(NamedTuple):
    out: int
    trace: tuple[int, ...]

    @property
    def positive(self):
        return all(x > 0 for x in self.trace[:-1])


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parameters(r):
    require(type(r) is int and 1 <= r <= 5, "supported block lengths are 1..5")
    radix = 1 << r
    return radix, radix - 1, 10 * radix * radix


def unpack(symbol, r):
    radix, mask, size = parameters(r)
    require(type(symbol) is int and 0 <= symbol < size, "invalid local symbol")
    return symbol & mask, (symbol >> r) & mask, symbol >> (2 * r)


def initial_symbol(r):
    radix, _, _ = parameters(r)
    return radix + radix * radix


def terminal_symbol(symbol, r):
    _, mask, _ = parameters(r)
    lm, hm, y = unpack(symbol, r)
    return hm == (mask ^ lm) and y == 9 * (lm & 1)


def build_tiles(r):
    """Guess H'/Y', reconstruct x_0, and propagate the quotient inequalities."""
    radix, _, size = parameters(r)
    result = []
    for source in range(size):
        lm, hm, y = unpack(source, r)
        row = []
        for hp in range(radix):
            for yp in range(10):
                x = 10 * (hm & 1) + yp - (hp & 1)
                trace, lp = [x], 0
                for j in range(r):
                    l, h, hn = (lm >> j) & 1, (hm >> j) & 1, (hp >> j) & 1
                    if not (0 <= x <= 18 and 10 * h <= x + hn <= 10 * h + 9):
                        break
                    ln = int(x + l >= 10)
                    require(10 * ln <= x + l <= 10 * ln + 9,
                            "invalid forward quotient")
                    lp |= ln << j
                    x = x + l - 10 * ln + (y if j == 0 else x + hn - 10 * h)
                    trace.append(x)
                else:
                    require(0 <= x <= 18, "invalid right coefficient port")
                    row.append(Tile(lp + radix * hp + radix * radix * yp, tuple(trace)))
        require(len({t.out for t in row}) == len(row), "nonunique symbol-pair trace")
        result.append(tuple(sorted(row)))
    return tuple(result)


def normalization_tiles(r):
    """Enumerate raw coefficient/carry inputs; infer both source and target.

    This does not use the quotient-inequality builder or reconstruct x_0
    from Y'.  Every normalization operand is a nonnegative ordinary integer.
    The free choices are x_0 (19), Y (10), L (2**r), and H' (2**r).
    """
    radix, _, size = parameters(r)
    rows = [dict() for _ in range(size)]
    for x0 in range(19):
        for y in range(10):
            for lm in range(radix):
                for hp in range(radix):
                    x, hm, lp, trace = x0, 0, 0, [x0]
                    for j in range(r):
                        forward = divmod(x + ((lm >> j) & 1), 10)
                        reverse = divmod(x + ((hp >> j) & 1), 10)
                        lp |= forward[0] << j
                        hm |= reverse[0] << j
                        x = forward[1] + (y if j == 0 else reverse[1])
                        trace.append(x)
                    yp = (x0 + (hp & 1)) % 10
                    source = lm + radix * hm + radix * radix * y
                    target = lp + radix * hp + radix * radix * yp
                    require(target not in rows[source], "normalization choices collided")
                    rows[source][target] = Tile(target, tuple(trace))
    return tuple(tuple(sorted(row.values())) for row in rows)


def positive_tile_count(r):
    """Independent 19-coefficient transfer count, without symbols or tile lists."""
    parameters(r)
    current = Counter()
    # x_0 is a source coefficient; the last port x_r need not be positive.
    for x0 in range(1, 19):
        for l0 in (0, 1):
            for y in range(10):
                current[(x0 + l0) % 10 + y] += 2  # the two reverse-carry choices
    for _ in range(1, r):
        following = Counter()
        for x, multiplicity in current.items():
            if x == 0:
                continue
            for l in (0, 1):
                for h_next in (0, 1):
                    following[(x + l) % 10 + (x + h_next) % 10] += multiplicity
        current = following
    return sum(current.values())


def canonical_rows(table):
    """Stable rows: source target left right positive x_0 ... x_(r-1)."""
    return sorted((s, t.out, t.trace[0], t.trace[-1], int(t.positive), *t.trace[:-1])
                  for s, row in enumerate(table) for t in row)


def digest_rows(rows):
    digest = hashlib.sha256()
    for row in rows:
        digest.update((" ".join(map(str, row)) + "\n").encode("ascii"))
    return digest.hexdigest()


def audit_local(r, table):
    reference = normalization_tiles(r)
    require(table == reference, f"complete normalization table mismatch at r={r}")
    radix, _, size = parameters(r)
    neutral_count, positive_count, max_per_left = 0, 0, 0
    for source, row in enumerate(table):
        require(all(len(t.trace) == r + 1 and all(0 <= x <= 18 for x in t.trace)
                    and 0 <= t.out < size for t in row), "invalid tile range")
        neutral_loop = Tile(source, (9,) * (r + 1)) in row
        require(neutral_loop == terminal_symbol(source, r), "neutral terminal characterization")
        neutral_count += neutral_loop
        positive_count += sum(t.positive for t in row)
        max_per_left = max(max_per_left, max(Counter(t.trace[0] for t in row).values(), default=0))
    require(neutral_count == radix, "wrong number of terminal symbols")
    require(not terminal_symbol(initial_symbol(r), r), "physical initial cut accepted as terminal")
    count = sum(map(len, table))
    require(count == 190 * 4**r, "raw-choice count mismatch")
    require(positive_count == positive_tile_count(r), "independent first-column count mismatch")
    rows = canonical_rows(table)
    return rows, {
        "r": r, "tiles": count, "input_symbols": size,
        "live_inputs": sum(bool(row) for row in table),
        "max_tiles_per_input": max(map(len, table)),
        "max_tiles_per_input_left": max_per_left,
        "positive_tiles": positive_count, "terminal_symbols": neutral_count,
        "initial_symbol": initial_symbol(r),
        "canonical_sha256": digest_rows(rows),
    }


def compare_program(executable, r, expected):
    process = subprocess.run([executable, "--tiles", str(r)], capture_output=True,
                             text=True, timeout=30)
    require(process.returncode == 0,
            f"r={r} external tile export failed ({process.returncode}): {process.stderr[-1000:]}")
    actual = []
    for line in process.stdout.splitlines():
        if line.strip():
            row = tuple(map(int, line.split()))
            require(len(row) == r + 5, f"r={r} wrong exported column count")
            actual.append(row)
    actual.sort()
    require(actual == expected, f"r={r} compiled full table differs")
    return len(actual)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r", type=int, choices=range(1, 6), nargs="+", default=list(range(1, 6)))
    parser.add_argument("--mdd", help="compiled exterior_mdd executable, supporting --tiles R")
    args = parser.parse_args()
    compiled_rows = 0
    for r in sorted(set(args.r)):
        rows, summary = audit_local(r, build_tiles(r))
        if args.mdd:
            compiled_rows += compare_program(str(Path(args.mdd).resolve()), r, rows)
            summary["compiled_rows_checked"] = len(rows)
        print("LOCAL", json.dumps(summary, sort_keys=True), flush=True)
    if args.mdd:
        print("COMPILED", json.dumps({"rows_checked": compiled_rows}), flush=True)
    print("AUDIT PASS: exact local decimal exterior blocks r=" + ",".join(map(str, sorted(set(args.r)))))


if __name__ == "__main__":
    main()
