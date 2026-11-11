#!/usr/bin/env python3
"""symcheck.py (r14a): confirm on small K that the symmetry group R (t+2), C (complement), S (column shift) acts as predicted.
For each class id given: for every member file and every orbit, compute (E_acc(K,T), accepting, parents, exact) for K <= Ks with bin_mc14a run;
map (file W', orbit o') to the representative's orbit via Phi and compare the vectors exactly."""
import sys, os, json, subprocess, time
sys.path.insert(0, 'src')
from classes2 import read_lat, orbits
Ks = int(os.environ.get('SYM_K', '11'))
ids = [int(x) for x in sys.argv[1:]]
t = json.load(open('class/classes.json'))
def veccounts(fn, o):
    out = subprocess.run(['./bin_mc14a', 'run', fn, str(o), str(Ks), '1', '1'], capture_output=True, text=True, timeout=7200).stdout
    v = []
    for ln in out.splitlines():
        if ln.startswith('K '):
            tok = ln.split()
            v.append((int(tok[1]), int(tok[3]), int(tok[5]), int(tok[7]), int(tok[9])))
    return v
def main():
    for cid in ids:
        rec = t[cid]
        rep = rec['rep']
        base, tp, nB, m, clk, B, W = read_lat(rep)
        orbs, orb_of = orbits(m, clk)
        repvec = {o: veccounts(rep, o) for o in range(len(orbs))}
        # check orbit-classes of the representative
        for oc in rec['orbit_classes']:
            for o in oc[1:]:
                ok = repvec[o] == repvec[oc[0]]
                print(f'class {cid} rep orbits {oc[0]} vs {o}: {"OK" if ok else "MISMATCH"}', flush=True)
        for fn in rec['members']:
            if fn == rep: continue
            b2, tp2, nB2, m2, clk2, B2, W2 = read_lat(fn)
            found = False
            for r in range(4):
                for c in range(2):
                    for sigma in range(m):
                        good = all((W[(tt + 2*r) % 8][(x + sigma) % m] if c == 0 else 18 - W[(tt + 2*r) % 8][(x + sigma) % m]) == W2[tt][x]
                                   for tt in range(8) for x in range(m))
                        if good:
                            found = True
                            for o2, ph in enumerate(orbits(m2, clk2)[0]):
                                tt, j, par = ph[0]
                                o = orb_of[((tt + 2*r) % 8, (j + sigma) % m, par)]
                                v2 = veccounts(fn, o2)
                                ok = (v2 == repvec[o])
                                print(f'class {cid} {os.path.basename(fn)} orbit {o2} ~ rep orbit {o} (r={r},c={c},sigma={sigma}): {"OK" if ok else "MISMATCH"} last={v2[-1] if v2 else None}', flush=True)
                            break
                    if found: break
                if found: break
            if not found:
                print(f'class {cid} {fn}: no element found', flush=True)
    print('symcheck done', flush=True)
main()
