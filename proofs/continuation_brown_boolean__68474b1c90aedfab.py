"""Compact positive-family search using verified decimal addition Boolean gates."""
import json,time,sys
from pathlib import Path
import z3 as z
CLOCK=[[17,13,14],[8,12,9],[17,5,0],[8,13,5],[17,6,11],[8,14,8],[17,8,17],[8,16,16]]
v=lambda n:z.BitVecVal(n,5)
v4=lambda n:z.BitVecVal(n,4)
v1=lambda n:z.BitVecVal(n,1)
def trans(q,c):
    if z.is_bv_value(q):
        n=q.as_long()
        if n<9:return z.If(c,v4(n+1),v4(n)),z.BoolVal(False)
        if n==9:return z.If(c,v4(0),v4(9)),c
        return z.If(c,v4(n-9),v4(n-10)),z.BoolVal(True)
    q0,q1,q2,q3,q4=[z.Extract(i,i,q)==v1(1)for i in range(5)]
    h=z.Or(q4,z.And(q3,z.Or(q2,q1,z.And(q0,c))))
    a1=z.And(q0,c);b1=z.Xor(q1,a1)
    a2=z.And(q1,a1);b2=z.Xor(q2,a2)
    a3=z.And(q2,a2);b3=z.Xor(q3,a3)
    e2=z.And(h,z.Not(b1));e3=z.And(e2,z.Not(b2))
    bits=[z.Xor(q0,c),z.Xor(b1,h),z.Xor(b2,e2),z.Xor(z.Xor(b3,h),e3)]
    digit=z.Concat(*[z.If(b,v1(1),v1(0))for b in bits[::-1]])
    return digit,h

def build(k,maximum_width=True):
    solver=z.SolverFor('QF_BV')
    edge=[v(a)for a in CLOCK[0]]+[z.BitVec(f'u_{i}',5)for i in range(3,k)]
    for a in edge:solver.add(z.ULE(a,v(18)))
    q=edge[:];B=14
    for t in range(72):
        J=len(q);H=B>=10;D=B%10
        for i,a in enumerate(CLOCK[t%8]):solver.add(q[i]==v(a));q[i]=v(a)
        if B<10:solver.add(z.Or(*[z.UGE(a,v(10))for a in q]))
        c=z.BoolVal(False);lo=[]
        for a in q:d,c=trans(a,c);lo.append(z.ZeroExt(1,d))
        lowbulk=z.If(c,v(D+1),v(D))
        c=z.BoolVal(H);hi=[None]*J
        for i in range(J-1,-1,-1):d,c=trans(q[i],c);hi[i]=z.ZeroExt(1,d)
        over=(t+1)%2;solver.add(c==z.BoolVal(bool(over)))
        if over:out=[lo[0]+v(1)]+[lo[i]+hi[i-1]for i in range(1,J)]+[lowbulk+hi[-1]]
        else:out=[a+b for a,b in zip(lo,hi)]+[lowbulk+v(D+int(H))]
        B=2*(D+int(H))
        if maximum_width:solver.add(out[-1]==v(B));out=out[:-1]
        q=[]
        for i,a in enumerate(out):
            b=z.BitVec(f'q_{t+1}_{i}',5);solver.add(b==a,z.ULE(b,v(18)));q.append(b)
    target=edge if maximum_width else edge+[v(14)]*72
    solver.add(*[a==b for a,b in zip(q,target)])
    return solver,edge

def verify_gates():
    # Force the nonconstant branch, then check every valid pair-sum/carry input.
    q=z.BitVec('gate_q',5);c=z.Bool('gate_c');d,h=trans(q,c)
    for n in range(19):
        for b in range(2):
            dd=z.simplify(z.substitute(d,(q,v(n)),(c,z.BoolVal(bool(b))))).as_long()
            hh=z.is_true(z.simplify(z.substitute(h,(q,v(n)),(c,z.BoolVal(bool(b))))))
            assert (dd,int(hh))==((n+b)%10,(n+b)//10),(n,b,dd,hh)
    print('Boolean decimal gate verified on all 38 valid inputs',flush=True)

if __name__=='__main__':
    verify_gates()
    k=int(sys.argv[1])if len(sys.argv)>1 else 24
    maximum='--triangular'not in sys.argv
    st=time.monotonic();s,edge=build(k,maximum)
    print(json.dumps({'stage':'built','k':k,'maximum_boundary_width':maximum,'seconds':round(time.monotonic()-st,3)}),flush=True)
    s.set(timeout=60000);st=time.monotonic();r=s.check()
    out={'k':k,'maximum_boundary_width':maximum,'period':72,'growth':36,'result':str(r),'seconds':round(time.monotonic()-st,3)}
    if r==z.sat:out['u']=[s.model().eval(a).as_long()for a in edge]
    elif r==z.unknown:out['reason']=s.reason_unknown()
    print(json.dumps(out),flush=True);Path('continuation_brown_boolean_result.json').write_text(json.dumps(out,indent=2))
