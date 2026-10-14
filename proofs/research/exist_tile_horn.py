"""Exact Horn encoding of closed full-carry-tile sublanguages.

All safe/closure clauses are Horn; only witness nonemptiness uses ranking.
A positive model is independently checked by graph reachability.
"""
from persist_spacetime_weighted import FS,FE,TS,OUT,TERMS,NW,history_path,safety_graph,trim
from persist_spacetime_tile_grammar import composed_tiles
from collections import defaultdict,deque
import z3,json,time,argparse


def horn_clauses():
    n=NW;clauses=[]
    st,initial,edges,terms=trim(safety_graph());sr=list(range(n,n+len(st)));n+=len(st)
    for i in initial:clauses.append(((),sr[i]))
    for u,v,cost in edges:
        k=next(iter(cost));assert cost[k]==-1
        clauses.append(((sr[u],k),sr[v]))
    for u,cost in terms:
        k=next(iter(cost));clauses.append(((sr[u],k),None))
    states,ee,tt=composed_tiles();fw=list(range(n,n+len(states)));n+=len(states);bw=list(range(n,n+len(states)));n+=len(states)
    for i in range(4):clauses.append(((),fw[i]))
    for u,v,a,b in ee:
        clauses.append(((fw[u],a),fw[v]))
        clauses.append(((bw[v],a),bw[u]))
        clauses.append(((fw[u],a,bw[v]),b))
    for u,a,extra,b in tt:
        clauses.append(((a,),bw[u]))
        clauses.append(((fw[u],a),b))
        if extra is not None:clauses.append(((fw[u],a),extra))
    clauses=list(dict.fromkeys((tuple(sorted(set(body))),head) for body,head in clauses))
    return n,clauses,dict(tiles=NW,variables=n,clauses=len(clauses),safety_states=len(st),composition_states=len(states))


def build(seed=None):
    n,clauses,meta=horn_clauses();xs=[z3.Bool(f'x{i}') for i in range(n)];s=z3.Solver()
    for body,head in clauses:s.add(z3.Or([z3.Not(xs[i]) for i in body]+([] if head is None else [xs[head]])))
    if seed is not None:s.add(*[xs[i] for i in history_path(seed)])
    else:
        witness=[z3.Bool(f'witness{i}') for i in range(len(FS))]
        rank=[z3.BitVec(f'rank{i}',6) for i in range(len(FS))]
        s.add(witness[0],witness[1],rank[0]==0,rank[1]==0)
        incoming=defaultdict(list)
        for k,(u,q,o,v) in enumerate(FE):incoming[v].append(z3.And(witness[u],xs[k],z3.ULT(rank[u],rank[v])))
        for i in range(2,len(FS)):s.add(z3.Implies(witness[i],z3.Or(incoming[i])))
        s.add(z3.Or([z3.And(witness[x],xs[k]) for (x,c),(extra,oc,k) in TERMS.items()]))
    return s,xs,meta


def least_closure(seed_tiles):
    n,clauses,meta=horn_clauses();inc=[[] for _ in range(n)];left=[]
    queue=deque(seed_tiles);seen=set();why={i:('seed',) for i in seed_tiles}
    for j,(body,head) in enumerate(clauses):
        left.append(len(body))
        if not body:
            if head is None:return None,dict(reason='empty negative clause')
            queue.append(head);why[head]=(j,)
        for v in body:inc[v].append(j)
    while queue:
        x=queue.popleft()
        if x in seen:continue
        seen.add(x)
        for j in inc[x]:
            left[j]-=1
            if left[j]==0:
                body,head=clauses[j]
                if head is None:return None,dict(conflict_clause=j,derived=len(seen),tiles=len([i for i in seen if i<NW]))
                if head not in seen:queue.append(head);why[head]=(j,)
    return sorted(i for i in seen if i<NW),dict(derived=len(seen),tiles=len([i for i in seen if i<NW]))


def path_and_check(allowed):
    aa=set(allowed);initial=[0,1];queue=deque(initial);paths={i:[] for i in initial}
    while queue:
        u=queue.popleft()
        for q,o,v,k in OUT[u]:
            if k in aa and v not in paths:paths[v]=paths[u]+[k];queue.append(v)
    accepting=[(paths[x]+[k],c) for (x,c),(extra,oc,k) in TERMS.items() if x in paths and k in aa]
    if not accepting:return dict(nonempty=False)
    # Independently enumerate the safety and composition product over allowed first-row edges.
    st,initial,edges,terms=trim(safety_graph());adj=defaultdict(list)
    for u,v,cost in edges:
        if next(iter(cost)) in aa:adj[u].append(v)
    live=set(initial);queue=deque(initial)
    while queue:
        for v in adj[queue.popleft()]:
            if v not in live:live.add(v);queue.append(v)
    badterms=[(u,next(iter(c))) for u,c in terms if u in live and next(iter(c)) in aa]
    states,ee,tt=composed_tiles();adj=defaultdict(list);rev=defaultdict(list)
    for u,v,a,b in ee:
        if a in aa:adj[u].append((v,b));rev[v].append(u)
    fw=set(range(4));queue=deque(fw)
    while queue:
        for v,b in adj[queue.popleft()]:
            if v not in fw:fw.add(v);queue.append(v)
    bw={u for u,a,extra,b in tt if a in aa};queue=deque(bw)
    while queue:
        for u in rev[queue.popleft()]:
            if u not in bw:bw.add(u);queue.append(u)
    missing=[b for u,v,a,b in ee if u in fw and v in bw and a in aa and b not in aa]
    for u,a,extra,b in tt:
        if u in fw and a in aa:
            if b not in aa:missing.append(b)
            if extra is not None and extra not in aa:missing.append(extra)
    path,c=min(accepting,key=lambda pc:len(pc[0]));pairs=[FE[k][1] for k in path[:-1]]
    return dict(nonempty=True,seed=[pairs,c],safe=not badterms,closed=not missing,safety_counterexamples=len(badterms),missing_tiles=sorted(set(missing)))


def solve(seconds,seed):
    t=time.monotonic();s,xs,meta=build(seed);s.set(timeout=int(seconds*1000));print('built',meta,flush=True)
    rr=s.check();out=dict(meta,status=str(rr),seconds=time.monotonic()-t)
    if rr==z3.sat:
        out['allowed_tiles']=[i for i in range(NW) if z3.is_true(s.model().eval(xs[i],model_completion=True))]
        out['independent_check']=path_and_check(out['allowed_tiles'])
        assert out['independent_check']['nonempty'] and out['independent_check']['safe'] and out['independent_check']['closed']
    elif rr==z3.unknown:out['reason']=s.reason_unknown()
    out['decimal_existence_proved']=rr==z3.sat
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=45);p.add_argument('--seed',default='any');p.add_argument('--engine',choices=['z3','horn'],default='z3');args=p.parse_args();seed=None if args.seed=='any' else ((7,),18) if args.seed=='196' else ((8,16),16)
    if args.engine=='horn':
        assert seed is not None;t=time.monotonic();tiles,meta=least_closure(history_path(seed));out=dict(meta,seed=seed,status='conflict' if tiles is None else 'safe_closed',seconds=time.monotonic()-t,decimal_existence_proved=tiles is not None)
        if tiles is not None:out['independent_check']=path_and_check(tiles);out['allowed_tiles']=tiles
    else:out=solve(args.seconds,seed)
    print(json.dumps(out,indent=2),flush=True);json.dump(out,open(f'exist_tile_horn_{args.seed}_{args.engine}.json','w'),indent=2)
