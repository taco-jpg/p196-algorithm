# Faithful Python model of the reach cell rule (reach.cpp: dfs/expand/accepts) and of the Agent120 exterior map
# (calculation/neutral_band_search.py nextB with a centre C realising e2 = 1 - e1, then maximal trimming of b-1).
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
import neutral_band_search as m

def phi(b, B):
    """Agent120 exterior map via the repo mirror itself: returns (trim(nextB), e1, gam)."""
    B = list(B); e1 = m.e1(b, B)
    C = [2 * b - 2] if e1 == 0 else [0]              # e2(B,C) = 1 - e1
    assert m.e2(b, B, C) == 1 - e1 and m.hyp(b, B, C)
    nb = m.nextB(b, B, C)
    while nb and nb[-1] == b - 1: nb = nb[:-1]
    return tuple(nb), e1, m.gam(b, B, C)

def trim(b, v):
    v = list(v)
    while v and v[-1] == b - 1: v.pop()
    return tuple(v)

def pad(b, B, H): return tuple(B) + (b - 1,) * (H - len(B))

# ---- one time step of the reach rule on a column (cells 0..H-1), as in reach.cpp dfs at a fixed t ----
def reach_step(b, v, g):
    """all branches (vnext, c_H, d_H, r_{H-1}) of the reach cell rule for one time step, bottom interface
    (c=0, d=g, r=1), cell by cell; d of each cell chosen as in reach (0/1 with (x+d)//b == dneed)."""
    out = []
    def rec(x, cin, dneed, rbelow, acc):
        if x == len(v): out.append((tuple(acc), cin, dneed, rbelow)); return
        val = v[x]
        for d in (0, 1):
            if (val + d) // b != dneed: continue
            e = (val + cin) % b; r = (val + d) % b; co = (val + cin) // b
            nx = e + rbelow if g else e + r
            rec(x + 1, co, d, r, acc + [nx])
    rec(0, 0, g, 1, [])
    return out

def wire_ok(b, g, c, d, r):   # reach.cpp accepts() in WIRE mode, one time step
    return d == 1 - c and (not g or r == (b - 1) * c)

def band_ok(b, g, c, d, r, BC, BR):  # reach.cpp accepts() in BAND mode, one time step
    return c == BC and d == BC and (not g or r == BR)

# ---- periodic interface graph (reach.cpp expand), with history multiplicities ----
def expand(b, T, ovf, node, root):
    """yield (successor node, cell series) for interface node=(c,d,r) (tuples over t; r only meaningful at ovf)."""
    c0, d0, r0 = node
    res = []
    def dfs(t, x, x0, cs, ds, rs, xs):
        if t == T:
            if x == x0: res.append(((tuple(cs), tuple(ds), tuple(rs)), tuple(xs)))
            return
        if root and x == 0: return
        if x < 0 or x > 2 * b - 2: return
        cin, dneed = c0[t], d0[t]
        for d in (0, 1):
            if (x + d) // b != dneed: continue
            e = (x + cin) % b; r = (x + d) % b; co = (x + cin) // b
            nx = e + r0[t] if ovf[t] else e + r
            dfs(t + 1, nx, x0, cs + [co], ds + [d], rs + [r if ovf[t] else 0], xs + [x])
    for x0 in range(1 if root else 0, 2 * b - 1):
        dfs(0, x0, x0, [], [], [], [])
    return res

def root_node(T, ovf): return (tuple([0] * T), tuple(ovf), tuple(1 if o else 0 for o in ovf))

def wire_accept(b, T, ovf, node):
    c, d, r = node
    return all(d[t] == 1 - c[t] for t in range(T)) and all(r[t] == (b - 1) * c[t] for t in range(T) if ovf[t])
