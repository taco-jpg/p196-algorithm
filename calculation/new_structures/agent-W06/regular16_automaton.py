#!/usr/bin/env python3
"""Exact 2-state transfer automaton for 16 p8/m20 +/-9 switches.
Run from repository root: python3 calculation/new_structures/agent-W06/regular16_automaton.py
Relies only on sibling toggle_family.py (previous W06 commit).
"""
import sys
sys.set_int_max_str_digits(1000000)
import random
from toggle_family import B,W,normalize,paired,split
CAND={0:8,1:12,2:10,3:4,4:8,5:2,6:5,7:12,8:9,9:10,10:11,12:16,13:12,14:5,15:3,19:4}
SITES=sorted(CAND)
valid=[]
for mask in range(1<<len(SITES)):
    bits=[j for i,j in enumerate(SITES) if mask>>i&1]
    if any(v-u==1 for u,v in zip(bits,bits[1:])):continue
    valid.append(mask)
print('single block patterns',len(valid),'site bits',len(SITES))
mat=[[0,0],[0,0]]
for last in [0,1]:
 for mask in valid:
  if last and mask&1:continue
  mat[last][int(bool(mask & (1<<(len(SITES)-1))))]+=1
print('transfer matrix',mat)
assert mat==[[1864,1864],[1152,1152]],mat
assert len(valid)==3728

def check(m,C,masks):
 assert len(masks)==m and 0<=C<=18 and C%2==0
 h=B.copy();a=h.copy();n0=0;prev=False
 for r,mask in enumerate(masks):
  assert mask in valid
  if prev:assert not mask&1
  prev=bool(mask>>(len(SITES)-1)&1)
  h+=W
  w=W.copy()
  for bit,j in enumerate(SITES):
   if mask>>bit&1:w[j]=CAND[j]
  a+=w
 p=h+[C]+h[::-1];q=a+[C]+a[::-1];n=len(p)
 d=normalize(p);e=normalize(q)
 expected={}
 for r,mask in enumerate(masks):
  for bit,j in enumerate(SITES):
   if mask>>bit&1:
    x=len(B)+20*r+j;y=n-1-x;s=1 if CAND[j]>W[j] else -1
    for pos,di in ((x,-s),(x+1,s),(y,-s),(y+1,s)):
     assert pos not in expected
     expected[pos]=di
 actual={i:v-u for i,(u,v) in enumerate(zip(d,e)) if u!=v}
 assert len(e)==len(d)==n+1 and expected==actual,(m,C,masks,expected,actual)
 assert paired(d)==paired(e)
 return True

def independent_bigint(m,C,masks):
    assert len(masks)==m
    def pairword(seq):
        h=B.copy()
        for mask in seq:
            w=W.copy()
            for bit,j in enumerate(SITES):
                if mask>>bit&1:w[j]=CAND[j]
            h+=w
        return h+[C]+h[::-1]
    def val(p):return int(''.join(str(x) for x in split(p)[::-1]))
    def R(x):return x+int(str(x)[::-1])
    a=val(pairword([0]*m));b=val(pairword(masks))
    assert (a==b)==all(x==0 for x in masks)
    assert R(R(a))==R(R(b))
    assert str(a)!=str(a)[::-1] and str(b)!=str(b)[::-1]
    assert str(R(a))!=str(R(a))[::-1] and str(R(b))!=str(R(b))[::-1]

if __name__=='__main__':
 for C in range(0,19,2):
  for mask in valid:check(1,C,[mask])
 print('exhaustive tests',len(valid)*10)
 rng=random.Random(4740616)
 for m in (2,3,5,10,100,320,1000):
  for _ in range(40):
   masks=[];prev=0
   for r in range(m):
    mask=rng.choice(valid)
    if prev and mask&1:mask=rng.choice([x for x in valid if not x&1])
    masks.append(mask);prev=bool(mask&(1<<15))
   C=rng.randrange(10)*2
   assert check(m,C,masks)
   if _ < 5:independent_bigint(m,C,masks)
  print('tested',m)
 # Deliberately invalid adjacent switches within a period break erasure.
 assert paired(normalize((B+W*3)+[18]+(B+W*3)[::-1]))!=paired(normalize((lambda h:h+[18]+h[::-1])((B+W*3)[:39+7]+[12,9]+(B+W*3)[39+9:])))
 print('independent Python BIGINT controls',7*5,'and adjacent mutant rejected')
 for M in (1,2,3,320):
  count=3728*3016**(M-1)
  print('M',M,'count bits',count.bit_length(),'count exact',count if M<=3 else '3728*3016^319')
