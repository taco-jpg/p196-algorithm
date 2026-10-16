"""Replay the finite rank certificate without importing its search/checker code.

This checker uses no SCC algorithm and no bounded temporal-word search.
It reconstructs the full one-column inverse graph by decimal arithmetic,
then verifies the supplied ranks/projections on every edge. The written
cycle-rank argument explains why these finite checks cover all periods.
"""
from pathlib import Path
from itertools import product, permutations
import json, hashlib, time

HERE=Path(__file__).resolve().parent


def letter(a,b,c,z):
    assert a in (0,1) and b in (0,1) and c in (0,1) and -1<=z<=9
    return 11*(4*a+2*b+c)+z+1


def inverse_options():
    out=[set() for _ in range(88)]
    # These are all freely chosen forward-column inputs, before temporal
    # adjacency is imposed. Ordinary divmod supplies all four carry bits.
    for q,a,b,d,e in product(range(19),range(2),range(2),range(2),range(2)):
        alpha,low=divmod(q+a,10)
        c,high=divmod(q+d,10)
        r=low+high
        beta,_=divmod(r+b,10)
        zeta=r-10*e
        if -1<=zeta<=9:
            out[letter(alpha,beta,d,zeta)].add((q,a,b,c,e,r))
    return [sorted(xs) for xs in out]


def old_letter(x,y):
    q,a,b,c,e,r=x
    prior_z=y[0]-((r+b)%10)-e
    # The delayed high digit and z coordinate must both be admissible.
    if -1<=prior_z<=9 and 0<=prior_z+e<=9:
        return letter(a,b,c,prior_z)
    return None


def raw_preimage(graph,options):
    es=graph['edges'];n=graph['vertices']
    leaving=[[] for _ in range(n)]
    for i,(u,v,l) in enumerate(es):
        assert 0<=u<n and 0<=v<n and 0<=l<88
        leaving[u].append(i)
    vertices=[(i,x) for i,(_,_,l) in enumerate(es) for x in options[l]]
    index={v:i for i,v in enumerate(vertices)}
    assert len(index)==len(vertices)
    edges=[]
    for u,(i,x) in enumerate(vertices):
        for j in leaving[es[i][1]]:
            for y in options[es[j][2]]:
                l=old_letter(x,y)
                if l is not None:edges.append((u,index[j,y],l))
    return vertices,edges


def incoming(q,i,direction):
    for distance in range(1,len(q)+1):
        v=q[(i+direction*distance)%len(q)]
        if v!=9:return int(v>=10)
    raise ValueError('ambiguous all-nine periodic carry')


def bulk_word(B):
    q=B;slots=[];phase_rows=[]
    for t in range(12):
        phase_rows.append(q)
        if t%2==0:
            a=incoming(q,0,-1)
            c=(q[0]+incoming(q,0,1))//10
        else:
            b=incoming(q,0,-1)
            high=(q[-1]+incoming(q,-1,1))//10
            slots.append(letter(a,b,c,q[-1]-10*high))
        h=t%2
        q=tuple((q[i]+incoming(q,i,-1))%10+
                (q[(i-h)%3]+incoming(q,(i-h)%3,1))%10
                for i in range(3))
    assert q==B
    # The two-step deterministic bulk map has least period six. Therefore
    # every even return time has this six-letter cut word as a power.
    assert all(phase_rows[t]!=B for t in (2,4,6,8,10))
    return tuple(slots)


def accepts(graph,word):
    by_label={}
    for u,v,l in graph['edges']:
        by_label.setdefault((u,l),set()).add(v)
    for start in range(graph['vertices']):
        vertices={start}
        for l in word:
            vertices={v for u in vertices for v in by_label.get((u,l),())}
        if start in vertices:return True
    return False


def run():
    begin=time.monotonic()
    path=HERE/'reverse/sofic_rank_certificate.json'
    data=path.read_bytes();cert=json.loads(data)
    assert cert['alphabet_size']==88
    graphs=cert['graphs'];transitions=cert['transitions']
    assert len(graphs)==len(transitions)==len(cert['root_ranks'])==8
    root=letter(0,1,1,7)
    assert root==cert['root_letter']
    options=inverse_options()
    assert sorted(map(len,options))==[0]*2+[1]*8+[2]*78
    edge_counts=[];equal_rank_edges=0
    for k,tr in enumerate(transitions):
        assert tr['source']==k
        dest=tr['destination']
        assert dest==k+1 if k<7 else dest==5
        vertices,es=raw_preimage(graphs[k],options)
        assert len(vertices)==tr['raw_vertices'] and len(es)==tr['raw_edges']
        rank=tr['rank'];mapping=tr['mapping']
        assert len(rank)==len(mapping)==len(vertices)
        assert all(isinstance(x,int) and x>=0 for x in rank)
        assert all(-1<=x<graphs[dest]['vertices'] for x in mapping)
        target_edges=set(map(tuple,graphs[dest]['edges']))
        for u,v,l in es:
            assert rank[u]<=rank[v],(k,u,v,l)
            if rank[u]==rank[v]:
                equal_rank_edges+=1
                assert mapping[u]>=0 and mapping[v]>=0
                assert (mapping[u],mapping[v],l) in target_edges
        edge_counts.append(len(es))
    for graph,rank in zip(graphs,cert['root_ranks']):
        assert len(rank)==graph['vertices']
        assert all(isinstance(x,int) and x>=0 for x in rank)
        for u,v,l in graph['edges']:
            if l==root:assert rank[u]<rank[v]
    bulks=list(permutations((9,3,6)))+list(permutations((9,12,15)))
    words=[bulk_word(B) for B in bulks]
    assert len(set(words))==12
    assert all(accepts(graphs[0],w) for w in words)
    result=dict(status='root_rank_certificate_replay_passed',
        scope='all finite widths and all positive temporal periods of the specified alternating 8/17 exterior',
        graph_count=8,graph_vertices=[g['vertices'] for g in graphs],
        graph_edges=[len(g['edges']) for g in graphs],
        raw_preimage_edges=edge_counts,equal_rank_edges=equal_rank_edges,
        source_code_imports_from_search=False,SCC_algorithm_used=False,
        inverse_fibers_exhaustively_reconstructed=True,
        backward_language_closed=True,uniform_root_closed_walk_excluded=True,
        primitive_six_pair_bulk_words_checked=len(words),
        certificate_sha256=hashlib.sha256(data).hexdigest(),
        elapsed_seconds=time.monotonic()-begin,
        decimal_lychrel_existence_proved=False,main_conjecture_lean_proved=False)
    (HERE/'root_sofic_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':run()
