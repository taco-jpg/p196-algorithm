#!/usr/bin/env python3
"""Independent 8-phase four-cell covariance rank via ordinary decimal normalization."""
from itertools import product
from hashlib import sha256
from pathlib import Path
from random import Random
ROOT=Path(__file__).resolve().parent
W0=list(map(int,(ROOT/'rec2_w0.txt').read_text().split()))
B=[list(map(int,line.split())) for line in (ROOT/'rec2_prefix.txt').read_text().splitlines()]
assert len(W0)==48 and len(B)==8 and all(len(x)==11 for x in B)

def normalize(P):
 # Digits low-to-high of a (possibly zero-padded) ordinary integer.
 hi=[min(x,9) for x in P];lo=[x-h for x,h in zip(P,hi)]
 D=lo+hi[::-1];n=len(D);O=[];C=[0]
 for j in range(n):
  v=D[j]+D[n-1-j]+C[-1];O.append(v%10);C.append(v//10)
 if C[-1]:O.append(C[-1])
 return D,O,C

def fbits(P,C,j):
 n=len(P);b=0
 for k in range(4):
  b|=(P[j+k]&1)<<k
  b|=C[j+k]<<(4+k)
  b|=C[2*n-1-j-k]<<(8+k)
 return b

def feature(P,cache):
 R=P*4;_,_,C=normalize(R);v=0
 for j in range(48,96):
  b=fbits(R,C,j)
  if b not in cache:
   x=0;s=b
   while True:
    x|=1<<s
    if s==0:break
    s=(s-1)&b
   cache[b]=x
  v^=cache[b]
 return v

def physical_step(P,g):
 # Prefix 1 enforces g=0; prefix 18 enforces g=1 for every physical P.
 R=[18 if g else 1]+P*4;h=len(R);D,O,C=normalize(R)
 assert D[-1]>0 and len(O)==2*h+g
 return [O[j]+O[2*h-1-j+g] for j in range(1+48,1+96)]

def rank_add(piv,x):
 while x:
  k=(x&-x).bit_length()-1
  if k in piv:x^=piv[k]
  else:piv[k]=x;return True
 return False

def graph_control():
 # Independent physical carry graph glued into 4-column walks.
 V=list(product(range(19),range(2),range(2)));idx={s:i for i,s in enumerate(V)}
 E=[];out=[[] for _ in V]
 for u,(p,a,d) in enumerate(V):
  for q in range(19):
   for A,D in product((0,1),repeat=2):
    if A!=(p+a)//10 or d!=(q+D)//10:continue
    v=idx[q,A,D];i=len(E);E.append((u,v));out[u].append(i)
 assert len(E)==1444
 pat={};count=0
 for u,v in E:
  p,a,d=V[u];q,A,D=V[v]
  for e in out[v]:
   _,w=E[e];r,Bb,F=V[w]
   for z in out[w]:
    _,h=E[z];s,C,G=V[h]
    bits=(p&1)|((q&1)<<1)|((r&1)<<2)|((s&1)<<3)|(a<<4)|(A<<5)|(Bb<<6)|(C<<7)|(d<<8)|(D<<9)|(F<<10)|(G<<11)
    pat[bits]=1;count+=1
 assert count==521284 and len(pat)==1312

def run():
 graph_control()
 cache={};piv={};rng=Random(9397);first=None
 for i in range(1471):
  rank_add(piv,feature([rng.randrange(19) for _ in range(48)],cache))
  if len(piv)==1024 and first is None:first=i+1
 assert len(piv)==1024 and first==1471
 rng=Random(9410);out=[{},{}];cov={};hit=[None,None];digest=sha256()
 for i in range(1628):
  P=[rng.randrange(19) for _ in range(48)]
  src=feature(P,cache)
  words=[physical_step(P,g) for g in (0,1)]
  for word in words:digest.update(bytes(word))
  dst=[feature(word,cache) for word in words]
  for g in (0,1):
   rank_add(out[g],dst[g])
   if len(out[g])==1024 and hit[g] is None:hit[g]=i+1
  for t in range(8):
   g=1-t%2
   row=dst[g]<<(4096*((t+1)%8))
   if g:row^=src<<(4096*t)
   rank_add(cov,row)
 assert digest.hexdigest()=="11e0b07166a90a341e3400a836fd0cdbf0017d91d9b337c215ab253ec00a3ff9"
 assert hit==[1025,1628] and [len(x) for x in out]==[1024,1024] and len(cov)==8192
 W=[W0]
 for t in range(8):
  R=B[t]+W[t]*4;h=len(R);D,O,C=normalize(R);g=1-t%2
  assert D[-1]>0 and len(D)==406 and len(O)==406+g
  assert any(O[j]+O[2*h-1-j+(1-g)]!=O[j]+O[2*h-1-j+g] for j in range(11+48,11+96))
  outword=[O[j]+O[2*h-1-j+g] for j in range(11+48,11+48*3)]
  assert outword[:48]==outword[48:]
  if t<7:W.append(outword[:48])
  else:assert outword[:48]==W0
 print('INDEPENDENT PASS: physical 76-state carry graph gives 1312 four-cell patterns')
 print('INDEPENDENT PASS: schoolbook 384-column seed9397 rank1024 at sample1471')
 print('INDEPENDENT PASS: actual 386-digit forced-overflow outputs g0/g1 ranks1024 at samples1025/1628')
 print('INDEPENDENT PASS: 3256 output words SHA256 11e0b07166a90a341e3400a836fd0cdbf0017d91d9b337c215ab253ec00a3ff9')
 print('INDEPENDENT PASS: 32768-feature 8-phase covariance rank8192 with lowest-bit elimination')
 print('INDEPENDENT PASS: eight 406-digit rec2 root controls and wrong-overflow negative checks')
if __name__=='__main__':run()
