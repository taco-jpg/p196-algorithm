import sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from replay_sym import lattice, parse, axes
def run(b, fn, ri, e, periods=3, verbose=True):
    rec = parse(fn)[ri]; L = lattice(rec, b)
    p, nB, m, gam = L['p'], L['nB'], L['m'], L['gam']
    assert m == 1
    T = Template(b, [('L', tuple(L['Bt'][0])), ('B', tuple(L['Wt'][0]), 0)], tuple(L['Wt'][0]) if e else ())
    cur = T; tot = 0
    for t in range(p * periods):
        try:
            nxt, gm, info = step(cur)
        except Exception as ex:
            print('engine exception at step', t, type(ex).__name__, ex); return None
        off = sum(v[2] for v in gm.values()); mult = [v[1] for v in gm.values()]
        tot += off
        if not info['differs']:
            print('palindrome flag at step', t); return None
        cur = nxt
        if (t + 1) % p == 0:
            same = (cur == T)
            if verbose: print(f'period {(t+1)//p}: template==start? {same}; cumulative gap offset {tot}; mult {mult}; e-parity core len {len(cur.core)}')
    return True
b = int(sys.argv[1]); fn = sys.argv[2]; ri = int(sys.argv[3])
for e in (0, 1):
    print('e =', e); run(b, fn, ri, e)
