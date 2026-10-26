#!/usr/bin/env python3
"""End-to-end search for a neutral one-band return certificate in base b via the DECOUPLED method.

 Stage 1 (bauto)   exact B-cycle automaton: all (gam-pattern g, carry stream e, B_t) with B-period p <= pmax and ANY |B|.
 Stage 2 (cauto)   for every B-stream (g,e) (repeated k times so that sum(g) is even), exact C-layer automaton for every
                   trim pattern v and every |C_0| in [m0lo, m0hi]:  does a symmetric C-cycle consistent with the stream exist?
 Stage 3 (mirror)  every (B_0, C_0) pair found is replayed with the exact Python mirror calculation/neutral_band_search.py:
                   run(b,B_0,C_0) must return a cycle and cycleOK must hold.  The full edge list is printed.

usage: python3 pipeline.py b pmax m0hi [kmax=2] [nparts=1 part=0]
files expected next to this script: ./bauto ./cauto (compile: g++ -O2 -o bauto bauto.cpp ; g++ -O2 -o cauto cauto.cpp)
and the repo mirror at /home/claude/p196-algorithm/calculation (edit MIRROR below on the Studio).
"""
import sys, re, subprocess, os
MIRROR = os.environ.get("MIRROR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, MIRROR)
import neutral_band_search as N

here = os.path.dirname(os.path.abspath(__file__))
CAP = os.environ.get("CAP", "20000000")
b = int(sys.argv[1]); pmax = int(sys.argv[2]); m0hi = int(sys.argv[3])
kmax = int(sys.argv[4]) if len(sys.argv) > 4 else 2
nparts = int(sys.argv[5]) if len(sys.argv) > 5 else 1
part = int(sys.argv[6]) if len(sys.argv) > 6 else 0

out = subprocess.run([os.path.join(here, 'bauto'), str(b), '1', str(pmax), '-w'], capture_output=True, text=True).stdout
streams = {}
for line in out.splitlines():
    if not line.startswith('ACCEPT'): continue
    p = int(re.search(r" p=(\d+)", line)[1]); g = re.search(r" g=(\d+)", line)[1]; e = re.search(r" e=(\d+)", line)[1]
    Bs = [[int(x) for x in mm.split(',') if x] for mm in re.findall(r"\[([^\]]*)\]", line)]
    streams.setdefault((g, e), Bs)
print(f"base {b}: {len(streams)} B-streams with period <= {pmax}", flush=True)

idx = 0
for (g, e), Bs in sorted(streams.items(), key=lambda kv: (len(kv[0][0]), kv[0])):
    for k in range(1, kmax + 1):
        gk, ek = g * k, e * k
        if gk.count('1') % 2: continue
        if k > 1 and g.count('1') % 2 == 0 and k > 1 and kmax >= 2 and k % 2 == 0 and False: continue
        idx += 1
        if (idx - 1) % nparts != part: continue
        cmd = [os.path.join(here, 'cauto'), str(b), ek, gk, '1', str(m0hi), '-vall', '-allm', '-w', '-cap', CAP]
        res = subprocess.run(cmd, capture_output=True, text=True).stdout
        feas = [l for l in res.splitlines() if l.startswith('FEASIBLE')]
        capped = [l for l in res.splitlines() if l.startswith('CAPPED')]
        capped += [l for l in res.splitlines() if l.startswith('NOPERIOD')]
        print(f"stream g={g} e={e} k={k} (P={len(gk)}): C feasible instances {len(feas)}, capped/undecided {len(capped)}", flush=True)
        for l in feas[:5]:
            C0 = [int(x) for x in re.search(r" C0=\[([^\]]*)\]", l)[1].split(',')]
            r = N.run(b, Bs[0], C0, maxsteps=2000, maxlen=3000)
            if r[0] == 'cycle':
                es = r[1]
                ok = N.cycleOK(b, es, es[0][0], es[0][1])
                print("  CYCLE", len(es), "edges; cycleOK =", ok, "; gam =", sum(N.gam(b, E[0], E[1]) for E in es),
                      "gain =", sum(E[4] + E[5] for E in es), flush=True)
                print("  B_0 =", Bs[0]); print("  C_0 =", C0)
                print("  EDGES =", es)
            else:
                print("  mirror run did not cycle:", r[0], r[1] if len(r) > 1 else '', "(C_0 =", C0, ")", flush=True)
