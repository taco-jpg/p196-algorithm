#!/usr/bin/env python3
"""Independent schoolbook digit-normalization and exact GF(2) rank checker."""
import json,random,itertools
from pathlib import Path
HERE=Path(__file__).resolve().parent
z=list(map(int,(HERE/'lat2.txt').read_text().split()))
assert z[:12]==[8,11,48,10,1,0,1,0,1,0,1,0]
W=[z[12+48*t:12+48*(t+1)] for t in range(8)]
E=[sum(1<<m for m in range(64) if m&x==m) for x in range(64)]

def digits(P):
 n=len(P);up=[];dn=[]
 for seed in (0,1):
  c=seed;a=[]
  for x in P:a.append(c);c=(x+c)//10
  if c==seed:up.append(a)
  c=seed;d=[0]*n
  for j in range(n-1,-1,-1):d[j]=c;c=(P[j]+c)//10
  if c==seed:dn.append(d)
 assert len(up)==len(dn)==1
 a,d=up[0],dn[0]
 lo=[(P[j]+a[j])%10 for j in range(n)]
 hi=[(P[j]+d[j])%10 for j in range(n)]
 return lo,hi,a,d

def feature(P):
 _,_,a,d=digits(P);n=len(P);acc=0
 for j in range(n):
  k=(j+1)%n
  bits=(P[j]%2)|((P[k]%2)<<1)|(a[j]<<2)|(d[j]<<3)|(a[k]<<4)|(d[k]<<5)
  acc^=E[bits]
 return acc

def covariance(t,P):
 lo,hi,_,_=digits(P);g=1-(t%2);n=len(P)
 N=[lo[j]+hi[(j-g)%n] for j in range(n)]
 v=feature(N)<<(64*((t+1)%8))
 if g:v^=feature(P)<<(64*t)
 return v

def tagged(tag):
 t,j,s,u=tag;P=W[t].copy()
 if j>=0:
  P[j]+=s
  if u:P[(j+1)%48]+=u
 return covariance(t,P)

def rank(vs):
 piv={}
 for v in vs:
  while v:
   j=(v&-v).bit_length()-1
   if j not in piv:piv[j]=v;break
   v^=piv[j]
 return len(piv)

def run():
 ref=[tuple(x) for x in json.loads((HERE/'rank_witness.json').read_text())]
 assert len(ref)==388 and rank(tagged(t) for t in ref)==388
 all_tags=[]
 for t in range(8):
  all_tags.append((t,-1,0,0))
  for j in range(48):
   for s in (-1,1):
    if 0<=W[t][j]+s<=18:all_tags.append((t,j,s,0))
  for j in range(48):
   for s,u in itertools.product((-1,1),repeat=2):
    if 0<=W[t][j]+s<=18 and 0<=W[t][(j+1)%48]+u<=18:all_tags.append((t,j,s,u))
 assert len(all_tags)==2252 and rank(tagged(t) for t in all_tags)==388
 rng=random.Random(4196);words=[[rng.randrange(19) for _ in range(48)] for _ in range(100)]
 glob=json.loads((HERE/'global_witness.json').read_text())
 assert len(glob)==400 and rank(covariance(t,words[i]) for i,t in glob)==400
 graph=json.loads((HERE/'graph_certificate.json').read_text())
 assert rank(graph['masks'])==14
 states=[(p,a,d) for p in range(19) for a in (0,1) for d in (0,1)]
 assert states==[tuple(s) for s in graph['states']]
 idx={s:i for i,s in enumerate(states)};edges=0
 for p,a,d in states:
  u=idx[p,a,d]
  for q in range(19):
   for D in (0,1):
    A=(p+a)//10
    if d!=(q+D)//10:continue
    v=idx[q,A,D]
    bits=(p%2)|((q%2)<<1)|(a<<2)|(d<<3)|(A<<4)|(D<<5)
    for m,(k,phi) in zip(graph['masks'],graph['proofs']):
     assert (E[bits]&m).bit_count()%2==(k^phi[u]^phi[v])
    edges+=1
 assert edges==1444
 bad=json.loads((HERE/'counterexamples.json').read_text())
 masks=[int(x,16) for x in bad['masks']]
 assert len(masks)==12 and rank(masks)==12
 assert all(all((tagged(t)&m).bit_count()%2==0 for t in all_tags) for m in masks)
 signatures=[]
 for x in bad['examples']:
  P=x['P'];t=x['phase'];_,_,a,d=digits(P)
  assert all(0<=z<=18 for z in P)
  assert sum(a[j]*(1-a[(j+1)%48]) for j in range(48))==sum(d[j]*(1-d[(j+1)%48]) for j in range(48))
  signatures.append(sum(((covariance(t,P)&m).bit_count()%2)<<i for i,m in enumerate(masks)))
 assert rank(signatures)==12
 print('INDEPENDENT PASS: digit-normalized ranks 388 (local) and 400 (unrestricted)')
 print('INDEPENDENT PASS: all 1444 graph edges, 12 independent physical cyclic-word counterexamples')
if __name__=='__main__':run()
