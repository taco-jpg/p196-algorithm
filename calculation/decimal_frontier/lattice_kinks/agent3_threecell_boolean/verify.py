#!/usr/bin/env python3
"""Exact 288 de Bruijn graph coboundaries and 814/1792 rank certificates."""
import collections,hashlib,json,random,sys
from pathlib import Path
from model import W,EVAL,feature,covariance,step,tags,tagged,add,rank,kernel
ROOT=Path(__file__).resolve().parent

def graph():
 states=[(p,a,d) for p in range(19) for a in (0,1) for d in (0,1)]
 idx={s:i for i,s in enumerate(states)};edges=[];out=[[] for _ in states]
 for u,(p,a,d) in enumerate(states):
  A=int(p+a>=10)
  for q in range(19):
   for D in (0,1):
    if d!=int(q+D>=10):continue
    e=len(edges);edges.append((u,idx[(q,A,D)]));out[u].append(e)
 assert len(edges)==1444
 H=[[] for _ in edges];count=0
 for e,(u,v) in enumerate(edges):
  p,a,d=states[u];q,A,D=states[v]
  for f in out[v]:
   _,w=edges[f];r,B,F=states[w]
   bits=(p&1)|((q&1)<<1)|((r&1)<<2)|(a<<3)|(A<<4)|(B<<5)|(d<<6)|(D<<7)|(F<<8)
   val=EVAL[bits]
   H[e].append((f,val));H[f].append((e,val));count+=1
 assert count==27436
 return states,edges,H,count

def potential(mask,H):
 for kap in (0,1):
  phi=[None]*len(H);good=True
  for root in range(len(H)):
   if phi[root] is not None:continue
   phi[root]=0;Q=collections.deque([root])
   while Q and good:
    u=Q.popleft()
    for v,f in H[u]:
     want=phi[u]^((f&mask).bit_count()%2)^kap
     if phi[v] is None:phi[v]=want;Q.append(v)
     elif phi[v]!=want:good=False;break
   if not good:break
  if good:return (kap,phi)
 raise AssertionError('mask not a universal graph coboundary')

def digest(obj):
 return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def run(export=False):
 manifest=json.loads((ROOT/'manifest.json').read_text())
 assert all(step(W[t],1-t%2)==W[(t+1)%8] for t in range(8))
 rp={};refs=[]
 for tag in tags():
  if add(rp,tagged(tag)):refs.append(tag)
 assert len(refs)==len(rp)==814 and len(list(tags()))==2252
 assert digest(refs)==manifest['reference_witness_sha256']
 rng=random.Random(9396);fp={};gp={};glob=[]
 for i in range(229):
  P=[rng.randrange(19) for _ in range(48)]
  add(fp,feature(P))
  for t in range(8):
   if add(gp,covariance(t,P)):glob.append([i,t])
 assert len(fp)==224 and len(gp)==len(glob)==1792
 assert digest(glob)==manifest['global_witness_sha256']
 masks=list(kernel(fp,512));assert len(masks)==288 and rank(masks)==288
 states,edges,H,count=graph();proofs=[potential(mask,H) for mask in masks]
 graph_cert={'masks':masks,'proofs':proofs,'base_states':states,'base_edges':edges,'H_edges':count}
 assert digest(graph_cert)==manifest['graph_certificate_sha256']
 # 288 independent zero functions per phase => 2304-dimensional universal kernel.
 assert rank(m<<(512*t) for t in range(8) for m in masks)==2304
 counter=json.loads((ROOT/'counterexample.json').read_text())
 bit=512*counter['coefficient_phase']+counter['monomial_mask']
 assert all((tagged(tag)>>bit)&1==0 for tag in tags())
 assert ((covariance(counter['test_phase'],counter['P'])>>bit)&1)==1
 if export:
  for name,obj in [('reference_witness.json',refs),('global_witness.json',glob),('graph_certificate.json',graph_cert)]:
   (ROOT/name).write_text(json.dumps(obj,separators=(',',':')))
 print('PASS: 2252 rec2 tests rank814/4096; 814 explicit deterministic independent tags')
 print('PASS: 229 seeded cyclic words give rank1792/4096; 288 independent graph coboundaries per phase')
 print('PASS: 1444 base carry edges, 27436 de Bruijn edges, 288 exact potential checks, all SHA256 digests')
 print('PASS: degree-five single-monomial finite-test false positive has a physical cyclic-word counterexample')
 print('PAPER PROOF: all 3-cell Boolean local covariance zero functions form a 2304-dimensional kernel')
if __name__=='__main__':run('--export' in sys.argv)
