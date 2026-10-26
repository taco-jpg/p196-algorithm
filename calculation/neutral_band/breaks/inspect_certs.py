import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N
from neutral_band_search import *
_lean_certs = N._lean_certs
for b, es in _lean_certs():
    print(f"=== base {b}: {len(es)} edges")
    for E in es:
        B,C,B2,C2,u,v = E
        print(f"  |B|={len(B):3d} |C|={len(C):3d} e1={e1(b,B)} e2={e2(b,B,C)} gam={gam(b,B,C)} u={u} v={v} Csym={C==C[::-1]}  nextC-len={len(nextC(b,B,C))}")
