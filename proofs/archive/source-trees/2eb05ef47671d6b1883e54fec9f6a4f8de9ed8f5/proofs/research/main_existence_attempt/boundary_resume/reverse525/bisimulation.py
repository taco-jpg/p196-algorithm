"""Labeled forward bisimulation quotient, preserving cyclic words up to powers.

Every quotient edge has a matching edge from EVERY member of its source
block. Consequently a repeated quotient closed walk lifts to an infinite
path in the original finite graph. A repeated original vertex/phase gives
a closed lift of a positive power of the quotient word. This is sufficient
for all-temporal-period exterior existence, and for excluding a uniform
root cycle. A witness must be lifted before ordinary arithmetic replay.
"""
from collections import defaultdict
import json,time
from pathlib import Path

def quotient(n,edges):
    outgoing=[[]for _ in range(n)]
    for u,v,l in edges:outgoing[u].append((l,v))
    blocks=[0]*n;rounds=0
    while True:
        ids={};new=[]
        for u in range(n):
            key=(blocks[u],tuple(sorted({(l,blocks[v])for l,v in outgoing[u]})))
            if key not in ids:ids[key]=len(ids)
            new.append(ids[key])
        rounds+=1
        if new==blocks:break
        blocks=new
    m=max(blocks,default=-1)+1
    qedges=sorted({(blocks[u],blocks[v],l)for u,v,l in edges})
    # Every member must realize exactly the same quotient outgoing edges.
    wanted=[set()for _ in range(m)]
    for u,v,l in qedges:wanted[u].add((l,v))
    assert all({(l,blocks[v])for l,v in outgoing[u]}==wanted[blocks[u]]for u in range(n))
    return dict(vertices=m,edges=qedges,blocks=blocks,rounds=rounds)

if __name__=='__main__':
    here=Path(__file__).resolve().parent;records=[]
    for k in range(9):
        g=json.loads((here/f'graph_{k}.json').read_text());start=time.monotonic();q=quotient(g['vertices'],g['edges'])
        r=dict(depth=k,vertices=g['vertices'],edges=len(g['edges']),qvertices=q['vertices'],qedges=len(q['edges']),rounds=q['rounds'],seconds=time.monotonic()-start)
        records.append(r);print(json.dumps(r),flush=True)
        (here/f'bisim_graph_{k}.json').write_text(json.dumps(q,separators=(',',':'))+'\n')
    (here/'bisim_summary.json').write_text(json.dumps(records,indent=2)+'\n')
