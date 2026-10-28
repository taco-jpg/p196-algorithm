#!/usr/bin/env python3
"""Reproduce agent-2's rec0 periodic-lattice boundary table without external Python packages.

Usage from repository root:
  python3 calculation/decimal_frontier/lattice_kinks/code/agent2_boundary_data.py
This writes 20 rec0 spatial rows then 39 transient rows to stdout. Redirect
that output to a local file and pass it to boundary_transfer.cpp.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'calculation/decimal_frontier/lattice_formats/p8_scc.txt'


def rows(path=SOURCE):
    line = next(l for l in path.read_text().splitlines() if l.startswith('SCC'))
    def blocks(string):
        return [list(map(int, x.split(','))) for x in re.findall(r'\[([^]\n]+)\]', string)]
    prefix, cycle = line.split(' cyc=', 1)
    pathpart = prefix.split(' path=', 1)[1]
    w, b = blocks(cycle), blocks(pathpart)
    assert (len(w), len(b)) == (20, 39)
    assert all(len(row) == 8 and all(0 <= v <= 18 for v in row) for row in w + b)
    return w + b


if __name__ == '__main__':
    for row in rows():
        print(*row)