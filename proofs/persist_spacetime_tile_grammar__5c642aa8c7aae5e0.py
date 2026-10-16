"""Synthesize an exact all-length invariant language of allowed carry tiles.

The addition transducer itself supplies all grammar states. Boolean choices
allow or reject each full carry/digit edge and valid center tile. A candidate
must avoid palindrome-producing outputs and remain closed under one more
addition. No finite iteration or word-length cutoff occurs in these clauses.
"""
from persist_spacetime_weighted import FS,FE,TS,OUT,TERMS,NW,history_path,safety_graph,trim
import z3,json,time,argparse

def composed_tiles():
    states=[(a,b) for a in (0,1) for b in (0,1)];ids={s:i for i,s in enumerate(states)}
    edges=[];terms=[]
    for x,y in states:
        u=ids[x,y]
        for (xx,c),(extra,oc,k) in TERMS.items():
            if xx!=x:continue
            endpoints=[(y,None)] if extra is None else [(yy,j) for q,o,yy,j in OUT[y] if q==extra]
            for yy,j in endpoints:
                if (yy,oc) in TERMS:terms.append((u,k,j,TERMS[yy,oc][2]))
        for q,o,xx,k in OUT[x]:
            for q2,o2,yy,j in OUT[y]:
                if q2!=o:continue
                ns=(xx,yy)
                if ns not in ids:ids[ns]=len(states);states.append(ns)
                edges.append((u,ids[ns],k,j))
    return states,edges,terms

def build(seed=((8,16),16)):
    solver=z3.Solver();allowed=[z3.Bool(f'a{i}') for i in range(NW)]
    st,initial,edges,terms=trim(safety_graph());safe=[z3.Bool(f's{i}') for i in range(len(st))]
    solver.add(*[safe[i] for i in initial])
    for u,v,cost in edges:
        k=next(iter(cost));assert cost[k]==-1
        solver.add(z3.Implies(z3.And(safe[u],allowed[k]),safe[v]))
    for u,cost in terms:
        k=next(iter(cost));solver.add(z3.Not(z3.And(safe[u],allowed[k])))
    states,ee,tt=composed_tiles()
    good=[z3.Bool(f'g{i}') for i in range(len(states))]
    bad=[z3.Bool(f'b{i}') for i in range(len(states))]
    solver.add(*good[:4])
    for u,v,a,b in ee:
        solver.add(z3.Implies(z3.And(good[u],allowed[a],allowed[b]),good[v]))
        solver.add(z3.Implies(z3.And(good[u],allowed[a],z3.Not(allowed[b])),bad[v]))
        solver.add(z3.Implies(z3.And(bad[u],allowed[a]),bad[v]))
    for u,a,extra,b in tt:
        solver.add(z3.Not(z3.And(bad[u],allowed[a])))
        required=allowed[b] if extra is None else z3.And(allowed[extra],allowed[b])
        solver.add(z3.Implies(z3.And(good[u],allowed[a]),required))
    if seed is not None:
        solver.add(*[allowed[i] for i in history_path(seed)])
    else:
        # A ranked witness establishes genuine nonemptiness, including paths
        # of every length: any accepting path can be shortened to a simple
        # one in the 46-state fixed transducer.
        witness=[z3.Bool(f'witness{i}') for i in range(len(FS))]
        rank=[z3.BitVec(f'rank{i}',6) for i in range(len(FS))]
        solver.add(witness[0],witness[1],rank[0]==0,rank[1]==0)
        incoming={i:[] for i in range(len(FS))}
        for k,(u,q,o,v) in enumerate(FE):
            incoming[v].append(z3.And(witness[u],allowed[k],z3.ULT(rank[u],rank[v])))
        for i in range(2,len(FS)):solver.add(z3.Implies(witness[i],z3.Or(incoming[i])))
        solver.add(z3.Or([z3.And(witness[x],allowed[k]) for (x,c),(extra,oc,k) in TERMS.items()]))
    return solver,allowed,dict(tiles=NW,safety_states=len(st),composition_states=len(states),composition_edges=len(ee),composition_terminals=len(tt),seed=seed)

def solve(seed=((8,16),16),seconds=40):
    start=time.monotonic();s,a,meta=build(seed);s.set(timeout=int(seconds*1000))
    print('built',round(time.monotonic()-start,3),meta,flush=True)
    result=s.check();out=dict(meta,status=str(result),seconds=time.monotonic()-start)
    if result==z3.sat:out['allowed_tiles']=[i for i,x in enumerate(a) if z3.is_true(s.model().eval(x,model_completion=True))]
    if result==z3.unknown:out['reason']=s.reason_unknown()
    out['infinite_existence_proved']=False
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=40);p.add_argument('--seed',default='18887');args=p.parse_args()
    seed=None if args.seed=='any' else ((7,),18) if args.seed=='196' else ((8,16),16)
    out=solve(seed,args.seconds);print(json.dumps(out,indent=2),flush=True)
    json.dump(out,open('persist_spacetime_tile_grammar_'+args.seed+'.json','w'),indent=2)
