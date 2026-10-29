#!/usr/bin/env python3
"""Independent brute-force graph and ordinary integer digit-normalization checks.
Does not import primary.py or use its recurrence or carry normalizer.
"""
from collections import defaultdict
from itertools import product
from pathlib import Path
from random import Random
ROOT=Path(__file__).resolve().parent
W0=[int(x) for x in (ROOT/'rec2_w0.txt').read_text().split()]
B=[[int(x) for x in line.split()] for line in (ROOT/'rec2_prefix.txt').read_text().splitlines()]
assert len(W0)==48 and len(B)==8 and all(len(x)==11 for x in B)

def digit_normalize(P):
 """Create an ordinary base-10 integer with mirrored pairword P, then add its reversal."""
 hi=[min(9,p) for p in P];lo=[p-h for p,h in zip(P,hi)]
 D=lo+list(reversed(hi));n=len(D)
 assert all(0<=v<=9 for v in D)
 C=[0];O=[]
 for j in range(n):
  total=D[j]+D[n-1-j]+C[-1]
  O.append(total%10);C.append(total//10)
 if C[-1]:O.append(C[-1])
 return D,O,C

def bits(P,C,j):
 n=len(P);assert j+2<n
 x,y,z=P[j:j+3]
 a,A,Z=C[j:j+3]
 d,D,F=(C[2*n-1-j-k] for k in range(3))
 return (x&1)|((y&1)<<1)|((z&1)<<2)|(a<<3)|(A<<4)|(Z<<5)|(d<<6)|(D<<7)|(F<<8)

def boundary(b):
 return ((b&1)|(((b>>1)&1)<<1)|(((b>>3)&1)<<2)|(((b>>4)&1)<<3)|(((b>>6)&1)<<4)|(((b>>7)&1)<<5))

def rank_low(rows):
 piv={}
 for x in rows:
  while x:
   k=(x&-x).bit_length()-1
   if k not in piv:piv[k]=x;break
   x^=piv[k]
 return len(piv)

def feature(P):
 # Genuine 384-digit schoolbook integer carries, with four periodic copies.
 R=P*4;_,_,C=digit_normalize(R);out=0
 for j in range(48,96):
  b=bits(R,C,j)
  for mask in range(512):
   if b&mask==mask:out^=1<<mask
 return out

def graph():
 # Independent enumeration by gluing pairs of 76 physical carry states.
 V=list(product(range(19),range(2),range(2)))
 I={v:i for i,v in enumerate(V)}
 out=[[] for _ in V];incoming=[[] for _ in V];E=[]
 for u,(p,a,d) in enumerate(V):
  for q in range(19):
   for A,D in product(range(2),repeat=2):
    if A!=(p+a)//10 or d!=(q+D)//10:continue
    v=I[q,A,D];k=len(E);E.append((u,v));out[u].append(k);incoming[v].append(k)
 assert len(E)==1444
 allowed={};count=0
 for mid in range(len(V)):
  for ei in incoming[mid]:
   u,_=E[ei]
   for ej in out[mid]:
    _,w=E[ej];p,a,d=V[u];q,A,D=V[mid];r,Z,F=V[w]
    b=(p%2)|((q%2)<<1)|((r%2)<<2)|(a<<3)|(A<<4)|(Z<<5)|(d<<6)|(D<<7)|(F<<8)
    l=boundary(b);rr=((q&1)|((r&1)<<1)|(A<<2)|(Z<<3)|(D<<4)|(F<<5))
    assert b not in allowed or allowed[b]==(l,rr)
    allowed[b]=(l,rr);count+=1
 assert count==27436 and len(allowed)==288
 return allowed

def run():
 allowed=graph();adj=[set() for _ in range(64)]
 for u,v in allowed.values():adj[u].add(v);adj[v].add(u)
 assert all(adj)
 seen={0};stack=[0]
 while stack:
  x=stack.pop()
  for y in adj[x]:
   if y not in seen:seen.add(y);stack.append(y)
 assert len(seen)==64 and sum(u==v for u,v in allowed.values())==6
 rng=Random(9396)
 words=[[rng.randrange(19) for _ in range(48)] for _ in range(229)]
 assert rank_low(feature(P) for P in words)==224
 W=[W0];ph=[];allstates=set()
 for t in range(8):
  P=B[t]+W[t]*4;h=len(P)
  D,O,C=digit_normalize(P)
  assert D[-1]>0 and len(O)==2*h+(1-t%2)
  g=1-t%2
  # Negative control: the opposite overflow shift must fail on a bulk cell.
  assert any(O[j]+O[2*h-1-j+(1-g)] != O[j]+O[2*h-1-j+g] for j in range(11+48,11+96))
  nxt=[];st=[]
  for j in range(11+48,11+48*3):
   nxt.append(O[j]+O[2*h-1-j+g])
   b=bits(P,C,j);assert b in allowed
   st.append(boundary(b))
  if t==7:assert nxt==[W0[j%48] for j in range(48,144)]
  if t<7:
   new=[O[j]+O[2*h-1-j+g] for j in range(11+48,11+96)]
   W.append(new)
  assert st[:48]==st[48:96]
  phase=len(set(st[:48]));ph.append(phase);allstates.update(st)
  for L in range(48):
   for n in (1,2,3,4,7,11,24,47,48,49,96):
    for k in range(1,64):
     lhs=sum((st[(L+i)%48]==k)^(st[(L+i+1)%48]==k) for i in range(n))%2
     rhs=(st[L]==k)^(st[(L+n)%48]==k)
     assert lhs==rhs
 assert ph==[35,29,27,35,35,29,27,35] and len(allstates)==64
 assert W[-1]!=W0 and len(W)==8
 print('INDEPENDENT PASS: 76-state / 1444-edge physical carry graph, 27436 triples, 288 9-bit patterns')
 print('INDEPENDENT PASS: 229 genuine schoolbook integer reverse-add samples rank224')
 print('INDEPENDENT PASS: 8 rec2 prefix-controlled genuine integer overflows and 768 bulk pairword checks')
 print('INDEPENDENT PASS: all 64 6-bit endpoint signatures; 8*48*11 interval telescope controls')
if __name__=='__main__':run()
