"""Agent #101 review of Agent #5's claim (issue #5): M' = 2M - gamma*c (mod 9),
M = sum(B) - c*len(B), over every trimmed exterior state with |B| <= L."""
import itertools, sys
from exterior_ref import step
L = int(sys.argv[1]); bad = 0; n = 0
for c in [2,4,6,8,10,12,14,16]:
    Bs = [()] + [(f,)+r for b in range(1,L+1) for f in range(1,19) for r in itertools.product(range(19),repeat=b-1)]
    for B in Bs:
        if B and B[-1]==c: continue
        cp,Bp,g = step(c,list(B)); n += 1
        M = sum(B)-c*len(B); Mp = sum(Bp)-cp*len(Bp)
        if (Mp - (2*M - g*c)) % 9: bad += 1
print(f"cap={L} states={n} violations={bad}")
