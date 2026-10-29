#!/usr/bin/env python3
"""Check exact 388/400 ranks, 14 universal graph identities and 12 false positives."""
import json,random
from pathlib import Path
from model import W,EVAL,feat,cov,step,tags,tagged,rank,add
HERE=Path(__file__).resolve().parent

def check():
 assert all(step(W[t],1-t%2)==W[(t+1)%8] for t in range(8))
 graph=json.loads((HERE/'graph_certificate.json').read_text())
 masks=graph['masks'];states=[tuple(s) for s in graph['states']]
 assert len(states)==76 and len(masks)==14 and rank(masks)==14
 idx={s:i for i,s in enumerate(states)};edge_count=0
 for u,(p,a,d) in enumerate(states):
  A=int(p+a>=10)
  for q in range(19):
   for D in (0,1):
    if d!=int(q+D>=10):continue
    v=idx[q,A,D];bits=(p&1)|((q&1)<<1)|(a<<2)|(d<<3)|(A<<4)|(D<<5)
    f=EVAL[bits]
    for mask,(kap,phi) in zip(masks,graph['proofs']):
     assert kap in (0,1) and len(phi)==76
     assert (f&mask).bit_count()%2==kap^phi[u]^phi[v]
    edge_count+=1
 assert edge_count==graph['edges']==1444
 identity=[m<<(64*t) for t in range(8) for m in masks]
 assert rank(identity)==112
 refs=[tuple(x) for x in json.loads((HERE/'rank_witness.json').read_text())]
 all_tags=list(tags());assert len(all_tags)==2252 and len(refs)==388
 assert len(set(refs))==388 and set(refs).issubset(set(all_tags))
 assert rank(tagged(x) for x in refs)==388
 assert rank(tagged(x) for x in all_tags)==388
 rng=random.Random(4196);words=[[rng.randrange(19) for _ in range(48)] for _ in range(100)]
 glob=[tuple(x) for x in json.loads((HERE/'global_witness.json').read_text())]
 assert len(glob)==400 and rank(cov(t,words[i]) for i,t in glob)==400
 for i in identity:
  assert all((tagged(tag)&i).bit_count()%2==0 for tag in refs)
  assert all((cov(t,words[j])&i).bit_count()%2==0 for j,t in glob)
 bad=json.loads((HERE/'counterexamples.json').read_text())
 b=[int(x,16) for x in bad['masks']]
 assert len(b)==len(bad['examples'])==12 and rank(b)==12
 assert all(all((tagged(tag)&x).bit_count()%2==0 for tag in all_tags) for x in b)
 signatures=[]
 for item in bad['examples']:
  P=item['P'];t=item['phase']
  assert len(P)==48 and all(0<=x<=18 for x in P) and any(x!=9 for x in P)
  signatures.append(sum(((cov(t,P)&v).bit_count()%2)<<k for k,v in enumerate(b)))
 assert rank(signatures)==12
 rng=random.Random(642031)
 for _ in range(10000):
  P=[rng.randrange(19) for _ in range(48)];f=feat(P)
  assert all((f&m).bit_count()%2==0 for m in masks)
 print('PASS: 76-state/1444-edge carry graph, 14 independent all-row zero identities')
 print('PASS: rec2 2252-row rank=388/512; 388 explicit independent witness tags')
 print('PASS: 400 independent unrestricted covariance rows; universal kernel dimension=112')
 print('PASS: 12 independent local-test false positives, 12 physical cyclic-word counterexamples')
 print('CONTROL: 10,000 random physical cyclic carry words satisfy all 14 identities')
 print('PAPER PROOF: complete 64-feature all-Boolean rec2 covariance classification')
if __name__=='__main__':check()
