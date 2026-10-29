#!/usr/bin/env python3
"""Independent arithmetic proof/check for odd-centre modulo-11 necessary gate."""
from pathlib import Path
from independent import read,ulist,templ
LATTICE=(Path(__file__).with_name('lattice.txt') if Path(__file__).with_name('lattice.txt').exists() else Path(__file__).resolve().parents[2]/'decimal_frontier/lattice_kinks/data/lat_p12m9.txt')
B,W=read(LATTICE)
C=[4,14,4]
A=lambda x:sum(v*(-1)**i for i,v in enumerate(x))
assert (A(B),A(W),A(C))==(-6,12,-6)
assert (2*A(B)+A(W))%11==0
Ugood=[(i,u) for i,u in enumerate(ulist()) if (A(u)-A(C))%11==0]
assert Ugood==[(0,[9,0,18]),(28,[18,0,9])],Ugood
cnt=[0]*11;cnt[0]=1
for sign in (1,-1,1,-1,1):
 nxt=[0]*11
 for r,x in enumerate(cnt):
  for a in range(19):nxt[(r+sign*a)%11]+=x
 cnt=nxt
assert sum(cnt)==19**5
assert cnt[3]==225121, cnt
Js=[[0,0,0,0,3],[18,18,18,18,3],[2,6,9,6,4]]
for J in Js:
 if A(J)%11!=3:continue
 for _,u in Ugood:
  for q,k in ((14,100),(14,101),(15,100),(15,101)):
   assert A(templ(B,W,J,u,C,q,k))%11==0,(J,u,q,k)
print('ODD_C_MOD11_GATE_PASS','Uindices0based',[i for i,_ in Ugood],'J_count_per_U',cnt[3],'total',2*cnt[3])
print('RESIDUES',cnt)
