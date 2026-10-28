import sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from replay_sym import lattice, parse, axes
b = int(sys.argv[1]); fn = sys.argv[2]; ri = int(sys.argv[3]); e = int(sys.argv[4]); periods = int(sys.argv[5])
rec = parse(fn)[ri]; L = lattice(rec, b)
p, nB, m, gam = L['p'], L['nB'], L['m'], L['gam']
T = Template(b, [('L', tuple(L['Bt'][0])), ('B', tuple(L['Wt'][0]), 0)], tuple(L['Wt'][0]) if e else ())
cur = T; seen = {}; tot = 0
for t in range(p * periods + 1):
    key = (t % p, cur)
    if key in seen:
        t0, tot0 = seen[key]
        print(f'CYCLE: template at step {t} equals step {t0}; steps {t-t0}; gap offset per cycle {tot - tot0}')
        break
    seen[key] = (t, tot)
    nxt, gm, info = step(cur)
    assert info['differs']
    assert all(v[1] == 1 for v in gm.values())
    tot += sum(v[2] for v in gm.values())
    cur = nxt
    lit = [len(it[1]) for it in cur.Hs if it[0] == 'L']; band = [len(it[1]) for it in cur.Hs if it[0] == 'B']
    if t % p == p - 1: print('period', (t + 1) // p, 'literal lens', lit, 'band lens', band, 'core', len(cur.core), 'gap total offset', tot)
