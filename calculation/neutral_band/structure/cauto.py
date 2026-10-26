"""Exact layer-automaton for the C-system (symmetric centre block) under a periodic driver stream.
Scans C layers j=0,1,.. from the OUTER end inward (layer j = the symmetric pair of positions j and m_t-1-j).
Inputs: b, e (carry-in bit per step), g (gam per step), m0 (length of C_0), v (trim per step, 0/1).  Finds all (C_0..C_{P-1}) with
C_P = C_0 (cycle), carry(C_t, e_t) = 1-e_t at each step, C_{t+1} = trim_v(pairsum(DC_t [+ y])).
State between layers: l_t (carry into left position j), r_t (carry out of right position m-1-j), Rd_t (previous right digit, g_t=1 steps),
Z_t (guess for c_{t+1}[j] at v_t=1 steps, verified one layer later: c_{t+1}[j] = c'_t[j+1])."""
import sys, itertools

def lengths(g, v, m0):
    P = len(g); m = [m0]
    for t in range(P): m.append(m[-1] + g[t] - 2*v[t])
    if m[P] != m0 or min(m) < 1: return None
    return m[:P]

def solve(b, e, g, m0, v, want_all=False, maxsol=1, cap=2_000_000):
    P = len(e); m = lengths(g, v, m0)
    if m is None: return None
    J = [(m[t]+1)//2 for t in range(P)]
    Jp = [(m[t]+g[t]+1)//2 for t in range(P)]
    Vs = [t for t in range(P) if v[t] == 1]
    assert Vs, "need at least one trim step"
    Jall = max(Jp)
    yd = [(b-1)*e[t] for t in range(P)]
    nxt = lambda t: (t+1) % P
    prv = lambda t: (t-1) % P
    # initial state
    l0 = tuple(e); r0 = tuple(1-x for x in e)
    Rd0 = tuple(yd[t] if g[t] else -1 for t in range(P))
    Z0 = tuple(-1 for t in range(P))
    start = (l0, r0, Rd0, Z0)
    # segment order: start at s with v[s-1]==1
    starts = [nxt(t) for t in Vs]
    order = []
    for s in starts:
        seg = [s]; t = s
        while v[t] == 0: t = nxt(t); seg.append(t)
        order.append(seg)
    frontier = {start: None}; layers = []   # per layer: dict state -> (parent, cols)
    for j in range(Jall):
        new = {}
        for S, _ in frontier.items():
            l, r, Rd, Z = S
            # DFS over segments
            def seg_rec(si, nl, nr, nRd, nZ, cols):
                if si == len(order):
                    st = (tuple(nl), tuple(nr), tuple(nRd), tuple(nZ))
                    if st not in new: new[st] = (S, tuple(cols))
                    return
                seg = order[si]
                s = seg[0]
                # starting coefficient: guess Z if c_s[j] exists, else none
                if j < J[s]:
                    cand = range(2*b-1)
                else:
                    cand = [None]
                for c0 in cand:
                    # process the segment sequentially (with branching on right guesses)
                    def tstep(k, c, nl, nr, nRd, nZ, cols, ok_cb):
                        pass
                    rec_seg(si, 0, c0, list(nl), list(nr), list(nRd), list(nZ), list(cols))
            def rec_seg(si, k, c, nl, nr, nRd, nZ, cols):
                seg = order[si]; t = seg[k]
                # c is c_t[j] (None if time t not active at this layer)
                cprime = None
                branches = []
                if j < J[t]:
                    # active
                    lin = l[t]; sm = c + lin; Ld = sm % b; lout = sm // b
                    rreq = r[t]
                    centre_odd = (m[t] % 2 == 1 and j == J[t]-1)
                    last_even = (m[t] % 2 == 0 and j == J[t]-1)
                    if centre_odd:
                        if lout != rreq: return
                        Rdj = Ld; rins = [None]
                    elif last_even:
                        rin = lout
                        if (c + rin)//b != rreq: return
                        Rdj = (c + rin) % b; rins = [rin]
                    else:
                        rins = [x for x in (0, 1) if (c + x)//b == rreq]
                        Rdj = None
                    for rin in rins:
                        if rin is None: Rd_j = Rdj
                        elif Rdj is not None: Rd_j = Rdj
                        else: Rd_j = (c + rin) % b
                        # c'_t[j]
                        if g[t] == 0:
                            cp = 2*Ld if centre_odd else Ld + Rd_j
                        else:
                            leftpart = Ld   # j <= (m-1)/2 holds for active layers
                            rightpart = yd[t] if j == 0 else Rd[t]
                            cp = leftpart + rightpart
                        branches.append((rin, Rd_j, lout, cp))
                else:
                    # inactive; virtual layer for g=1 and even m
                    if j < Jp[t]:
                        assert g[t] == 1 and m[t] % 2 == 0 and j == J[t]
                        branches.append((None, None, None, 2*Rd[t]))
                    else:
                        branches.append((None, None, None, None))
                for rin, Rd_j, lout, cp in branches:
                    nl2, nr2, nRd2, nZ2, cols2 = nl, nr, nRd, nZ, cols
                    nl2 = list(nl); nr2 = list(nr); nRd2 = list(nRd); nZ2 = list(nZ)
                    cols2 = list(cols)
                    if j < J[t]:
                        nl2[t] = lout
                        if rin is not None: nr2[t] = rin
                        if g[t]: nRd2[t] = Rd_j
                        cols2.append((t, c))
                    # after time t: set c_{t+1}[j] or verify
                    if v[t] == 0:
                        if cp is not None:
                            # c_{t+1}[j] = cp; must be <= 2b-2
                            if cp > 2*b-2: continue
                            # next time in segment
                            rec_seg(si, k+1, cp, nl2, nr2, nRd2, nZ2, cols2)
                        else:
                            rec_seg(si, k+1, None, nl2, nr2, nRd2, nZ2, cols2)
                    else:
                        # verification of previous guess / trim
                        if cp is not None:
                            if j == 0:
                                if cp != b-1: continue
                            else:
                                if Z[t] != cp: continue
                        else:
                            if j > 0 and Z[t] != -1: continue
                        # new guess for c_{t+1}[j] is the segment start of the next segment: store c0 of next segment
                        # (the guess value is the first element of the next segment's c); record in nZ2 at index t
                        nxt_seg = (si+1) % len(order)
                        nZ2[t] = guess_of[nxt_seg]
                        seg_done(si, nl2, nr2, nRd2, nZ2, cols2)
            def seg_done(si, nl, nr, nRd, nZ, cols):
                seg_rec(si+1, nl, nr, nRd, nZ, cols)
            # the guess values: chosen jointly. To keep this simple choose all guesses first
            guess_of = {}
            ranges = [range(2*b-1) if j < J[order[si][0]] else [None] for si in range(len(order))]
            for combo in itertools.product(*ranges):
                for si, c0 in enumerate(combo): guess_of[si] = c0
                def run_all(si, nl, nr, nRd, nZ, cols):
                    if si == len(order):
                        # verify last segment's end guess consistency: handled; store
                        st = (tuple(nl), tuple(nr), tuple(nRd), tuple(nZ))
                        if st not in new: new[st] = (S, tuple(cols))
                        return
                    rec_seg_wrap(si, nl, nr, nRd, nZ, cols)
                # re-bind seg_rec continuation
                def seg_rec_cont(si, nl, nr, nRd, nZ, cols):
                    run_all(si, nl, nr, nRd, nZ, cols)
                def rec_seg_wrap(si, nl, nr, nRd, nZ, cols):
                    rec_seg_k(si, 0, guess_of[si], nl, nr, nRd, nZ, cols)
                def rec_seg_k(si, k, c, nl, nr, nRd, nZ, cols):
                    seg = order[si]; t = seg[k]
                    branches = []
                    if j < J[t]:
                        lin = l[t]; sm = c + lin; Ld = sm % b; lout = sm // b
                        rreq = r[t]
                        centre_odd = (m[t] % 2 == 1 and j == J[t]-1)
                        last_even = (m[t] % 2 == 0 and j == J[t]-1)
                        if centre_odd:
                            if lout != rreq: continue_flag = True
                            else:
                                branches.append((None, Ld, lout, 2*Ld if g[t]==0 else Ld + (yd[t] if j == 0 else Rd[t])))
                        elif last_even:
                            rin = lout
                            if (c + rin)//b == rreq:
                                Rj = (c + rin) % b
                                cp = (Ld + Rj) if g[t]==0 else (Ld + (yd[t] if j == 0 else Rd[t]))
                                branches.append((rin, Rj, lout, cp))
                        else:
                            for rin in (0, 1):
                                if (c + rin)//b == rreq:
                                    Rj = (c + rin) % b
                                    cp = (Ld + Rj) if g[t]==0 else (Ld + (yd[t] if j == 0 else Rd[t]))
                                    branches.append((rin, Rj, lout, cp))
                    else:
                        if j < Jp[t]:
                            branches.append((None, None, None, 2*Rd[t]))
                        else:
                            branches.append((None, None, None, None))
                    for rin, Rj, lout, cp in branches:
                        nl2 = list(nl); nr2 = list(nr); nRd2 = list(nRd); nZ2 = list(nZ); cols2 = list(cols)
                        if j < J[t]:
                            nl2[t] = lout
                            if rin is not None: nr2[t] = rin
                            if g[t]: nRd2[t] = Rj
                            cols2.append((t, c))
                        if v[t] == 0:
                            if cp is not None and cp > 2*b-2: continue
                            if k+1 < len(seg):
                                rec_seg_k(si, k+1, cp, nl2, nr2, nRd2, nZ2, cols2)
                            else:
                                run_all(si+1, nl2, nr2, nRd2, nZ2, cols2)
                        else:
                            if cp is not None:
                                if j == 0:
                                    if cp != b-1: continue
                                else:
                                    if Z[t] != cp: continue
                            else:
                                if j > 0 and Z[t] != -1: continue
                            nxtsi = (si+1) % len(order)
                            nZ2[t] = guess_of[nxtsi] if guess_of[nxtsi] is not None else -1
                            run_all(si+1, nl2, nr2, nRd2, nZ2, cols2)
                run_all(0, list(l), list(r), list(Rd), [-1]*P, [])
                if len(new) > cap: return ('cap', len(new))
        layers.append(new); frontier = new
        if not new: return None
    # all layers done: any state in frontier is an accepting solution (all pending verified by construction)
    return layers

def reconstruct(layers, b, P, m, J):
    """return list of C_t arrays for the first solution"""
    # walk back from any final state
    S = next(iter(layers[-1]))
    cols = []
    for j in range(len(layers)-1, -1, -1):
        par, cc = layers[j][S]; cols.append(cc); S = par
    cols.reverse()
    C = [[None]*J[t] for t in range(P)]
    for j, cc in enumerate(cols):
        for (t, c) in cc:
            if c is not None: C[t][j] = c
    out = []
    for t in range(P):
        half = C[t]; mm = m[t]
        arr = [None]*mm
        for j in range(J[t]):
            arr[j] = half[j]; arr[mm-1-j] = half[j]
        out.append(arr)
    return out

if __name__ == "__main__":
    b = int(sys.argv[1]); e = [int(x) for x in sys.argv[2]]; g = [int(x) for x in sys.argv[3]]
    m0 = int(sys.argv[4]); v = [int(x) for x in sys.argv[5]]
    res = solve(b, e, g, m0, v)
    if res is None: print("INFEASIBLE or bad lengths")
    elif isinstance(res, tuple): print(res)
    else:
        P = len(e); m = lengths(g, v, m0); J = [(x+1)//2 for x in m]
        print("FEASIBLE", reconstruct(res, b, P, m, J), "states per layer", [len(x) for x in res])
