"""
Folded reverse-and-add: column-history chain search in an arbitrary sheared frame.

Folded picture (digits least significant first, L digits):
  column i has low digit a_i = x_i and high digit b_i = x_{L-1-i}, pair sum s_i = a_i + b_i.
  c_i = carry into position i            (flows inward:  c_{i+1} = [s_i + c_i >= B])
  d_i = carry into position L-1-i        (flows outward: d_{i-1} = [s_i + d_i >= B])
  overflow g = [s_0 + d_0 >= B]
  a_i' = (s_i + c_i) mod B
  b_{i+g}' = (s_i + d_i) mod B           (b_0' = 1 on overflow)

Sheared frame: column index j = i - phi(t), phi(t+1) = phi(t) + alpha(t).
  a_j(t+1) = (s + c)(j + alpha(t), t) mod B
  b_j(t+1) = (s + d)(j - gamma(t), t) mod B,   gamma(t) = g(t) - alpha(t)
Outer frame: alpha = 0, gamma = g.

A node is a P-periodic column history H = (a, b, c, d), tuples of length P.
d[t] == 2 is a wildcard: allowed only when gamma[t] == 1 and s[t] != B-1
(the value does not influence this column and is fixed by the inner neighbour).
"""
import sys
from collections import deque

sys.setrecursionlimit(100000)


class Frame:
    def __init__(self, B, alpha, gamma):
        assert len(alpha) == len(gamma)
        self.B = B
        self.alpha = tuple(alpha)
        self.gamma = tuple(gamma)
        self.P = len(alpha)
        for x, y in zip(alpha, gamma):
            assert x in (0, 1) and y in (0, 1)


def expand(F, H):
    """All inner neighbours H' of H (column j -> column j+1)."""
    B = F.B
    P = F.P
    al = F.alpha
    ga = F.gamma
    a, b, c, d = H
    s = [a[t] + b[t] for t in range(P)]
    cp = [1 if s[t] + c[t] >= B else 0 for t in range(P)]
    out = []
    A = [0] * (P + 1)
    Bv = [0] * (P + 1)
    D = [0] * P
    Bm1 = B - 1

    def dfs(t):
        if t == P:
            if A[P] == A[0] and Bv[P] == Bv[0]:
                out.append((tuple(A[:P]), tuple(Bv[:P]), tuple(cp), tuple(D)))
            return
        sp = A[t] + Bv[t]
        if al[t] == 1 and (sp + cp[t]) % B != a[(t + 1) % P]:
            return
        dt = d[t]
        if dt != 2:
            if sp == Bm1:
                dopts = (dt,)
            else:
                if (1 if sp >= B else 0) != dt:
                    return
                dopts = (0, 1) if ga[t] == 0 else (2,)
        else:
            dopts = (0, 1) if sp == Bm1 else (2,)
        for dp in dopts:
            D[t] = dp
            if ga[t] == 0:
                nb = (sp + dp) % B
            else:
                if dt != 2:
                    actual = dt
                else:
                    actual = dp if sp == Bm1 else (1 if sp >= B else 0)
                nb = (s[t] + actual) % B
            Bv[t + 1] = nb
            if al[t] == 0:
                A[t + 1] = (sp + cp[t]) % B
                dfs(t + 1)
            else:
                for na in range(B):
                    A[t + 1] = na
                    dfs(t + 1)

    # b'[0] is known in advance when gamma[P-1] == 1 and d[P-1] is concrete
    if ga[P - 1] == 1 and d[P - 1] != 2:
        b0s = [(s[P - 1] + d[P - 1]) % B]
    else:
        b0s = range(B)
    for a0 in range(B):
        for b0 in b0s:
            A[0] = a0
            Bv[0] = b0
            dfs(0)
    return out


def root_node(B, g):
    """Virtual column in front of column 0 for overflow clock g (outer frame)."""
    P = len(g)
    z = tuple([0] * P)
    return (z, z, z, tuple(g))


def closure(F, starts, maxnodes=200000, verbose=False):
    seen = {}
    order = []
    edges = []
    dq = deque()
    for H in starts:
        if H not in seen:
            seen[H] = len(order)
            order.append(H)
            edges.append(None)
            dq.append(H)
    while dq:
        H = dq.popleft()
        i = seen[H]
        succ = expand(F, H)
        lst = []
        for S in succ:
            if S not in seen:
                seen[S] = len(order)
                order.append(S)
                edges.append(None)
                dq.append(S)
            lst.append(seen[S])
        edges[i] = lst
        if verbose and i % 200 == 0:
            print("  expanded", i, "known", len(order), file=sys.stderr)
        if len(order) > maxnodes:
            return order, edges, False
    return order, edges, True


def sccs(n, edges):
    """Tarjan, iterative. Returns list of components (lists of node ids)."""
    index = [None] * n
    low = [0] * n
    onst = [False] * n
    st = []
    comps = []
    idx = 0
    for r in range(n):
        if index[r] is not None:
            continue
        work = [(r, 0)]
        while work:
            v, pi = work[-1]
            if pi == 0:
                index[v] = idx
                low[v] = idx
                idx += 1
                st.append(v)
                onst[v] = True
            recurse = False
            es = edges[v] or []
            while pi < len(es):
                w = es[pi]
                pi += 1
                if index[w] is None:
                    work[-1] = (v, pi)
                    work.append((w, 0))
                    recurse = True
                    break
                elif onst[w]:
                    low[v] = min(low[v], index[w])
            if recurse:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = st.pop()
                    onst[w] = False
                    comp.append(w)
                    if w == v:
                        break
                comps.append(comp)
    return comps


def live_nodes(n, edges):
    """Nodes from which an infinite walk exists (can reach a cycle)."""
    comps = sccs(n, edges)
    comp_of = [0] * n
    for k, cmp_ in enumerate(comps):
        for v in cmp_:
            comp_of[v] = k
    cyc = [False] * len(comps)
    for k, cmp_ in enumerate(comps):
        if len(cmp_) > 1:
            cyc[k] = True
        else:
            v = cmp_[0]
            if v in (edges[v] or []):
                cyc[k] = True
    # Tarjan emits components in reverse topological order: successors first
    live = [False] * len(comps)
    for k, cmp_ in enumerate(comps):
        if cyc[k]:
            live[k] = True
            continue
        for v in cmp_:
            for w in edges[v] or []:
                if live[comp_of[w]]:
                    live[k] = True
    return [live[comp_of[v]] for v in range(n)], comps, cyc


def psums(H):
    a, b, c, d = H
    return tuple(x + y for x, y in zip(a, b))


def ra_step(digs, B=10):
    L = len(digs)
    out = []
    carry = 0
    for j in range(L):
        v = digs[j] + digs[L - 1 - j] + carry
        out.append(v % B)
        carry = v // B
    if carry:
        out.append(carry)
    return out


def is_pal(digs):
    return digs == digs[::-1]
