"""Independent complete finite successor generation and closure audit.

The reference relation enumerates actual q and incoming high carry in each
phase, directly normalizes the two decimal columns, and then closes time.
It does not use the discovery routine's eliminated-carry branch formulas.
"""
from pathlib import Path
from collections import deque
import json,hashlib
from columns import successors,initial,bulk_state
HERE=Path(__file__).resolve().parent


def reference(state,clock):
    aa,bb,zz=state;p=len(clock);bpos=zpos=0;phase=[]
    for t,h in enumerate(clock):
        table={q:[]for q in range(19)}
        for q in range(19):
            low=(q+aa[t])%10;next_low=(q+aa[t])//10
            for incoming_high in (0,1):
                high=(q+incoming_high)%10;outgoing_high=(q+incoming_high)//10
                if h:
                    previous_high_digit=zz[zpos]+outgoing_high
                    if not 0<=previous_high_digit<=9:continue
                    next_q=low+previous_high_digit
                    item=(next_q,next_low,None,q-10*outgoing_high)
                else:
                    if outgoing_high!=bb[bpos]:continue
                    item=(low+high,next_low,incoming_high,None)
                if item not in table[q]:table[q].append(item)
        phase.append(table)
        if h:zpos+=1
        else:bpos+=1
    out={}
    for first in range(19):
        paths=[(first,(),(),(),())]
        for t,table in enumerate(phase):
            nextpaths=[]
            for q,a,b,z,word in paths:
                for r,na,nb,nz in table[q]:
                    nextpaths.append((r,a+(na,),b+(()if nb is None else(nb,)),
                                      z+(()if nz is None else(nz,)),word+(q,)))
            paths=nextpaths
        for q,a,b,z,word in paths:
            if q==first:out.setdefault((a,b,z),word)
    return out


def outer_edges(q):
    # Normalize the outer mirrored pair with each possible inward carry.
    out=set()
    for inward in (0,1):
        h=(q+inward)//10
        nxt=q%10+(1 if h else(q+inward)%10)
        out.add((nxt,h))
    return sorted(out)


def outer_catalog(p,g):
    def canon(x):return min(x[i:]+x[:i]for i in range(len(x)))
    cycles=set()
    def dfs(path,growth):
        t=len(path)
        for q,h in outer_edges(path[-1]):
            ng=growth+h
            if ng>g or ng+p-t<g:continue
            if t==p:
                if q==path[0] and ng==g:cycles.add(canon(path))
            else:dfs(path+(q,),ng)
    for q in range(1,19):dfs((q,),0)
    return sorted(cycles)


def verify_graph(outer,clock,stored=None):
    root=initial(outer,clock);depth={root:1};todo=deque([root]);edges={}
    while todo:
        state=todo.popleft();ref=reference(state,clock);got=successors(state,clock)
        assert set(ref)==set(got),'successor completeness mismatch'
        edges[state]=tuple(ref)
        for nxt in ref:
            if nxt not in depth:depth[nxt]=depth[state]+1;todo.append(nxt)
    if stored is not None:assert set(depth)==stored
    # A topological ordering verifies acyclicity independently of BFS depth.
    indegree={s:0 for s in depth}
    for s,ns in edges.items():
        for n in ns:indegree[n]+=1
    queue=deque(s for s in depth if not indegree[s]);rank={s:1 for s in queue}
    visited=0
    while queue:
        s=queue.popleft();visited+=1
        for n in edges[s]:
            rank[n]=max(rank.get(n,0),rank[s]+1);indegree[n]-=1
            if indegree[n]==0:queue.append(n)
    assert visited==len(depth),'closed graph has cycles'
    assert all(rank[v]>rank[u]for u,vs in edges.items()for v in vs)
    return dict(outer=outer,clock=clock,states=len(depth),edges=sum(map(len,edges.values())),
                maximum_columns=max(rank.values()),acyclic=True,
                complete_reference_replay=True),depth


def run():
    full=outer_catalog(14,6);assert len(full)==19
    archived=json.loads((HERE/'clock14_outer.json').read_text())
    assert full==sorted(tuple(r['clock'])for r in archived)
    records=[]
    for i,outer in enumerate(full):
        clock=[next(h for q,h in outer_edges(outer[t])if q==outer[(t+1)%14])for t in range(14)]
        result,states=verify_graph(outer,clock)
        result['catalog_index']=i;records.append(result)
        data=json.dumps(list(states),separators=(',',':'))+'\n'
        name=f'catalog14_{i}_closed.json';(HERE/name).write_text(data)
        result['certificate_file']=name
        result['certificate_sha256']=hashlib.sha256(data.encode()).hexdigest()
        print(json.dumps(result),flush=True)
    result=dict(period=14,gain=6,outer_cycles=len(records),
                states=sum(r['states']for r in records),
                edges=sum(r['edges']for r in records),
                maximum_columns=max(r['maximum_columns']for r in records),
                all_graphs_complete_acyclic=True,records=records,
                scope='Excludes a14-step gain6 recurrence of55 outer q coefficients in words of at least110 digits; in particular excludes growing fixed-prefix-limit pumps at this period/gain.',
                decimal_existence_proved=False,new_lean_theorem=False)
    (HERE/'audit14.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':run()
