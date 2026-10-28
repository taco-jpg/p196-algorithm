import sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
from replay_sym import lattice, parse, axes
def run(b, fn, ri, maxper=40, verbose=True):
    rec = parse(fn)[ri]; L = lattice(rec, b)
    p, nB, m, gam = L['p'], L['nB'], L['m'], L['gam']
    w0 = tuple(L['Wt'][0])
    out = []
    for a in axes(w0):
        for r1 in range(m):
            for e in (0, 1):
                if (2 * r1 + e) % m != (a + 1) % m: continue
                Hs = [('L', tuple(L['Bt'][0])), ('B', w0, 0)]
                if r1: Hs.append(('L', w0[:r1]))
                core = (w0[r1 % m],) if e else ()
                T = Template(b, Hs, core)
                cur = T; seen = {}; tot = 0; status = None
                try:
                    for t in range(p * maxper + 1):
                        key = (t % p, cur)
                        if key in seen:
                            t0, tot0 = seen[key]
                            status = ('CYCLE', t0, t - t0, tot - tot0); break
                        seen[key] = (t, tot)
                        nxt, gm, info = step(cur)
                        if not info['differs']: status = ('PALINDROME', t); break
                        if any(v[1] != 1 for v in gm.values()): status = ('MULT!=1', t); break
                        tot += sum(v[2] for v in gm.values())
                        cur = nxt
                except (Ambiguous, Unsupported) as ex:
                    status = ('ENGINE-UNSUPPORTED', str(ex)[:60])
                out.append((a, r1, e, status))
                if verbose: print(f'base {b} rec {ri} axis {a} r1={r1} e={e}: {status}')
    return out
if __name__ == '__main__':
    run(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
