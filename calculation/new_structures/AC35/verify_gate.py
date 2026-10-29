#!/usr/bin/env python3
"""Independent residue DP for the all-width odd-centre gate and true-bigint controls."""
from collections import Counter
from scan import rotations,run
D={0:1}
for i in range(1,6):
 E=Counter()
 for r,c in D.items():
  for digit in range(19):E[(r+(-1 if i%2 else 1)*digit)%11]+=c
 D=E
counts=[D[(3-j)%11] for j in range(19)]
assert sum(counts)==4276882 and counts[0]==225077
eligible=[]
for rank,U in enumerate(rotations()):
 a=sum((1 if i%2==0 else -1)*d for i,d in enumerate(U))
 if a%11==5:eligible.append(rank)
assert eligible==[0,28]
for j0 in range(19):
 for rank in eligible:
  v=run((j0,0,1,2,3,4),rotations()[rank],(4,14,4),14,100)
  assert v['overflow_sum']==30 and not v['return'] and v['first_mismatch']<160
print('PASS: 19^6',19**6,'gate',sum(counts),'per U; ranks 0/28; 38 true-bigint controls')
print('J0 counts:',counts)
