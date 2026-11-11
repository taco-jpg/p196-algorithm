#!/usr/bin/env python3
import os
"""r13b walkcheck.py: soundness test of an E_acc file: for random accepting states s of E_acc(K,T) find an explicit closed T-walk through s
inside the file's state sets (BFS over layers using klib.window_step edges) and replay it with klib.window_step (reference rule).
Reports for each sampled state: found a closed T-walk through it, checked independently: each step (Din, ghost) gives the next window,
all ok flags true, start=end, bottom cell off-lattice at s.
usage: walkcheck.py NAME ORBIT L K FILE [nsamples] [seed]"""
import sys, struct, random, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../lattice_kinks/edge_relaxation'))
from klib import load, window_step
name, oi, LL, K, fn = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
nsamp = int(sys.argv[6]) if len(sys.argv) > 6 else 20; seed = int(sys.argv[7]) if len(sys.argv) > 7 else 1
random.seed(seed)
lat = load(name); P = lat.p; M = lat.m
def nxt(t, j, par):
    g = lat.g[t]; dh = 1 if (g == 1 and par == 0) else 0
    return (t + 1) % P, (j + dh) % M, (par + g) % 2
NPH = 2 * P * M; seen = {}; reps = []
for s in range(NPH):
    if s in seen: continue
    reps.append(s); t, j, par = (s // 2) // M, (s // 2) % M, s % 2; x = s
    while True:
        seen[x] = len(reps) - 1; t, j, par = nxt(t, j, par); x = (t * M + j) * 2 + par
        if x == s: break
s = reps[oi]; Ph = []; t, j, par = (s // 2) // M, (s // 2) % M, s % 2
while True:
    Ph.append((t, j, par)); t, j, par = nxt(t, j, par)
    if (t, j, par) == Ph[0]: break
Lo = len(Ph); T = LL * Lo; base = lat.nB + 5 * lat.m
f = open(fn, 'rb'); lo, W = struct.unpack('ii', f.read(8)); assert lo == Lo
Eset = []
for l in range(Lo):
    n = struct.unpack('Q', f.read(8))[0]; data = f.read(8 * W * n); S = set()
    for i in range(n):
        words = struct.unpack_from('<%dQ' % W, data, 8 * W * i)
        S.add(tuple((words[q // 12] >> (5 * (q % 12))) & 31 for q in range(K)))
    Eset.append(S)
print(f'{name} orbit {oi} K={K} T={T}: |E|={sum(len(s) for s in Eset)}', flush=True)
def succs(l, w):
    t, j, par = Ph[l]; dh = 1 if (lat.g[t] == 1 and par == 0) else 0; c = base + j; n = 100 + par
    res = {}
    for Din in (0, 1):
        for gh in (range(10) if dh else [0]):
            new, ok = window_step(lat, t, c, n, list(w), Din, gh)
            if ok and tuple(new) in Eset[(l + 1) % Lo]: res[tuple(new)] = (Din, gh)
    return res
accepting = [(l, w) for l in range(Lo) for w in Eset[l] if w[0] != lat.cell(Ph[l][0], base + Ph[l][1])]
print(f'accepting states in file: {len(accepting)}', flush=True)
samp = random.sample(accepting, min(nsamp, len(accepting))); okc = 0; t0 = time.time()
for (l0, w0) in samp:
    # BFS over unrolled T layers from (l0,w0)
    frontier = {w0: None}; layers = [frontier]
    for k in range(T):
        l = (l0 + k) % Lo; nf = {}
        for w in layers[k]:
            for v in succs(l, w): 
                if v not in nf: nf[v] = w
        layers.append(nf)
    assert w0 in layers[T], 'closed walk not found (E_acc claims one exists)'
    # reconstruct walk backwards, replay with window_step
    walk = [w0]; cur = w0
    for k in range(T, 0, -1):
        cur = layers[k][cur]; walk.append(cur)
    walk.reverse()
    assert walk[0] == w0 and walk[-1] == w0
    for k in range(T):
        l = (l0 + k) % Lo; t, j, par = Ph[l]; dh = 1 if (lat.g[t] == 1 and par == 0) else 0; c = base + j; n = 100 + par
        found = False
        for Din in (0, 1):
            for gh in (range(10) if dh else [0]):
                new, ok = window_step(lat, t, c, n, list(walk[k]), Din, gh)
                if ok and tuple(new) == walk[k + 1]: found = True
        assert found, 'edge not valid'
    assert w0[0] != lat.cell(Ph[l0][0], base + Ph[l0][1])
    okc += 1
    print(f'  sample {okc}: layer {l0} closed {T}-walk through accepting state found and replayed with window_step: OK', flush=True)
print(f'walkcheck: {okc}/{len(samp)} OK, {time.time()-t0:.0f}s')
