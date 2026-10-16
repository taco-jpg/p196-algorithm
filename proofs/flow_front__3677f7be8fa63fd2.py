"""Numerical discovery of EXACTLY RECHECKED integer flow counterexamples.

This routine never reports absence. Bounds and numerical infeasibility have
no proof status; only a connected, exactly verified integral flow is returned.
"""
import time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix

def components(edges,mult,source):
    adj={}
    for amount,(u,v,*_) in zip(mult,edges):
        if amount:adj.setdefault(u,set()).add(v);adj.setdefault(v,set()).add(u)
    left=set(adj);parts=[]
    while left:
        part={next(iter(left))};todo=list(part)
        while todo:
            for v in adj[todo.pop()]:
                if v not in part:part.add(v);todo.append(v)
        parts.append(part);left.difference_update(part)
    return parts

def discover(edges,n,source,sink,seconds=5,limit=10000):
    began=time.monotonic();ne=len(edges)
    rows=[{} for _ in range(n)];low=[0]*n;high=[0]*n
    low[source]=high[source]=1;low[sink]=high[sink]=-1
    for j,(u,v,*_) in enumerate(edges):
        rows[u][j]=rows[u].get(j,0)+1;rows[v][j]=rows[v].get(j,0)-1
    rows += [{j:e[2] for j,e in enumerate(edges) if e[2]},
             {j:e[3] for j,e in enumerate(edges) if e[3]},
             {j:1 for j in range(ne)}]
    low += [1,-np.inf,0];high += [np.inf,0,limit]
    while time.monotonic()-began<seconds:
        ii=[];jj=[];vv=[]
        for i,row in enumerate(rows):
            for j,v in row.items():
                if v:ii.append(i);jj.append(j);vv.append(v)
        matrix=coo_matrix((vv,(ii,jj)),shape=(len(rows),ne)).tocsc()
        result=milp(np.ones(ne),integrality=np.ones(ne),bounds=Bounds(0,limit),
                    constraints=LinearConstraint(matrix,low,high),
                    options={'time_limit':max(.01,seconds-(time.monotonic()-began)),
                             'mip_rel_gap':0.0})
        if result.x is None:return None
        mult=[int(round(x)) for x in result.x]
        if any(x<0 for x in mult):return None
        # Numerical success is accepted only after exact integer arithmetic.
        if any((lo!=-np.inf and sum(mult[j]*a for j,a in row.items())<lo) or
               (hi!=np.inf and sum(mult[j]*a for j,a in row.items())>hi)
               for row,lo,hi in zip(rows,low,high)):return None
        parts=components(edges,mult,source)
        root=next(part for part in parts if source in part)
        restricted=[a if e[0] in root else 0 for a,e in zip(mult,edges)]
        if sum(a*e[2] for a,e in zip(restricted,edges))>=1 and sum(a*e[3] for a,e in zip(restricted,edges))<=0:
            return restricted
        for part in parts:
            if source in part:continue
            row={}
            for j,(u,v,*_) in enumerate(edges):
                coefficient=int(u in part or v in part)-limit*int((u in part)!=(v in part))
                if coefficient:row[j]=coefficient
            rows.append(row);low.append(-np.inf);high.append(0)
    return None
