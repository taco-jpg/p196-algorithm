#!/usr/bin/env python3
"""brute-force controls: run hbf on every primitive neutral exterior stream of the given bases (all c values), report HYBRID-OK cycles
usage: ctrl_bf.py <bases comma> <W>"""
import sys, subprocess
from streams_all import collect
bases = [int(x) for x in sys.argv[1].split(',')]; W = sys.argv[2]
S = collect()
for b in bases:
    N = b - 1
    cs = [str(c) for c in range(2 * b - 1) if c != N]
    for (g, e) in sorted(S.get(b, []), key=lambda x: (len(x[0]), x)):
        r = subprocess.run(['code/hbf', str(b), W, g, e] + cs, capture_output=True, text=True)
        cyc = [l for l in r.stdout.splitlines() if l.startswith('CYCLE')]
        ok = [l for l in cyc if 'HYBRID-OK' in l]
        print(f"b={b} g={g} e={e} W<={W}: cycles {len(cyc)} hybrid-ok {len(ok)}", flush=True)
        for l in ok[:6]: print("   ", l, flush=True)
