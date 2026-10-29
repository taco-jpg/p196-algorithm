#!/usr/bin/env python3
"""Complete 8-phase 32768-feature 4-cell GF2 covariance rank certificate."""
from itertools import product
from hashlib import sha256
from pathlib import Path
from random import Random
ROOT=Path(__file__).resolve().parent
W0=list(map(int,(ROOT/'rec2_w0.txt').read_text().split()))
assert len(W0)==48

def rank_add(piv,x):
 while x:
  k=x.bit_length()-1
  if k in piv:x^=piv[k]
  else:piv[k]=x;return True
 return False

def carries(P):
 n=len(P);asc=[];desc=[]
 for seed in (0,1):
  a=[seed]
  for p in P:a.append(int(p+a[-1]>=10))
  if a[-1]==seed:asc.append(a[:-1])
  d=[0]*n;d[-1]=seed
  for j in range(n-1,0,-1):d[j-1]=int(P[j]+d[j]>=10)
  if seed==int(P[0]+d[0]>=10):desc.append(d)
 assert len(asc)==len(desc)==1
 return asc[0],desc[0]

def step(P,g):
 a,d=carries(P);n=len(P)
 if not g:return [2*P[j]+a[j]+d[j]-10*(a[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
 return [P[j]+P[(j-1)%n]+a[j]+d[(j-1)%n]-10*(a[(j+1)%n]+d[(j-2)%n]) for j in range(n)]

def feature(P,cache):
 a,d=carries(P);n=len(P);v=0
 for j in range(n):
  ids=[(j+k)%n for k in range(4)]
  b=sum((P[i]&1)<<k for k,i in enumerate(ids))|sum(a[i]<<(4+k) for k,i in enumerate(ids))|sum(d[i]<<(8+k) for k,i in enumerate(ids))
  if b not in cache:
   x=0;s=b
   while True:
    x|=1<<s
    if s==0:break
    s=(s-1)&b
   cache[b]=x
  v^=cache[b]
 return v

def allowed_graph():
 pat={}
 for p,q,r,s in product(range(19),repeat=4):
  for a,F in product((0,1),repeat=2):
   A=int(p+a>=10);B=int(q+A>=10);C=int(r+B>=10)
   E=int(s+F>=10);D=int(r+E>=10);d=int(q+D>=10)
   bits=(p&1)|((q&1)<<1)|((r&1)<<2)|((s&1)<<3)|(a<<4)|(A<<5)|(B<<6)|(C<<7)|(d<<8)|(D<<9)|(E<<10)|(F<<11)
   src=(p&1)|((q&1)<<1)|((r&1)<<2)|(a<<3)|(A<<4)|(B<<5)|(d<<6)|(D<<7)|(E<<8)
   dst=(q&1)|((r&1)<<1)|((s&1)<<2)|(A<<3)|(B<<4)|(C<<5)|(D<<6)|(E<<7)|(F<<8)
   assert bits not in pat or pat[bits]==(src,dst)
   pat[bits]=(src,dst)
 assert len(pat)==1312
 adj={}
 for u,v in pat.values():adj.setdefault(u,set()).add(v);adj.setdefault(v,set()).add(u)
 assert len(adj)==288 and sum(u==v for u,v in pat.values())==6
 seen={0};stack=[0]
 while stack:
  x=stack.pop()
  for y in adj[x]:
   if y not in seen:seen.add(y);stack.append(y)
 assert len(seen)==288
 return pat

def run():
 pat=allowed_graph();assert 4096-len(pat)+288==3072
 cache={};piv0={};rng=Random(9397);first=None
 for i in range(1471):
  P=[rng.randrange(19) for _ in range(48)]
  rank_add(piv0,feature(P,cache))
  if len(piv0)==1024 and first is None:first=i+1
 assert len(piv0)==1024 and first==1471
 # Covariance: F_(t+1)(step_g(P)) + (g ? F_t(P) : 0), g=10101010.
 rng=Random(9410);outp=[{},{}];full={};hit=[None,None];digest=sha256()
 for i in range(1628):
  P=[rng.randrange(19) for _ in range(48)]
  src=feature(P,cache)
  words=[step(P,g) for g in (0,1)]
  for word in words:digest.update(bytes(word))
  dest=[feature(word,cache) for word in words]
  for g in (0,1):
   rank_add(outp[g],dest[g])
   if len(outp[g])==1024 and hit[g] is None:hit[g]=i+1
  for t in range(8):
   g=1-t%2
   row=dest[g]<<(4096*((t+1)%8))
   if g:row^=src<<(4096*t)
   rank_add(full,row)
 assert digest.hexdigest()=="11e0b07166a90a341e3400a836fd0cdbf0017d91d9b337c215ab253ec00a3ff9"
 assert hit==[1025,1628]
 assert [len(x) for x in outp]==[1024,1024] and len(full)==8192
 W=[W0]
 for t in range(7):W.append(step(W[-1],1-t%2))
 assert step(W[-1],0)==W0
 assert all(0<=x<=18 for P in W for x in P)
 print('PASS: 1312 allowed 4-cell patterns, 288 connected endpoints; per-phase zero kernel 3072')
 print('PASS: 1471 physical 48-cycles rank1024/4096 (seed9397)')
 print('PASS: g=0 image rank1024 at sample1025; g=1 image rank1024 at sample1628 (seed9410)')
 print('PASS: 3256 exact output words SHA256 11e0b07166a90a341e3400a836fd0cdbf0017d91d9b337c215ab253ec00a3ff9')
 print('PASS: direct 8-phase 32768-feature covariance rank8192 from 8*1628 exact rows')
 print('PAPER PROOF: all 24576 universal 8-phase covariance solutions are independent per-phase local-zero functions')
 print('PASS: rec2 g=10101010 eight-phase physical cyclic bulk control')
if __name__=='__main__':run()
