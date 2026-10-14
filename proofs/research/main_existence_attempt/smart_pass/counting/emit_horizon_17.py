"""Emit the exact timed-out length-17 query without launching a solver."""
from pathlib import Path
import z3
BASE=Path(__file__).parent
T=[list(map(int,line.split())) for line in(BASE/'compact_transitions.txt').read_text().splitlines()]
s=z3.Solver();old=[z3.BoolVal(True)]*240
for k in range(1,18):
 y=z3.BitVec('y_'+str(k),3);new=[z3.Bool('s_%d_%d'%(k,v)) for v in range(240)]
 for v in range(240):
  cases=[]
  for q in range(8):
   a,b=T[v][q],T[v][q+8]
   if a>=0 and b>=0:cases.append(z3.And(y==q,old[a],old[b]))
  s.add(new[v]==z3.Or(cases))
 old=new
s.add(z3.Or([old[15*g+14] for g in range(16)]))
(BASE/'rho_horizon_17_unknown.smt2').write_text('(set-option :timeout 60000)\n'+s.to_smt2())
print('Saved length-17 formula; status remains UNKNOWN.')
