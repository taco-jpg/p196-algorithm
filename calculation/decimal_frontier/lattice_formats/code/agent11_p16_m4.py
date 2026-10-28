#!/usr/bin/env python3
"""Enumerate decimal p16, m=4 reflection-symmetric periodic absorbing rows and
build an exact root-reachability test against agent11's shared position automaton.
Only rows fixed after ONE 16-step overflow period are in scope.
"""
from pathlib import Path
import itertools
import sys

B, M, P = 10, 4, 16
G = [t & 1 for t in range(P)]

def phi(row, gam):
    i0 = next((i for i, x in enumerate(row) if x != B-1), None)
    if i0 is None:
        return None
    A, D = [None]*M, [None]*M
    A[(i0+1)%M] = int(row[i0]>=B)
    for j in range(1,M):
        i = (i0+j)%M
        A[(i+1)%M] = (row[i]+A[i])//B
    D[(i0-1)%M] = int(row[i0]>=B)
    for j in range(1,M):
        i = (i0-j)%M
        D[(i-1)%M] = (row[i]+D[i])//B
    e = [(row[i]+A[i])%B for i in range(M)]
    f = [(row[i]+D[i])%B for i in range(M)]
    out = tuple(e[i]+(f[(i-1)%M] if gam else f[i]) for i in range(M))
    return out,A,D

def pack(L,H,Y):
    v=0
    for y in reversed(Y):v=v*10+y
    return L+(H<<16)+(v<<32)

def canon(key):
    l=key&65535;h=(key>>16)&65535;y=[];v=key>>32
    for _ in range(8):y.append(v%10);v//=10
    best=key
    for j in range(1,8):
        i=2*j
        ll=((l>>i)|(l<<(16-i)))&65535
        hh=((h>>i)|(h<<(16-i)))&65535
        yy=[y[(q+j)&7] for q in range(8)]
        best=min(best,pack(ll,hh,yy))
    return best

def cuts(rows):
    keys=[]
    for k in range(M):
        L=H=0;Y=[]
        for t,row in enumerate(rows):
            _,A,D=phi(row,G[t])
            L|=A[k]<<t
            H|=((row[k]+D[k])//B)<<t
            if G[t]:Y.append((row[(k-1)%M]+D[(k-1)%M])%B)
        keys.append(canon(pack(L,H,Y)))
    return keys

def enumerate_targets():
    targets=set(); roots=set(); cycles=[]; checks=0
    for alpha in range(M):
        partner=[(alpha-i)%M for i in range(M)]
        reps=[i for i in range(M) if i<=partner[i]]
        for vals in itertools.product(range(2*B-1),repeat=len(reps)):
            row=[0]*M
            for i,v in zip(reps,vals):row[i]=row[partner[i]]=v
            rows=[];cur=tuple(row)
            for gam in G:
                step=phi(cur,gam)
                if step is None:break
                rows.append(cur);cur=step[0]
            else:
                if cur!=tuple(row) or tuple(row) in roots:continue
                roots.add(tuple(row))
                mp=min(d for d in (1,2,4) if all(r[k]==r[(k+d)%M] for r in rows for k in range(M)))
                if mp!=4:continue
                keys=cuts(rows);cycles.append((alpha,row,keys))
                targets.update(keys)
                # Independently verify digit/carry-column recursion and cut edges.
                for k in range(M):
                    seq=[]
                    for t,r in enumerate(rows):
                        _,A,D=phi(r,G[t]);x=r[k];c=D[k]
                        y=(r[(k-1)%M]+D[(k-1)%M])%B
                        x2=(x+A[k])%B+(y if G[t] else (x+c)%B)
                        assert x2==rows[(t+1)%P][k]
                        seq.append((c,(x+A[k])//B,(x+c)%B))
                        checks+=1
                    L2=sum(q[1]<<t for t,q in enumerate(seq))
                    H2=sum(q[0]<<t for t,q in enumerate(seq))
                    Y2=[seq[t][2] for t in range(P) if G[t]]
                    assert canon(pack(L2,H2,Y2))==keys[(k+1)%M]
    return cycles,sorted(targets),checks

def prepare(out):
    cycles,targets,checks=enumerate_targets()
    assert len(cycles)==48 and len(targets)==8 and checks==3072
    out.mkdir(parents=True,exist_ok=True)
    (out/'target_keys.txt').write_text('\n'.join(map(str,targets))+'\n')
    cpp='''static inline bool accepting(int L,int H,const unsigned char*Y){
 static constexpr u64 targets[] = {''' + ', '.join(str(k)+'ULL' for k in targets) + '''};
 u64 key=pack(L,H,Y);
 for(u64 k:targets)if(key==k)return true;
 return false;
}
'''
    here=Path(__file__).resolve().parent
    for ix in (1,2):
        s=(here/f'agent11_p16_stage{ix}.cpp').read_text()
        a=s.index('static inline bool accepting(')
        b=s.index('template<class Func>',a)
        (out/f'm4_stage{ix}.cpp').write_text(s[:a]+cpp+s[b:])
    print(f'M4_TARGETS_OK cycles={len(cycles)} unique_cut_states={len(targets)} independently_checked_columns={checks}')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: agent11_p16_m4.py WORKDIR')
    prepare(Path(sys.argv[1]).resolve())
