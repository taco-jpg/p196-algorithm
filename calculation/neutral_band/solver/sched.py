import os
#!/usr/bin/env python3
"""Schedule enumerator for the sweep.  A schedule is a cyclic sequence of (n_k,m_k); see p196cp.derive.
Parametrised by shape = (gam_k, u_k, v_k) with sum(u)=sum(gam)=G, sum(v)=G/2, plus the offsets (n_0,m_0)."""
import itertools, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p196cp as P

def weak_compositions(total, parts):
    if parts == 1: yield (total,); return
    for i in range(total + 1):
        for rest in weak_compositions(total - i, parts - 1): yield (i,) + rest

def shapes(p, G):
    """canonical (up to rotation) shapes with exactly G overflow steps (G even)"""
    seen = set()
    for pos in itertools.combinations(range(p), G):
        gam = tuple(1 if k in pos else 0 for k in range(p))
        for u in weak_compositions(G, p):
            for v in weak_compositions(G // 2, p):
                sh = tuple(zip(gam, u, v))
                c = min(sh[i:] + sh[:i] for i in range(p))
                if c in seen: continue
                seen.add(c); yield c

def realize(sh, NMAX, MMAX, NMIN=0, MMIN=0):
    """all (n_0,m_0) such that all lengths lie in [NMIN,NMAX] x [MMIN,MMAX]; yields length schedules"""
    p = len(sh); pn = [0]; pm = [0]
    for (g, u, v) in sh[:-1]:
        pn.append(pn[-1] + g - u); pm.append(pm[-1] + g - 2 * v)
    lo_n = max(NMIN - x for x in pn); hi_n = min(NMAX - x for x in pn)
    lo_m = max(MMIN - x for x in pm); hi_m = min(MMAX - x for x in pm)
    for n0 in range(lo_n, hi_n + 1):
        for m0 in range(lo_m, hi_m + 1):
            yield tuple((n0 + pn[k], m0 + pm[k]) for k in range(p))

COVERED_B, COVERED_C = 3, 6   # base 10: every start with |B|<=3 and palindromic |C|<=6 breaks (RESULTS.md, 99,296,982 starts)
def covered(S, base=10):
    """a cycle containing a state inside the exhaustively refuted box cannot exist (base 10 only)"""
    return base == 10 and any(n <= COVERED_B and m <= COVERED_C for n, m in S)

def schedules(p, G, NMAX, MMAX, NMIN=0, MMIN=0, base=10, skip_covered=True):
    seen = set()
    for sh in shapes(p, G):
        for S in realize(sh, NMAX, MMAX, NMIN, MMIN):
            c = P.canon(list(S))
            if c in seen: continue
            seen.add(c)
            if skip_covered and covered(c, base): continue
            yield c

if __name__ == "__main__":
    NM, MM = int(sys.argv[1]), int(sys.argv[2])
    for G in (2, 4):
        for p in range(2, 13):
            if G == 4 and p > 8: break
            n = sum(1 for _ in schedules(p, G, NM, MM))
            print(f"G={G} p={p}: {n} schedules (n<={NM}, m<={MM}, covered box removed)", flush=True)
