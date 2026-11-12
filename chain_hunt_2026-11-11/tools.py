from chain import *

def make_frame(B, g, adv):
    """g: clock over P steps; adv: set of times where the frame advances (must be overflow steps)."""
    P = len(g)
    alpha = [1 if t in adv else 0 for t in range(P)]
    for t in range(P):
        assert not (alpha[t] == 1 and g[t] == 0)
    gamma = [g[t] - alpha[t] for t in range(P)]
    phi = [0] * (P + 1)
    for t in range(P):
        phi[t + 1] = phi[t] + alpha[t]
    return Frame(B, alpha, gamma), phi

def actual_d(B, Hs, i, t):
    """actual d of column Hs[i] at time t, Hs a cyclic list of outer-frame nodes (period d)."""
    m = len(Hs)
    H = Hs[i % m]
    if H[3][t] != 2:
        return H[3][t]
    N = Hs[(i + 1) % m]
    s = N[0][t] + N[1][t]
    if s != B - 1:
        return 1 if s >= B else 0
    return actual_d(B, Hs, i + 1, t)

def lattice_cells(B, cyc):
    """cells[i][t] = (a,b,c,d_actual) for a cycle of outer-frame nodes."""
    m = len(cyc); d = len(cyc[0][0])
    return [[(cyc[i][0][t], cyc[i][1][t], cyc[i][2][t], actual_d(B, cyc, i, t)) for t in range(d)] for i in range(m)]

def sheared_node(B, F, phi, cells, j):
    m = len(cells); d = len(cells[0]); P = F.P
    assert P % d == 0
    a = []; b = []; c = []; dd = []
    for t in range(P):
        ca, cb, cc, cd = cells[(j + phi[t]) % m][t % d]
        a.append(ca); b.append(cb); c.append(cc)
        if F.gamma[t] == 0 or ca + cb == B - 1:
            dd.append(cd)
        else:
            dd.append(2)
    return (tuple(a), tuple(b), tuple(c), tuple(dd))

def parity_seq(g, alpha, case):
    """L parity (0 even, 1 odd) at each time for mirror case 'i' or 'ii'; None if inconsistent."""
    P = len(g)
    # find first overflow to anchor
    par = [None] * P
    t0 = None
    for t in range(P):
        if g[t] == 1:
            t0 = t; break
    if t0 is None:
        return None
    # case i: non-advancing overflow goes even->odd ; case ii: non-advancing overflow goes odd->even
    if case == 'i':
        p = 0 if alpha[t0] == 0 else 1
    else:
        p = 1 if alpha[t0] == 0 else 0
    par[t0] = p
    t = t0
    for k in range(P):
        nt = (t + 1) % P
        np_ = par[t] ^ g[t]
        if par[nt] is None:
            par[nt] = np_
        elif par[nt] != np_:
            return None
        t = nt
    # consistency of every overflow with the case
    for t in range(P):
        if g[t] == 1:
            want = (0 if alpha[t] == 0 else 1) if case == 'i' else (1 if alpha[t] == 0 else 0)
            if par[t] != want:
                return None
    return par

def dmatch(x, y):
    return x == 2 or y == 2 or x == y

def mirror_edge(H, Hn, par, case):
    """necessary mirror conditions for columns K=H, K+1=Hn."""
    P = len(par)
    for t in range(P):
        a, b, c, d = H[0][t], H[1][t], H[2][t], H[3][t]
        an, bn, cn, dn = Hn[0][t], Hn[1][t], Hn[2][t], Hn[3][t]
        if case == 'i':
            if par[t] == 0:   # axis between K and K+1
                if not (an == b and bn == a and dmatch(dn, c) and dmatch(d, cn)):
                    return False
            else:             # axis on K+1
                if not (an == bn and dmatch(dn, cn)):
                    return False
        else:
            if par[t] == 1:   # axis on K
                if not (a == b and dmatch(d, c)):
                    return False
            else:             # axis between K and K+1
                if not (an == b and bn == a and dmatch(dn, c) and dmatch(d, cn)):
                    return False
    return True

def find_path(edges, src_set, dst):
    """BFS predecessor path from any node in src_set to dst."""
    from collections import deque
    prev = {s: None for s in src_set}
    dq = deque(src_set)
    while dq:
        v = dq.popleft()
        if v == dst:
            path = []
            while v is not None:
                path.append(v); v = prev[v]
            return path[::-1]
        for w in edges[v] or []:
            if w not in prev:
                prev[w] = v; dq.append(w)
    return None

def digits_to_str(digs):
    return ''.join('0123456789abcdefghijklmnopqrstuvwxyz'[x] for x in digs[::-1])

def build_number(left_cols, band_cols, n, centre_cols, mid=None):
    """columns are (a,b) at t=0; band_cols repeated n times; mid: optional middle digit (odd length)."""
    cols = list(left_cols) + list(band_cols) * n + list(centre_cols)
    low = [c[0] for c in cols]
    high = [c[1] for c in cols][::-1]
    return low + ([mid] if mid is not None else []) + high

def check_template(B, make, n0, Q, P, periods=6, ns=3):
    """make(n) -> digit list. Checks RA^(k*P)(make(n)) == make(n + k*Q) and no palindromes on the way."""
    for n in range(n0, n0 + ns):
        digs = make(n)
        for k in range(1, periods + 1):
            for _ in range(P):
                if is_pal(digs):
                    return False, 'palindrome'
                digs = ra_step(digs, B)
            if digs != make(n + k * Q):
                return False, 'mismatch n=%d k=%d' % (n, k)
    return True, 'ok'
