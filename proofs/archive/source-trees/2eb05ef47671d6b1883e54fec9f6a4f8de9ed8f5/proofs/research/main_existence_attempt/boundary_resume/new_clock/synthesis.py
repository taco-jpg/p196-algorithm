"""Period-14/gain-6 family synthesis with finite exterior and center.

The searched family is P B^m W reverse(B)^m reverse(P), m>=1.
All phase equations are finite carry equations; no finite iteration test
is promoted to a return certificate. Solver UNSAT is a bounded-template
result only. A SAT output requires exact whole-word verification before any
positive claim.
"""
from pathlib import Path
import sys, json, time, argparse
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,'/workspace/scratch/fe6abe1df721/boundary_runtime')
import z3 as z
from astra_substitution_gluing import cyclic
from main_existence_attempt.constructive.bulk_mixture import bulk_step

HERE=Path(__file__).resolve().parent
bv=lambda v:z.BitVecVal(v,5)


def bulk_trace(B,clock):
    q=tuple(B);out=[]
    for h in clock:
        out.append(cyclic(q))
        nxt=bulk_step(q,h)
        assert len(nxt)==1
        q=next(iter(nxt))
    assert q==tuple(B)
    return out


def digits(s,row,carry,name):
    c=bv(carry);ds=[]
    for i,x in enumerate(row):
        v=x+c
        nc=z.BitVec(f'{name}_{i}',5)
        s.add(nc==z.If(z.UGE(v,bv(10)),bv(1),bv(0)))
        ds.append(v-10*nc);c=nc
    return ds,c


def rows_for(s,kind,B,clock,outer,width,label):
    bt=bulk_trace(B,clock);p=len(clock)
    growth=[0]
    for h in clock:growth.append(growth[-1]+h)
    assert growth[-1]%6==0 and len(B)==3
    rows=[]
    for t in range(p):
        n=width+(growth[t]%2 if kind=='center' else 0)
        row=[z.BitVec(f'{label}q{t}_{i}',5)for i in range(n)]
        for x in row:s.add(z.ULE(x,bv(18)))
        if kind=='center':
            for i in range(n//2):s.add(row[i]==row[-1-i])
            if n%2:s.add(row[n//2]&bv(1)==bv(0))
        else:s.add(row[0]==bv(outer[t]))
        rows.append(row)
    for t,row in enumerate(rows):
        nt=(t+1)%p;h=clock[t];b=bt[t];bn=bt[nt];n=len(row)
        nrow=rows[nt]
        if kind=='exterior':
            lo,lc=digits(s,row,0,f'{label}lo{t}')
            hh,rc=digits(s,row[::-1],b['R'][0],f'{label}hi{t}')
            hi=hh[::-1]
            s.add(lc==bv(b['A'][0]),rc==bv(h))
            for i in range(n):s.add(nrow[i]==lo[i]+(bv(1)if h and i==0 else hi[i-h]))
            if h:s.add(bv(bn['q'][0])==bv(b['lo'][0])+hi[-1])
        else:
            g=growth[t];ng=growth[t+1];d=g//2;shift=ng//2-d
            lo,lc=digits(s,row,b['A'][d%3],f'{label}lo{t}')
            hi=lo[::-1]
            s.add(lc==bv(b['R'][d%3]))
            def digit(i,which):
                if 0<=i<n:return (lo if which=='lo'else hi)[i]
                if i<0:return bv(b[which][(d+i)%3])
                other='hi'if which=='lo'else'lo'
                return bv(b[other][(d-1-(i-n))%3])
            def target(i):
                if 0<=i<len(nrow):return nrow[i]
                if i<0:return bv(bn['q'][(d+shift+i)%3])
                return bv(bn['q'][(d+shift-1-(i-len(nrow)))%3])
            for i in range(-1,len(nrow)+1):
                s.add(digit(shift+i,'lo')+digit(shift+i-h,'hi')==target(i))
    return rows,bt


def solve(B,clock,outer,k,w,seconds=3,kind='joint'):
    began=time.monotonic()
    s=z.Then('simplify','propagate-values','solve-eqs','simplify','bit-blast','sat').solver()
    s.set(timeout=int(seconds*1000))
    ex=ce=None
    if kind in ('joint','exterior'):
        ex,bt=rows_for(s,'exterior',B,clock,outer,k,'e')
    if kind in ('joint','center'):
        ce,bt=rows_for(s,'center',B,clock,outer,w,'c')
    if kind=='joint':
        # Exact q palindrome-predecessor criterion, every phase.
        for t in range(len(clock)):
            q=ex[t]+[bv(x)for x in bt[t]['q']]+ce[t]
            s.add(z.Or([z.UGT(x,bv(9))for x in q]))
            s.add(z.Or(ex[t][0]!=bv(11),z.Or([z.And(x!=bv(0),x!=bv(11))for x in q])))
    built=time.monotonic();r=s.check()
    out=dict(kind=kind,bulk=B,clock=clock,outer=outer,exterior_width=k,
             center_width=w,status=str(r),build_seconds=built-began,
             solve_seconds=time.monotonic()-built,
             exact_finite_return_supplied=False,decimal_existence_proved=False)
    if r==z.sat:
        m=s.model()
        vals=lambda rows:[[m.eval(x,model_completion=True).as_long()for x in row]for row in rows]
        if ex is not None:out['exterior_rows']=vals(ex)
        if ce is not None:out['center_rows']=vals(ce)
    elif r==z.unknown:out['reason']=s.reason_unknown()
    return out


if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--clock-index',type=int,default=1)
    a.add_argument('--kind',choices=['joint','center','exterior'],default='joint')
    a.add_argument('--width',type=int,default=12)
    a.add_argument('--center-width',type=int,default=6)
    a.add_argument('--seconds',type=float,default=3)
    a.add_argument('--out',default='joint14.json')
    args=a.parse_args()
    row=json.loads((HERE/'clock14_bulk.json').read_text())[args.clock_index]
    results=[]
    for B in row['returning_period3']:
        if B in ([0,0,0],[18,18,18]):continue
        r=solve(B,row['overflow'],row['clock'],args.width,args.center_width,args.seconds,args.kind)
        results.append(r)
        (HERE/args.out).write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(r),flush=True)
        if r['status']=='sat' and args.kind=='joint':break
