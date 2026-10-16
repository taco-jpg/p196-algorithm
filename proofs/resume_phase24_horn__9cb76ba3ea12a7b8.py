"""Exact symbolic unbounded-width reachability; unknown is not a proof."""
import z3 as z, json,time,argparse
from resume_phase24_targets import target_states

def packed(st):
    ls,lc,rc=st;v=0
    for j in range(len(ls)):v|=(ls[j]|lc[j]<<4|rc[j]<<6)<<(8*j)
    return v

def relation(s,n,dr0,ins,k):
    c=[];dr=z.ZeroExt(1,dr0)
    for j in range(k):
        dl=z.ZeroExt(1,z.Extract(8*j+3,8*j,s));lc=z.Extract(8*j+5,8*j+4,s);rc=z.Extract(8*j+7,8*j+6,s)
        c.extend([z.ULE(dl,9),z.ULE(dr,9)])
        for t in range(2):
            li=z.ZeroExt(4,z.Extract(2*j+t,2*j+t,ins));ri=z.ZeroExt(4,z.Extract(t,t,rc))
            a=dl+dr+li;b=dl+dr+ri
            lo=z.UGE(a,10);ro=z.UGE(b,10)
            c.append(lo==(z.Extract(t,t,lc)==1))
            c.append(z.Extract(8*j+4+t,8*j+4+t,n)==z.Extract(2*j+t,2*j+t,ins))
            c.append((z.Extract(8*j+6+t,8*j+6+t,n)==1)==ro)
            dl=z.If(lo,a-10,a);dr=z.If(ro,b-10,b)
        c.append(z.Extract(8*((j+1)%k)+3,8*((j+1)%k),n)==z.Extract(3,0,dl))
    c.append(dr==z.ZeroExt(1,dr0))
    return z.And(c)

def run(k,blocks,seconds):
    fp=z.Fixedpoint();fp.set(engine='spacer',timeout=int(seconds*1000))
    S=z.BitVecSort(8*k);R=z.Function('Reach',S,z.BoolSort());Bad=z.Function('Bad',z.BoolSort())
    fp.register_relation(R,Bad)
    a,b=z.BitVecs('a b',8*k);dr=z.BitVec('dr',4);ins=z.BitVec('ins',2*k)
    fp.declare_var(a,b,dr,ins)
    start=z.BitVecVal(packed(((1,)*k,(2,)*k,(0,)*k)),8*k)
    fp.rule(R(b),[relation(start,b,z.BitVecVal(7,4),ins,k)])
    fp.rule(R(b),[R(a),relation(a,b,dr,ins,k)])
    targets=set()
    for B in blocks:
        for st in target_states(B):
            assert k==12
            for shift in range(k):
                ss=tuple(v[shift:]+v[:shift]for v in st);targets.add(packed(ss))
    fp.rule(Bad(),[R(a),z.Or(*[a==v for v in targets])])
    ts=time.monotonic()
    try:result=str(fp.query(Bad()))
    except z.Z3Exception as e:result='unknown: '+str(e)
    out={'period':2*k,'targets':len(targets),'result':result,'seconds':time.monotonic()-ts,'method':'symbolic unbounded-width Horn reachability'}
    if result!='unknown':
        try:open('resume_phase24_horn_answer.txt','w').write(str(fp.get_answer()))
        except Exception:pass
    print(json.dumps(out),flush=True);open('resume_phase24_horn_result.json','w').write(json.dumps(out,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=int,default=60);a=p.parse_args()
    run(12,[(0,0,18),(0,9,18),(0,18,9),(0,18,18),(2,2,14),(4,4,10)],a.seconds)
