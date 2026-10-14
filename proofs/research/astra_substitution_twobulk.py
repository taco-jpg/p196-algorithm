"""Finite SMT discovery for two independently growing nonconstant word bulks.

The exact periodic-family verifier audits SAT outputs. UNSAT here only covers
the displayed bounded template and sample lengths; UNKNOWN remains unresolved.
"""
import argparse,json,random,time
from pathlib import Path
import z3 as z
from astra_substitution_periodic import candidate,primitive
from resume_renewal_bulk import transform

def pool(period):
    data=json.load(open('resume_renewal_bulk_results.json'))
    out=set()
    for row in data:
        if row['width']!=3:continue
        for cycle in row['cycles_mod_rotation']:
            for word in cycle:
                if len(primitive(tuple(word)))==1:continue
                for r in range(3):
                    q=tuple(word[r:]+word[:r]);w=q
                    for t in range(period):w=transform(w,t%2)
                    if w==q:out.add(q)
    return sorted(out)

def solve(B,C,k,vlen,wlen,seconds=2,period=24,m=12,n=13):
    assert period==24 and len(B)==len(C)==3
    start=time.monotonic();slv=z.SolverFor('QF_BV');slv.set(timeout=int(1000*seconds))
    bv=lambda n:z.BitVecVal(n,5)
    P=[bv(8)]+[z.BitVec(f'P{i}',5) for i in range(1,k)]
    V=[z.BitVec(f'V{i}',5) for i in range(vlen)]
    Wh=[z.BitVec(f'W{i}',5) for i in range((wlen+1)//2)]
    W=Wh+Wh[:wlen//2][::-1]
    for x in P+V+Wh:slv.add(z.ULE(x,bv(18)))
    if wlen%2:slv.add(Wh[-1]&bv(1)==bv(0))
    def template(a,b):
        half=P+[bv(x) for x in B]*a+V+[bv(x) for x in C]*b
        return half+W+half[::-1]
    Q=template(m,n)
    for t in range(period):
        # Symmetric column sum words have this complete next-palindrome test.
        slv.add(z.Or([z.UGT(x,bv(9)) for x in Q]))
        slv.add(z.Or(Q[0]!=bv(11),z.Or([z.And(x!=bv(0),x!=bv(11)) for x in Q])))
        ds=[];carry=bv(0)
        for i,x in enumerate(Q):
            if z.is_bv_value(x):
                xv=x.as_long();nc=bv(0) if xv<9 else bv(1) if xv>9 else carry
            else:
                nc=z.BitVec(f'c{t}_{i}',5)
                slv.add(nc==z.If(z.UGE(x+carry,bv(10)),bv(1),bv(0)))
            ds.append(z.simplify(x+carry-bv(10)*nc));carry=nc
        overflow=t%2;slv.add(carry==bv(overflow))
        if overflow:ds.append(bv(1))
        new=[]
        for i in range((len(ds)+1)//2):
            expr=z.simplify(ds[i]+ds[-1-i])
            if z.is_bv_value(expr):new.append(expr)
            else:
                var=z.BitVec(f'q{t}_{i}',5);slv.add(var==expr);new.append(var)
        Q=new+new[:len(ds)//2][::-1]
    target=template(m+1,n+1)
    assert len(Q)==len(target)
    for x,y in zip(Q,target):slv.add(x==y)
    result=slv.check()
    out={'B':B,'C':C,'exterior':k,'interface':vlen,'center':wlen,'period':period,'m':m,'n':n,'status':str(result),'seconds':time.monotonic()-start}
    if result==z.sat:
        model=slv.model();vals=lambda xs:tuple(model.eval(x).as_long() for x in xs)
        pp,vv,ww=vals(P),vals(V),vals(W)
        out.update(P=pp,V=vv,W=ww)
        initial=[(pp,len(pp),False),(B,3*m,True),(vv,len(vv),False),(C,3*n,True),(ww,len(ww),False),(C[::-1],3*n,True),(vv[::-1],len(vv),False),(B[::-1],3*m,True),(pp[::-1],len(pp),False)]
        initial=[s for s in initial if s[1]]
        final=[(w,length+(3 if repeat else 0),repeat) for w,length,repeat in initial]
        cert,why=candidate(initial,final,period)
        out['exact_check']=why
        if cert:out['certificate']=cert
    elif result==z.unknown:out['reason']=slv.reason_unknown()
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--count',type=int,default=60);p.add_argument('--seconds',type=float,default=2);p.add_argument('--seed',type=int,default=196);p.add_argument('--out',default='astra_substitution_twobulk_results.json');args=p.parse_args()
    rng=random.Random(args.seed);bulks=pool(24);print(json.dumps({'returning_period3_motifs':len(bulks)}),flush=True)
    records=[]
    for it in range(args.count):
        B,C=rng.sample(bulks,2)
        k,v,w=rng.choice([(3,2,2),(4,3,4),(6,4,4),(8,6,6),(12,8,8)])
        row=solve(B,C,k,v,w,args.seconds)
        records.append(row);Path(args.out).write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(row),flush=True)
        if 'certificate' in row:break
