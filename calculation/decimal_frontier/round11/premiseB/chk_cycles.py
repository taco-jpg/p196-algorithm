# Theorem B, global form, exhaustive in a box: for every clock g of length T and every height h <= Hmax,
#   #{Agent120 exteriors (B_0..B_{T-1}), Phi^T(B_0)=B_0, gam word g, e1 word e, max width <= h}
# = #{accepting reach histories of height exactly h with stream e}    (Python model of reach)
# and the C++ reach binary (WIRE, maxdepth Hmax) reports exactly the streams whose first height <= Hmax, at that height.
import sys, itertools, collections, subprocess, re
from rmodel import *
def lists(b, L):
    yield ()
    for n in range(1, L + 1):
        for B in itertools.product(range(2 * b - 1), repeat=n):
            if B[0] == 0 or B[-1] == b - 1: continue
            yield B
def sigmaA(b, T, L):
    F = {B: phi(b, B) for B in lists(b, L)}
    cnt = collections.Counter()      # (g, e, W) -> number of start lists B_0
    for B0 in F:
        B = B0; g = []; e = []; W = 0; ok = True
        for t in range(T):
            W = max(W, len(B))
            nb, e1, gm = F[B]; g.append(gm); e.append(e1)
            if len(nb) > L: ok = False; break
            B = nb
        if ok and B == B0: cnt[(tuple(g), tuple(e), W)] += 1
    return cnt
def reachDP(b, T, ovf, Hmax):
    """counts[h][e] = number of accepting histories of height h with stream e; plus reachable sets per height"""
    root = root_node(T, ovf); layer = collections.Counter()
    for nd, xs in expand(b, T, ovf, root, True): layer[nd] += 1
    out = []; seen = set(layer); sets = [set(layer)]
    for h in range(1, Hmax + 1):
        acc = collections.Counter()
        for nd, k in layer.items():
            if wire_accept(b, T, ovf, nd): acc[nd[0]] += k
        out.append(acc)
        if h == Hmax: break
        nl = collections.Counter()
        cache = {}
        for nd, k in layer.items():
            for s, xs in expand(b, T, ovf, nd, False): nl[s] += k
        layer = nl; sets.append(set(nl))
    return out, sets
def cpp_streams(b, T, g, Hmax):
    o = subprocess.run(['./src/reach', str(b), str(T), ''.join(map(str, g)), 'WIRE', '100000000', str(Hmax)], capture_output=True, text=True).stdout
    return {s: int(h) for h, s in re.findall(r'NEW STREAM at height (\d+): ([01]+)', o)}
def run(b, Tmax, Hmax):
    bad = 0; tot = 0; nonzero = 0; rotbad = 0
    for T in range(1, Tmax + 1):
        A = sigmaA(b, T, Hmax)
        for g in itertools.product((0, 1), repeat=T):
            dp, sets = reachDP(b, T, g, Hmax)
            first = {}
            for h in range(1, Hmax + 1):
                for e in set(list(dp[h - 1]) + [k[1] for k in A if k[0] == g]):
                    a = sum(v for (gg, ee, W), v in A.items() if gg == g and ee == e and W <= h)
                    r = dp[h - 1].get(e, 0); tot += 1
                    if a != r: bad += 1; print('COUNT MISMATCH', b, T, g, e, h, a, r)
                    if r: nonzero += 1; first.setdefault(''.join(map(str, e)), h)
            cs = cpp_streams(b, T, g, Hmax)
            if cs != first: bad += 1; print('CPP MISMATCH', b, T, g, cs, first)
            # ROT: every reachable layer closed under the time shift by any k with g shifted = g
            for k in range(1, T):
                if tuple(g[k:] + g[:k]) != tuple(g): continue
                sh = lambda x: tuple(x[k:] + x[:k])
                for S in sets:
                    for (c, d, r) in S:
                        if (sh(c), sh(d), sh(r)) not in S: rotbad += 1
    print(f'base {b}, T<={Tmax}, h<={Hmax}: {tot} (g,e,h) comparisons, {nonzero} nonzero, count/cpp mismatches {bad}, shift-closure violations {rotbad}')
    return bad + rotbad
if __name__ == '__main__':
    args = [tuple(map(int, a.split(','))) for a in sys.argv[1:]] or [(2, 6, 8), (3, 5, 6), (4, 4, 5), (10, 4, 3)]
    t = sum(run(*a) for a in args); print('TOTAL', t)
