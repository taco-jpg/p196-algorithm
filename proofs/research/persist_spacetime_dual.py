"""Recover an exact rational Farkas certificate on a numerical dual support."""
from persist_spacetime_weighted import constraints
from fractions import Fraction as F
from collections import defaultdict
import json,time,sys,heapq

def eliminate(equations,rhs,n):
    incidence=[set() for _ in range(n)]
    for i,row in enumerate(equations):
        for j in row:incidence[j].add(i)
    heap=[(len(row),i) for i,row in enumerate(equations) if row];heapq.heapify(heap)
    active=set(range(len(equations)));pivots=[]
    while heap:
        size,i=heapq.heappop(heap)
        if i not in active or not equations[i] or len(equations[i])!=size:continue
        row=equations[i]
        j=min(row,key=lambda j:(len(incidence[j]),abs(row[j].numerator)+row[j].denominator))
        pivot=row[j];row={k:v/pivot for k,v in row.items()};b=rhs[i]/pivot
        pivots.append((j,row,b));active.remove(i)
        for k in row:incidence[k].discard(i)
        affected=list(incidence[j])
        for ii in affected:
            rr=equations[ii];mult=rr[j];rhs[ii]-=mult*b
            for k,v in row.items():
                value=rr.get(k,F(0))-mult*v
                if value:
                    if k not in rr:incidence[k].add(ii)
                    rr[k]=value
                elif k in rr:del rr[k];incidence[k].discard(ii)
            if not rr:
                if rhs[ii]:return None,dict(inconsistent=True,pivots=len(pivots))
                active.discard(ii)
            else:heapq.heappush(heap,(len(rr),ii))
        if len(pivots)%100==0:print('pivots',len(pivots),'active',len(active),flush=True)
    sol=[F(0) for _ in range(n)]
    for j,row,b in reversed(pivots):sol[j]=b-sum(v*sol[k] for k,v in row.items() if k!=j)
    return sol,dict(pivots=len(pivots),free=n-len(pivots))

def recover(path):
    start=time.monotonic();record=json.load(open(path));lam=record['lambda_'];seed=record['seed']
    if not isinstance(seed,dict):seed=(tuple(seed[0]),seed[1])
    nv,rows,rhs,meta=constraints(lam,seed)
    support=sorted(map(int,record['dual_approx_support']));ix={k:i for i,k in enumerate(support)}
    equations=[{} for _ in range(nv)]
    for k in support:
        for j,v in rows[k].items():equations[j][ix[k]]=F(v)
    objective=[F(rows[-1].get(j,0)) for j in range(nv)]
    sol,info=eliminate(equations,objective,len(support))
    result=dict(lambda_=lam,seed=seed,support=len(support),**info)
    if sol is not None:
        coeff=defaultdict(F)
        for k,y in zip(support,sol):
            for j,v in rows[k].items():coeff[j]+=y*v
        mismatch=[j for j in range(nv) if coeff[j]!=rows[-1].get(j,0)]
        result.update(signs_ok=all(y<=0 for y in sol),mismatch_count=len(mismatch),positive_duals=sum(y>0 for y in sol))
        result['exact_certificate']=result['signs_ok'] and not mismatch
        if result['exact_certificate']:result['dual']={k:str(y) for k,y in zip(support,sol) if y}
    result['seconds']=time.monotonic()-start
    return result

if __name__=='__main__':
    path=sys.argv[1] if len(sys.argv)>1 else 'persist_spacetime_weighted_scipy_1.json'
    result=recover(path)
    print(json.dumps({k:v for k,v in result.items() if k!='dual'},indent=2),flush=True)
    json.dump(result,open('persist_spacetime_dual_'+result['lambda_'].replace('/','_')+'.json','w'),indent=2)
