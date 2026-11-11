#!/usr/bin/env python3
import os
"""Control: the surviving tower of (g=0001, d0=4, L=12) must contain N12's columns above its birth column.
N12 from r12c py/n12_wit.txt (B_t, t=0..11).  Birth column index a=2: column 2 of N12 equals (up to rotation) the column of the surviving tower.
Check: compute the exact tower kept windows above that birth (python, up to level R) and test that N12's columns 3..3+R-1 are in the kept set at each level, for the rotation that matches."""
import sys
sys.path.insert(0,os.path.expanduser('~/p196_run/r13c/py'))
b=10
wit=os.path.expanduser('~/p196_run/r12c/py/n12_wit.txt')
B=[list(map(int,l.split(','))) for l in open(wit).read().strip().split('\n')]; T=len(B)
def col(j): return [ (B[t][j] if j<len(B[t]) else 9) for t in range(T)]
spec='100010001001|0,0,0,6,0,0,0,7,0,0,0,15|211321232123'
vcol=[10,1,3,6,10,1,3,7,11,3,7,15]
cs,xs,As=spec.split('|'); c=[int(x) for x in cs]; xb=[int(x) for x in xs.split(',')]; A=[int(x) for x in As]
g=[int('0001'[t%4]) for t in range(12)]
col2=col(2)
rots=[r for r in range(12) if all(vcol[t]==col2[(t+r)%12] for t in range(12))]
print("birth column equals N12 col2 rotated by r in",rots)
r=rots[0]
# tower exact via python functions
def trans(w,t,h):
    k=len(w); H=[0]*(k+2); H[k+1]=h
    for i in range(k,0,-1): H[i]=(w[i-1]+H[i+1])//b
    if not (A[t]>>H[1])&1: return None
    L=c[t]; y=[0]*k
    for i in range(1,k+1):
        wi=w[i-1]; cin=L; L=(wi+L)//b
        if g[t]: low=(xb[t] if i==1 else w[i-2]); part=(low+H[i])%b
        else: part=(wi+H[i+1])%b
        y[i-1]=(wi+cin)%b+part
    return tuple(y)
Lp=12
def closedset(nodes):
    succ={n:[] for n in nodes}
    for (w,t) in nodes:
        for h in (0,1):
            y=trans(w,t,h)
            if y is None: continue
            m=(y,(t+1)%Lp)
            if m in nodes and m not in succ[(w,t)]: succ[(w,t)].append(m)
    t0=0
    layer=[ [n for n in nodes if n[1]==t] for t in range(Lp)]
    keep=set()
    for s in layer[t0]:
        fw=[{s}]
        for i in range(Lp):
            nx=set()
            for n in fw[-1]: nx.update(succ[n])
            fw.append(nx)
        if s not in fw[Lp]: continue
        bw=[None]*(Lp+1); bw[Lp]={s}
        for i in range(Lp-1,-1,-1):
            bw[i]=set(n for n in fw[i] if any(m in bw[i+1] for m in succ[n]))
        for i in range(Lp): keep|=(fw[i]&bw[i])
    return keep
nodes=set(((v,),t) for t in range(12) for v in range(19))
Rmax=int(sys.argv[1]) if len(sys.argv)>1 else 40
ok=True
for R in range(1,Rmax+1):
    keep=closedset(nodes)
    # N12 window at level R above column 2 (columns 3..2+R), with rotation r: at tower phase t the window is col(3+j)[(t+r)%12]
    win_ok=True
    for t in range(12):
        w=tuple(col(3+j)[(t+r)%12] for j in range(R))
        if (w,t) not in keep: win_ok=False; print("LEVEL",R,"phase",t,"missing N12 window",w[:6]); break
    print(f"level {R}: kept={len(keep)} N12 windows present: {win_ok}")
    if not win_ok: ok=False; break
    nodes=set((w+(d,),t) for (w,t) in keep for d in range(19))
print("RESULT","N12 present at all levels" if ok else "FAIL")
