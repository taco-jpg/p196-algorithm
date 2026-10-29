#!/usr/bin/env python3
"""Self-contained finite proof generator: 232 rank witnesses and 13 universal graph coboundaries."""
from pathlib import Path
import collections,json,random,sys
from model import W,MON,N,features,step,edge_feature,tags,test_row,add,rank

STATES=[(p,a,d) for p in range(19) for a in range(2) for d in range(2)]
INDEX={x:i for i,x in enumerate(STATES)}
EDGES=[]
for u,(p,a,d) in enumerate(STATES):
    next_a=int(p+a>=10)
    for q in range(19):
        for next_d in (0,1):
            if d!=int(q+next_d>=10):continue
            v=INDEX[(q,next_a,next_d)]
            EDGES.append((u,v,edge_feature((p&1,q&1,a,d,next_a,next_d))))
assert len(STATES)==76 and len(EDGES)==1444

def zeros(piv):
    used=set(piv)
    for f in range(N):
        if f in used:continue
        mask=1<<f
        for k in sorted(used):
            if (mask&piv[k]).bit_count()%2:mask^=1<<k
        assert all((mask&r).bit_count()%2==0 for r in piv.values())
        yield mask

def potential(mask):
    for constant in (0,1):
        adj=[[] for _ in STATES]
        for u,v,f in EDGES:
            parity=((mask&f).bit_count()&1)^constant
            adj[u].append((v,parity));adj[v].append((u,parity))
        phi=[None]*len(STATES);good=True
        for root in range(len(STATES)):
            if phi[root] is not None:continue
            phi[root]=0;queue=collections.deque([root])
            while queue:
                u=queue.popleft()
                for v,parity in adj[u]:
                    want=phi[u]^parity
                    if phi[v] is None:phi[v]=want;queue.append(v)
                    elif phi[v]!=want:good=False;break
                if not good:break
            if not good:break
        if good:
            assert all(((mask&f).bit_count()&1)==(phi[u]^phi[v]^constant) for u,v,f in EDGES)
            return constant,phi
    raise AssertionError('candidate does not universally telescope')

def run():
    assert all(step(W[t],1-t%2)==W[(t+1)%8] for t in range(8))
    piv={}; witness=[];ct=0
    for tag in tags():
        ct+=1
        if add(piv,test_row(tag)):witness.append(list(tag))
    assert ct==2252 and len(piv)==len(witness)==232
    rng=random.Random(77);pivfeature={}
    for _ in range(250):
        P=[rng.randrange(19) for i in range(48)]
        add(pivfeature,features(P))
    assert len(pivfeature)==29
    masks=list(zeros(pivfeature))
    assert len(masks)==rank(masks)==13
    proofs=[potential(x) for x in masks]
    zero=[x<<(t*N) for t in range(8) for x in masks]
    assert rank(zero)==104
    assert all(all(((test_row(tuple(tag))&z).bit_count()&1)==0 for z in zero) for tag in witness)
    rng=random.Random(319648)
    for _ in range(10000):
        P=[rng.randrange(19) for i in range(48)]
        f=features(P)
        assert all((f&m).bit_count()%2==0 for m in masks)
    cert=dict(rank_witness=witness,identity_masks=masks,graph_potentials=[list(q[1]) for q in proofs],graph_constants=[q[0] for q in proofs],vertices=len(STATES),edges=len(EDGES),phase_rank=len(piv),single_phase_function_rank=len(pivfeature))
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(cert,separators=(',',':'))+'\n')
    print('PASS: 2252 rec2 tests; 232 independent rows among 336 phase coefficients')
    print('PASS: 76 cyclic carry states, 1444 valid edges, 13 independent telescoping feature identities')
    print('PASS: 104-dimensional universal zero-function kernel exhausts covariance constraints')
    print('CONTROLS: 10000 independent physical-carry cyclic rows')
    print('PAPER PROOF: no nonzero degree<=3 local GF(2) cyclic-bulk covariance observable')
if __name__=='__main__':run()
