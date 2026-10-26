"""Exact position-automaton for B-cycles of the autonomous B-system (all lengths n at once).
usage: python3 bauto.py b g           g = gam pattern string e.g. 01 (period p=len(g))
Scans B positions k=0,1,2,... ; cut state = (L,H,Y):
   L[t] = carry into position k (from below) at time t           (determined)
   H[t] = carry position k must pass down to position k-1        (required)
   Y[t] = digit (x_t[k-1]+h_{t,k-1}) mod b, only for t with g_t=1 (partner digit of the gam-shift)
Accept when L[t]+H[t]=1 for all t and Y[t]=(b-1)*L[t]  (steady neutral band above).
Prints shortest witness (B_0..B_{p-1}) and the set of accepted e-streams (e_t = L[t] at acceptance)."""
import sys, itertools
from collections import deque

def run(b, g, want_all=True, maxn=200):
    p = len(g); G = [t for t in range(p) if g[t] == '1']
    start = (tuple([0]*p), tuple(int(c) for c in g), tuple([1]*len(G)))
    def acc(s):
        L, H, Y = s
        return all(L[t] + H[t] == 1 for t in range(p)) and all(Y[i] == (b-1)*L[G[i]] for i in range(len(G)))
    par = {start: None}; dq = deque([(start, 0)]); accepted = {}; first = {}
    Hguess = list(itertools.product((0, 1), repeat=p))
    while dq:
        s, d = dq.popleft()
        if acc(s):
            e = s[0]
            if e not in accepted: accepted[e] = (s, d)
            # do not expand beyond accepting steady states? (they may also continue with nonneutral positions) -> continue expanding
        if d >= maxn: continue
        L, H, Y = s
        for x0 in range(2*b-1):
            for Hn in Hguess:
                xs = [x0]; ok = True; x = x0
                for t in range(p):
                    # consistency of the required down-carry
                    if (x + Hn[t]) // b != H[t]: ok = False; break
                    nxt = (x + L[t]) % b + (Y[G.index(t)] if g[t] == '1' else (x + Hn[t]) % b)
                    xs.append(nxt); x = nxt
                if not ok or xs[p] != x0: continue
                if x0 == 0 or any(xs[t] == 0 for t in range(p)) and False: pass
                if xs[0] == 0 and d == 0: continue      # B_0 coefficient must be nonzero: only matters at position 0
                if d == 0 and any(v == 0 for v in xs[:p]): continue
                L2 = tuple((xs[t] + L[t]) // b for t in range(p))
                Y2 = tuple((xs[t] + Hn[t]) % b for t in G)
                ns = (L2, Hn, Y2)
                if ns not in par:
                    par[ns] = (s, tuple(xs[:p])); dq.append((ns, d + 1))
    return par, accepted

def witness(par, s):
    cols = []
    while par[s] is not None:
        s, xs = par[s]; cols.append(xs)
    cols.reverse()
    p = len(cols[0]) if cols else 0
    return [[cols[k][t] for k in range(len(cols))] for t in range(p)]

if __name__ == "__main__":
    b = int(sys.argv[1]); g = sys.argv[2]
    par, acc = run(b, g)
    print(f"base {b} g={g}: states {len(par)}, accepted e-streams: {sorted(''.join(map(str,e)) for e in acc)}")
    for e, (s, d) in sorted(acc.items()):
        W = witness(par, s)
        # strip trailing b-1
        W2 = []
        for row in W:
            r = list(row)
            while r and r[-1] == b-1: r.pop()
            W2.append(r)
        print("  e", ''.join(map(str, e)), "n=", d, "B_t:", W2)
