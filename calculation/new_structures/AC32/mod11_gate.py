#!/usr/bin/env python3
"""Phase-11 uniform odd-centre mod-11 necessary gate; not endpoint-only pruning."""
from itertools import product
from collections import Counter
B=[5,2,3,3,3,16,9,7,18,6,0,1,5,8,13,9,18,12,12,8,12,8,17,9,6,14,5,18,14,11,12,11,9,12]
W=[2,9,2,4,0,17,11,9,12]
C=[4,14,4]
def A(x):return sum((-1)**i*a for i,a in enumerate(x))
def Uwords():
 for a in range(0,19,2):
  v=[9,a,18-a]
  for shift in range(3):yield tuple(v[shift:]+v[:shift])
def analytic(q,k,J,U):
 s=(-1)**q
 return 2*A(B)+2*(q%2)*A(W)+2*s*A(J)-2*s*(k%2)*A(U)-(-1)**(q+k)*A(C)
def direct(q,k,J,U):
 h=B+W*q+list(J)+list(U)*k;p=h+C+h[::-1]
 return A(p)
if __name__=='__main__':
 assert (A(B),A(W),A(C))==(6,-12,-6)
 for U in Uwords():
  for J in ([0]*5,[3,2,10,1,4],[18]*5):
   for q,k in product(range(1,8),range(1,8)):
    assert analytic(q,k,J,U)==direct(q,k,J,U)
 eligible=[u for u in Uwords() if (A(u)+6)%11==0]
 assert eligible==[(9,0,18),(18,0,9)]
 dp={0:1}
 for sign in (1,-1,1,-1,1):
  nxt=Counter()
  for residue,count in dp.items():
   for v in range(19):nxt[(residue+sign*v)%11]+=count
  dp=nxt
 assert sum(dp.values())==19**5 and dp[2]==225117
 print('A(B), A(W), A(C):',A(B),A(W),A(C))
 print('Eligible U:',eligible)
 print('J count:',dp[2],'of',19**5)
 print('Survivors:',len(eligible)*dp[2],'of',30*19**5)
 print('ALL_PARITY_DIRECT_CHECKS_PASSED')
