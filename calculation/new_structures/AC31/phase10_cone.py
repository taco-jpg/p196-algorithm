#!/usr/bin/env python3
"""Sound endpoint-only phase-10 two-ended carry enclosure. No strict W9 pruning."""
import argparse, json, sys
from pathlib import Path
if hasattr(sys,"set_int_max_str_digits"): sys.set_int_max_str_digits(0)
DATA=Path(__file__).resolve().parents[2]/"decimal_frontier/lattice_kinks/data/lat_p12m9.txt"

def load(path):
    r=[[int(x) for x in line.split()] for line in Path(path).read_text().splitlines() if line.strip()]
    assert r[0]==[12,34,9,10] and len(r)==38
    assert len(r[1])==12
    assert all(len(x)==9 for x in r[2:14])
    assert all(len(x)==34 for x in r[26:38])
    return r[1],r[26:38],r[2:14]

def normalize(p,c):
    out=[]
    for a in p:
        assert 0<=a<=18 and c in (0,1)
        v=a+c;out.append(v%10);c=v//10
    return out,c

def successors(a):
    """Enumerate both possible high carry inlets; retain genuine gamma shift."""
    L=len(a)
    lo,_=normalize(a,0)
    ret=set()
    for inlet in (0,1):
        hi,g=normalize(a[::-1],inlet)
        if g:
            s=(lo[0]+1,)+tuple(lo[i]+hi[L-i] for i in range(1,L-1))
        else:
            if hi[-1]==0: continue
            s=tuple(lo[i]+hi[L-1-i] for i in range(L-1))
        ret.add((s,g))
    return ret

def enclosure(B,W,clock):
    prefix=B+W*14
    states={tuple(prefix)}
    by_time={0:states}
    rows=[]
    for t in range(1,121):
        next_pairs={z for a in states for z in successors(a)}
        gammas={g for _,g in next_pairs}
        assert gammas=={clock[(10+t-1)%12]},(t,gammas)
        states={p for p,_ in next_pairs}
        assert states
        by_time[t]=states
        rows.append((t,160-t,len(states),''.join(map(str,sorted(gammas))),
                     '/'.join(map(str,sorted({p[8] for p in states})))))
    assert len(states)==1 and next(iter(states))==tuple(prefix[:40])
    return by_time,rows

def realize(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(p[i],9);lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo;d[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0
    return int(''.join(map(str,d[::-1])))

def pair(n):
    d=list(map(int,str(n)[::-1]))
    return tuple(d[i]+d[-i-1] for i in range(len(d)))

def digit_step(P):
    d,g=normalize(P,0)
    if g:d.append(g)
    return tuple(d[i]+d[-i-1] for i in range(len(d))),g

def audit(B,W,by_time,J,U,C,q,k):
    H=B+W*q+J+U*k
    P=tuple(H+C+H[::-1])
    n=realize(P)
    assert pair(n)==P
    gammas=[]
    for t in range(1,121):
        old=str(n);nn=n+int(old[::-1])
        pp,g=digit_step(P)
        assert pair(nn)==pp and len(str(nn))-len(old)==g
        n=nn;P=pp;gammas.append(g)
        ss=by_time[t];assert P[:len(next(iter(ss)))] in ss
    T=B+W*q+J+U*(k+5)
    target=tuple(T+C+T[::-1])
    first=next((i for i,(x,y) in enumerate(zip(P,target)) if x!=y),None)
    if first is None and len(P)!=len(target):first=min(len(P),len(target))
    return {'q':q,'k':k,'J':J,'U':U,'C':C,'first_mismatch':first,
            'overflow_count':sum(gammas),'length':len(P),'target_length':len(target)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--data',type=Path,default=DATA)
    p.add_argument('--write-tsv',type=Path)
    p.add_argument('--audit',action='store_true')
    a=p.parse_args()
    clock,Bs,Ws=load(a.data);B=Bs[10];W=Ws[10]
    by_time,rows=enclosure(B,W,clock)
    if a.write_tsv:
        a.write_tsv.write_text('step\tremaining\tstates\tgamma\tcoefficient8\n'+
                               ''.join('\t'.join(map(str,r))+'\n' for r in rows))
    print('COMPUTED 120 layers, first 40 restored, max states',max(r[2] for r in rows),
          'forced overflows',sum(int(r[3]) for r in rows))
    if a.audit:
        controls=[([0]*5,[9,0,18],[4,14,4]),
                  ([18]*5,[9,18,0],[4,4]),
                  ([0,1,2,3,4],[9,10,8],[4,14,4]),
                  ([9]*5,[16,9,2],[4,4])]
        for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
            for J,U,C in controls:
                r=audit(B,W,by_time,J,U,C,q,k)
                assert r['overflow_count']==30 and r['first_mismatch']>=40
                print('BIGINT',json.dumps(r))
if __name__=='__main__':main()
