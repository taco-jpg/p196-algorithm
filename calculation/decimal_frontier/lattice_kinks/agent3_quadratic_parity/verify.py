#!/usr/bin/env python3
"""Finite exact GF(2) rank and nine universal identity certificate checks."""
from pathlib import Path
import json,random
from model import W,NUM,IDENTITY,covariance,all_tests,test_row,features,step,rank
ROOT=Path(__file__).resolve().parent
def run():
 assert len(IDENTITY)==9 and rank(IDENTITY)==9
 assert all(step(W[t],1-t%2)==W[(t+1)%8] for t in range(8))
 tags=[tuple(v) for v in json.loads((ROOT/'rank_witness.json').read_text())]
 assert len(tags)==104 and len(set(tags))==104
 assert all(t in set(all_tests()) for t in tags)
 assert rank(test_row(t) for t in tags)==104
 identity_rows=[v<<(t*NUM) for t in range(8) for v in IDENTITY]
 assert rank(identity_rows)==72
 for tag in tags:
  r=test_row(tag)
  assert all((r&v).bit_count()%2==0 for v in identity_rows)
 allrows=[test_row(t) for t in all_tests()]
 assert len(allrows)==2252 and rank(allrows)==104
 rng=random.Random(314159)
 for i in range(10000):
  P=[rng.randrange(19) for _ in range(48)]
  q=features(P)
  assert all((q&v).bit_count()%2==0 for v in IDENTITY)
  if i<1000:
   for t in range(8):
    r=covariance(t,P)
    assert all((r&v).bit_count()%2==0 for v in identity_rows)
 print('PASS: 104 independent finite rec2 test rows; full 2252-row GF(2) rank=104')
 print('PASS: 9 independent cyclic identities per phase; 72-dimensional kernel exhausts all 176 coefficients')
 print('CONTROL: 10,000 random cyclic words satisfy 9 identities; 8,000 random covariance equations respect 72 trivial identities')
 print('PAPER PROOF: every local quadratic parity/carry covariance observable in this basis is identically zero')
if __name__=='__main__':run()
