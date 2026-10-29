#!/usr/bin/env python3
"""Independent generic carry/digit recurrence at three positions for test parameters."""
import sys,json
w=json.load(open(sys.argv[1]));g=[int(x) for x in w['g']]
for n in [0,1,2,3,10,100,1000,1000000]:
 base=w['base']+n*w['step']
 rows=[[w[name][t]+n*w[name+'Slope'][t] for t in range(22)] for name in ('first','second','third')]
 assert all(x[0]==x[-1] for x in rows)
 for t,overflow in enumerate(g):
  carry_from_lower=0;high=overflow;partner=1
  for j in range(3):
   coeff=rows[j][t];higher_carry=w['c'+str(j)][t]
   assert (coeff+higher_carry)//base==high
   assert 0<=coeff<=2*base-2 and (j>0 or coeff>0)
   value=(coeff+carry_from_lower)%base+(partner if overflow else (coeff+higher_carry)%base)
   assert value==rows[j][t+1],(n,t,j,value,rows[j][t+1])
   partner=(coeff+higher_carry)%base
   carry_from_lower=(coeff+carry_from_lower)//base
   high=higher_carry
 print('INDEPENDENT 3-POSITION REPLAY PASS',n,'base',base,'starting',tuple(x[0] for x in rows))
print('All independent checks use generic divmod for each spatial cut and temporal step')
