"""bcore.py -- exact spatial transfer automaton for the autonomous B-block of a neutral-band return certificate.

THEORY (all verified against the Lean-mirror library on thousands of transitions and on every known certificate):
  * Carry out of a block = polarity (H: entry>=b, L: entry<=b-2) of its top-most NON-NEUTRAL entry (neutral = b-1 is transparent).
  * B, as a state of a certificate cycle, is AUTONOMOUS: next B depends only on B and e2, and e2 = 1-e1(B) is forced by the
    hypothesis e1 != e2.  C talks to B only through the three bit streams e1(t), e2(t)=1-e1(t), gam(t).
  * Cell rule (lam_i / rho_i = polarity of nearest non-neutral cell below / above cell i; defaults lam_0=0, rho_top=1-e1):
        no overflow : B'_i = 2B_i + lam_i + rho_i - b(lam_{i+1} + rho_{i-1})
        overflow    : B'_i = B_i + lam_i - b lam_{i+1} + B_{i-1} + rho_{i-1} - b rho_{i-2}   (i>=1),   B'_0 = B_0 - b lam_1 + 1
    (cells above the real block are the neutral vacuum b-1; trimming = cells that become b-1.)
  * For a fixed period p and overflow pattern O in {0,1}^p the cells are added one at a time from the bottom; the state
    (column of the last cell over time, lam_{i+1}(t), rho_i(t), rho_{i-1}(t)) is finite, so reachability decides, for ALL
    block lengths, whether a p-periodic B exists with that overflow pattern.  A state is accepting if the vacuum can sit on top.

decide(b,p,O,maxstates,collect) -> (status, nstates, results)
    status in EXISTS / NONE / LIMIT ;  results = sorted list of (e1_stream, B_at_time_0) (one B per distinct e1 stream).
Requires b-1 <= 127 (byte-packed states)."""
import itertools


def patterns(p, minones=1, maxones=None):
    """overflow patterns of period p, one representative per rotation class (uses combinations when maxones is small)"""
    seen = set()
    if maxones is not None and maxones < p:
        cands = (tuple(1 if i in S else 0 for i in range(p))
                 for k in range(minones, maxones + 1) for S in map(set, itertools.combinations(range(p), k)))
    else:
        cands = itertools.product((0, 1), repeat=p)
    for O in cands:
        s = sum(O)
        if s < minones or (maxones is not None and s > maxones):
            continue
        key = min(O[i:] + O[:i] for i in range(p))
        if key in seen:
            continue
        seen.add(key)
        yield key


def decide(b, p, O, maxstates=20_000_000, collect=True, maxresults=64):
    n = b - 1
    assert 2 * n <= 255
    start = bytes(p) + bytes(p) + bytes(O) + bytes(p)   # pseudo cell -1: V=0, lam_0=0, rho_{-1}=O, rho_{-2}=0
    parent = {start: None}
    frontier = [start]
    terminals = []
    first_level = True
    while frontier:
        nxt = []
        for st in frontier:
            V = st[0:p]; lam = st[p:2 * p]; rho = st[2 * p:3 * p]; rhom1 = st[3 * p:4 * p]
            rho_b = bytes(rho)
            for v0 in range(1 if first_level else 0, 2 * n + 1):
                stack = [(0, (v0,), (), ())]
                while stack:
                    t, vc, lc, rc = stack.pop()
                    v = vc[-1]
                    if t == p:
                        if v != vc[0]:
                            continue
                        ns = bytes(vc[:p]) + bytes(lc) + bytes(rc) + rho_b
                        if ns not in parent:
                            parent[ns] = st
                            nxt.append(ns)
                        continue
                    if v == n:
                        opts = (rho[t],)
                    else:
                        if (1 if v >= b else 0) != rho[t]:
                            continue
                        opts = (0, 1)
                    lam_nx = lam[t] if v == n else (1 if v >= b else 0)
                    for rn in opts:
                        if O[t]:
                            nv = v + lam[t] - b * lam_nx + V[t] + rho[t] - b * rhom1[t]
                        else:
                            nv = 2 * v + lam[t] + rn - b * (lam_nx + rho[t])
                        if nv < 0 or nv > 2 * n:
                            continue
                        if first_level and nv < 1:
                            continue
                        stack.append((t + 1, vc + (nv,), lc + (lam_nx,), rc + (rn,)))
        first_level = False
        if len(parent) > maxstates:
            return 'LIMIT', len(parent), None
        for ns in nxt:
            V = ns[0:p]; lam = ns[p:2 * p]; rho = ns[2 * p:3 * p]; rhom1 = ns[3 * p:4 * p]
            ok = True
            for t in range(p):
                if rho[t] != 1 - lam[t]:
                    ok = False
                    break
                if O[t] and V[t] + rho[t] - b * rhom1[t] != n * lam[t]:
                    ok = False
                    break
            if ok:
                terminals.append(ns)
                if not collect:
                    break
        if terminals and not collect:
            break
        frontier = nxt
    if not terminals:
        return 'NONE', len(parent), None
    results = {}
    for ns in terminals:
        e1 = tuple(ns[p:2 * p])
        if e1 in results:
            continue
        path = []
        s = ns
        while s is not start:
            path.append(s)
            s = parent[s]
        B = [st[0] for st in path[::-1]]
        while B and B[-1] == n:
            B.pop()
        results[e1] = B
        if len(results) >= maxresults:
            break
    return 'EXISTS', len(parent), sorted(results.items())
