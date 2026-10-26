"""Exact layer-automaton for the C-system (cleaned version of cauto.py).  See cauto.py for the model.
solve(b,e,g,m0,v) -> list of per-layer frontier dicts or None (infeasible).  v entries in {0,1}.
Additions: time limit / state cap, shared structure for reuse."""
import sys, itertools, time

def lengths(g, v, m0):
    P = len(g); m = [m0]
    for t in range(P): m.append(m[-1] + g[t] - 2*v[t])
    if m[P] != m0 or min(m) < 1: return None
    return m[:P]

def solve(b, e, g, m0, v, cap=3_000_000, tl=1e9):
    t0 = time.time()
    P = len(e); m = lengths(g, v, m0)
    if m is None: return None
    J = [(m[t]+1)//2 for t in range(P)]
    Jp = [(m[t]+g[t]+1)//2 for t in range(P)]
    Vs = [t for t in range(P) if v[t] == 1]
    assert Vs
    Jall = max(Jp)
    yd = [(b-1)*e[t] for t in range(P)]
    nx = lambda t: (t+1) % P
    order = []
    for t in Vs:
        s = nx(t); seg = [s]; u = s
        while v[u] == 0: u = nx(u); seg.append(u)
        order.append(seg)
    nseg = len(order)
    start = (tuple(e), tuple(1-x for x in e), tuple(yd[t] if g[t] else -1 for t in range(P)), tuple([-1]*P))
    frontier = {start: None}; layers = []
    for j in range(Jall):
        new = {}
        # guess ranges for segment starts
        ranges = [range(2*b-1) if j < J[order[si][0]] else (None,) for si in range(nseg)]
        for S in frontier:
            l, r, Rd, Z = S
            for guess in itertools.product(*ranges):
                # DFS state: lists
                def walk(si, k, c, nl, nr, nRd, nZ, cols):
                    # process time t = order[si][k] with coefficient c (None if inactive)
                    seg = order[si]; t = seg[k]
                    outs = []
                    if j < J[t]:
                        lin = l[t]; sm = c + lin; Ld = sm % b; lout = sm // b; rreq = r[t]
                        if j == 0: rp = yd[t]
                        else: rp = Rd[t]
                        if m[t] % 2 == 1 and j == J[t]-1:      # centre
                            if lout != rreq: return
                            cp = 2*Ld if g[t] == 0 else Ld + rp
                            outs.append((None, Ld, lout, cp))
                        elif m[t] % 2 == 0 and j == J[t]-1:    # last pair, adjacent positions
                            rin = lout
                            if (c + rin)//b != rreq: return
                            Rj = (c + rin) % b
                            cp = Ld + Rj if g[t] == 0 else Ld + rp
                            outs.append((rin, Rj, lout, cp))
                        else:
                            for rin in (0, 1):
                                if (c + rin)//b == rreq:
                                    Rj = (c + rin) % b
                                    cp = Ld + Rj if g[t] == 0 else Ld + rp
                                    outs.append((rin, Rj, lout, cp))
                    else:
                        if j < Jp[t]: outs.append((None, None, None, 2*Rd[t]))
                        else: outs.append((None, None, None, None))
                    for rin, Rj, lout, cp in outs:
                        nl2 = list(nl); nr2 = list(nr); nRd2 = list(nRd); nZ2 = list(nZ); cols2 = cols
                        if j < J[t]:
                            nl2[t] = lout
                            if rin is not None: nr2[t] = rin
                            if g[t]: nRd2[t] = Rj
                            cols2 = cols + [(t, c)]
                        if v[t] == 0:
                            if cp is not None and cp > 2*b-2: continue
                            if k+1 < len(seg): walk(si, k+1, cp, nl2, nr2, nRd2, nZ2, cols2)
                            else: nextseg(si+1, nl2, nr2, nRd2, nZ2, cols2)
                        else:
                            if cp is not None:
                                if j == 0:
                                    if cp != b-1: continue
                                elif Z[t] != cp: continue
                            else:
                                if j > 0 and Z[t] != -1: continue
                            gv = guess[(si+1) % nseg]
                            nZ2[t] = gv if gv is not None else -1
                            nextseg(si+1, nl2, nr2, nRd2, nZ2, cols2)
                def nextseg(si, nl, nr, nRd, nZ, cols):
                    if si == nseg:
                        st = (tuple(nl), tuple(nr), tuple(nRd), tuple(nZ))
                        if st not in new: new[st] = (S, tuple(cols))
                        return
                    walk(si, 0, guess[si], nl, nr, nRd, nZ, cols)
                nextseg(0, list(l), list(r), list(Rd), [-1]*P, [])
            if len(new) > cap or time.time() - t0 > tl: return ('cap', j, len(new))
        layers.append(new); frontier = new
        if not new: return None
    return layers

def reconstruct(layers, b, P, m):
    J = [(x+1)//2 for x in m]
    S = next(iter(layers[-1])); cols = []
    for j in range(len(layers)-1, -1, -1):
        par, cc = layers[j][S]; cols.append(cc); S = par
    cols.reverse()
    C = [[None]*J[t] for t in range(P)]
    for j, cc in enumerate(cols):
        for (t, c) in cc:
            if c is not None: C[t][j] = c
    out = []
    for t in range(P):
        mm = m[t]; arr = [None]*mm
        for j in range(J[t]): arr[j] = C[t][j]; arr[mm-1-j] = C[t][j]
        out.append(arr)
    return out

if __name__ == "__main__":
    b = int(sys.argv[1]); e = [int(x) for x in sys.argv[2]]; g = [int(x) for x in sys.argv[3]]
    m0 = int(sys.argv[4]); v = [int(x) for x in sys.argv[5]]
    res = solve(b, e, g, m0, v)
    if res is None: print("INFEASIBLE")
    elif isinstance(res, tuple): print(res)
    else:
        P = len(e); m = lengths(g, v, m0)
        print("FEASIBLE", reconstruct(res, b, P, m), "states per layer", [len(x) for x in res])
