#!/usr/bin/env python3
"""Deterministically regenerate both compact proof certificates; Python 3 stdlib."""
import argparse,collections,json,random
from pathlib import Path
from model import W,NUM,features,tags,test_row,local_feature,rank
ROOT=Path(__file__).resolve().parent

def pivot_add(piv,v):
    while v:
        k=v.bit_length()-1
        if k in piv:v^=piv[k]
        else:piv[k]=v;return True
    return False

def kernel(piv,n):
    keys=set(piv)
    for free in range(n):
        if free in keys:continue
        v=1<<free
        for k in sorted(keys):
            if (v&piv[k]).bit_count()%2:v^=1<<k
        assert all((v&row).bit_count()%2==0 for row in piv.values())
        yield v

def make_graph():
    states=[(p,a,d) for p in range(19) for a in (0,1) for d in (0,1)]
    idx={x:i for i,x in enumerate(states)}
    edges=[]
    for u,(p,a,d) in enumerate(states):
        A=int(p+a>=10)
        for q in range(19):
            for D in (0,1):
                if d!=int(q+D>=10):continue
                v=idx[q,A,D]
                edges.append((u,v,local_feature((p&1,q&1,a,d,A,D))))
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
                    want=phi[u]^w^kap
                    if phi[v] is None:phi[v]=want;queue.append(v)
                    elif phi[v]!=want:good=False;break
            if not good:break
        if good:return [kap,phi]
    raise ValueError('mask is not a graph coboundary')

def run(write=False):
    piv={};rng=random.Random(77)
    for _ in range(250):
        P=[rng.randrange(19) for _ in range(48)]
        pivot_add(piv,features(P))
    assert len(piv)==29
    masks=list(kernel(piv,NUM))
    assert len(masks)==13 and rank(masks)==13
    states,edges=make_graph()
    graph={'masks':masks,'proofs':[potential(mask,states,edges) for mask in masks],
           'states':states,'edges':len(edges)}
    assert all(all((f&m).bit_count()%2==(k^phi[u]^phi[v]) for u,v,f in edges)
               for m,(k,phi) in zip(masks,graph['proofs']))
    piv={};witness=[]
    for tag in tags():
        if pivot_add(piv,test_row(tag)):witness.append(tag)
    assert len(witness)==len(piv)==232
    for name,obj in [('graph_certificate.json',graph),('rank_witness.json',witness)]:
        path=ROOT/name
        encoded=json.dumps(obj,separators=(',',':'))
        if write:path.write_text(encoded)
        else:assert json.loads(path.read_text())==json.loads(encoded),(name,'regeneration mismatch')
    print('PASS: regenerated 13 coboundaries, 76-state graph, 232 independent rec2 tags')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true')
    run(parser.parse_args().write)
