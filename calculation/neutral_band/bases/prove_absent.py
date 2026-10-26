import os
#!/usr/bin/env python3
"""For base b and each p in [plo, phi]: run the exhaustive BFS for every overflow word s in {0,1}^p (up to rotation).
Report: number of words whose BFS dies (=> NO exterior of period p with that word, for ANY length L), words whose BFS
survives to Lmax (undecided / candidate), and exteriors found. usage: prove_absent.py b plo phi Lmax"""
import sys, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ext_transfer import cell_transitions
b, plo, phi, Lmax = map(int, sys.argv[1:5])
for p in range(plo, phi + 1):
    t0 = time.time(); died = 0; alive = []; found = 0; words = 0; maxsz = 0
    for s in itertools.product((0, 1), repeat=p):
        if not any(s) or s != min(s[i:] + s[:i] for i in range(p)): continue
        words += 1
        shifted = [t for t in range(p) if s[t]]
        layer = {(tuple([0] * p), tuple(s), tuple([1] * len(shifted))): 1}
        dead = False
        for j in range(Lmax):
            nxt = {}
            for st in layer:
                cw, dw, T = st
                for ns, qo in cell_transitions(b, p, s, cw, dw, T, first=(j == 0)):
                    nxt[ns] = 1
            layer = nxt; maxsz = max(maxsz, len(layer))
            if not layer: dead = True; break
        if dead: died += 1
        else: alive.append(''.join(map(str, s)))
    print(f"base {b} p={p}: {words} overflow words; BFS dies for {died} (=> no exterior, any L); survive to L={Lmax}: {len(alive)} {alive[:6]}; "
          f"max layer {maxsz}; {time.time()-t0:.1f}s", flush=True)
