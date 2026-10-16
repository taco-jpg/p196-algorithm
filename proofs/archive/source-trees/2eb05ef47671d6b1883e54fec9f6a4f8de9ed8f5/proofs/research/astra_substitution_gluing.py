"""Local exterior/interface/center synthesis for a two-bulk 24-step pump.

This is discovery. A glued positive construction must additionally pass the
separate exact whole-word periodic-family checker and independent arithmetic.
"""
import argparse,json,time
from pathlib import Path
import z3 as z
from astra_substitution_twobulk import pool
from resume_renewal_bulk import transform
from astra_substitution_periodic import candidate

bv=lambda x:z.BitVecVal(x,5)

def cyclic(q):
    p=len(q);j=next(i for i,v in enumerate(q) if v!=9)
    L=[0]*p;R=[0]*p;L[j]=R[j]=int(q[j]>=10)
    for k in range(1,p):
        i=(j+k)%p;L[i]=(q[i]+L[(i-1)%p])//10
        i=(j-k)%p;R[i]=(q[i]+R[(i+1)%p])//10
    A=[L[(i-1)%p] for i in range(p)]
    lo=[q[i]+A[i]-10*L[i] for i in range(p)]
    hi=[q[i]+R[(i+1)%p]-10*R[i] for i in range(p)]
    return dict(q=q,A=A,R=R,lo=lo,hi=hi)

def trace(q,period=24):
    out=[]
    for t in range(period):out.append(cyclic(q));q=transform(q,t%2)
    assert q==out[0]['q']
    return out

def fold(solver,vs,low,high,name):
    c=bv(low);lo=[]
    for i,x in enumerate(vs):
        nc=z.BitVec(f'{name}a{i}',5);solver.add(nc==z.If(z.UGE(x+c,bv(10)),bv(1),bv(0)))
        lo.append(x+c-bv(10)*nc);c=nc
    lc=c;c=bv(high);hi=[None]*len(vs)
    for i in reversed(range(len(vs))):
        x=vs[i];nc=z.BitVec(f'{name}b{i}',5);solver.add(nc==z.If(z.UGE(x+c,bv(10)),bv(1),bv(0)))
        hi[i]=x+c-bv(10)*nc;c=nc
    return lo,hi,lc,c

def query(kind,B,width,C=None,seconds=.2):
    start=time.monotonic();s=z.Then('simplify','propagate-values','solve-eqs','simplify','bit-blast','sat').solver();s.set(timeout=int(seconds*1000))
    bt=trace(B);ct=trace(C) if C is not None else None
    rows=[]
    for t in range(24):
        size=width+((t//2)%2 if kind=='center' else 0)
        row=[z.BitVec(f'q{t}_{i}',5) for i in range(size)]
        for x in row:s.add(z.ULE(x,bv(18)))
        if kind=='center':
            for i in range(size):s.add(row[i]==row[-1-i])
            if size%2:s.add(row[size//2]&bv(1)==bv(0))
        rows.append(row)
    for t,row in enumerate(rows):
        h=t%2;nt=(t+1)%24;nrow=rows[nt];b=bt[t];bn=bt[nt];n=len(row)
        if kind=='exterior':
            s.add(row[0]==bv(8 if h==0 else 17))
            lo,hi,lc,rc=fold(s,row,0,b['R'][0],f't{t}')
            s.add(lc==bv(b['A'][0]),rc==bv(h))
            for i in range(n):s.add(nrow[i]==lo[i]+(bv(1) if h and i==0 else hi[i-h]))
            if h:s.add(bv(bn['q'][0])==bv(b['lo'][0])+hi[-1])
        else:
            if kind=='interface':
                c=ct[t];cn=ct[nt];d=t//8;shift=(t+1)//8-d
                low=b['A'][d%3];high=c['R'][d%3]
                lowgoal=c['A'][d%3];highgoal=b['R'][d%3]
                def outside(i,which):
                    return bv(b[which][(d+i)%3]) if i<0 else bv(c[which][(d+i-n)%3])
                def target(i):return bv(bn['q'][(d+shift+i)%3]) if i<0 else bv(cn['q'][(d+shift+i-len(nrow))%3])
            else:
                g=t//2;ng=(t+1)//2;d=g//2;shift=ng//2-d
                low=high=b['A'][d%3];lowgoal=highgoal=b['R'][d%3]
                def outside(i,which):
                    if i<0:return bv(b[which][(d+i)%3])
                    other='hi' if which=='lo' else 'lo'
                    return bv(b[other][(d-1-(i-n))%3])
                def target(i):
                    return bv(bn['q'][(d+shift+i)%3]) if i<0 else bv(bn['q'][(d+shift-1-(i-len(nrow)))%3])
            lo,hi,lc,rc=fold(s,row,low,high,f't{t}')
            s.add(lc==bv(lowgoal),rc==bv(highgoal))
            def digit(i,which):return (lo if which=='lo' else hi)[i] if 0<=i<n else outside(i,which)
            for i in range(-1,len(nrow)+1):
                actual=digit(shift+i,'lo')+digit(shift+i-h,'hi')
                wanted=nrow[i] if 0<=i<len(nrow) else target(i)
                s.add(actual==wanted)
    result=s.check();out={'kind':kind,'B':B,'C':C,'width':width,'result':str(result),'seconds':time.monotonic()-start}
    if result==z.sat:
        model=s.model();out['rows']=[[model.eval(x).as_long() for x in row] for row in rows]
    elif result==z.unknown:out['reason']=s.reason_unknown()
    return out

def whole(B,C,ext,interface,center):
    P=tuple(ext['rows'][0]);V=tuple(interface['rows'][0]);W=tuple(center['rows'][0]);m=12;n=13
    start=[(P,len(P),False),(B,3*m,True),(V,len(V),False),(C,3*n,True),(W,len(W),False),(C[::-1],3*n,True),(V[::-1],len(V),False),(B[::-1],3*m,True),(P[::-1],len(P),False)]
    end=[(w,l+(3 if r else 0),r) for w,l,r in start]
    cert,why=candidate(start,end,24)
    return dict(exact_check=why,certificate=cert)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=.2);p.add_argument('--width',type=int,default=6);p.add_argument('--limit',type=int,default=198);p.add_argument('--include-uniform',action='store_true');p.add_argument('--out',default='astra_substitution_gluing_results.json');a=p.parse_args()
    motifs=pool(24)[:a.limit]
    if a.include_uniform:motifs += [(v,v,v) for v in range(0,19,2)]
    records=[];exteriors=[];centers=[]
    for kind,good in [('exterior',exteriors),('center',centers)]:
        for B in motifs:
            row=query(kind,B,a.width,seconds=a.seconds);records.append(row)
            if row['result']=='sat':good.append((B,row))
            if len(records)%20==0:
                Path(a.out).write_text(json.dumps(records,indent=2)+'\n')
                print(json.dumps({'queries':len(records),'kind':kind,'exteriors':len(exteriors),'centers':len(centers)}),flush=True)
    for B,ex in exteriors:
        for C,ce in centers:
            if B==C:continue
            row=query('interface',B,a.width,C,a.seconds);records.append(row)
            if row['result']=='sat':
                row['glued']=whole(B,C,ex,row,ce)
                print(json.dumps(row),flush=True)
                if row['glued']['certificate']:
                    Path(a.out).write_text(json.dumps(records,indent=2)+'\n');raise SystemExit
    Path(a.out).write_text(json.dumps(records,indent=2)+'\n')
    from collections import Counter
    print(json.dumps({'queries':len(records),'counts':dict(Counter(r['kind']+':'+r['result'] for r in records)),'exteriors':len(exteriors),'centers':len(centers)}),flush=True)
