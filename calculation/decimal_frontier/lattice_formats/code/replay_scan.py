import sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from replay_int import *
def one(b, fn, ri, l0, periods):
    rec = parse(fn)[ri]; L = lattice(rec, b)
    p, nB, m, gam = L['p'], L['nB'], L['m'], L['gam']
    w0 = L['Wt'][0]
    res = {}
    for a in axes(w0):
        if (l0 % m) != (a + 1) % m: continue
        P = build_pair(L['Bt'][0], w0, l0)
        try: d = split_pair(P, b)
        except AssertionError: return 'nosplit'
        N = d
        if N == N[::-1]: return 'N0pal'
        l = l0
        for t in range(p * periods):
            N = rev_add(N, b)
            if N == N[::-1]: return 'pal@%d' % (t + 1)
            Pn = [N[i] + N[len(N) - 1 - i] for i in range(len(N))]
            tt = (t + 1) % p; l += gam[t % p]
            if Pn != build_pair(L['Bt'][tt], L['Wt'][tt], l): return 'mismatch@%d' % (t + 1)
        return 'ok'
    return 'noaxis'
b = int(sys.argv[1]); fn = sys.argv[2]; ri = int(sys.argv[3]); lo = int(sys.argv[4]); hi = int(sys.argv[5]); per = int(sys.argv[6])
from collections import Counter
cnt = Counter(); first_ok = None; bad = []
for l0 in range(lo, hi):
    r = one(b, fn, ri, l0, per)
    cnt[r] += 1
    if r == 'ok' and first_ok is None: first_ok = l0
    if r not in ('ok', 'nosplit', 'noaxis'): bad.append((l0, r))
print('base', b, 'rec', ri, 'l0 in', (lo, hi), dict(cnt), 'first ok', first_ok, 'failures', bad[:12], '...' if len(bad) > 12 else '')
