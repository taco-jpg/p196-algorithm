import os
#!/usr/bin/env python3
"""Validation 2 (independent of any solver): in a tiny base, enumerate ALL states (B,C) with |B|<=NB, |C|<=MB
(C palindrome), follow the mirror's canonical map, collect every cycle lying inside the box, and compare with the
solver's SAT/UNSAT verdict on EVERY valid length schedule of period p<=PMAX inside the box.
 expected SAT set = {canon(schedule of an in-box cycle of length q repeated p/q times) : q | p}
 usage: validate_bruteforce.py b NB MB PMAX [backend]"""
import sys, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p196cp as P
mirror = P.mirror
b, NB, MB, PMAX = map(int, sys.argv[1:5]); backend = sys.argv[5] if len(sys.argv) > 5 else 'cpsat'
top = 2 * (b - 1)
def pal(Lm):
    for half in itertools.product(range(top + 1), repeat=(Lm + 1) // 2):
        yield tuple(half) + tuple(half[:Lm // 2][::-1])
t0 = time.time()
Bs = [()] + [B for n in range(1, NB + 1) for B in itertools.product(range(top + 1), repeat=n) if B[0] != 0]
Cs = [C for m in range(MB + 1) for C in pal(m)]
nxt = {}
for B in Bs:
    for C in Cs:
        E = mirror.step(b, list(B), list(C))
        if E is None: continue
        s2 = (tuple(E[2]), tuple(E[3]))
        if len(s2[0]) <= NB and len(s2[1]) <= MB: nxt[(B, C)] = s2
print(f"base {b} box |B|<={NB} |C|<={MB}: {len(Bs)*len(Cs)} states, {len(nxt)} with in-box successor ({time.time()-t0:.1f}s)")
# cycles of the partial function
cycles = []; seen = {}
for s in list(nxt):
    if s in seen: continue
    path = {}; cur = s
    while cur in nxt and cur not in seen and cur not in path:
        path[cur] = len(path); cur = nxt[cur]
    if cur in path:
        order = sorted(path, key=path.get); cycles.append(order[path[cur]:])
    for x in path: seen[x] = 1
print("in-box cycles:", len(cycles), "lengths", sorted(len(c) for c in cycles))
for c in cycles[:5]:
    print("   cycle", len(c), [(len(B), len(C)) for B, C in c], "sumgam", sum(mirror.gam(b, list(B), list(C)) for B, C in c))
expected = set()
for c in cycles:
    q = len(c); S = tuple((len(B), len(C)) for B, C in c)
    for p in range(q, PMAX + 1, q): expected.add(P.canon(list(S) * (p // q)))
# all valid schedules
pairs = [(n, m) for n in range(NB + 1) for m in range(MB + 1)]
def gen(p):
    seen = set()
    def rec(seq):
        if len(seq) == p:
            S = tuple(seq)
            if P.derive(S) is not None:
                c = P.canon(list(S))
                if c not in seen: seen.add(c); yield c
            return
        for pr in pairs:
            if seq:
                n, m = seq[-1]; g = (pr[1] - m) % 2
                if pr[0] > n + g or pr[1] > m + g: continue
            yield from rec(seq + [pr])
    yield from rec([])
got = set(); n_inst = 0; nsat_mismatch = 0; tt = 0
for p in range(1, PMAX + 1):
    for S in gen(p):
        r = P.solve(b, S, backend=backend, maximal=True, time_limit=60); n_inst += 1; tt += r['time']
        if r['status'] == 'SAT':
            assert r['certificate']['cycleOK_mirror'], S
            got.add(S)
        elif r['status'] != 'UNSAT': print("UNKNOWN", S)
    print(f"  p={p}: cumulative instances {n_inst}, SAT {len(got)}, solver time {tt:.1f}s", flush=True)
print("expected SAT schedules:", len(expected), " solver SAT schedules:", len(got))
print("missing (brute force has cycle, solver UNSAT):", sorted(expected - got)[:5])
print("extra   (solver SAT, no brute-force cycle)   :", sorted(got - expected)[:5])
print("MATCH" if got == expected else "MISMATCH")
