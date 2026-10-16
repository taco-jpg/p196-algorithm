"""Constructive one-uniform-core search via exact one-sided boundary propagation."""
import json,sys,time
import z3 as z
from pathlib import Path

def search(k,outer=17,period=72,background=14,timeout=45000):
    solver=z.SolverFor('QF_BV');solver.set(timeout=timeout)
    def v(n):return z.BitVecVal(n,5)
    clock=[[17,13,14],[8,12,9],[17,5,0],[8,13,5],[17,6,11],[8,14,8],[17,8,17],[8,16,16]]
    edge=[v(a)for a in clock[0]]+[z.BitVec(f'u_{i}',5)for i in range(3,k)]
    for a in edge:solver.add(z.ULE(a,v(18)))
    q=edge[:];B=background;growth=0
    for t in range(period):
        J=len(q);H=int(B>=10);D=B%10
        for i,a in enumerate(clock[t%8]):
            solver.add(q[i]==v(a));q[i]=v(a)
        if B<10:solver.add(z.Or([z.UGE(a,v(10))for a in q]))
        c=v(0);lo=[]
        for a in q:
            n=z.simplify(z.If(z.UGE(a+c,v(10)),v(1),v(0)))
            lo.append(z.simplify(a+c-v(10)*n));c=n
        lowbulk=z.simplify(v(D)+c)
        c=v(H);hi=[None]*J
        for i in range(J-1,-1,-1):
            a=q[i];n=z.simplify(z.If(z.UGE(a+c,v(10)),v(1),v(0)))
            hi[i]=z.simplify(a+c-v(10)*n);c=n
        over=(t+1)%2;solver.add(c==v(over))
        if over:
            out=[z.simplify(lo[0]+v(1))]+[z.simplify(lo[i]+hi[i-1])for i in range(1,J)]+[z.simplify(lowbulk+hi[-1])]
            growth+=1
        else:out=[z.simplify(a+b)for a,b in zip(lo,hi)]+[z.simplify(lowbulk+v(D+H))]
        q=[]
        for i,a in enumerate(out):
            if z.is_bv_value(a):q.append(a)
            else:
                b=z.BitVec(f'q_{t+1}_{i}',5);solver.add(b==a);q.append(b)
        B=2*(D+H)
    assert B==background
    target=edge+[v(B)]*period
    assert len(q)==len(target)
    solver.add(*[a==b for a,b in zip(q,target)])
    t0=time.monotonic();res=solver.check()
    result={'k':k,'outer':outer,'period':period,'core':background,'growth':growth,'result':str(res),'seconds':round(time.monotonic()-t0,3)}
    if res==z.sat:
        model=solver.model();result['u']=[model.eval(a).as_long()for a in edge]
    if res==z.unknown:result['reason']=solver.reason_unknown()
    return result

if __name__=='__main__':
    cases=[(8,17),(16,17),(24,17)]
    if len(sys.argv)>1:cases=[(int(sys.argv[1]),int(sys.argv[2]))]
    results=[]
    for k,outer in cases:
        result=search(k,outer)
        print(json.dumps(result),flush=True);results.append(result)
        Path('outer_invariant_brown72_results.json').write_text(json.dumps(results,indent=2))
        if result['result']=='sat':break
