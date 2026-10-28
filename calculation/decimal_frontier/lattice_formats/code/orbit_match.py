import sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from scc_to_tmpl import parse
import kink_sat
def ext_words(fn, ri, b=10, X=400):
    kink_sat.b = b
    L = kink_sat.lattice_data(parse(fn)[ri])
    p, nB, m = L['p'], L['nB'], L['m']
    ws = []
    for t in range(p):
        w = list(L['Bt'][t]) + [L['Wt'][t][(x - nB) % m] for x in range(nB, X)]
        ws.append(w)
    return L, ws
def orbit_pairs(N, steps, b=10):
    # N python int in base 10 (digits), yields pair words lowest-first limited
    out = []
    for s in range(steps):
        d = [int(c) for c in str(N)[::-1]]
        P = [d[i] + d[len(d) - 1 - i] for i in range(len(d))]
        out.append(P)
        N = N + int(str(N)[::-1])
    return out
if __name__ == '__main__':
    seed = int(sys.argv[1]); steps = int(sys.argv[2])
    recs = [ext_words('../out/p8_scc.txt', ri) for ri in range(3)]
    N = seed; best = []
    for s in range(steps):
        sN = str(N); d = [int(c) for c in sN[::-1]]
        n = len(d)
        P = [d[i] + d[n - 1 - i] for i in range(min(120, n))]
        bestL = (0, None)
        for ri, (L, ws) in enumerate(recs):
            for t in range(L['p']):
                w = ws[t]; j = 0
                while j < len(P) and j < len(w) and P[j] == w[j]: j += 1
                if j > bestL[0]: bestL = (j, (ri, t))
        best.append((s, bestL[0], bestL[1], n))
        N = N + int(sN[::-1])
    import collections
    mx = max(best, key=lambda x: x[1])
    print('seed', seed, 'steps', steps, 'max lattice-prefix match', mx)
    hist = collections.Counter(min(x[1] // 4 * 4, 60) for x in best)
    print('hist of match length (bins of 4):', sorted(hist.items()))
    # longest run with match >= 12
    for thr in (8, 12, 20):
        run = 0; mxr = 0; at = 0
        for s, l, _, _ in best:
            run = run + 1 if l >= thr else 0
            if run > mxr: mxr = run; at = s
        print('thr', thr, 'longest consecutive run', mxr, 'ending at step', at)
