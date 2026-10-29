#!/usr/bin/env python3
"""Bounded 0/9 buffer reset co-composition search, not an exclusion theorem."""
from construct import B1,W1,split,step,pairs
def trial(pos,v,L,c,ni=0):
 H=list(B1)+list(W1)*10
 if pos==0:H+=[v]*L+[5,5,2]*80+list(W1)*ni
 if pos==1:H+=[5,5,2]*80+[v]*L+list(W1)*ni
 if pos==2:H+=[5,5,2]*80+list(W1)*ni+[v]*L
 if pos==3:H+=list(W1)*ni+[v]*L+[5,5,2]*80
 return split(H+[c]+H[::-1])
success=[]
for pos in range(4):
 for L in [1,2,4,8,20,60]:
  for c in range(0,19,2):
   for ni in [0,1,3]:
    a=step(trial(pos,0,L,c,ni));b=step(trial(pos,9,L,c,ni))
    if pairs(a)==pairs(b):success.append((pos,L,c,ni))
print('720 settings, one-step equal full-pairword resets:',len(success))
assert len(success)==0
