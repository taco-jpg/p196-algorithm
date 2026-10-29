#!/usr/bin/env python3
"""Regenerate exact rec2 rank, all-row graph identities, and 12 false positives."""
import argparse,collections,json,random
from pathlib import Path
from model import W,EVAL,feat,cov,tags,tagged,add,rank,kernel
HERE=Path(__file__).resolve().parent

def graph():
 states=[(p,a,d) for p in range(19) for a in (0,1) for d in (0,1)]
 idx={s:i for i,s in enumerate(states)};edges=[]
 for u,(p,a,d) in enumerate(states):
  A=int(p+a>=10)
  for q in range(19):
   for D in (0,1):
    if d!=int(q+D>=10):continue
    bits=(p&1)|((q&1)<<1)|(a<<2)|(d<<3)|(A<<4)|(D<<5)
    edges.append((u,idx[(q,A,D)],EVAL[bits]))
 assert len(edges)==1444
 return states,edges

def potential(mask,states,edges):
 adj=[[] for _ in states]
 for u,v,f in edges:
  w=(f&mask).bit_count()%2
  adj[u].append((v,w));adj[v].append((u,w))
 for kap in (0,1):
  phi=[None]*len(states);good=True
  for start in range(len(states)):
   if phi[start] is not None:continue
   phi[start]=0;queue=collections.deque([start])
   while queue and good:
    u=queue.popleft()
    for v,w in adj[u]:
     val=phi[u]^w^kap
     if phi[v] is None:phi[v]=val;queue.append(v)
     elif phi[v]!=val:good=False;break
   if not good:break
  if good:return [kap,phi]
 raise AssertionError('not a graph coboundary')

def make():
 # 250 seeded physical cyclic words yield 50 independent feature rows;
 # graph certificates then upgrade each of the 14 kernel masks to an ALL-row identity.
 piv={};rng=random.Random(4196)
 for _ in range(250):add(piv,feat([rng.randrange(19) for _ in range(48)]))
 assert len(piv)==50
 masks=list(kernel(piv,64));assert len(masks)==14 and rank(masks)==14
 states,edges=graph();proofs=[potential(m,states,edges) for m in masks]
 gc={'masks':masks,'proofs':proofs,'states':states,'edges':1444}
 # Exactly 2252 local rec2 rows: 388 independent.
 rp={};ref_witness=[]
 for tag in tags():
  if add(rp,tagged(tag)):ref_witness.append(tag)
 assert len(rp)==len(ref_witness)==388
 # 100 deterministic independently digit-normalizable cyclic words suffice
 # to exhibit 400 independent unrestricted covariance rows.
 rng=random.Random(4196);words=[[rng.randrange(19) for _ in range(48)] for _ in range(100)]
 gp={};global_witness=[]
 for i,P in enumerate(words):
  for t in range(8):
   if add(gp,cov(t,P)):global_witness.append([i,t])
 assert len(gp)==len(global_witness)==400
 # Select a basis for the 12-dimensional excess finite-test kernel.
 sp={};bad=[]
 for v in kernel(rp,512):
  sig=sum(((cov(t,P)&v).bit_count()%2)<<j for j,(i,t) in enumerate(global_witness) for P in (words[i],))
  if add(sp,sig):bad.append(v)
 assert len(bad)==len(sp)==12
 # Find twelve explicit cyclic-word/phase counterexamples with independent
 # 12-bit violation signatures, so no linear combination of bad masks vanishes.
 wp={};counter=[]
 for i,t in global_witness:
  P=words[i]
  sig=sum(((cov(t,P)&v).bit_count()%2)<<k for k,v in enumerate(bad))
  if add(wp,sig):counter.append({'phase':t,'P':P})
 assert len(counter)==len(wp)==12
 assert all(all((tagged(tag)&v).bit_count()%2==0 for tag in tags()) for v in bad)
 return {'graph_certificate.json':gc,'rank_witness.json':ref_witness,
         'global_witness.json':global_witness,
         'counterexamples.json':{'masks':[hex(x) for x in bad],'examples':counter}}

def run(write=False):
 data=make()
 for name,obj in data.items():
  path=HERE/name;encoded=json.dumps(obj,separators=(',',':'))
  if write:path.write_text(encoded)
  else:assert json.loads(path.read_text())==json.loads(encoded),(name,'mismatch')
 print('PASS: regenerated 14 all-row coboundaries, 388 local pivots, 400 global pivots, 12 independent false positives')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true')
 run(parser.parse_args().write)
