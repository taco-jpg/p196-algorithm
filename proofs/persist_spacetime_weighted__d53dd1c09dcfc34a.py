"""All-length additive invariant synthesis with one full row of carry memory.

Every weight labels an exact digit/carry transition of reverse-and-add, rather
than a pair-sum symbol alone. Finite transducer potentials certify inequalities
on arbitrarily long accepted words. A solver result is not an existence claim.
"""
from collections import defaultdict,deque
from fractions import Fraction
from creative_regular_direct import fst_graph
import creative_regular_invariant as r
import json,time,argparse

FS,FE=fst_graph()
OUT=defaultdict(list)
for i,(a,q,s,b) in enumerate(FE):OUT[a].append((q,s,b,i))
TERMS={}; TS=[]
for x,(h,a,b,d,started) in enumerate(FS):
    for center in [None]+list(range(0,19,2)):
        if not started and (center is None or center==0):continue
        if center is None:
            if a!=b:continue
            extra=None; oc=2*d if h else None
        else:
            if r.C(center,a)!=b:continue
            extra=r.D(center,a)+d if h else None
            oc=None if h else 2*r.D(center,a)
        k=len(FE)+len(TS)
        TERMS[x,center]=(extra,oc,k)
        TS.append((x,center,extra,oc))
NW=len(FE)+len(TS)

def add(*dicts):
    out=defaultdict(int)
    for ds in dicts:
        for k,v in ds.items():out[k]+=v
    return {k:v for k,v in out.items() if v}

def advance(flags,q):
    low,exc,started=flags
    return low and q<=9,exc and (q in (0,11) if started else q==11),True

def terminal_bad(flags,center):
    low,exc,started=flags
    return (low and (center is None or center<=9)) or (exc and started and (center is None or center==0))

def safety_graph():
    states=[(0,True,True,False),(1,True,True,False)];ids={s:i for i,s in enumerate(states)}
    edges=[];terms=[]
    for st in states:
        x,*flags=st;u=ids[st]
        for (xx,c),(extra,oc,k) in TERMS.items():
            if xx!=x:continue
            ff=flags if extra is None else advance(flags,extra)
            if terminal_bad(ff,oc):terms.append((u,{k:-1}))
        for q,o,y,k in OUT[x]:
            ff=advance(flags,o)
            if not (ff[0] or ff[1]):continue
            ns=(y,*ff)
            if ns not in ids:ids[ns]=len(states);states.append(ns)
            edges.append((u,ids[ns],{k:-1}))
    return states,[0,1],edges,terms

def closure_graph(lam,mode='all'):
    lam=Fraction(lam);num,den=lam.numerator,lam.denominator
    states=[(a,b) for a in (0,1) for b in (0,1) if mode=='all' or (a!=b if mode=='alternating' else a==b)]
    initial=list(range(len(states)));ids={s:i for i,s in enumerate(states)}
    edges=[];terms=[]
    for x,y in states:
        u=ids[x,y]
        for (xx,c),(extra,oc,k) in TERMS.items():
            if xx!=x:continue
            endpoints=[(y,{})] if extra is None else [(yy,{j:den}) for q,o,yy,j in OUT[y] if q==extra]
            for yy,weight in endpoints:
                if (yy,oc) not in TERMS:continue
                kk=TERMS[yy,oc][2]
                terms.append((u,{k:-1} if mode=='wrong_clock_safety' else add(weight,{kk:den},{k:-num})))
        for q,o,xx,k in OUT[x]:
            for q2,o2,yy,j in OUT[y]:
                if q2!=o:continue
                ns=(xx,yy)
                if ns not in ids:ids[ns]=len(states);states.append(ns)
                edges.append((u,ids[ns],{k:-1} if mode=='wrong_clock_safety' else add({j:den},{k:-num})))
    return states,initial,edges,terms

def trim(graph):
    states,initial,edges,terms=graph
    rev=defaultdict(list)
    for u,v,c in edges:rev[v].append(u)
    live={u for u,c in terms};todo=deque(live)
    while todo:
        for u in rev[todo.popleft()]:
            if u not in live:live.add(u);todo.append(u)
    ix={s:i for i,s in enumerate(sorted(live))}
    return [states[s] for s in sorted(live)],[ix[s] for s in initial if s in live],[(ix[u],ix[v],c) for u,v,c in edges if u in live and v in live],[(ix[u],c) for u,c in terms]

def history_path(word):
    pairs,center=word
    paths=[(x,[]) for x in (0,1)]
    for q in pairs:
        paths=[(y,path+[k]) for x,path in paths for qq,o,y,k in OUT[x] if qq==q]
    paths=[path+[TERMS[x,center][2]] for x,path in paths if (x,center) in TERMS]
    assert len(paths)==1,(word,len(paths))
    return paths[0]

def history_weights(word):
    return add(*[{i:1} for i in history_path(word)])

def constraints(lam,seed):
    """Return exact integral rows A*x<=b; weights and potentials are free."""
    rows=[];rhs=[];nv=NW;meta=[]
    alternating=isinstance(seed,dict) and seed.get('restriction')=='alternating-clock'
    graphs=[('safety',safety_graph()),('closure',closure_graph(lam,'alternating' if alternating else 'all'))]
    if alternating:graphs.append(('wrong_clock_safety',closure_graph(lam,'wrong_clock_safety')))
    for name,graph in graphs:
        states,initial,edges,terms=trim(graph);base=nv;nv+=len(states)
        for i in initial:
            rows.extend([{base+i:1},{base+i:-1}]);rhs.extend([0,0])
        for u,v,cost in edges:
            rows.append(add({base+v:1},{base+u:-1},{k:-v for k,v in cost.items()}));rhs.append(0)
        for u,cost in terms:
            rows.append(add({base+u:-1},{k:-v for k,v in cost.items()}));rhs.append(0)
        meta.append(dict(name=name,states=len(states),edges=len(edges),terminals=len(terms)))
    score=({int(k):v for k,v in seed['history_linear_form'].items()} if isinstance(seed,dict) else history_weights(seed))
    rows.append({k:-v for k,v in score.items()});rhs.append(-1)
    return nv,rows,rhs,meta

def solve(lam='1',seconds=30,engine='scipy',seed=((7,),18)):
    start=time.monotonic();nv,rows,rhs,meta=constraints(lam,seed)
    result=dict(lambda_=lam,seed=seed,weights=NW,variables=nv,constraints=len(rows),graphs=meta,engine=engine)
    if engine=='scipy':
        import numpy as np
        from scipy.optimize import linprog
        from scipy.sparse import coo_matrix
        ii=[];jj=[];data=[]
        # Normalize the free homogeneous cone and maximize seed positivity.
        # This avoids an ill-conditioned infeasible pure-feasibility problem.
        objective=np.zeros(nv)
        for j,v in rows[-1].items():objective[j]=v
        for i,row in enumerate(rows[:-1]):
            for j,v in row.items():ii.append(i);jj.append(j);data.append(v)
        matrix=coo_matrix((data,(ii,jj)),shape=(len(rows)-1,nv)).tocsr()
        out=linprog(objective,A_ub=matrix,b_ub=rhs[:-1],bounds=[(-1,1)]*NW+[(None,None)]*(nv-NW),method='highs-ds',options={'time_limit':seconds})
        result.update(status=int(out.status),message=out.message)
        if out.status==0:
            result['max_seed_score']=-float(out.fun)
            result['candidate']=[str(Fraction(float(v)).limit_denominator(100000)) for v in out.x]
            vals=[Fraction(v) for v in result['candidate']]
            violations=[i for i,row in enumerate(rows[:-1]) if sum(vals[j]*v for j,v in row.items())>rhs[i]]
            result['exact_recheck_violations']=violations[:10]
            result['exact_recheck_passed']=not violations
            result['exact_seed_score']=str(-sum(vals[j]*v for j,v in rows[-1].items()))
            # An exact dual of a zero optimum proves this entire score cone
            # cannot be positive on the seed; floating infeasibility never does.
            dual=[Fraction(float(v)).limit_denominator(1000000) for v in out.ineqlin.marginals]
            coefficients=defaultdict(Fraction)
            for i,y in enumerate(dual):
                if y:
                    for j,a in rows[i].items():coefficients[j]+=y*a
            equalities=[j for j in range(nv) if coefficients[j]!=Fraction(int(objective[j]))]
            result['dual_nonzero']=sum(bool(v) for v in dual)
            result['dual_signs_ok']=all(v<=0 for v in dual)
            result['exact_dual_mismatch_count']=len(equalities)
            result['exact_dual_proves_seed_nonpositive']=not equalities and all(v<=0 for v in dual)
            result['dual_approx_support']={i:repr(float(v)) for i,v in enumerate(out.ineqlin.marginals) if abs(v)>1e-12}
            if result['exact_dual_proves_seed_nonpositive']:
                result['dual_certificate']={i:str(v) for i,v in enumerate(dual) if v}
    else:
        import z3
        solver=z3.SolverFor('QF_LRA');solver.set(timeout=int(seconds*1000))
        xs=[z3.Real(f'w{i}') for i in range(nv)]
        def expr(row):
            terms=[f'w{j}' if v==1 else f'(- w{j})' if v==-1 else f'(* {v} w{j})' for j,v in row.items()]
            return '0' if not terms else terms[0] if len(terms)==1 else '(+ '+' '.join(terms)+')'
        smt='\n'.join([f'(declare-fun w{i} () Real)' for i in range(nv)]+[f'(assert (<= {expr(row)} {b}))' for row,b in zip(rows,rhs)])
        solver.from_string(smt)
        print('exact solver built',round(time.monotonic()-start,3),flush=True)
        out=solver.check();result['status']=str(out)
        if out==z3.sat:result['candidate']=[str(solver.model().eval(v,model_completion=True)) for v in xs]
        if out==z3.unknown:result['reason']=solver.reason_unknown()
    result['seconds']=time.monotonic()-start
    result['infinite_existence_proved']=False
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--lambda',dest='lam',default='1');ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--engine',default='scipy');args=ap.parse_args()
    out=solve(args.lam,args.seconds,args.engine)
    print(json.dumps({k:v for k,v in out.items() if k not in ('candidate','dual_certificate','dual_approx_support')},indent=2),flush=True)
    with open('persist_spacetime_weighted_'+args.engine+'_'+args.lam.replace('/','_')+'.json','w') as f:json.dump(out,f,indent=2)
