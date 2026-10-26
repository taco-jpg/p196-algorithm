import sys
from ortools.sat.python import cp_model
import bcycle_relax as R
# re-solve p=8, K=16, M=22 and print rows (copy of model returning V)
b=10; p=8; M=26; K=20
n=b-1
import types
src=open('bcycle_relax.py').read()
src=src.replace("    return nm, ([s.Value(g) for g in gamv] if st in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None)",
 "    return nm, ([s.Value(g) for g in gamv] if st in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None), ([[s.Value(V[t][i]) for i in range(M)] for t in range(p+1)] if st in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None)")
src=src.split('if __name__')[0]
ns={}; exec(src,ns)
nm,g,rows=ns['solve_relaxed'](b,p,M,K,30)
print(nm,g)
sg=lambda b,v:'H' if v>=b else ('N' if v==b-1 else 'L')
for t,r in enumerate(rows):
    print(t, ' '.join(f"{v:2d}" for v in r))
    print('  ', ' '.join(f" {sg(b,v)}" for v in r))
