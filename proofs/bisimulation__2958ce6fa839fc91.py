"""Exact strong-bisimulation quotient for fixed two-coordinate edge scores."""

def quotient(n,source,sink,edges):
    outgoing=[[] for _ in range(n)]
    for j,e in enumerate(edges):outgoing[e[0]].append(j)
    blocks=[1 if v==source else 2 if v==sink else 0 for v in range(n)]
    rounds=0
    while True:
        signatures={};new=[]
        for u in range(n):
            choices=tuple(sorted({(edges[j][2],edges[j][3],blocks[edges[j][1]]) for j in outgoing[u]}))
            sig=(blocks[u],choices)
            if sig not in signatures:signatures[sig]=len(signatures)
            new.append(signatures[sig])
        stable=len(set(new))==len(set(blocks));blocks=new;rounds+=1
        if stable:break
    unique={}
    for u,v,a,b,kind,label in edges:
        e=(blocks[u],blocks[v],a,b,'quotient',None)
        unique.setdefault(e[:4],e)
    reduced=list(unique.values())
    # Verify the defining equality of outgoing transition signatures within
    #every block, independently of the refinement stopping criterion.
    signatures={}
    for u in range(n):
        sig={(edges[j][2],edges[j][3],blocks[edges[j][1]]) for j in outgoing[u]}
        if blocks[u] in signatures:assert sig==signatures[blocks[u]]
        else:signatures[blocks[u]]=sig
    context=dict(original_edges=edges,outgoing=outgoing,blocks=blocks,
                 original_source=source,original_sink=sink,rounds=rounds)
    return len(set(blocks)),blocks[source],blocks[sink],reduced,context

def lift(trail,quotient_edges,context):
    edges=context['original_edges'];blocks=context['blocks'];out=context['outgoing']
    current=context['original_source'];answer=[]
    for j in trail:
        u,v,a,b,*_=quotient_edges[j];assert blocks[current]==u
        choices=[k for k in out[current] if edges[k][2:4]==(a,b) and blocks[edges[k][1]]==v]
        assert choices
        chosen=choices[0];answer.append(edges[chosen]);current=edges[chosen][1]
    assert current==context['original_sink']
    return answer
