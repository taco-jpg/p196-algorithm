#!/usr/bin/env python3
"""Independent exact checks for the rooted p12/m9 U6=(3,3,9,15,15,9) 240-clock lane.
Uses the same decimal definitions as ordinary n + reverse(n), plus an independent digit-array oracle.
"""
import sys
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(0)

B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
U = [3,3,9,15,15,9]

def gamma(t): return int(t % 4 == 0)
def tr(x,c): return int(x+c >= 10)

def F(w,g):
    m=len(w); lo=[0]*m; hi=[0]*m; z=0
    for _ in range(2):
        for x in w: z=tr(x,z)
    lo[0]=z
    for i in range(1,m): lo[i]=tr(w[i-1],lo[i-1])
    z=0
    for _ in range(2):
        for x in w[::-1]: z=tr(x,z)
    hi[0]=z
    for i in range(m-1,0,-1): hi[i]=tr(w[i],hi[(i+1)%m])
    assert all(tr(w[i],lo[i])==lo[(i+1)%m] for i in range(m))
    assert all(tr(w[i],hi[(i+1)%m])==hi[i] for i in range(m))
    return tuple((w[i]+lo[i])%10 + ((w[i]+hi[(i+1)%m])%10 if not g else (w[(i-1)%m]+hi[i])%10) for i in range(m))

def rows(w, n):
    out=[tuple(w)]
    for t in range(n): out.append(F(out[-1],gamma(t)))
    return out

def cone(v, n):
    m=len(v[0]); left=right=0
    for t in range(n):
        w=v[t]
        left += 1 + int(w[left % m] == 9)
        right += 1 + int(w[(-right-1) % m] == 9) - gamma(t)
    return left,right

def realize(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]); lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo; d[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0 and all(0<=x<=9 for x in d)
    return int(''.join(map(str,d[::-1])))

def pair(n):
    d=list(map(int,str(n)[::-1]))
    return [d[i]+d[-1-i] for i in range(len(d))]

def digit_array_step(n):
    d=list(map(int,str(n)[::-1])); carry=0; out=[]
    for x,y in zip(d,d[::-1]):
        z=x+y+carry; out.append(z%10); carry=z//10
    if carry: out.append(carry)
    return int(''.join(map(str,out[::-1])))

def seed(q,k,J,C,Uword=U):
    H=B+W*q+list(J)+list(Uword)*k
    P=H+list(C)+H[::-1]
    assert P==P[::-1]
    return realize(P)

def insert(p,w,c):
    L=len(p)
    return p[:c]+list(w)+p[c:L-c]+list(w)[::-1]+p[L-c:]

def w_loss_240(q, wr):
    m=len(B)+len(W)*q
    start=m
    for t in range(240):
        r=0
        while wr[t][(m-35-r)%len(W)]==9: r+=1
        m-=1+r-gamma(t)
    return start-m,m

def verify_insertions(q,k,J,C):
    wr=rows(W,240); ur=rows(U,240)
    for kind in ('W','U6'):
        if kind=='W':
            x=seed(q,k,J,C); y=seed(q+1,k,J,C); cut=34+18; rr=wr
        else:
            x=seed(q,k,J,C); y=seed(q,k+1,J,C); cut=34+9*q+len(J)+330; rr=ur
        for t in range(241):
            px=pair(x); py=pair(y)
            assert py==insert(px,rr[t],cut),(kind,q,k,J,C,t,'paired insertion')
            assert any(z&1 for z in px[:34]),(kind,t,'palindrome guard')
            if t==240: break
            nx=x+int(str(x)[::-1]); ny=y+int(str(y)[::-1])
            assert nx==digit_array_step(x),(kind,t,'digit-array oracle x')
            assert ny==digit_array_step(y),(kind,t,'digit-array oracle y')
            assert len(str(nx))-len(str(x))==gamma(t),(kind,t,'clock x')
            assert len(str(ny))-len(str(y))==gamma(t),(kind,t,'clock y')
            x,y=nx,ny
        print(f'INSERTION_PASS kind={kind} q={q} k={k} |J|={len(J)} |C|={len(C)} steps=240 bigint+digit-array')

def prefix_step(P, urow, g):
    """Exact low-prefix transition, cut 330 U6 cells beyond J; lookahead resets high carry."""
    M=len(P); r=next(i for i,x in enumerate(urow) if x!=9)
    stop=M+r
    b=[0]*(M+6)
    b[stop]=urow[r]//10
    def get(i): return P[i] if i<M else urow[i-M]
    for i in range(stop-1,-1,-1): b[i]=(get(i)+b[i+1])//10
    low=[0]*M; high=[0]*M; c=0
    for i in range(M):
        z=P[i]+c; low[i]=z%10; c=z//10
    for i in range(M): high[i]=(P[i]+b[i+1])%10
    Q=[0]*M
    if not g:
        for i in range(M): Q[i]=low[i]+high[i]
    else:
        Q[0]=low[0]+1
        for i in range(1,M): Q[i]=low[i]+high[i-1]
    assert all(0<=x<=18 for x in Q)
    return Q

def verify_local_prefix(q,k,J,C):
    ur=rows(U,240)
    H=B+W*q+list(J)+U*k
    src=H+list(C)+H[::-1]
    n=realize(src)
    M=len(B)+9*q+len(J)+330
    P=B+W*q+list(J)+U*55
    for t in range(241):
        actual=pair(n)
        assert actual[:M]==P,(q,k,J,C,t,'local prefix differs from full bigint pairword')
        assert P[M-6:]==list(ur[t][:6]),(q,k,J,C,t,'cut guard not pure U6')
        if t==240: break
        nn=n+int(str(n)[::-1])
        assert nn==digit_array_step(n),(q,k,J,C,t,'digit-array mismatch')
        assert len(str(nn))-len(str(n))==gamma(t),(q,k,J,C,t,'overflow clock mismatch')
        P=prefix_step(P,ur[t],gamma(t))
        n=nn
    if q>=24:
        target=B+W*q+list(J)+U*55
        first=next(i for i,(x,y) in enumerate(zip(P,target)) if x!=y)
        w_end=len(B)+9*q
        assert 34 <= w_end-first <= 48,(q,k,J,C,first,w_end,'expected W9 mismatch window')
    print(f'LOCAL_PREFIX_BIGINT_PASS q={q} k={k} J={J} C={C} phases=240')

def main():
    wr=rows(W,240); ur=rows(U,240)
    assert wr[12]==tuple(W) and wr[240]==tuple(W)
    assert ur[48]==tuple(U) and ur[120]==(15,15,9,3,3,9) and ur[240]==tuple(U)
    assert ''.join(map(str,[gamma(t) for t in range(240)]))=='1000'*60
    assert all(sum(r)==54 and all(not (r[i]==r[(i+1)%6]==9) for i in range(6)) for r in ur)
    print('U6 cycle: phase-48 return, phase-120 half-turn, phase-240 return; 240 clock=(1000)^60; every row sum=54, no adjacent 9s.')
    rotcones=[]
    for rot in range(6):
        v=rows(U[rot:]+U[:rot],240)
        rotcones.append(cone(v,240))
        assert v[240]==tuple(U[rot:]+U[:rot])
    print('U6 cone losses for six spatial rotations:',rotcones)
    assert max(x for x,y in rotcones)==300 and max(y for x,y in rotcones)==240
    loss,remain=w_loss_240(24,wr)
    print(f'Rooted W9 cone: q=24 starts at {34+9*24}, 240-step loss={loss}, protected prefix remains={remain}, W cut=52 leaves {remain-52} coefficients.')
    assert loss==181 and remain==69 and remain-52==17
    # Exact truncated-prefix engine versus independent full integers at the required widths.
    for q,k,J,C in [
        (20,100,[0,0,0],[0,0,0]),
        (24,100,[0,0,0],[0,0,0]),
        (24,100,[18,18,18,18],[0,0,0]),
        (24,100,[0,1,2,3,4],[0,0,0]),
        (24,100,[18,18,18,18,18],[0,0,0]),
        (40,160,[13,16,4,9],[0,0,0]),
        (80,320,[18,18,18,18],[0,0,0]),
        (160,640,[5,18,10],[8,8]),
    ]:
        verify_local_prefix(q,k,J,C)
    # Paired insertions: two centre parities and two independent widths.
    for q,k,J,C in [
        (24,100,[0,0,0],[0,0,0]),
        (24,100,[13,16,4,9],[0,0,0]),
        (24,100,[0,1,2,3,4],[0,0,0]),
        (40,160,[18,18,18,18,18],[0,0,0]),
        (80,320,[5,18,10],[8,8]),
        (160,640,[1,7,11],[10]),
    ]:
        verify_insertions(q,k,J,C)
    print('U6_240_CONTROLS_PASS')

if __name__=='__main__': main()
