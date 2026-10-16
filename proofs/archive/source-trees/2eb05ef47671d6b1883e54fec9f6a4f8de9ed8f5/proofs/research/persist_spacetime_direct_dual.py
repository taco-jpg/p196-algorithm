"""Numerically minimize certificate size, then recover and check it exactly."""
from persist_spacetime_weighted import constraints
from persist_spacetime_dual import recover
from persist_spacetime_check_certificate import check
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import json,time,sys

def run(source):
    start=time.monotonic();r=json.load(open(source));seed=r['seed']
    if not isinstance(seed,dict):seed=(tuple(seed[0]),seed[1])
    nv,rows,rhs,meta=constraints(r['lambda_'],seed)
    ii=[];jj=[];data=[]
    for i,row in enumerate(rows[:-1]):
        for j,v in row.items():ii.append(j);jj.append(i);data.append(v)
    matrix=coo_matrix((data,(ii,jj)),shape=(nv,len(rows)-1)).tocsr()
    target=np.array([rows[-1].get(j,0) for j in range(nv)])
    out=linprog(-np.ones(len(rows)-1),A_eq=matrix,b_eq=target,bounds=(None,0),method='highs-ds',options={'time_limit':40})
    print('direct dual',out.status,out.message,'seconds',time.monotonic()-start,flush=True)
    if out.status!=0:return dict(status=int(out.status),message=out.message)
    r['dual_approx_support']={i:repr(float(v)) for i,v in enumerate(out.x) if abs(v)>1e-12}
    temp=source.replace('.json','_dual_support.json');json.dump(r,open(temp,'w'))
    exact=recover(temp)
    dst=source.replace('weighted','direct_dual');json.dump(exact,open(dst,'w'),indent=2)
    print({k:v for k,v in exact.items() if k!='dual'},flush=True)
    if exact.get('exact_certificate'):print(check(dst),flush=True)
    return exact

if __name__=='__main__':run(sys.argv[1])
