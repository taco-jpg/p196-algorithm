"""Pair-sum version of the exact free-clock uniform-run pump search.

All bounds are uint5 (values never exceed 19 in column addition). A SAT
model would give an invariant family of pair-sum words, hence a genuine
finite Lychrel witness after applying the first reverse-add operation.
"""
import argparse, json, time
from pathlib import Path
import z3
from exist_geom_uniform_freeclock import decimal_cycle


def solve(p,k,g,seconds=30,d0=8,forced_clock=None,mod11=False):
    start=time.monotonic()
    ds=decimal_cycle(d0)
    assert p%len(ds)==0
    ds=[ds[t%len(ds)] for t in range(p)]
    slv=z3.SolverFor('QF_BV');slv.set(timeout=int(1000*seconds))
    q=[[z3.BitVec(f'q_{t}_{i}',5) for i in range(k)] for t in range(p)]
    a=[[z3.BitVec(f'a_{t}_{i}',5) for i in range(k+1)] for t in range(p)]
    b=[[z3.BitVec(f'b_{t}_{i}',5) for i in range(k+1)] for t in range(p)]
    h=[z3.Bool(f'h_{t}') for t in range(p)]
    for t in range(p):
        for x in q[t]:slv.add(z3.ULE(x,18))
        slv.add(q[t][0]!=0)
        for x in a[t]+b[t]:slv.add(z3.ULE(x,1))
        eps=int(ds[t]>=5)
        slv.add(a[t][0]==0,a[t][-1]==eps,b[t][-1]==eps)
        slv.add(h[t]==(b[t][0]==1))
        low=[];high=[]
        for i in range(k):
            x=q[t][i]+a[t][i]
            y=q[t][i]+b[t][i+1]
            slv.add(a[t][i+1]==z3.If(z3.UGE(x,10),z3.BitVecVal(1,5),z3.BitVecVal(0,5)))
            slv.add(b[t][i]==z3.If(z3.UGE(y,10),z3.BitVecVal(1,5),z3.BitVecVal(0,5)))
            low.append(x-10*a[t][i+1]);high.append(y-10*b[t][i])
        nt=(t+1)%p
        for i in range(k):
            oq=low[i]+(1 if i==0 else high[i-1])
            nq=low[i]+high[i]
            slv.add(q[nt][i]==z3.If(h[t],oq,nq))
        slv.add(z3.Implies(h[t],high[-1]==ds[nt]))
        # The exact next-palindrome criterion: N needs at least one carry.
        # O is automatically nonpalindromic because the nonempty uniform
        # bulk coefficient 2*d is neither 0 nor 11.
        if ds[t]<5:
            slv.add(z3.Implies(z3.Not(h[t]),z3.Or([z3.UGE(x,10) for x in q[t]])))
        if mod11:
            # Every positive-growth pump is eventually forced divisible by
            # 11; a return of two periods preserves its residue modulo 11.
            # Evaluate the odd-width symmetric q word at decimal base -1.
            bits=(36*k+18).bit_length()
            total=z3.BitVecVal(18*k+((-1)**k)*ds[t],bits)
            for i,x in enumerate(q[t]):
                xx=z3.ZeroExt(bits-5,x)
                total=total+xx if i%2==0 else total-xx
            slv.add(z3.URem(total,11)==(18*k)%11)
    w=(p+1).bit_length()
    slv.add(sum([z3.If(x,z3.BitVecVal(1,w),z3.BitVecVal(0,w)) for x in h],z3.BitVecVal(0,w))==g)
    if forced_clock is not None:
        assert len(forced_clock)==p
        for x,y in zip(h,forced_clock):slv.add(x==bool(y))
    r=slv.check()
    out=dict(period=p,exterior_width=k,growth=g,bulk_digit=d0,result=str(r),seconds=time.monotonic()-start)
    if r==z3.sat:
        model=slv.model()
        qs=[[model.eval(x).as_long() for x in row] for row in q]
        hs=[int(z3.is_true(model.eval(x))) for x in h]
        aa=''.join(str(min(x,9)) for x in qs[0])
        bb=''.join(str(x-min(x,9)) for x in qs[0][::-1])
        checked=[]
        for m in [1,2,3,7,20,101]:
            n=int(aa+str(d0)*m+bb)
            length=m
            for step in range(3*p):
                t=step%p
                digs=[int(x) for x in str(n)[::-1]]
                coeff=[x+y for x,y in zip(digs,reversed(digs))]
                assert coeff==qs[t]+[2*ds[t]]*length+qs[t][::-1]
                n+=int(str(n)[::-1])
                assert str(n)!=str(n)[::-1]
                length+=hs[t]
            checked.append(m)
        out.update(q=qs,clock=hs,initial_A=aa,initial_B=bb,tested_bulk_lengths=checked)
    elif r==z3.unknown:out['reason']=slv.reason_unknown()
    return out


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--period',type=int,default=24)
    ap.add_argument('--widths',default='1,2,3,4,6,8,12,16,24,32')
    ap.add_argument('--growth',type=int,default=9)
    ap.add_argument('--digit',type=int,default=8)
    ap.add_argument('--seconds',type=float,default=10)
    ap.add_argument('--mod11',action='store_true')
    ap.add_argument('--output',default='exist_geom_uniform_qclock_results.json')
    args=ap.parse_args();res=[]
    for k in map(int,args.widths.split(',')):
        row=solve(args.period,k,args.growth,args.seconds,args.digit,mod11=args.mod11)
        res.append(row);Path(args.output).write_text(json.dumps(res,indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if row['result']=='sat':break
