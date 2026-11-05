"""N12 cut states u_h (bx format) for h = 0..W, from n12_wit.txt; verifies the witness under the exact mirror first."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import neutral_band_search as nb
b = 10
rows = [list(map(int, l.split(','))) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'n12_wit.txt')) if l.strip()]
def step(B):
    E1 = nb.e1(b, B); C = [0] if E1 == 1 else [10]
    g = nb.gam(b, B, C); B2 = nb.nextB(b, B, C)
    while B2 and B2[-1] == 9: B2 = B2[:-1]
    return B2, g, E1
gs, es = [], []
for t in range(12):
    B2, g, E1 = step(rows[t]); gs.append(g); es.append(E1)
    assert B2 == rows[(t + 1) % 12], t
gw = ''.join(map(str, gs)); ew = ''.join(map(str, es))
# rotate so that clock is 000100010001
r = next(r for r in range(12) if (gw[r:] + gw[:r]) == '000100010001')
R = rows[r:] + rows[:r]; gw = gw[r:] + gw[:r]; ew = ew[r:] + ew[:r]
print('# clock', gw, 'e1', ew, 'widths', [len(x) for x in R], file=sys.stderr)
W = max(len(x) for x in R) + 2
X = [x + [9] * (W - len(x)) for x in R]
# backward carries H[t][i] = carry into position i from above (H[t][W] = 1 - e1), forward L[t][i]
out = []
for h in range(W + 1):
    Lb = Hb = 0; Y = []
    for t in range(12):
        x = X[t]
        Hc = [0] * (W + 1); Hc[W] = 1 - es[(t + r) % 12] if False else 1 - int(ew[t])
        for i in range(W - 1, -1, -1): Hc[i] = (x[i] + Hc[i + 1]) // b
        assert Hc[0] == int(gw[t])
        Lc = [0] * (W + 1)
        for i in range(W): Lc[i + 1] = (x[i] + Lc[i]) // b
        if h == 0: l, hh, y = 0, int(gw[t]), 1
        else: l, hh, y = Lc[h], Hc[h], (x[h - 1] + Hc[h]) % b
        Lb |= l << t; Hb |= hh << t
        if gw[t] == '1': Y.append(y)
    out.append((h, Lb, Hb, Y))
    print(h, Lb, Hb, ' '.join(map(str, Y)))
