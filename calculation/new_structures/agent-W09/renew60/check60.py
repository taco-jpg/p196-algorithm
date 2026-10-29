#!/usr/bin/env python3
# Independent decimal native-integer controls of all 61 states.
import sys
sys.set_int_max_str_digits(0)
L=(2,2,11,6,0,12,15,13,3,11,7,4,13,3,17,13,0,14,11,2,10,18,10,15,4,6,4,17,12,13,15,8,1,18,0,8,14,17,8,12,18,1,10,3,8,10,4,1,0,16,14,15,16,17,15,16,16,9,13,16)
PH=(8,16,14,10,2,4)
def seed(k):
 return ''.join(str(x-x//2) for x in L)+'4'*(2*k)+''.join(str(x//2) for x in L[::-1])
def capwidth(s,x):
 p=[int(a)+int(b) for a,b in zip(s[::-1],s)]
 l=(len(p)-1)//2;r=len(p)//2
 while l>=0 and r<len(p) and p[l]==x and p[r]==x:l-=1;r+=1
 w=r-l-1
 return tuple(p[:(len(p)-w)//2]),w
ref={}
for k in (80,81,100,150):
 s=seed(k)
 for t in range(61):
  c,w=capwidth(s,PH[t%6]);assert w>=6,(k,t,w)
  assert any(x%2 for x in c),(k,t,'odd cap missing')
  state=(c,w-2*k)
  if t not in ref:ref[t]=state
  else:assert ref[t]==state,(k,t,'counter dependence')
  assert s!=s[::-1],(k,t,'palindrome')
  if t<60:s=str(int(s)+int(s[::-1]))
expected={0:0,6:-4,12:-2,18:-3,24:-3,30:-2,36:4,42:0,48:-3,54:-7,60:6}
for t,b in expected.items():assert ref[t][1]==b
assert len(ref[0][0])==60 and len(ref[60][0])==69
print('60-step genuine Python integer and all-k central-pump controls PASS')
print([(t,ref[t][1],len(ref[t][0])) for t in expected])
