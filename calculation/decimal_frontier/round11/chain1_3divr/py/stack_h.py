"""Closure test (b) of stack_uniform.py for every N12 cut u_h (h=0..W) instead of only the 9-sea cut.
(b_h): CL(AT_h) subset CL(A_h). If it holds, the cut set above u_h^k is CL_k(A_h) at every height, for every k."""
import sys, itertools
from collections import deque
src = open("stack_uniform.py").read()
pre = src.split("# --- A: edges")[0]
cuts = [list(map(int, l.split())) for l in open("n12cuts.txt") if l.strip()]
CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 3000000; sys.argv = sys.argv[:1]
for row in cuts:
    h, Lb, Hb = row[:3]; Y = row[3:]
    ns = {}; exec(pre, ns)
    g = ns["g"]; P = 12; b = 10; yi = iter(Y)
    u = []
    for f in range(P):
        u.append(((Lb >> f) & 1, (Hb >> f) & 1, next(yi) if g[f] else 0))
    ns["u"] = u
    body = src.split("# --- A: edges")[1].split("# cycles of accepting")[0]
    body = body.replace("while dq and bad is None:", "while dq and bad is None and len(seen) < CAP:").replace("    nstates += len(seen)", "    nstates += len(seen); CAPHIT[0] |= len(seen) >= CAP")
    ns["CAP"] = CAP; ns["CAPHIT"] = [False]
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec("# --- A: edges" + body, ns)
    capped = ns["nstates"] >= CAP
    print(h, buf.getvalue().strip(), "CAPPED(HOLDS not proved)" if ns["CAPHIT"][0] else "", flush=True)
