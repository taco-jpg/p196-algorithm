import sys, time
from hsurv import survive
from runsat import stream
name = sys.argv[1]; lp = sys.argv[2]; Wmax = int(sys.argv[3]); Tcap = int(sys.argv[4])
loops = {'0': [0], '18': [18], '6': [6, 12], '2': [2, 4, 8, 16, 14, 10]}[lp]
cyc = stream(name); p = len(cyc)
for W in range(0, Wmax + 1):
    best = 0; bt = None
    for t0 in range(p):
        for s in range(len(loops)):
            # extend T while feasible
            T = max(1, best)  # only need to beat the best so far: test T=best+1 first
            while T <= Tcap:
                gam = [cyc[(t0 + t) % p][1] for t in range(T)]; e1 = [cyc[(t0 + t) % p][2] for t in range(T)]
                cs = [loops[(s + t) % len(loops)] for t in range(T)]
                st, _ = survive(10, gam, e1, cs, W, 60)
                if st in ('OPTIMAL', 'FEASIBLE'):
                    if T > best: best = T; bt = (t0, s)
                    T += 1
                else: break
    print(name, lp, 'W', W, 'max survival T*', best, 'at (t0,s)', bt, flush=True)
