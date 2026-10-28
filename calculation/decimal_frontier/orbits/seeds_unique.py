#!/usr/bin/env python3
"""unique-orbit Lychrel candidates per base: first K candidates (no palindrome in 300 steps) whose orbits
do not merge (within 60 steps) with an earlier representative."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nbs
def orbit_head(b, n, k):
    out = []; x = n
    for _ in range(k):
        out.append(x); x = nbs.rev_add(b, x)
    return out
def survives(b, n, steps):
    x = n
    for t in range(steps + 1):
        d = nbs.digits(b, x)
        if d == d[::-1]: return False
        x = x + sum(v * b ** k for k, v in enumerate(d[::-1]))
    return True
def unique_candidates(b, K=8, steps=300, nmax=10**8, tlimit=60):
    reps, sets = [], []
    t0 = time.time()
    for n in range(b, nmax):
        if time.time() - t0 > tlimit: break
        if not survives(b, n, steps): continue
        head = orbit_head(b, n, 60)
        hs = set(head)
        if any(hs & s for s in sets): continue
        reps.append(n); sets.append(hs)
        if len(reps) >= K: break
    return reps
if __name__ == '__main__':
    fn = 'data/candidates_unique.json'
    res = json.load(open(fn)) if os.path.exists(fn) else {}
    for b in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        if str(b) in res: continue
        t0 = time.time(); r = unique_candidates(b, K=int(sys.argv[3]), tlimit=float(sys.argv[4]))
        res[str(b)] = r; json.dump(res, open(fn, 'w'))
        print(b, r, round(time.time() - t0, 1), flush=True)
