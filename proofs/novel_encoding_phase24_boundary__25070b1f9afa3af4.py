"""Bounded-width positive search: forced8-step exterior, period3 bulk, 24steps.

A SAT witness is only a proposed exterior interface and must be independently
validated together with a central interface. UNSAT applies only to the chosen
maximum width at every phase. Unknown/timeout is not an impossibility result.
"""
import z3 as z,json,time,argparse
from continuation_brown_boolean import trans,v
from family_search_bulk_periods import bulk_step
CLOCK=[(17,13,14),(8,12,9),(17,5,0),(8,13,5),(17,6,11),(8,14,8),(17,8,17),(8,16,16)]

def build(B,K):
    solver=z.SolverFor('QF_BV');edge=[v(a) for a in CLOCK[0]]+[z.BitVec(f'e{i}',5) for i in range(3,K)]
    for x in edge:solver.add(z.ULE(x,v(18)))
    p=edge[:];b=tuple(B)
    for t in range(24):
        h=1-t%2
        for i,a in enumerate(CLOCK[t%8]):solver.add(p[i]==v(a));p[i]=v(a)
        q=p+[v(x) for x in b*3];L=len(q)
        c=z.BoolVal(False);low=[]
        for a in q:
            d,c=trans(a,c);low.append(z.ZeroExt(1,d))
        hc=int(next(x for x in b if x!=9)>=10)
        c=z.BoolVal(bool(hc));high=[None]*L
        for i in range(L-1,-1,-1):
            d,c=trans(q[i],c);high[i]=z.ZeroExt(1,d)
        solver.add(c==z.BoolVal(bool(h)))
        out=([low[0]+v(1)]+[low[i]+high[i-1]for i in range(1,L)]) if h else [a+b for a,b in zip(low,high)]
        nb=next(iter(bulk_step(b,h)))
        for i in range(K,L-3):solver.add(out[i]==v(nb[(i-K)%3]))
        p=[]
        for i,a in enumerate(out[:K]):
            x=z.BitVec(f'q{t+1}_{i}',5);solver.add(x==a,z.ULE(x,v(18)));p.append(x)
        b=nb
    assert b==tuple(B)
    solver.add(*[a==b for a,b in zip(p,edge)])
    return solver,edge


def validate_boundary_rule(samples=2000):
    import random
    rng=random.Random(1729)
    for _ in range(samples):
        K=rng.randrange(3,18)
        P=[rng.randrange(1,19)]+[rng.randrange(19)for _ in range(K-1)]
        B=tuple(rng.randrange(19)for _ in range(3))
        if B==(9,9,9):continue
        q=P+list(B)*3;c=0;lo=[]
        for x in q:lo.append((x+c)%10);c=(x+c)//10
        c=int(next(x for x in B if x!=9)>=10);hi=[0]*len(q)
        for i in range(len(q)-1,-1,-1):
            hi[i]=(q[i]+c)%10;c=(q[i]+c)//10
        out=([lo[0]+1]+[lo[i]+hi[i-1]for i in range(1,len(q))]) if c else [a+b for a,b in zip(lo,hi)]
        full=P+list(B)*10+[2*rng.randrange(10)]+list(B[::-1])*10+P[::-1]
        L=len(full);d=[0]*L
        for i in range(L//2):d[L-1-i]=min(full[i],9);d[i]=full[i]-d[L-1-i]
        d[L//2]=full[L//2]//2
        numeral=''.join(map(str,d[::-1]));n=int(numeral)+int(numeral[::-1])
        numeral=str(n);actual=[int(a)+int(b)for a,b in zip(numeral,numeral[::-1])]
        assert out[:K+6]==actual[:K+6]
    return {'validation':'passed','random_seed':1729,'samples':samples}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=8);ap.add_argument('--timeout',type=int,default=2000);ap.add_argument('--validate',action='store_true')
    args=ap.parse_args()
    if args.validate:
        print(json.dumps(validate_boundary_rule()));raise SystemExit
    src=json.load(open('carry_invariant_research_centers_results.json'))
    blocks=sorted({tuple(r['block'])for r in src if r['schedule'][0]==1 and sum(r['block'])%9==0})
    rows=[]
    for B in blocks:
        ts=time.monotonic();s,e=build(B,args.width);s.set(timeout=args.timeout);answer=s.check()
        row={'block':B,'max_width':args.width,'period':24,'result':str(answer),'seconds':time.monotonic()-ts}
        if answer==z.sat:row['prefix']=[s.model().eval(x).as_long()for x in e]
        rows.append(row);print(json.dumps(row),flush=True)
    open(f'novel_encoding_phase24_width{args.width}.json','w').write(json.dumps(rows,indent=2))
