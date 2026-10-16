"""Exact unknown periodic-bulk, free-clock reverse-add pump search.

The q family is E_t ++ take(2*r*m+G_t, cycle(Q_t)) ++ reverse(E_t).
The two periodic carry streams are constrained at the ACTUAL center, not
merely at artificial bulk boundaries. Thus SAT would imply an all-m family.
Current uses require total growth divisible by 2*r. No SAT witness claimed.
"""
import argparse,json,time
from pathlib import Path
import z3


def numeric_q(n):
    d=[int(x) for x in str(n)[::-1]]
    return [a+b for a,b in zip(d,reversed(d))]


def realize(q):
    assert q==q[::-1]
    n=len(q);digits=[0]*n
    for i in range(n//2):
        digits[i]=q[i]-min(9,q[i]);digits[n-1-i]=min(9,q[i])
    if n%2:
        assert q[n//2]%2==0
        digits[n//2]=q[n//2]//2
    assert digits[-1]>0
    return int(''.join(map(str,digits[::-1])))


def solve(p,k,r,g,seconds=10,nonuniform=True,forced_clock=None,forced_bulk=None,forced_outer=None):
    assert g>0 and g%(2*r)==0
    start=time.monotonic()
    slv=z3.SolverFor('QF_BV');slv.set(timeout=int(seconds*1000))
    bv=lambda n:z3.BitVecVal(n,5)
    car=lambda x:z3.If(z3.UGE(x,10),bv(1),bv(0))
    Q=[[z3.BitVec(f'Q_{t}_{j}',5) for j in range(r)] for t in range(p)]
    E=[[z3.BitVec(f'E_{t}_{i}',5) for i in range(k)] for t in range(p)]
    A=[[z3.BitVec(f'A_{t}_{j}',5) for j in range(r)] for t in range(p)]
    B=[[z3.BitVec(f'B_{t}_{j}',5) for j in range(r)] for t in range(p)]
    a=[[z3.BitVec(f'a_{t}_{i}',5) for i in range(k+1)] for t in range(p)]
    b=[[z3.BitVec(f'b_{t}_{i}',5) for i in range(k+1)] for t in range(p)]
    h=[z3.Bool(f'h_{t}') for t in range(p)]
    gw=(p+1).bit_length()
    G=[z3.BitVec(f'G_{t}',gw) for t in range(p+1)]
    slv.add(G[0]==0,G[-1]==g)
    for t in range(p):
        nt=(t+1)%p
        slv.add(G[t+1]==G[t]+z3.If(h[t],z3.BitVecVal(1,gw),z3.BitVecVal(0,gw)))
        slv.add(z3.ULE(G[t],g))
        for x in Q[t]+E[t]:slv.add(z3.ULE(x,18))
        for x in A[t]+B[t]+a[t]+b[t]:slv.add(z3.ULE(x,1))
        slv.add(E[t][0]!=0)
        if nonuniform:slv.add(z3.Or([Q[t][j]!=Q[t][0] for j in range(1,r)]))
        lo=[];hi=[]
        for j in range(r):
            nj=(j+1)%r
            slv.add(A[t][nj]==car(Q[t][j]+A[t][j]))
            slv.add(B[t][j]==car(Q[t][j]+B[t][nj]))
            lo.append(Q[t][j]+A[t][j]-10*A[t][nj])
            hi.append(Q[t][j]+B[t][nj]-10*B[t][j])
        for j in range(r):
            slv.add(Q[nt][j]==z3.If(h[t],lo[j]+hi[(j-1)%r],lo[j]+hi[j]))
        # Canonical q words must be symmetric and represent actual digits.
        # All possible growth residues are enumerated; no unbounded modulus.
        for s in range(g+1):
            guard=G[t]==s
            slv.add(z3.Implies(guard,z3.And([Q[t][j]==Q[t][(s-1-j)%r] for j in range(r)])))
            if s%2==0:
                j=(s//2)%r
                slv.add(z3.Implies(guard,A[t][j]==B[t][j]))
            else:
                j=((s-1)//2)%r
                slv.add(z3.Implies(guard,z3.And(Q[t][j]&bv(1)==0,A[t][j]==B[t][(j+1)%r])))
        slv.add(a[t][0]==0,a[t][-1]==A[t][0],b[t][-1]==B[t][0])
        slv.add(h[t]==(b[t][0]==1))
        el=[];eh=[]
        for i in range(k):
            x=E[t][i]+a[t][i];y=E[t][i]+b[t][i+1]
            slv.add(a[t][i+1]==car(x),b[t][i]==car(y))
            el.append(x-10*a[t][i+1]);eh.append(y-10*b[t][i])
        for i in range(k):
            slv.add(E[nt][i]==z3.If(h[t],el[i]+(1 if i==0 else eh[i-1]),el[i]+eh[i]))
        slv.add(z3.Implies(h[t],eh[-1]==hi[-1]))
        allq=E[t]+Q[t]
        # Complete exact next-palindrome criterion, with a nonempty bulk.
        safeN=z3.Or([z3.UGE(x,10) for x in allq])
        safeO=z3.Or(E[t][0]!=11,z3.Or([z3.And(x!=0,x!=11) for x in allq]))
        slv.add(z3.If(h[t],safeO,safeN))
    if forced_clock is not None:
        assert len(forced_clock)==p
        for x,y in zip(h,forced_clock):slv.add(x==bool(y))
    if forced_bulk is not None:
        assert len(forced_bulk)==p
        for row,values in zip(Q,forced_bulk):
            assert len(values)==r
            for x,y in zip(row,values):slv.add(x==y)
    if forced_outer is not None:
        assert len(forced_outer)==p
        for row,y in zip(E,forced_outer):slv.add(row[0]==y)
    result=slv.check()
    out=dict(period=p,exterior_width=k,spatial_period=r,growth=g,
             nonuniform=nonuniform,result=str(result),seconds=time.monotonic()-start)
    if result==z3.sat:
        model=slv.model()
        qq=[[model.eval(x).as_long() for x in row] for row in Q]
        ee=[[model.eval(x).as_long() for x in row] for row in E]
        hh=[int(z3.is_true(model.eval(x))) for x in h]
        gg=[model.eval(x).as_long() for x in G]
        checks=[]
        for m in [1,2,3,7,20]:
            length=2*r*m
            q0=ee[0]+[qq[0][j%r] for j in range(length)]+ee[0][::-1]
            n=realize(q0)
            for step in range(3*p):
                t=step%p
                expected=ee[t]+[qq[t][j%r] for j in range(length)]+ee[t][::-1]
                assert numeric_q(n)==expected
                n+=int(str(n)[::-1])
                assert str(n)!=str(n)[::-1]
                length+=hh[t]
            checks.append(m)
        out.update(bulk=qq,exterior=ee,clock=hh,accumulated_growth=gg,numeric_tests=checks)
    elif result==z3.unknown:out['reason']=slv.reason_unknown()
    return out


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--period',type=int,default=20)
    ap.add_argument('--spatial-period',type=int,default=4)
    ap.add_argument('--growth',type=int,default=8)
    ap.add_argument('--widths',default='1,2,3,4,6,8,12,16')
    ap.add_argument('--seconds',type=float,default=5)
    ap.add_argument('--allow-uniform',action='store_true')
    ap.add_argument('--output',default='exist_geom_periodic_qpump_results.json')
    args=ap.parse_args();res=[]
    for k in map(int,args.widths.split(',')):
        row=solve(args.period,k,args.spatial_period,args.growth,args.seconds,not args.allow_uniform)
        res.append(row);Path(args.output).write_text(json.dumps(res,indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if row['result']=='sat':break
