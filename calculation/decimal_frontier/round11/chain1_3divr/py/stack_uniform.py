"""k-uniform check that nothing can be stacked on N12^k's 9-sea cut (all k >= 1 at once).

Cut letters (bx convention), time phase f = t mod 12, clock g = 000100010001:
  letter a = (L, H, Y)  (Y only at overflow phases, else 0)
One column x in 0..18 above a cut letter: choose c in {0,1} with floor((x+c)/10) = H;
  x_next = (x+L)%10 + (Y if g else (x+c)%10);  output letter (floor((x+L)/10), c, (x+c)%10 if g else 0).
A   = one column above u (u = 12-periodic 9-sea cut of N12): nodes (f, x).
AT  = two columns above u: nodes (f, x1, x2), label = output of x2.
CL(X) = set of labels of closed walks of length 12k (k>=1) through phase 0.
Checks (each one is a statement for every k simultaneously):
  (b)  CL(AT) subset of CL(A)                 -> reachable cut set above u^k is CL_k(A) for every height
  (c)  in A, every cycle of accepting-label edges has x == 9 throughout
  (c') in AT, every cycle of accepting-label edges has x2 == 9 throughout
Then: no exterior with clock (0001)^(3k) has a non-9 column above N12^k's 9-sea cut (PAPER PROOF given b, c, c')."""
import sys, itertools
from collections import deque
b = 10; P = 12
g = [int(c) for c in '000100010001']
e = [int(c) for c in sys.argv[1]] if len(sys.argv) > 1 else [int(c) for c in '101101010010']
u = [(e[f], 1 - e[f], 9 * e[f] if g[f] else 0) for f in range(P)]   # 9-sea cut (accepting)
def acc(a): return a[1] == 1 - a[0] and (a[2] == 9 * a[0] if True else True)
def accf(f, a): return a[1] == 1 - a[0] and (not g[f] or a[2] == 9 * a[0])
def col(f, x, a):
    L, H, Y = a; out = []
    for c in (0, 1):
        if ((x + c) >= b) != (H == 1): continue
        xn = (x + L) % b + (Y if g[f] else (x + c) % b)
        out.append((xn, ((x + L) // b, c, (x + c) % b if g[f] else 0)))
    return out
# --- A: edges[f][x] -> list of (x', label)
A = [[col(f, x, u[f]) for x in range(2 * b - 1)] for f in range(P)]
# --- AT edges
def AT_edges(f, x1, x2):
    res = []
    for x1n, a1 in A[f][x1]:
        for x2n, a2 in col(f, x2, a1): res.append(((x1n, x2n), a2))
    return res
NX = 2 * b - 1
# label -> transitions in A, for membership tracking
Alab = [dict() for f in range(P)]
for f in range(P):
    for x in range(NX):
        for xn, a in A[f][x]: Alab[f].setdefault(a, [[] for _ in range(NX)])[x].append(xn)
def track(f, S, a):
    tbl = Alab[f].get(a)
    if tbl is None: return tuple(0 for _ in S)
    out = []
    for s in S:
        m = 0; v = s
        while v:
            lb = v & -v; x = lb.bit_length() - 1; v ^= lb
            for xn in tbl[x]: m |= 1 << xn
        out.append(m)
    return tuple(out)
init = tuple(1 << x for x in range(NX))
# (b): search for a closed walk in AT whose label is not in CL(A)
bad = None; nstates = 0
for z0 in itertools.product(range(NX), repeat=2):
    seen = set(); dq = deque([(0, z0, init, 0)]); seen.add((0, z0, init))
    while dq and bad is None:
        f, z, S, steps = dq.popleft()
        for zn, a in AT_edges(f, *z):
            fn = (f + 1) % P; Sn = track(f, S, a)
            if fn == 0 and zn == z0 and not any((Sn[x] >> x) & 1 for x in range(NX)):
                bad = (z0, steps + 1); break
            key = (fn, zn, Sn)
            if key not in seen: seen.add(key); dq.append((fn, zn, Sn, steps + 1))
    nstates += len(seen)
    if bad: break
print('(b) CL(AT) subset CL(A):', 'FAILS at start %s, walk length %d' % bad if bad else 'HOLDS', '| product states explored', nstates)
# cycles of accepting-label edges
def acc_cycles(nodes_edges):
    # nodes_edges: dict node -> list of successor nodes (accepting edges only); return nodes on cycles (SCC with an internal edge)
    idx = {}; low = {}; st = []; on = set(); comp = []; cnt = [0]
    sys.setrecursionlimit(100000)
    def sc(v):
        idx[v] = low[v] = cnt[0]; cnt[0] += 1; st.append(v); on.add(v)
        for w in nodes_edges.get(v, []):
            if w not in idx: sc(w); low[v] = min(low[v], low[w])
            elif w in on: low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            cc = []
            while True:
                w = st.pop(); on.discard(w); cc.append(w)
                if w == v: break
            comp.append(cc)
    for v in list(nodes_edges): 
        if v not in idx: sc(v)
    oncyc = set()
    for cc in comp:
        s = set(cc)
        if any(w in s for v in cc for w in nodes_edges.get(v, [])): oncyc |= s
    return oncyc
EA = {}
for f in range(P):
    for x in range(NX):
        for xn, a in A[f][x]:
            if accf(f, a): EA.setdefault((f, x), []).append(((f + 1) % P, xn))
cyc = acc_cycles(EA)
print('(c) accepting cycles in A visit x values:', sorted(set(v[1] for v in cyc)))
EAT = {}
for f in range(P):
    for x1 in range(NX):
        for x2 in range(NX):
            for zn, a in AT_edges(f, x1, x2):
                if accf(f, a): EAT.setdefault((f, x1, x2), []).append(((f + 1) % P,) + zn)
cyc2 = acc_cycles(EAT)
print("(c') accepting cycles in AT visit x2 values:", sorted(set(v[2] for v in cyc2)))
