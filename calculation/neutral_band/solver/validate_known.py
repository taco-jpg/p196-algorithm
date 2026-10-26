import os
#!/usr/bin/env python3
"""Validation 1: the encoding re-finds a closed chain with the length schedule of each known Lean certificate.
 (a) non-maximal mode with the Lean certificate's own schedule; (b) maximal mode with the schedule of the
 canonical (maximally trimmed) cycle that the mirror's deterministic run reaches from the certificate."""
import sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p196cp as P
bases = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [2, 4, 8, 26]
backend = sys.argv[2] if len(sys.argv) > 2 else 'cpsat'
tl = float(sys.argv[3]) if len(sys.argv) > 3 else 100
for b, es in P.mirror._lean_certs():
    if b not in bases: continue
    S = tuple((len(e[0]), len(e[1])) for e in es)
    r = P.solve(b, S, backend=backend, maximal=False, time_limit=tl)
    c = r.get('certificate', {})
    print(f"base {b} p={len(es)} (a) Lean schedule, non-maximal: {r['status']} {r['time']}s vars={r.get('nvars')} cons={r.get('ncons')}"
          f" mirror_cycleOK={c.get('cycleOK_mirror')} start_B_equals_Lean={c.get('start_B') == es[0][0] if c else None}", flush=True)
    run = P.mirror.run(b, es[0][0], es[0][1])
    cyc = run[1]; S2 = tuple((len(e[0]), len(e[1])) for e in cyc)
    r = P.solve(b, S2, backend=backend, maximal=True, time_limit=tl)
    c = r.get('certificate', {})
    print(f"          (b) canonical cycle p={len(cyc)} schedule {S2[:4]}..: maximal: {r['status']} {r['time']}s vars={r.get('nvars')} cons={r.get('ncons')}"
          f" mirror_cycleOK={c.get('cycleOK_mirror')}", flush=True)
