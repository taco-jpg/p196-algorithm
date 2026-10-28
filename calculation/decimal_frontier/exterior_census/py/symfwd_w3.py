# COPY of /home/claude/research/w3_formats/code/symfwd.py (written by workstream W3), unchanged; imported by symacc.py (W5).
#!/usr/bin/env python3
# symfwd.py : SYMBOLIC (BDD, CUDD via dd.cudd) forward reachability for the position automaton of the uniform-band /
# periodic-lattice exterior search.  State = (L_t, H_t in {0,1}, Y_i in 0..b-1 at overflow times) over the time ring Z/p.
# Transition (same semantics as bwd_common.h transitions()):
#   hidden columns x_t in [0,2b-2] (t=0..p-1, x_p = x_0), c_t = H'_t in {0,1};
#   floor((x_t+c_t)/b) = H_t ; L'_t = floor((x_t+L_t)/b) ; Y'_i = (x_t+c_t) % b at gam times ;
#   x_{t+1} = (x_t+L_t)%b + (g_t ? Y_t : (x_t+c_t)%b).        First position: all x_t >= 1, start (L=0,H=g,Y=1).
# usage: symfwd.py b word [-maxlev N] [-targets uniform|none] [-reorder K] [-quiet]
# Prints per level: new-state count (exact, via BDD model counting), node counts; reports CLOSED / hits.
import sys, time
import dd.cudd as cudd


class Sym:
    def __init__(self, b, gstr, reorder_every=0, max_mem_gb=1.8, cache_size=2**22, unique_size=2**20):
        self.b = b
        self.gs = gstr
        self.g = [c == '1' for c in gstr]
        self.p = len(gstr)
        self.xb = (2 * b - 2).bit_length()
        self.yb = max(1, (b - 1).bit_length())
        self.bdd = cudd.BDD(initial_cache_size=cache_size)
        self.bdd.configure(max_memory=int(max_mem_gb * 1024 ** 3), reordering=False)
        p = self.p
        names = []
        self.Xn = [[f"X{t}_{j}" for j in range(self.xb)] for t in range(p)]
        names += self.Xn[0]
        self.Ln = [f"L{t}" for t in range(p)]
        self.Hn = [f"H{t}" for t in range(p)]
        self.Lpn = [f"Lp{t}" for t in range(p)]
        self.Hpn = [f"Hp{t}" for t in range(p)]
        self.Yn = [[f"Y{t}_{j}" for j in range(self.yb)] if self.g[t] else None for t in range(p)]
        self.Ypn = [[f"Yp{t}_{j}" for j in range(self.yb)] if self.g[t] else None for t in range(p)]
        for t in range(p):
            if t > 0:
                names += self.Xn[t]
            names += [self.Ln[t], self.Hn[t]]
            if self.g[t]:
                names += self.Yn[t]
            names += [self.Lpn[t], self.Hpn[t]]
            if self.g[t]:
                names += self.Ypn[t]
        self.bdd.declare(*names)
        self.svars = []
        self.pvars = []
        for t in range(p):
            self.svars += [self.Ln[t], self.Hn[t]] + (self.Yn[t] if self.g[t] else [])
            self.pvars += [self.Lpn[t], self.Hpn[t]] + (self.Ypn[t] if self.g[t] else [])
        self.ren = {pv: sv for pv, sv in zip(self.pvars, self.svars)}
        self.nS = len(self.svars)
        self.reorder_every = reorder_every
        self._lit = {}

    # ---- literals / cubes ----
    def lit(self, name, val):
        k = (name, val)
        f = self._lit.get(k)
        if f is None:
            v = self.bdd.var(name)
            f = v if val else ~v
            self._lit[k] = f
        return f

    def num(self, names, val):
        r = self.bdd.true
        for j, n in enumerate(names):
            r = r & self.lit(n, (val >> j) & 1)
        return r

    def slot(self, t, first):
        b = self.b
        bdd = self.bdd
        g = self.g[t]
        Xt = self.Xn[t]
        Xn = self.Xn[(t + 1) % self.p]
        rel = bdd.false
        for x in range(1 if first else 0, 2 * b - 1):
            cx = self.num(Xt, x)
            for Lt in (0, 1):
                for c in (0, 1):
                    Ht = (x + c) // b
                    Lp = (x + Lt) // b
                    base = (x + Lt) % b
                    ypn = (x + c) % b
                    common = cx & self.lit(self.Ln[t], Lt) & self.lit(self.Hn[t], Ht) & self.lit(self.Lpn[t], Lp) & self.lit(self.Hpn[t], c)
                    if not g:
                        nx = base + (x + c) % b
                        rel = rel | (common & self.num(Xn, nx))
                    else:
                        cp = common & self.num(self.Ypn[t], ypn)
                        for y in range(b):
                            nx = base + y
                            rel = rel | (cp & self.num(self.Yn[t], y) & self.num(Xn, nx))
        return rel

    def build_T(self, first):
        p = self.p
        bdd = self.bdd
        acc = self.slot(0, first)
        for t in range(1, p):
            acc = acc & self.slot(t, first)
            acc = bdd.exist(self.Xn[t], acc)
        acc = bdd.exist(self.Xn[0], acc)
        return acc

    def state_cube(self, L, H, Y):
        """L,H lists of bits (len p), Y list of digits (len ng)"""
        r = self.bdd.true
        yi = 0
        for t in range(self.p):
            r = r & self.lit(self.Ln[t], L[t]) & self.lit(self.Hn[t], H[t])
            if self.g[t]:
                r = r & self.num(self.Yn[t], Y[yi])
                yi += 1
        return r

    def prep_slots(self, first):
        return [self.slot(t, first) for t in range(self.p)]

    def image_part(self, F, Cs):
        """partitioned image with early quantification: F over unprimed vars, Cs = per-slot relations"""
        bdd = self.bdd
        p = self.p
        acc = F
        for t in range(p):
            acc = acc & Cs[t]
            q = [self.Ln[t], self.Hn[t]] + (self.Yn[t] if self.g[t] else [])
            if t > 0:
                q = q + self.Xn[t]
            acc = bdd.exist(q, acc)
        acc = bdd.exist(self.Xn[0], acc)
        return bdd.let(self.ren, acc)

    def image(self, F, T):
        bdd = self.bdd
        G = bdd.apply('and', F, T)
        G = bdd.exist(self.svars, G)
        return bdd.let(self.ren, G)

    def count(self, F):
        return self.bdd.count(F, self.nS)


def loops_of(b):
    nxt = [-1] * (2 * b - 1)
    for k in range(2 * b - 1):
        if k != b - 1:
            c = 1 if k >= b else 0
            nxt[k] = 2 * ((k + c) % b)
    st = [0] * (2 * b - 1)
    R = []
    for k in range(2 * b - 1):
        if k == b - 1 or st[k]:
            continue
        path = []
        x = k
        while x != b - 1 and x >= 0 and st[x] == 0:
            st[x] = 1
            path.append(x)
            x = nxt[x]
        if x != b - 1 and x >= 0 and st[x] == 1 and x in path:
            R.append(path[path.index(x):])
        for y in path:
            st[y] = 2
    return R


def uniform_targets(S):
    b, p = S.b, S.p
    out = []
    for lp in loops_of(b):
        ell = len(lp)
        if p % ell:
            continue
        for ph in range(ell):
            u = [lp[(t + ph) % ell] for t in range(p)]
            L = [1 if x >= b else 0 for x in u]
            H = L[:]
            Y = [(u[t] + H[t]) % b for t in range(p) if S.g[t]]
            out.append((lp[0], ph, S.state_cube(L, H, Y)))
    return out


def main():
    b = int(sys.argv[1])
    gs = sys.argv[2]
    maxlev = 10 ** 9
    quiet = False
    reorder = 0
    tmode = 'uniform'
    part = False
    i = 3
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == '-maxlev':
            maxlev = int(sys.argv[i + 1]); i += 1
        elif a == '-quiet':
            quiet = True
        elif a == '-part':
            part = True
        elif a == '-reorder':
            reorder = int(sys.argv[i + 1]); i += 1
        elif a == '-targets':
            tmode = sys.argv[i + 1]; i += 1
        i += 1
    t0 = time.time()
    S = Sym(b, gs)
    p = S.p
    if part:
        C1 = S.prep_slots(True)
        C = S.prep_slots(False)
        print(f"built slots: nodes first={sum(len(c) for c in C1)} std={sum(len(c) for c in C)} t={time.time()-t0:.1f}s", flush=True)
    else:
        T1 = S.build_T(True)
        T = S.build_T(False)
        print(f"built T: nodes first={len(T1)} std={len(T)} t={time.time()-t0:.1f}s", flush=True)
    img_first = (lambda F: S.image_part(F, C1)) if part else (lambda F: S.image(F, T1))
    img_std = (lambda F: S.image_part(F, C)) if part else (lambda F: S.image(F, T))
    Hst = [1 if c else 0 for c in S.g]
    start = S.state_cube([0] * p, Hst, [1] * sum(S.g))
    targets = uniform_targets(S) if tmode == 'uniform' else []
    F = img_first(start)
    visited = start | F
    Fr = F
    lev = 1
    hit_levels = {}
    while True:
        n = S.count(Fr)
        if n == 0:
            print(f"CLOSED levels={lev-1} total={S.count(visited)} t={time.time()-t0:.0f}s")
            break
        for (l0, ph, tc) in targets:
            if (l0, ph) not in hit_levels and (Fr & tc) != S.bdd.false:
                hit_levels[(l0, ph)] = lev
                print(f"HIT target loop0={l0} ph={ph} at level {lev}", flush=True)
        if not quiet or lev % 10 == 0:
            print(f"level {lev} new={n} total={S.count(visited)} nodesFr={len(Fr)} nodesVis={len(visited)} t={time.time()-t0:.0f}s", flush=True)
        if lev >= maxlev:
            print(f"STOP maxlev={maxlev} total={S.count(visited)}")
            break
        if reorder and lev % reorder == 0:
            S.bdd.reorder()
        img = img_std(Fr)
        new = img & ~visited
        visited = visited | new
        Fr = new
        lev += 1
    print(f"targets={len(targets)} hit={len(hit_levels)} {hit_levels}")


if __name__ == '__main__':
    main()
