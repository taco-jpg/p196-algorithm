#!/usr/bin/env python3
"""Exhaustive rec2 local Boolean covariance rank by perturbation support diameter."""
import itertools,json
from pathlib import Path
from model import W,EVAL,cov,add,rank,tags,tagged
HERE=Path(__file__).resolve().parent

def pair_rows(sep):
 for t in range(8):
  for j in range(48):
   k=(j+sep)%48
   for s,u in itertools.product((-1,1),repeat=2):
    P=W[t].copy();P[j]+=s;P[k]+=u
    if 0<=P[j]<=18 and 0<=P[k]<=18:
     yield ('pair',t,j,sep,s,u),cov(t,P)

def triple_rows():
 for t in range(8):
  for j in range(48):
   I=(j,(j+1)%48,(j+2)%48)
   for ss in itertools.product((-1,1),repeat=3):
    P=W[t].copy()
    for k,s in zip(I,ss):P[k]+=s
    if all(0<=P[k]<=18 for k in I):
     yield ('triple',t,j,*ss),cov(t,P)

def check():
 cert=json.loads((HERE/'graph_certificate.json').read_text())
 assert len(cert['masks'])==14 and rank(cert['masks'])==14
 states=[(p,a,d) for p in range(19) for a in (0,1) for d in (0,1)]
 assert states==[tuple(x) for x in cert['states']]
 idx={s:i for i,s in enumerate(states)};edges=0
 for u,(p,a,d) in enumerate(states):
  A=int(p+a>=10)
  for q in range(19):
   for D in (0,1):
    if d!=int(q+D>=10):continue
    v=idx[q,A,D];bits=(p&1)|((q&1)<<1)|(a<<2)|(d<<3)|(A<<4)|(D<<5)
    for m,(kap,phi) in zip(cert['masks'],cert['proofs']):
     assert (EVAL[bits]&m).bit_count()%2==(kap^phi[u]^phi[v])
    edges+=1
 assert edges==1444
 refs=[tuple(x) for x in json.loads((HERE/'rank_witness.json').read_text())]
 assert len(refs)==388 and rank(tagged(x) for x in refs)==388
 p={};assert len(list(tags()))==2252
 for tag in tags():add(p,tagged(tag))
 assert len(p)==388
 expected=[tuple(x) for x in json.loads((HERE/'augmentation_tags.json').read_text())]
 new=[];counts={}
 for sep in (2,):
  count=0
  for tag,v in pair_rows(sep):
   count+=1
   if add(p,v):new.append(tag)
  counts[sep]=count
 assert len(p)==396 and counts[2]==1488
 count=0
 for tag,v in triple_rows():
  count+=1
  if add(p,v):new.append(tag)
 assert count==2928 and len(p)==398
 count=0
 for tag,v in pair_rows(3):
  count+=1
  if add(p,v):new.append(tag)
 assert count==1488 and len(p)==400
 assert new==expected and len(new)==12
 for sep in range(4,25):
  count=0
  for _,v in pair_rows(sep):
   count+=1
   assert not add(p,v)
  counts[sep]=count
 assert len(p)==400
 # Exhaustively decide all 2-site perturbations without the triples.
 q={}
 for tag in tags():add(q,tagged(tag))
 total=0
 for sep in range(2,25):
  for _,v in pair_rows(sep):
   total+=1;add(q,v)
 assert total==34236 and len(q)==398
 # Exactly 14 zero-function graph masks per phase give 112 independent
 # universal kernel vectors; 400 independent rows saturate the upper bound.
 assert rank(m<<(64*t) for m in cert['masks'] for t in range(8))==112
 print('PASS: 2252 reference rank388; separation2 rank396; contiguous triples rank398; separation3 rank400')
 print('PASS: all 34236 additional arbitrary two-site rows rank398 without triples')
 print('PASS: 12 independent extra row tags, 2928 contiguous triple controls, 1444 graph edges')
 print('PAPER PROOF: support in <=3 consecutive cells is insufficient; <=4 consecutive cells suffice')
if __name__=='__main__':check()
