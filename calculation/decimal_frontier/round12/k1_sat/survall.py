# lifetime for every start phase r (0..m-1) and both centre parities, width w: max per class o = n mod 4
import sys, time
from tsat import *
lat = load_lattice(sys.argv[1]); w = int(sys.argv[2]); Hs = int(sys.argv[3])
best = {}
for r in range(lat.m):
    for Lc in (2*w, 2*w-1):
        part = lat.W[0][:r]; C = fixed_centre_specs(Lc); c0 = part + C + part[::-1]
        n = 2*(lat.nB + 5*lat.m + r) + Lc; o = n % 4
        H = Hs; last = None
        while True:
            G = sum(lat.g[t % lat.p] for t in range(H))
            I = Inst(lat, 5, H, 0, c0, [None]*(len(c0)+G))
            ok, model, E, tenc, tt, _ = solve_inst(I, "cadical195", prefix_k=0, confine_w=w)
            if ok: last = H; H += 1
            else:
                if last is None: H -= 3; continue
                break
        best[o] = max(best.get(o, 0), last)
        print(f"r={r} Lc={Lc} o={o} lifetime={last}", flush=True)
print("MAX per class", best)
