"""Exact affine families with changing mass parameter and residue defects.

One symbolic state covers every m=M+k (k>=0).  No digit word is sampled to
infer identities.  The finite horizon diagnoses candidate recurrences only;
the general long-18-run obstruction is stated separately in the report.
"""
from pathlib import Path
from collections import defaultdict
import sys,json

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/"continuation"),str(ROOT/"research")]
from wall_renewal_check import Len,ONE,ZERO,canon,normal,add_runs,expand


def min_len(a,b):
    if (a-b).nonnegative():return b
    if (b-a).nonnegative():return a
    raise ValueError(("affine crossing",a,b))


def take(runs,amount):
    left=[];runs=list(runs)
    while amount!=ZERO:
        assert runs
        x,n=runs.pop(0)
        part=min_len(n,amount)
        left.append((x,part));amount=amount-part
        if n!=part:runs.insert(0,(x,n-part))
    return canon(left),canon(runs)


def size(runs):
    return Len(sum(n.a for x,n in runs),sum(n.b for x,n in runs))


def mass_parameter(runs):
    a=sum(x*n.a for x,n in runs);b=sum(x*n.b for x,n in runs)
    assert a%18==b%18==0
    return Len(a//18,b//18)


def budgets(q,D):
    out=[(0,D)]
    tail=list(q)
    while tail:
        length=size(tail)
        if (length-D).nonnegative():part,tail=take(tail,D)
        elif (D-length).nonnegative():part=canon(tail+[(0,D-length)]);tail=[]
        else:raise ValueError(("width crossing",length,D))
        out=add_runs(out,part)
    return out


def step(q):
    d,h=normal(q,0)
    if h:d=canon(d+[(1,ONE)])
    return add_runs(d,list(reversed(d))),h


def original_coordinates(runs,M):
    return [[x,n.a,n.b-n.a*M] for x,n in runs]


def template(runs):
    # Variable run offsets may shift; all bounded words must match exactly.
    return tuple((x,n.a,None if n.a else n.b) for x,n in runs)


def shifted_identity(old,new):
    if len(old)!=len(new):return None
    shifts=set()
    for (x,a),(y,b) in zip(old,new):
        if x!=y or a.a!=b.a:return None
        if a.a==0:
            if a.b!=b.b:return None
        else:
            delta=b.b-a.b
            if delta%a.a:return None
            shifts.add(delta//a.a)
    return next(iter(shifts)) if len(shifts)==1 else None


def run(M=256,horizon=128):
    w=[(1,ONE),(9,Len(2,2*M-1)),(8,ONE),(2,ONE),(9,Len(2,2*M-1)),
       (16,ONE),(10,ONE),(9,Len(2,2*M-1)),(17,ONE)]
    q=canon(w+list(reversed(w)))
    rows=[];seen_q=defaultdict(list);seen_b=defaultdict(list)
    q_matches=[];budget_matches=[];overflow_count=0
    for t in range(horizon+1):
        D=mass_parameter(q);B=budgets(q,D)
        assert all(n.a==0 or x==18 for x,n in B), (t,B)
        nonzero=[(x-18,n) for x,n in B if x!=18]
        support=sum(n.b for x,n in nonzero)
        l1=sum(abs(x)*n.b for x,n in nonzero)
        centers=[];prefix=ZERO
        for x,n in B:
            if x!=18:centers.append([prefix.a,prefix.b-prefix.a*M,x-18,n.b])
            prefix=prefix+n
        row={"step":t,"overflows":overflow_count,"D_offset":D.b-6*M,
             "width_offset":size(q).b-12*M,"q_runs":len(q),
             "budget_runs":len(B),"defect_support":support,"defect_l1":l1,
             "variable_q_runs":[[x,n.a,n.b-n.a*M] for x,n in q if n.a],
             "defect_intervals_m_coordinates":centers,
             "q":original_coordinates(q,M),"budgets":original_coordinates(B,M)}
        rows.append(row)
        for earlier,old in seen_q[template(q)]:
            shift=shifted_identity(old,q)
            if shift is not None:q_matches.append([earlier,t,shift])
        seen_q[template(q)].append((t,q))
        for earlier,old in seen_b[template(B)]:
            shift=shifted_identity(old,B)
            if shift is not None:budget_matches.append([earlier,t,shift])
        seen_b[template(B)].append((t,B))
        # Decimal predecessor safety is exact; each used witness has positive
        # minimum length throughout the parameter domain.
        present=[x for x,n in q if n.b>0]
        assert max(present)>=10 and (q[0][0]!=11 or any(x not in (0,11) for x in present))
        if t<horizon:
            q,h=step(q);overflow_count+=h
    result={"parameter_domain":f"m={M}+k, every integer k>=0", "horizon":horizon,
            "q_parameter_shift_matches":q_matches,
            "budget_parameter_shift_matches":budget_matches,"rows":rows}
    Path(__file__).with_name("symbolic_defects.json").write_text(json.dumps(result,indent=2)+"\n")
    chosen=[r for r in rows if r["step"] in [8,9,10,11,12,16,24,32,48,64,96,128]]
    print(json.dumps({"domain":result["parameter_domain"],"q_matches":q_matches,
                      "budget_matches":budget_matches,
                      "selected":[{k:r[k] for k in ["step","D_offset","q_runs","defect_support","defect_l1"]} for r in chosen]},indent=2))


if __name__=="__main__":run()
