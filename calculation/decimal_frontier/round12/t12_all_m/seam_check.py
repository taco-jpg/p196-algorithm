#!/usr/bin/env python3
"""Independent check of seam.cpp: Python cone + genuine big-integer n+rev(n)."""
import random, sys
from collections import Counter
sys.set_int_max_str_digits(100000)
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)
J0=34+9*14
def us(): return [tuple((9,a,18-a)[r:]+(9,a,18-a)[:r]) for a in range(0,19,2) for r in range(3)]
def norm(w,c):
    o=[]
    for x in w: z=x+c; o.append(z%10); c=z//10
    return o,c
def cone(p):
    for t in range(120):
        n=len(p); d,_=norm(p,0); a0,g0=norm(p[::-1],0); a1,g1=norm(p[::-1],1)
        assert g0==g1==(t%4==0)
        g=g0
        if g:
            l0=[d[0]+1]+[d[i]+a0[n-i] for i in range(1,n)]; l1=[d[0]+1]+[d[i]+a1[n-i] for i in range(1,n)]
        else:
            l0=[d[i]+a0[n-1-i] for i in range(n)]; l1=[d[i]+a1[n-1-i] for i in range(n)]
        j=next((i for i in range(n) if l0[i]!=l1[i]),n); p=l0[:j]
    return p
def realize(P):
    d=[0]*len(P)
    for i in range(len(P)//2): d[i]=max(0,P[i]-9); d[-i-1]=P[i]-d[i]
    if len(P)%2: d[len(P)//2]=P[len(P)//2]//2
    return d
def pairs(n):
    s=str(n)[::-1]; ds=[int(c) for c in s]; return [x+y for x,y in zip(ds,ds[::-1])]
def real_prefix(U,J,C,k=100):
    H=list(B)+list(W)*14+list(J)+list(U)*k
    P=H+list(C)+H[::-1]; d=realize(P)
    n=int(''.join(map(str,d[::-1])))
    assert pairs(n)==P
    for t in range(120):
        n+=int(str(n)[::-1])
    return pairs(n)
def first_mismatch(p,tg):
    return next((i-J0 for i in range(len(p)) if p[i]!=tg[i]),None)
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='hist':
        Lj=int(sys.argv[2]); h=Counter()
        import itertools
        for U in us():
            for J in itertools.product(range(19),repeat=Lj):
                J=J[::-1]
                p=list(B)+list(W)*14+list(J)+list(U)*60
                tg=list(B)+list(W)*14+list(J)+list(U)*65
                h[first_mismatch(cone(p),tg)]+=1
        print('Lj',Lj,sorted(h.items(),key=lambda x:(x[0] is None, x[0] or 0)))
    else:
        random.seed(int(sys.argv[2])); bad=0
        for trial in range(int(sys.argv[3])):
            U=random.choice(us()); Lj=random.randrange(0,9); J=[random.randrange(19) for _ in range(Lj)]
            Lc=random.randrange(1,9); h=[random.randrange(19) for _ in range((Lc+1)//2)]
            if Lc%2: h[-1]&=~1
            C=h+h[::-1] if Lc%2==0 else h+h[-2::-1]
            p=cone(list(B)+list(W)*14+J+list(U)*60)
            r=real_prefix(U,J,C)
            ok=r[:len(p)]==p
            tg=list(B)+list(W)*14+J+list(U)*105
            print('trial',trial,'U',U,'J',J,'C',C,'cone_len',len(p),'cone==real',ok,'cone_mis',first_mismatch(p,tg),'real_mis',first_mismatch(r,tg),flush=True)
            bad+= (not ok)
        print('BAD',bad)
