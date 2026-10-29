#!/usr/bin/env python3
"""Independent 4-cell carry graph and 384/406-digit ordinary reverse-add checker."""
from itertools import product
from pathlib import Path
from random import Random
ROOT=Path(__file__).resolve().parent
W0=list(map(int,(ROOT/'rec2_w0.txt').read_text().split()))
B=[list(map(int,line.split())) for line in (ROOT/'rec2_prefix.txt').read_text().splitlines()]
assert len(W0)==48 and len(B)==8 and all(len(x)==11 for x in B)

def graph():
 V=list(product(range(19),range(2),range(2)));idx={s:i for i,s in enumerate(V)}
 E=[];out=[[] for _ in V]
 for u,(p,a,d) in enumerate(V):
  for q in range(19):
   for A,D in product((0,1),repeat=2):
    if A!=(p+a)//10 or d!=(q+D)//10:continue
    v=idx[q,A,D];e=len(E);E.append((u,v));out[u].append(e)
 assert len(E)==1444
 pat={};count=0
 for e,(u,v) in enumerate(E):
  p,a,d=V[u];q,A,D=V[v]
  for f in out[v]:
   _,w=E[f];r,Bb,F=V[w]
   for z in out[w]:
    _,h=E[z];s,C,G=V[h]
    b=(p&1)|((q&1)<<1)|((r&1)<<2)|((s&1)<<3)|(a<<4)|(A<<5)|(Bb<<6)|(C<<7)|(d<<8)|(D<<9)|(F<<10)|(G<<11)
    left=(p&1)|((q&1)<<1)|((r&1)<<2)|(a<<3)|(A<<4)|(Bb<<5)|(d<<6)|(D<<7)|(F<<8)
    right=(q&1)|((r&1)<<1)|((s&1)<<2)|(A<<3)|(Bb<<4)|(C<<5)|(D<<6)|(F<<7)|(G<<8)
    assert b not in pat or pat[b]==(left,right)
    pat[b]=(left,right);count+=1
 assert count==521284 and len(pat)==1312
 return pat

def normalize_integer(P):
 hi=[min(x,9) for x in P];lo=[x-h for x,h in zip(P,hi)]
 D=lo+hi[::-1];n=len(D);carry=0;C=[0];O=[]
 for j in range(n):
  val=D[j]+D[n-1-j]+carry;O.append(val%10);carry=val//10;C.append(carry)
 if carry:O.append(carry)
 return D,O,C

def bits12(P,C,j):
 n=len(P);b=0
 for k in range(4):
  b|=(P[j+k]&1)<<k
  b|=C[j+k]<<(4+k)
  b|=C[2*n-1-j-k]<<(8+k)
 return b

def bits9(P,C,j):
 n=len(P);b=0
 for k in range(3):
  b|=(P[j+k]&1)<<k
  b|=C[j+k]<<(3+k)
  b|=C[2*n-1-j-k]<<(6+k)
 return b

def feature(P,cache):
 Q=P*4;_,_,C=normalize_integer(Q);v=0
 for j in range(48,96):
  b=bits12(Q,C,j)
  if b not in cache:
   x=0;s=b
   while True:
    x|=1<<s
    if s==0:break
    s=(s-1)&b
   cache[b]=x
  v^=cache[b]
 return v

def rank_low_1471():
 rng=Random(9397);cache={};piv={};first=None
 for i in range(1471):
  row=feature([rng.randrange(19) for _ in range(48)],cache)
  while row:
   k=(row&-row).bit_length()-1
   if k in piv:row^=piv[k]
   else:piv[k]=row;break
  if len(piv)==1024 and first is None:first=i+1
 assert len(piv)==1024 and first==1471

def run():
 pat=graph();adj={}
 for u,v in pat.values():adj.setdefault(u,set()).add(v);adj.setdefault(v,set()).add(u)
 assert len(adj)==288 and sum(u==v for u,v in pat.values())==6
 seen={0};stack=[0]
 while stack:
  x=stack.pop()
  for y in adj[x]:
   if y not in seen:seen.add(y);stack.append(y)
 assert len(seen)==288
 rank_low_1471()
 W=[W0];counts=[];allstates=set()
 for t in range(8):
  P=B[t]+W[t]*4;h=len(P);D,O,C=normalize_integer(P)
  g=1-t%2
  assert D[-1]>0 and len(D)==406 and len(O)==406+g
  assert any(O[j]+O[2*h-1-j+(1-g)] != O[j]+O[2*h-1-j+g] for j in range(11+48,11+96))
  st=[];nxt=[]
  for j in range(11+48,11+48*3):
   nxt.append(O[j]+O[2*h-1-j+g]);b=bits12(P,C,j)
   assert b in pat
   st.append(bits9(P,C,j))
  assert st[:48]==st[48:96]
  assert all(pat[bits12(P,C,11+48+j)]==(st[j],st[(j+1)%48]) for j in range(48))
  counts.append(len(set(st[:48])));allstates.update(st)
  if t<7:W.append(nxt[:48])
  else:assert nxt[:48]==W0
  for L in range(48):
   for length in (1,2,3,4,7,11,24,47,48,49,96):
    for k in set(st[:48]):
     lhs=sum((st[(L+i)%48]==k)^(st[(L+i+1)%48]==k) for i in range(length))%2
     assert lhs==((st[L]==k)^(st[(L+length)%48]==k))
 assert len(W)==8 and counts==[45,42,35,45,45,42,35,45] and len(allstates)==178
 print('INDEPENDENT PASS: 76-state 1444-edge graph, 521284 4-cell paths, 1312 physical 12-bit patterns')
 print('INDEPENDENT PASS: 1471 genuine 384-digit integer samples attain rank1024/4096')
 print('INDEPENDENT PASS: eight 406-digit rec2 controls, actual overflow, wrong-shift negative control, 768 bulk outputs')
 print('INDEPENDENT PASS: 288 endpoint graph connected, six loops; 178 rec2 endpoint signatures; interval telescopes')
if __name__=='__main__':run()
