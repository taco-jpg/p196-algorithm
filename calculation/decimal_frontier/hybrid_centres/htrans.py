#!/usr/bin/env python3
"""htrans.py -- EXACT spatial-transfer decision procedure for hybrid cycles of ANY width (for fixed stream/period T, core sequence c_t, front shift A).

Infinite-line picture (equivalent to the register model of hsat.py): cells i>=0, values v_i(t) in [0,2b-2], t in [0,T].
  cell rule (a=A_i(t) ascending carry in, din=D_i(t) descending carry in from above):
      A_{i+1}(t)=[v+a>=b], da=(v+a)%b ; Dout_i(t)=[v+din>=b], dd=(v+din)%b
      gam=0: v_i(t+1)=da+dd_i ;  gam=1: v_i(t+1)=da+dd_{i-1}   (dd_{-1}=N*e1)
  boundary: A_0(t)=e1(t), Dout_0(t)=1-e1(t);   closure: v_i(T)=v_{i-A}(0) (=N for i<A);  top: vacuum c(t) for all large i.
Link state s_i=(Aup(.), G(.), ddprev(.), mem(.)) with G_i(t)=Dout_i(t) (what cell i must send down), ddprev(t)=dd_{i-1}(t) at gam=1 times,
mem = the A values v_{i-A}(0..) needed for closure.  BFS over i with visited set => terminates (finite state space);
result: 'SUCCESS' (vacuum link state reachable => hybrid cycle exists; path returned), 'EXHAUSTED' (no hybrid cycle of any width), or 'CAP'.
"""
import sys, time
sys.setrecursionlimit(10000)

def make_vac(b, gam, e1, cs, A):
    T = len(gam); N = b - 1
    ks = [1 if c >= b else 0 for c in cs]; ys = [(c + k) % b for c, k in zip(cs, ks)]
    return (tuple(ks), tuple(ks), tuple(ys[t] if gam[t] else 0 for t in range(T)), tuple([cs[0]] * A))

def transfer(b, gam, e1, A, state, i):
    """all successor link states of `state` (cell i); returns list of (next_state, v0) """
    T = len(gam); N = b - 1
    Aup, G, ddprev, mem = state
    out = []
    req = mem[0] if A > 0 else None     # required v_i(T)
    for v0 in range(2 * b - 1):
        # DFS over t
        stack = [(0, v0, (), (), (), ())]   # t, v, din choices, Anext, ddcur(gam1), -
        # iterative DFS with explicit recursion for clarity
        def rec(t, v, dins, Anext, ddc):
            if t == T:
                need = mem[0] if A > 0 else v0
                if v != need: return
                nmem = (mem[1:] + (v0,)) if A > 0 else ()
                out.append(((tuple(Anext), tuple(dins), tuple(ddc), nmem), v0))
                return
            a = Aup[t]; g = G[t]
            for din in (0, 1):
                if ((v + din) >= b) != bool(g): continue
                dd = (v + din) % b
                da = (v + a) % b
                an = 1 if (v + a) >= b else 0
                vn = da + (ddprev[t] if gam[t] else dd)
                if vn > 2 * b - 2: continue
                rec(t + 1, vn, dins + [din], Anext + [an], ddc + [dd if gam[t] else 0])
        rec(0, v0, [], [], [])
    return out

def decide(b, gam, e1, cs, A, cap=2_000_000, maxlayers=100000, verbose=False):
    T = len(gam); N = b - 1
    ks = [1 if c >= b else 0 for c in cs]
    # A==0: closure v_i(T)=v_i(0) is v0 itself
    start = (tuple(e1), tuple(1 - x for x in e1), tuple(N * e1[t] if gam[t] else 0 for t in range(T)), tuple([N] * A))
    vac = make_vac(b, gam, e1, cs, A)
    visited = {start: None}
    frontier = [start]
    layer = 0
    while frontier:
        nxt = []
        for s in frontier:
            for (ns, v0) in transfer(b, gam, e1, A, s, layer):
                if ns == vac:
                    # reconstruct path
                    path = [v0]; cur = s
                    while visited[cur] is not None:
                        pv, pv0 = visited[cur]; path.append(pv0); cur = pv
                    return 'SUCCESS', layer + 1, list(reversed(path))
                if ns not in visited:
                    visited[ns] = (s, v0)
                    nxt.append(ns)
        layer += 1
        if verbose: print(f"  layer {layer}: frontier {len(nxt)} visited {len(visited)}", flush=True)
        if len(visited) > cap: return 'CAP', layer, len(visited)
        if layer > maxlayers: return 'CAP', layer, len(visited)
        frontier = nxt
    return 'EXHAUSTED', layer, len(visited)

if __name__ == '__main__':
    pass
