#!/usr/bin/env python3
"""Independent arithmetic audit and genuine-bignum near-miss checks."""
from collections import Counter
from independent import test
U=((9,0,18),(9,8,10),(9,16,2))
assert tuple((u[0]-u[1]+u[2])%11 for u in U)==(5,0,6)
D=Counter({0:1})
for sign in (-1,1,-1,1,-1):
 N=Counter()
 for r,n in D.items():
  for x in range(19):N[(r+sign*x)%11]+=n
 D=N
assert sum(D.values())==19**5 and D[3]==225077
brute=0
for z in range(19**5):
 v=z;J=[0]
 for i in range(5):J.append(v%19);v//=19
 if (2*(J[0]-J[1]+J[2]-J[3]+J[4]-J[5])-6)%11==0:brute+=1
assert brute==225077
near=[
 ([0,18,4,11,0,5],145),([0,9,4,1,17,8],145),
 ([0,18,13,1,17,8],145),([0,9,9,5,0,14],144),
 ([0,18,18,5,0,14],144),([0,18,18,14,9,14],144)]
checks=0
for J,first in near:
 for q,k in ((14,100),(20,100),(40,160),(80,320),(160,640)):
  z=test(0,1,J,q,k)
  assert z["first_mismatch"]==first+9*(q-14)
  assert z["gamma"]=="1000"*30 and z["palindrome_at"]==-1
  assert not z["returning"]
  checks+=1
print("225077/2476099 mod-11 survivors and",checks,"near-miss bigint checks PASS")
