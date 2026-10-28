#!/usr/bin/env python3
"""Exact finite symmetries of already published decimal lattice SCC words.

Does not run a new exterior census, search for a centre, or establish
a Lychrel certificate. Uses only the repository's stored lattice words.

Usage (from repository root):
    python3 /path/to/agent14_complement_twist.py
"""
import re
from pathlib import Path

ROOT = Path.cwd()
SCC = ROOT / "calculation/decimal_frontier/lattice_formats/p8_scc.txt"
P12 = ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"

def bracketed(text):
    return [
        [int(y) for y in x.split(",")]
        for x in re.findall(r"\[([0-9,]+)\]", text)
    ]

def load():
    rows = []
    for index, line in enumerate(
        x for x in SCC.read_text().splitlines() if x.startswith("SCC p=")
    ):
        # Parse the complete source record, including the exterior prefix.
        match = re.fullmatch(
            r"SCC p=(\d+) g=(\w+) size=(\d+) cyclen=(\d+) "
            r"depth=(\d+) path=(.*?) cyc=(.*)", line
        )
        p, g, _, m, _, prefix, cycle = match.groups()
        cols = bracketed(cycle)
        path_cols = bracketed(prefix)
        assert len(cols) == int(m)
        assert all(len(col) == int(p) for col in cols)
        rows.append({
            "name": f"p8-rec{index}", "p": int(p), "m": int(m),
            "g": [int(x) for x in g], "nB": len(path_cols),
            "W": [[col[t] for col in cols] for t in range(int(p))],
        })
    lines = P12.read_text().strip().splitlines()
    p, nB, m, b = map(int, lines[0].split())
    assert b == 10
    rows.append({
        "name": "p12-m9", "p": p, "m": m, "nB": nB,
        "g": list(map(int, lines[1].split())),
        "W": [list(map(int, line.split())) for line in lines[2:p + 2]],
    })
    for row in rows:
        assert len(row["W"]) == row["p"]
        assert all(len(w) == row["m"] for w in row["W"])
        assert all(0 <= v <= 18 for w in row["W"] for v in w)
    return rows

def glides(entry, complemented=False, reflected=False):
    p, m, W = entry["p"], entry["m"], entry["W"]
    out = []
    for dt in range(p):
        for dx in range(m):
            def match(t, j):
                other_j = (dx - j if reflected else dx + j) % m
                a, b = W[t][j], W[(t + dt) % p][other_j]
                return a + b == 18 if complemented else a == b
            if all(match(t, j) for t in range(p) for j in range(m)):
                out.append((dt, dx))
    return out

def carry_rows(entry):
    """The absorbing fixed-point carry entering each spatial column."""
    result = []
    for w in entry["W"]:
        c = 0
        for x in w:
            c = int(x + c >= 10)
        row = []
        initial = c
        for x in w:
            row.append(c)
            c = int(x + c >= 10)
        assert c == initial
        result.append(row)
    return result

def complement_carry_glides(entry):
    p, m, W = entry["p"], entry["m"], entry["W"]
    C = carry_rows(entry)
    out = []
    for dt in range(p):
        for dx in range(m):
            if all(
                W[t][j] + W[(t + dt) % p][(j + dx) % m] == 18
                and C[t][j] + C[(t + dt) % p][(j + dx) % m] == 1
                for t in range(p) for j in range(m)
            ):
                out.append((dt, dx))
    return out

def odd_counts(entry):
    return [sum(x % 2 for x in row) for row in entry["W"]]

def centre_period(entry):
    p, m, W, g = (
        entry["p"], entry["m"], entry["W"], entry["g"]
    )
    # This exceeds the group exponent; if any compatible d exists,
    # a candidate exists by p*(2m).
    upto = 2 * p * m
    for d in range(1, upto + 1):
        if not all(g[t] == g[(t + d) % p] for t in range(p)):
            continue
        delta = sum(g[t % p] for t in range(d))
        if delta % 2:
            continue
        shift = delta // 2
        if all(
            W[t][j] == W[(t + d) % p][(j + shift) % m]
            for t in range(p) for j in range(m)
        ):
            return d
    return None

def reflection_distance(entry):
    m, W = entry["m"], entry["W"]
    return [
        min(sum(w[j] != w[(a - j) % m] for j in range(m))
            for a in range(m))
        for w in W
    ]

def central_odd_obstructions(entry):
    """For each starting residue n0 mod 2m, count time slices in
    one alignment period at which odd n requires an even central
    pair coefficient but the unmodified lattice has an odd value.
    """
    p, m, nB, W, g = (
        entry["p"], entry["m"], entry["nB"],
        entry["W"], entry["g"]
    )
    T = centre_period(entry)
    out = []
    for residue in range(2 * m):
        n = 20000 + residue
        count = 0
        for t in range(T):
            if n % 2:
                h = (n + 1) // 2
                val = W[t % p][(h - 1 - nB) % m]
                count += val % 2
            n += g[t % p]
        out.append(count)
    return sorted(set(out))


def complement_twist_exclusion(entry):
    """Exhausts all start phases and all parity-preserving centre drifts.

    Repetition after L steps is exact: the overflow sum is a multiple of
    2m, so both row time phase and centre offset modulo m recur.
    """
    from math import gcd
    p, m, W, g = entry["p"], entry["m"], entry["W"], entry["g"]
    L = p * (2*m // gcd(2*m, sum(g)))
    eligible, min_twist = 0, m+1
    normal, twisted = [], []
    for t in range(p):
        growth = 0
        for d in range(1, L+1):
            growth += g[(t+d-1) % p]
            if growth % 2: continue
            eligible += 1
            shift = growth//2
            differences = sum(W[(t+d)%p][(j+shift)%m] != W[t][j]
                              for j in range(m))
            complements = sum(W[(t+d)%p][(j+shift)%m] != 18-W[t][j]
                              for j in range(m))
            if differences == 0: normal.append((t,d))
            if complements == 0: twisted.append((t,d))
            min_twist = min(min_twist, complements)
    assert normal == [(t,L) for t in range(p)]
    return (L, eligible, min_twist, twisted)

def main():
    expected = {
        "p8-rec0": ([(0,0),(4,10)], [(2,5),(6,15)], 80, [14]*8, [23]),
        "p8-rec1": ([(0,0),(4,10)], [(2,5),(6,15)], 80, [14]*8, [23]),
        "p8-rec2": ([(0,0)], [(4,24)], 192,
                    [36,36,38,38,36,36,38,38], [44,54]),
        "p12-m9": ([(0,0),(4,6),(8,3)], [], 72,
                    [4,6,6,6,4,6,6,6,4,6,6,6], [17]),
    }
    for entry in load():
        name = entry["name"]
        result = (
            glides(entry), glides(entry, complemented=True),
            centre_period(entry), reflection_distance(entry),
            central_odd_obstructions(entry)
        )
        assert result == expected[name], (name, result, expected[name])
        assert not glides(entry, reflected=True)
        assert complement_carry_glides(entry) == result[1]
        assert min(odd_counts(entry)) > 0
        twist = complement_twist_exclusion(entry)
        exact = {
            "p8-rec0": (80, 320, 16, []),
            "p8-rec1": (80, 320, 16, []),
            "p8-rec2": (192, 768, 39, []),
            "p12-m9": (72, 432, 7, []),
        }[name]
        assert twist == exact, (name, twist, exact)
        print(name, "COMPLETE", twist, "ordinary/control", result[2])
    print("ALL F1 COMPLEMENT-TWIST CHECKS PASSED")
if __name__ == "__main__":
    main()