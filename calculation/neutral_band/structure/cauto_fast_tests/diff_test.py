#!/usr/bin/env python3
"""Differential test: old cauto vs cauto_fast on random small streams, -vall -allm -w.
Compares stdout (minus DONE lines) and the stderr 'allm ...' lines byte for byte."""
import random, subprocess, sys, time
old, new = sys.argv[1], sys.argv[2]
NEWX = sys.argv[6:]
seed = int(sys.argv[3]); n = int(sys.argv[4]); tl = float(sys.argv[5]) if len(sys.argv) > 5 else 250
random.seed(seed)
def run(exe, b, e, g, extra=()):
    extra = tuple(extra) + (tuple(NEWX) if exe == new else ())
    r = subprocess.run([exe, str(b), e, g, '1', '1', '-vall', '-allm', '-w', '-cap', '3000000', *extra], capture_output=True, text=True, timeout=60)
    out = [l for l in r.stdout.splitlines() if not l.startswith('DONE')]
    err = [l for l in r.stderr.splitlines() if l.startswith('allm ')]
    return out, err
t0 = time.time(); tested = 0; bad = 0; feas = 0; totpat = 0
while tested < n and time.time() - t0 < tl:
    b = random.choice([2, 3, 4, 5, 6, 10, 11])
    P = random.choice([2, 3, 4, 5, 6, 7, 8])
    g = [random.randint(0, 1) for _ in range(P)]
    G = sum(g)
    if G == 0 or G % 2: continue
    if G // 2 > 4: continue
    e = [random.randint(0, 1) for _ in range(P)]
    es, gs = ''.join(map(str, e)), ''.join(map(str, g))
    if b >= 10 and P > 6: continue
    try:
        o1, e1 = run(old, b, es, gs)
        o2, e2 = run(new, b, es, gs)
    except subprocess.TimeoutExpired:
        print("timeout", b, es, gs); continue
    tested += 1; totpat += len(e1); feas += sum(1 for l in o1 if l.startswith('FEASIBLE'))
    if o1 != o2 or e1 != e2:
        bad += 1; print("MISMATCH", b, es, gs); 
        for x in o1[:3]: print(" old", x[:150])
        for x in o2[:3]: print(" new", x[:150])
print(f"streams tested {tested}, patterns {totpat}, FEASIBLE lines (old) {feas}, mismatches {bad}")
