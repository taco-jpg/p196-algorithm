#!/usr/bin/env python3
"""Exact 232-row rank certificate + 13 graph-coboundary identities."""
import json,random
from pathlib import Path
from model import W,NUM,MONOMS,local_feature,carries,step,features,test_row,tags,rank,covariance
HERE=Path(__file__).resolve().parent

def graph_edges():
    states=[(p,a,d) for p in range(19) for a in (0,1) for d in (0,1)]
    idx={s:i for i,s in enumerate(states)}
    edges=[]
    for u,(p,a,d) in enumerate(states):
        A=int(p+a>=10)
        for q in range(19):
            for D in (0,1):
                if d!=int(q+D>=10):continue
                v=idx[(q,A,D)]
                bits=(p&1,q&1,a,d,A,D)
                edges.append((u,v,local_feature(bits)))
    return states,edges

def run():
    assert all(step(W[t],1-t%2)==W[(t+1)%8] for t in range(8))
    cert=json.loads((HERE/'graph_certificate.json').read_text())
    masks=cert['masks'];proofs=cert['proofs']
    assert len(masks)==len(proofs)==13 and rank(masks)==13
    states,edges=graph_edges()
    assert states==[tuple(x) for x in cert['states']]
    assert len(states)==76 and len(edges)==cert['edges']==1444
    for mask,(kappa,phi) in zip(masks,proofs):
        assert kappa in (0,1) and len(phi)==76 and all(v in (0,1) for v in phi)
        assert all(((f&mask).bit_count()&1)==(kappa^phi[u]^phi[v]) for u,v,f in edges)
    # Each local identity is a graph coboundary + constant kappa. Over a 48-ring
    # every edge potential telescopes, and 48*kappa=0 mod 2.
    identity=[v<<(t*NUM) for t in range(8) for v in masks]
    assert rank(identity)==104
    witness=[tuple(x) for x in json.loads((HERE/'rank_witness.json').read_text())]
    all_tags=list(tags())
    assert len(all_tags)==2252 and len(witness)==232 and len(set(witness))==232
    assert set(witness).issubset(set(all_tags))
    assert rank(test_row(x) for x in witness)==232
    assert rank(test_row(x) for x in all_tags)==232
    for tag in all_tags:
        v=test_row(tag)
        assert all((v&i).bit_count()%2==0 for i in identity)
    rng=random.Random(319643)
    for trial in range(10000):
        P=[rng.randrange(19) for _ in range(48)]
        f=features(P)
        assert all((f&m).bit_count()%2==0 for m in masks)
        if trial<1000:
            for t in range(8):
                v=covariance(t,P)
                assert all((v&i).bit_count()%2==0 for i in identity)
    print('PASS: 76-vertex/1444-edge exact cyclic carry graph; 13 independent coboundaries')
    print('PASS: 232 independent rec2 witness rows; all 2252 covariance rows rank 232 of 336')
    print('PASS: 104 independent universal zero functions = complete 104-dimensional kernel')
    print('CONTROL: 10,000 random cyclic words, 8,000 covariance checks')
    print('PAPER PROOF: degree<=3 cyclic local GF(2) observables are universally zero')
if __name__=='__main__':run()
