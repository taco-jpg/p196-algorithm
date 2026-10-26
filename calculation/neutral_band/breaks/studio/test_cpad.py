"""test_cpad.py -- validation of ccycle_padded.solve_C: B-streams from bcore, then C, then library replay.  Seconds to ~1-2 min.
  python3 test_cpad.py 26 4 | 16 5 | 4 6 | 17 6 ...   (arguments: base p [zhi])"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from bcore import decide, patterns
from ccycle_padded import solve_C, real_part

b = int(sys.argv[1]); p = int(sys.argv[2]); zhi = int(sys.argv[3]) if len(sys.argv) > 3 else 30
tl = float(sys.argv[4]) if len(sys.argv) > 4 else 20
t00 = time.time()
for O in patterns(p, 1, None):
    st, ns, res = decide(b, p, O, 3_000_000, collect=True)
    if st != 'EXISTS':
        continue
    for e1s, B in res:
        gs = list(O); es = list(e1s)
        if sum(gs) % 2:
            gs *= 2; es *= 2
        print("stream O", O, "e1", e1s, "B", B, flush=True)
        for Z0 in range(3, zhi + 1):
            t0 = time.time()
            s, rows = solve_C(b, es, gs, Z0, tl, 1)
            print(f"  Z0={Z0}: {s} ({time.time()-t0:.1f}s)", flush=True)
            if rows:
                C0 = real_part(b, rows[0])
                r = run(b, list(B), C0, maxsteps=4000, maxlen=2000)
                print("  C0", C0, "library:", r[0], end=" ")
                if r[0] == 'cycle':
                    E = r[1]
                    print("edges", len(E), "cycleOK", cycleOK(b, E, E[0][0], E[0][1]), "is_cert", is_cert(b, E), "sumGam", sum(gam(b, e[0], e[1]) for e in E))
                else:
                    print(r)
                break
            if time.time() - t00 > 100:
                print("time budget reached"); sys.exit()
