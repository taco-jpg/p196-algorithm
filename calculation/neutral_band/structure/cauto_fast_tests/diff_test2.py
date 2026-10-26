#!/usr/bin/env python3
"""Differential test with FAST witnesses: old vs cauto_fast on random streams. Lines are compared with the witness part stripped;
every witness printed by cauto_fast is re-verified with an independent python implementation of the C step."""
import random, subprocess, sys, time, re
sys.path.insert(0, 'tests')
old, new, seed, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); tl = float(sys.argv[5])
random.seed(seed)
def cstep(b, C, e1, g, v):
    m = len(C); c = e1; DC = []
    for x in C: DC.append((x + c) % b); c = (x + c) // b
    if c != 1 - e1: return None
    yd = (b - 1) * e1
    if g == 0: cp = [DC[k] + DC[m - 1 - k] for k in range(m)]
    else:
        W = DC + [yd]; cp = [W[k] + W[m - k] for k in range(m + 1)]
    nn = len(cp)
    if v:
        if nn - 2 * v < 1: return None
        if any(x != b - 1 for x in cp[:v]) or any(x != b - 1 for x in cp[nn - v:]): return None
        cp = cp[v:nn - v]
    return cp
def valid(line):
    mt = re.match(r"FEASIBLE(?:_CLASS)? b=(\d+) e=(\d+) g=(\d+) v=(\d+) m0=(\d+)", line)
    b = int(mt[1]); e = [int(x) for x in mt[2]]; g = [int(x) for x in mt[3]]; v = [int(x) for x in mt[4]]
    Cs = [[int(x) for x in m.split(',')] for m in re.findall(r" C\d+=\[([^\]]*)\]", line)]
    P = len(e)
    if len(Cs) != P: return False
    for t in range(P):
        if Cs[t] != Cs[t][::-1] or any(not (0 <= x <= 2 * b - 2) for x in Cs[t]): return False
        if cstep(b, Cs[t], e[t], g[t], v[t]) != Cs[(t + 1) % P]: return False
    return True
def run(exe, b, e, g):
    r = subprocess.run([exe, str(b), e, g, '1', '1', '-vall', '-allm', '-w', '-cap', '3000000'], capture_output=True, text=True, timeout=60)
    return [l for l in r.stdout.splitlines() if not l.startswith('DONE')], [l for l in r.stderr.splitlines() if l.startswith('allm ')]
strip = lambda l: re.sub(r" C\d+=\[[^\]]*\]", "", l)
t0 = time.time(); tested = bad = feas = badw = 0
while tested < n and time.time() - t0 < tl:
    b = random.choice([2, 3, 4, 5, 7, 10]); P = random.choice([3, 4, 5, 6, 7, 8])
    g = [random.randint(0, 1) for _ in range(P)]; G = sum(g)
    if G == 0 or G % 2 or G // 2 > 3: continue
    e = [random.randint(0, 1) for _ in range(P)]; es, gs = ''.join(map(str, e)), ''.join(map(str, g))
    try: o1, e1 = run(old, b, es, gs); o2, e2 = run(new, b, es, gs)
    except subprocess.TimeoutExpired: continue
    tested += 1; feas += sum(l.startswith('FEASIBLE') for l in o1)
    if [strip(l) for l in o1] != [strip(l) for l in o2] or e1 != e2: bad += 1; print("MISMATCH", b, es, gs)
    for l in o2:
        if l.startswith('FEASIBLE') and not valid(l): badw += 1; print("BAD WITNESS", l[:100])
print(f"streams {tested}, FEASIBLE lines {feas}, mismatches {bad}, invalid witnesses {badw}")
