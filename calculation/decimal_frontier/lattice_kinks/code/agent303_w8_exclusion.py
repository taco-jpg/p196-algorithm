#!/usr/bin/env python3
"""Reproduce agent-303's width-eight p=8 rec0 horizon exclusions.

Run from the repository root:
  python3 calculation/decimal_frontier/lattice_kinks/code/agent303_w8_exclusion.py

Requires python-sat with Cadical153.  The four UNSAT instances rule out a
surviving (and hence periodic) free centre window of half-width at most eight
in every compatible parity class of rec0.
"""
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))

from lib7 import Lattice, parse_scc
from sat_kink import build, load_lat, solve


def write_lat0(path: Path) -> None:
    rec = parse_scc(str(ROOT / "calculation/decimal_frontier/lattice_formats/p8_scc.txt"))[0]
    lat = Lattice(rec)
    cups = []
    for t in range(lat.p):
        word = lat.Bt[t] + lat.Wt[t] * 40
        carries = []
        carry = 0
        for digit in word:
            carries.append(carry)
            carry = int(digit + carry >= 10)
        cups.append([carries[lat.nB + 30 * lat.m + j] for j in range(lat.m)])
    with path.open("w") as out:
        out.write(f"{lat.p} {lat.nB} {lat.m} 10\n")
        out.write(" ".join(map(str, lat.g)) + "\n")
        for row in lat.Wt + cups + lat.Bt:
            out.write(" ".join(map(str, row)) + "\n")


def main() -> None:
    # The first unsatisfiable horizon in each of the four classes.
    bounds = ((0, 33), (1, 35), (2, 30), (3, 39))
    with tempfile.TemporaryDirectory() as directory:
        filename = Path(directory) / "lat0.txt"
        write_lat0(filename)
        lat = load_lat(str(filename))
        for offset, horizon in bounds:
            encoding, _, _, _ = build(lat, 8, offset, "hor", horizon)
            sat, _, seconds = solve(encoding)
            print(f"w=8 o={offset} H={horizon}: {'SAT' if sat else 'UNSAT'} {seconds:.2f}s")
            if sat:
                raise SystemExit("unexpected survivor")


if __name__ == "__main__":
    main()
