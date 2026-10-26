#!/usr/bin/env python3
"""Exterior cycles of the neutral one-band map via a TRANSFER GRAPH over carry bit-words (any length L).

Model (exact; validated against brute force in selftest):
  The whole reverse-and-add step is a 1-D bidirectional cellular automaton on the pair sums q_j (j = 0 at the low end):
      c_{j+1} = [q_j + c_j >= b]            (carry travelling up from the low end, c_0 = 0)
      d_{j-1} = [q_j + d_j >= b]            (carry travelling down in the mirrored top half, d_{-1} = gam)
      Dbot_j = q_j + c_j - b c_{j+1},   Dtop_j = q_j + d_j - b d_{j-1}
      q'_j = Dbot_j + Dtop_{j - s},   s = gam  (the new leading digit 1 shifts the top half by one; Dtop_{-1} := 1)
  The neutral band is q = b-1 with c != d (then q' = b-1 again).
  An exterior cycle of period p with overflow word s in {0,1}^p is a column-by-column path: cell j has a time orbit
  q_j^{(t)}, t mod p; interface state between cell j-1 and cell j = (c_j word, d_{j-1} word, Dtop_{j-1}^{(t)} at the t
  with s_t = 1).  Start (0^p, s, 1's).  Closing (first neutral cell): d_{L-1} = NOT c_L and Dtop_{L-1}^{(t)} = (b-1) c_L^{(t)}.
  Cell equation for s_t = 0 at every t:  (2^p - 1) q_j^{(0)} = b(<c_{j+1}> + <d_{j-1}>) - (<c_j> + <d_j>)  (binary words,
  t = 0 most significant): the exterior exists only if these divisibilities hold for the base b.
usage:  ext_transfer.py selftest | ext_transfer.py scan b pmax Lmax
"""
import sys, itertools, time
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))


def cell_transitions(b, p, s, cw, dw, T, first):
    """all (nstate, qorbit) for one non-boundary cell. cw,dw: tuples of bits (len p); T: tuple of Dtop_{j-1} at shifted t."""
    shifted = [t for t in range(p) if s[t]]
    Tmap = {t: T[i] for i, t in enumerate(shifted)}
    out = []
    for q0 in range(1 if first else 0, 2 * b - 1):
        # DFS over t choosing d_j^t
        stack = [(0, q0, (q0,), (), ())]   # t, q_t, qorbit, djword, cprime word
        while stack:
            t, q, qo, djw, cpw = stack.pop()
            if t == p:
                if q == q0:
                    # compute T_j
                    Tj = tuple(qo[t2] + djw[t2] - b * dw[t2] for t2 in shifted)
                    out.append(((cpw, djw, Tj), qo[:p]))
                continue
            cp = 1 if q + cw[t] >= b else 0
            dbot = q + cw[t] - b * cp
            for dj in (0, 1):
                if (1 if q + dj >= b else 0) != dw[t]:
                    continue
                dtop_own = q + dj - b * dw[t]
                dtop = dtop_own if not s[t] else Tmap[t]
                qn = dbot + dtop
                if qn < 0 or qn > 2 * b - 2:
                    continue
                if first and qn == 0 and t + 1 < p:
                    continue
                stack.append((t + 1, qn, qo + ((qn,) if t + 1 < p else ()), djw + (dj,), cpw + (cp,)))
    return out


def exterior_cycles(b, p, s, Lmax):
    """returns dict L -> set of exterior vectors B^{(0)} (trimmed) for exteriors of (untrimmed all-time) length L."""
    shifted = [t for t in range(p) if s[t]]
    start = (tuple([0] * p), tuple(s), tuple([1] * len(shifted)))
    layer = {start: [()]}     # state -> list of cell-orbit paths (kept as list of paths; may blow up -> cap)
    found = {}
    for j in range(Lmax):
        nxt = {}
        for st, paths in layer.items():
            cw, dw, T = st
            for ns, qo in cell_transitions(b, p, s, cw, dw, T, first=(j == 0)):
                nl = nxt.setdefault(ns, [])
                if len(nl) < 2000:
                    nl.extend(pth + (qo,) for pth in paths[:2000])
                    del nl[2000:]
        layer = nxt
        for st, paths in layer.items():
            cw, dw, T = st
            if all(dw[t] == 1 - cw[t] for t in range(p)) and all(T[i] == (b - 1) * cw[t] for i, t in enumerate(shifted)):
                for pth in paths:
                    # last cell must be non-neutral at some time
                    if all(v == b - 1 for v in pth[-1]):
                        continue
                    found.setdefault(j + 1, set()).add((tuple(pth), cw))
    return found


def to_B0(b, pth):
    B = [qo[0] for qo in pth]
    while B and B[-1] == b - 1:
        B.pop()
    return tuple(B)


def scan(b, pmax, Lmax, verbose=True):
    from decouple import G_ext
    res = []
    t0 = time.time()
    for p in range(1, pmax + 1):
        for s in itertools.product((0, 1), repeat=p):
            if not any(s): continue
            # rotation canonical form for s to avoid duplicates
            rots = [s[i:] + s[:i] for i in range(p)]
            if s != min(rots): continue
            fd = exterior_cycles(b, p, s, Lmax)
            for L, items in sorted(fd.items()):
                for pth, cw in items:
                    B0 = to_B0(b, pth)
                    # verify with the mirror's exterior map
                    cur = list(B0); ok = True; Ew = []; Gw = []
                    for t in range(p):
                        r = G_ext(b, cur)
                        if r is None: ok = False; break
                        Ew.append(r[2]); Gw.append(r[3]); cur = r[0]
                    ok = ok and tuple(cur) == B0 and tuple(Gw) == tuple(s) and tuple(Ew) == tuple(cw)
                    res.append((p, s, L, B0, cw, ok))
                    if verbose:
                        print(f"  p={p} s={''.join(map(str,s))} L={L} E={''.join(map(str,cw))} verified={ok} B0={list(B0)}")
    if verbose: print(f"base {b}: {len(res)} exterior cycles (p<={pmax}, L<={Lmax}) in {time.time()-t0:.1f}s")
    return res


def brute_states(b, Lmax):
    """all states lying on G-cycles with every phase of trimmed length <= Lmax, with the cycle period."""
    from ext_cycles import cycles
    out = {}
    for c in cycles(b, Lmax):
        for st in c:
            out[st] = len(c)
    return out


def selftest():
    ok = True
    for b in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 16):
        Lmax = 4 if b <= 13 else 3
        pmax = 5
        res = scan(b, pmax, Lmax, verbose=False)
        tr = {}
        from decouple import G_ext
        for p, s, L, B0, cw, v in res:
            ok &= v
            cur = list(B0)
            for t in range(p):
                tr.setdefault(tuple(cur), set()).add(p)
                cur = G_ext(b, cur)[0]
        # brute force cycles (all phases length <= Lmax) with period dividing some p <= pmax
        br = brute_states(b, Lmax)
        br = {st: pp for st, pp in br.items() if pp <= pmax}
        # every brute-force state of a cycle with period pp <= pmax must be found by the transfer at p = pp
        missing = [st for st, pp in br.items() if st not in tr]
        extra = [st for st in tr if st not in br]
        print(f"base {b:2d}: brute-force cycle states {len(br):3d}, transfer states {len(tr):3d}, "
              f"missing {len(missing)}, extra {len(extra)}")
        ok &= (not missing) and (not extra)
    print("SELFTEST", "PASSED" if ok else "FAILED")
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'selftest': sys.exit(0 if selftest() else 1)
    if a[0] == 'scan': scan(int(a[1]), int(a[2]), int(a[3]))
