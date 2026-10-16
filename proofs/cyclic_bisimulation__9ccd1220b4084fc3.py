"""Strong forward bisimulation for finite edge-labeled graphs.

Quotienting preserves infinite traces and periodic closed-walk words up to
taking a positive power. It need not preserve single-period closed walks.
"""
from collections import defaultdict


def quotient(n,edges):
    outgoing=[[] for _ in range(n)]
    for u,v,label in edges:
        outgoing[u].append((label,v))
    blocks=[0]*n
    previous_count=1 if n else 0
    rounds=0
    while True:
        keys=[tuple(sorted({(label,blocks[v]) for label,v in row})) for row in outgoing]
        ids={key:i for i,key in enumerate(sorted(set(keys)))}
        new=[ids[key] for key in keys]
        rounds+=1
        blocks=new
        if len(ids)==previous_count:
            break
        previous_count=len(ids)
    count=max(blocks,default=-1)+1
    es=sorted({(blocks[u],blocks[v],label) for u,v,label in edges})
    # Exact local back-and-forth certificate of strong bisimulation.
    signatures={}
    for u,row in enumerate(outgoing):
        signature=frozenset((label,blocks[v]) for label,v in row)
        if blocks[u] in signatures:
            assert signatures[blocks[u]]==signature
        signatures[blocks[u]]=signature
    return count,es,blocks,rounds


def quotient_both(n,edges):
    """Alternate forward/reversed quotients, preserving periodic traces."""
    total=0
    while True:
        before=n
        n,edges,_,rounds=quotient(n,edges)
        total+=rounds
        n,rev,_,rounds=quotient(n,[(v,u,l) for u,v,l in edges])
        edges=sorted((v,u,l) for u,v,l in rev)
        total+=rounds
        if n==before:
            return n,edges,[],total
