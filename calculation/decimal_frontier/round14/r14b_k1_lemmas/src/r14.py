# r14.py: minimal reference implementation of the pair-word window rule (r12g sections 1-3), own code.
import sys, struct, os
class Lat:
    def __init__(s, fn):
        toks = open(fn).read().split()
        p = 0
        def rd(n):
            nonlocal p
            r = [int(x) for x in toks[p:p+n]]; p += n; return r
        s.base, s.tp, s.nB, s.m = rd(4)
        s.clk = rd(s.tp)
        s.B = [rd(s.nB) for _ in range(s.tp)]
        s.W = [rd(s.m) for _ in range(s.tp)]
        s.bs = s.base
        b = s.base; m = s.m
        s.UP = []; s.DN = []; s.EE = []
        for t in range(s.tp):
            W = s.W[t]
            # ascending periodic solution
            a = 0
            for rep in range(4):
                for x in range(m):
                    a = 1 if W[x] + a >= b else 0
            up = [0]*m; ee = [0]*m
            a0 = a
            for x in range(m):
                up[x] = a; ee[x] = (W[x] + a) % b; a = 1 if W[x] + a >= b else 0
            assert a == a0
            # descending
            bb = 0
            for rep in range(4):
                for x in range(m-1, -1, -1):
                    bb = 1 if W[x] + bb >= b else 0
            dn = [0]*m
            for x in range(m-1, -1, -1):
                dn[x] = bb; bb = 1 if W[x] + bb >= b else 0
            s.UP.append(up); s.DN.append(dn); s.EE.append(ee)
        # BOK[t][j][b]: lattice below stays exact if descending carry entering cell j-1 is b ; RB1 = r_{j-1}
        s.BOK = []; s.RB1 = []
        for t in range(s.tp):
            g = s.clk[t]; tn = (t+1) % s.tp
            ok_t = []; rb_t = []
            for j in range(m):
                o = [False, False]; rr1 = [0, 0]
                for bb in (0, 1):
                    LIM = 3*m
                    rr = [0]*(LIM+3)
                    bc = bb
                    for l in range(1, LIM+3):
                        col = (j-l) % m
                        v = s.W[t][col] + bc
                        rr[l] = v % b
                        bc = 1 if v >= b else 0
                    good = True
                    for l in range(1, LIM+1):
                        coly = (j-l) % m
                        val = s.EE[t][coly] + rr[l+1 if g else l]
                        if val != s.W[tn][coly]:
                            good = False; break
                    o[bb] = good; rr1[bb] = rr[1]
                ok_t.append(o); rb_t.append(rr1)
            s.BOK.append(ok_t); s.RB1.append(rb_t)
    def orbits(s):
        tot = s.tp*s.m*2; seen = [False]*tot; out = []
        for i in range(tot):
            if seen[i]: continue
            o = []; cur = i
            while not seen[cur]:
                seen[cur] = True
                par = cur & 1; rest = cur >> 1; t = rest // s.m; j = rest % s.m
                o.append((t,j,par))
                g = s.clk[t]; dh = 1 if (g == 1 and par == 0) else 0
                t2 = (t+1) % s.tp; j2 = (j+dh) % s.m; par2 = (par+g) % 2
                cur = ((t2*s.m+j2)*2)+par2
            out.append(o)
        return out
    def succ(s, ph, w):
        """R_K successors: list of (Din, topv or None, new window)."""
        b = s.base
        t, j, par = ph; g = s.clk[t]; dh = 1 if (g == 1 and par == 0) else 0; tn = (t+1) % s.tp
        K = len(w)
        e = [0]*K; r = [0]*K
        a = s.UP[t][j]
        for i in range(K):
            v = w[i] + a; e[i] = v % b; a = 1 if v >= b else 0
        out = []
        for Din in (0, 1):
            bc = Din
            for i in range(K-1, -1, -1):
                v = w[i] + bc; r[i] = v % b; bc = 1 if v >= b else 0
            if not s.BOK[t][j][bc]: continue
            rb1 = s.RB1[t][j][bc]
            if dh:
                if e[0] + rb1 != s.W[tn][j]: continue
                head = tuple(e[i+1] + r[i] for i in range(K-1))
                for v in range(b):
                    out.append((Din, v, head + (v + r[K-1],)))
            elif g == 0:
                out.append((Din, None, tuple(e[i] + r[i] for i in range(K))))
            else:
                prev = rb1; nw = []
                for i in range(K):
                    nw.append(e[i] + prev); prev = r[i]
                out.append((Din, None, tuple(nw)))
        return out
    def exact(s, ph, w):
        b = s.base
        t, j, par = ph; g = s.clk[t]; dh = 1 if (g == 1 and par == 0) else 0; tn = (t+1) % s.tp
        K = len(w)
        e = [0]*K; r = [0]*K
        a = s.UP[t][j]; topin = 0
        for i in range(K):
            if i == K-1: topin = a
            v = w[i] + a; e[i] = v % b; a = 1 if v >= b else 0
        Din = a if par == 0 else topin
        bc = Din
        for i in range(K-1, -1, -1):
            v = w[i] + bc; r[i] = v % b; bc = 1 if v >= b else 0
        if not s.BOK[t][j][bc]: return None
        rb1 = s.RB1[t][j][bc]
        if dh:
            if e[0] + rb1 != s.W[tn][j]: return None
            return tuple(e[i+1] + r[i] for i in range(K-1)) + (2*r[K-1],)
        if g == 0:
            return tuple(e[i] + r[i] for i in range(K))
        prev = rb1; nw = []
        for i in range(K):
            nw.append(e[i] + prev); prev = r[i]
        return tuple(nw)

def load_layers(fn):
    d = open(fn, "rb").read()
    T, K = struct.unpack_from("ii", d, 0); p = 8
    layers = []
    for l in range(T):
        t, j, par, n = struct.unpack_from("iiii", d, p); p += 16
        cells = [tuple(d[p+i*K:p+(i+1)*K]) for i in range(n)]; p += n*K
        layers.append(((t,j,par), cells))
    return T, K, layers
