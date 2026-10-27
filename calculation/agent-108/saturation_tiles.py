#!/usr/bin/env python3
"""Independent arithmetic audit of the saturated exterior block transducer.

Build tiles from quotient inequalities, compare a separate remainder-based
enumeration, and exhaust the full correlated G=1,2 frontiers.  With --mdd,
compare the compiled program's entire tile table and every small layer word.
This audits an exterior search, not a decimal Lychrel certificate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import NamedTuple


class Tile(NamedTuple):
    out: int
    trace: tuple[int, ...]  # x_0,...,x_4, including both horizontal ports

    @property
    def positive(self):
        return all(x > 0 for x in self.trace[:4])


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def unpack(symbol):
    require(0 <= symbol < 2560, "invalid local symbol")
    return symbol & 15, (symbol >> 4) & 15, symbol >> 8


def build_tiles():
    """Equational builder: guess output H/Y, reconstruct x_0, infer output L."""
    result = []
    for source in range(2560):
        lm, hm, y = unpack(source)
        row = []
        for hp in range(16):
            for yp in range(10):
                x = 10 * (hm & 1) + yp - (hp & 1)
                trace, lp = [x], 0
                for r in range(4):
                    l, h, hn = (lm >> r) & 1, (hm >> r) & 1, (hp >> r) & 1
                    if not (0 <= x <= 18 and 10 * h <= x + hn <= 10 * h + 9):
                        break
                    ln = (x + l) // 10
                    require(ln in (0, 1), "nonbinary forward carry")
                    lp |= ln << r
                    if r == 0:
                        x = x + l - 10 * ln + y
                    else:
                        x = 2 * x + l + hn - 10 * (ln + h)
                    trace.append(x)
                else:
                    require(0 <= x <= 18, "invalid right port")
                    row.append(Tile(lp + 16 * hp + 256 * yp, tuple(trace)))
        require(len({t.out for t in row}) == len(row), "nonunique local symbol pair")
        result.append(tuple(sorted(row)))
    return tuple(result)


def reference_local(source):
    """Separate direct-normalization enumeration over x_0 and reverse carry bits."""
    lm, hm, y = unpack(source)
    result = set()
    for x0 in range(19):
        for hp in range(16):
            x, lp, trace = x0, 0, [x0]
            for r in range(4):
                l, h, hn = (lm >> r) & 1, (hm >> r) & 1, (hp >> r) & 1
                if (x + hn) // 10 != h:
                    break
                lp |= ((x + l) // 10) << r
                x = (x + l) % 10 + (y if r == 0 else (x + hn) % 10)
                trace.append(x)
            else:
                yp = (x0 + (hp & 1)) % 10
                result.add(Tile(lp + 16 * hp + 256 * yp, tuple(trace)))
    return result


def terminal_symbol(symbol):
    lm, hm, y = unpack(symbol)
    return hm == (15 ^ lm) and y == 9 * (lm & 1)


def canonical_rows(table):
    """Stable export: source target left right positive x0 x1 x2 x3."""
    return sorted((s, t.out, t.trace[0], t.trace[4], int(t.positive), *t.trace[:4])
                  for s, row in enumerate(table) for t in row)


def serialize_rows(rows):
    return "".join(" ".join(map(str, row)) + "\n" for row in rows).encode("ascii")


def audit_local(table):
    for s, row in enumerate(table):
        require(set(row) == reference_local(s), f"local arithmetic mismatch at {s}")
        if terminal_symbol(s):
            require(Tile(s, (9,) * 5) in row, f"missing neutral-tail loop at {s}")
    count = sum(map(len, table))
    require(count == 48640, "unexpected universal tile count")
    require(sum(bool(row) for row in table) == 2000, "unexpected live input count")
    return {"tiles": count, "input_symbols": 2560, "live_inputs": 2000,
            "max_tiles_per_input": max(map(len, table))}


def indexed_tiles(table):
    return tuple(tuple(tuple(t for t in row if t.trace[0] == left)
                       for left in range(19)) for row in table)


def tile_successors(word, indexed, first):
    result, size = set(), len(word)

    def extend(j, initial, port, output):
        if j == size:
            if port == initial:
                result.add(tuple(output))
            return
        for tile in indexed[word[j]][port]:
            if not first or tile.positive:
                extend(j + 1, initial, tile.trace[4], output + [tile.out])

    for initial in range(19):
        extend(0, initial, initial, [])
    return result


def whole_period_successors(word, first):
    """Independent P-step recursion: no block tiles, MDDs, or repository imports."""
    p = 4 * len(word)
    ls, hs, ys = [], [], []
    for s in word:
        lm, hm, y = unpack(s)
        ls.extend((lm >> r) & 1 for r in range(4))
        hs.extend((hm >> r) & 1 for r in range(4))
        ys.append(y)
    result = set()

    def extend(t, x, initial, coefficients, reverse):
        if t == p:
            if x != initial:
                return
            output = []
            for j in range(len(word)):
                lm = sum(((coefficients[4*j+r] + ls[4*j+r]) // 10) << r
                         for r in range(4))
                hm = sum(reverse[4*j+r] << r for r in range(4))
                y = (coefficients[4*j] + reverse[4*j]) % 10
                output.append(lm + 16 * hm + 256 * y)
            result.add(tuple(output))
            return
        if first and x == 0:
            return
        for carry in (0, 1):
            if (x + carry) // 10 == hs[t]:
                partner = ys[t//4] if t % 4 == 0 else (x + carry) % 10
                following = (x + ls[t]) % 10 + partner
                extend(t + 1, following, initial, coefficients + [x], reverse + [carry])

    for initial in range(1 if first else 0, 19):
        extend(0, initial, initial, [], [])
    return result


def audit_global(g, indexed):
    require(g in (1, 2), "global audit supports only G=1,2")
    layers, seen, arcs = [{(272,) * g}], set(), 0
    for depth in range(32):
        frontier = layers[-1]
        if not frontier:
            break
        require(not any(all(terminal_symbol(s) for s in w) for w in frontier),
                "unexpected accepting control state")
        following = set()
        for word in sorted(frontier):
            expected = whole_period_successors(word, depth == 0)
            actual = tile_successors(word, indexed, depth == 0)
            require(expected == actual, f"correlated transition mismatch G={g} depth={depth}")
            following.update(expected)
            key = (depth == 0, word)
            if key not in seen:
                seen.add(key)
                arcs += len(expected)
        layers.append(following)
    require(not layers[-1], f"UNDECIDED: small global audit depth cap G={g}")
    expected_layers = ([1, 2, 4, 4, 10, 9, 0] if g == 1 else
                       [1, 4, 16, 24, 68, 41, 8, 32, 64, 56, 36, 12, 4, 0])
    require(list(map(len, layers)) == expected_layers, "known-layer control mismatch")
    return layers, {"G": g, "P": 4*g, "status": "EXHAUSTED_NO_B",
                    "states_with_initial_cut": len(seen), "arcs": arcs,
                    "layers": list(map(len, layers)), "accepts": 0}


def run_program(command):
    process = subprocess.run(command, text=True, capture_output=True, timeout=30)
    require(process.returncode == 0,
            f"external audit command failed ({process.returncode}): {process.stderr[-2000:]}")
    return process.stdout


def compare_mdd(executable, rows, layers_by_g):
    output = run_program([executable, "--tiles"])
    got = sorted(tuple(map(int, line.split())) for line in output.splitlines() if line.strip())
    require(got == rows, "compiled universal tile table differs")
    checked_layers, checked_words = 0, 0
    for g, layers in layers_by_g.items():
        for depth, expected in enumerate(layers):
            output = run_program([executable, str(g), "200000", "100000000", "64", "20",
                                  "--export-layer", str(depth)])
            words = json.loads(output.strip().splitlines()[-1])
            require(isinstance(words, list), "compiled layer export did not return words")
            actual = set(map(tuple, words))
            require(len(actual) == len(words), "compiled layer export repeats a word")
            require(actual == expected, f"compiled full layer mismatch G={g} depth={depth}")
            checked_layers += 1
            checked_words += len(words)
    return {"compiled_table_rows": len(got), "complete_layers": checked_layers,
            "complete_layer_words": checked_words}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-g", type=int, choices=(1, 2), nargs="+", default=[1, 2])
    parser.add_argument("--mdd", help="compiled saturation_mdd executable")
    parser.add_argument("--export-table", type=Path, help="optional canonical table outside the repository")
    args = parser.parse_args()
    table = build_tiles()
    local = audit_local(table)
    rows = canonical_rows(table)
    serialized = serialize_rows(rows)
    local["canonical_sha256"] = hashlib.sha256(serialized).hexdigest()
    print("LOCAL", json.dumps(local, sort_keys=True), flush=True)
    if args.export_table:
        args.export_table.write_bytes(serialized)
    indexed, layers_by_g = indexed_tiles(table), {}
    for g in sorted(set(args.audit_g)):
        layers, summary = audit_global(g, indexed)
        layers_by_g[g] = layers
        print("GLOBAL", json.dumps(summary, sort_keys=True), flush=True)
    if args.mdd:
        summary = compare_mdd(str(Path(args.mdd).resolve()), rows, layers_by_g)
        print("MDD", json.dumps(summary, sort_keys=True), flush=True)
    print("AUDIT PASS: exact local tiles and full correlated small-period transitions")


if __name__ == "__main__":
    main()
