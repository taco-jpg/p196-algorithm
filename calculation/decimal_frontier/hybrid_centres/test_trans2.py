import random, sys, time, math
from htrans import decide
from hsat import solve
from runbase import loops
from streams_all import collect
S = collect()
bases = [int(x) for x in sys.argv[1].split(',')]
Wsat = int(sys.argv[2]); Tmax = int(sys.argv[3])
agree = bad = nsucc = nex = 0; t0 = time.time()
for b in bases:
    for (g, e) in sorted(S.get(b, []), key=lambda x: (len(x[0]), x)):
        p = len(g)
        for lp in loops(b):
            per = len(lp); T0 = p; T = T0 * per // math.gcd(T0, per)
            if T > Tmax: continue
            gam = [int(g[t % p]) for t in range(T)]; e1 = [int(e[t % p]) for t in range(T)]
            for s in range(per):
                cs = [lp[(s + t) % per] for t in range(T)]
                for A in range(0, sum(gam) // 2 + 1):
                    res = decide(b, gam, e1, cs, A, cap=400000)
                    if res[0] == 'CAP': print('cap', b, g, e, lp, s, A); continue
                    if res[0] == 'SUCCESS':
                        nsucc += 1
                        st, Q0 = solve(b, gam, e1, cs, max(Wsat, res[1]), A, tl=60)
                        ok = st in ('OPTIMAL', 'FEASIBLE')
                        print('SUCC', b, g, e, lp, 's', s, 'A', A, 'layers', res[1], 'path', res[2], 'SAT', st[:3], flush=True)
                    else:
                        nex += 1
                        st, Q0 = solve(b, gam, e1, cs, Wsat, A, tl=60)
                        ok = (st == 'INFEASIBLE')
                    if ok: agree += 1
                    else: bad += 1; print('DISAGREE', b, g, e, lp, s, A, res[:2], st)
print('tests', agree + bad, 'agree', agree, 'success', nsucc, 'exhausted', nex, 'bad', bad, round(time.time() - t0, 1), 's')
