#!/usr/bin/env python3
"""X25 independent ordinary-bigint replay of seven actual decimal seeds."""
import argparse, hashlib, json, sys
sys.set_int_max_str_digits(1000000)
B=(17,5,0,1,13,4,14,12,9,8,15,16,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
W=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)
C=(8,0,0,16,0,0,8)
A=(6,1,0,1,11,14,10,6,11,16,1)
D=(16,0,9,11,1,10,8,5,14,18,0)
def root(q):
    h=list(B)+list(W)*q
    return h+list(C)+h[::-1]
def splice(word, packets):
    p=word.copy()
    for at,symbol in packets:
        for j,v in enumerate(symbol):p[at+j]=p[-1-at-j]=v
    return p
def realize(p):
    n=len(p);digits=[0]*n
    assert p==p[::-1] and p[0]>0
    for j in range(n//2):
        z=p[j];hi=max(1,z-9) if j==0 else max(0,z-9);lo=z-hi
        assert 0<=lo<=9 and 0<=hi<=9
        digits[j]=lo;digits[n-1-j]=hi
    if n%2:
        assert p[n//2]%2==0
        digits[n//2]=p[n//2]//2
    return int(''.join(map(str,digits[::-1])))
def pairs(n):
    s=str(n)
    return [int(a)+int(b) for a,b in zip(s[::-1],s)]
def check(q,gap,steps):
    assert gap>=180 and gap%180==0 and q*20>960+gap+11+steps
    src=root(q);x=960;y=x+gap
    p=[src,splice(src,[(x,A)]),splice(src,[(x,D)]),
       splice(src,[(y,A)]),splice(src,[(y,D)]),
       splice(src,[(x,A),(y,D)]),splice(src,[(x,D),(y,A)])]
    ns=[realize(z) for z in p]
    assert list(map(pairs,ns))==p
    nonlinear={'AD':None,'DA':None};daughter={'AD':None,'DA':None};phase={};checkpoints={}
    for t in range(steps+1):
        ss=[str(n) for n in ns]
        assert len(set(map(len,ss)))==1,('length split',t)
        assert all(s!=s[::-1] for s in ss),('palindrome',t)
        assert len(ss[0])==len(src)+(t+1)//2,('p8 clock',t)
        pw=[pairs(n) for n in ns]
        assert all(z[:39]==pw[0][:39] for z in pw),('exterior',t)
        sig=(pw[0][:39],pw[0][100:140],pw[0][170:210])
        if t<8:phase[t]=sig
        else:assert sig==phase[t%8],('p8 phase',t)
        L=len(pw[0])//2
        for out,one,two,name in ((5,1,4,'AD'),(6,2,3,'DA')):
            if nonlinear[name] is None:
                bad=[i for i in range(L) if pw[out][i]+pw[0][i]!=pw[one][i]+pw[two][i]]
                if bad:nonlinear[name]=(t,bad[0],len(bad))
            if daughter[name] is None:
                bad=[i for i in range(L) if pw[out][i]!=pw[0][i] and pw[one][i]==pw[0][i] and pw[two][i]==pw[0][i]]
                if bad:daughter[name]=(t,bad[0],len(bad))
        if t in (0,392,395,398,407,788,791,794,803,steps):
            checkpoints[t]=hashlib.sha256('|'.join(ss).encode()).hexdigest()
        if t<steps:ns=[n+int(str(n)[::-1]) for n in ns]
    k=gap//180
    expected={'AD':(198*k-4,135*k+962,2),'DA':(198*k-1,135*k+964,2)}
    assert nonlinear==expected,(nonlinear,expected)
    if gap==360:assert daughter=={'AD':(407,1231,1),'DA':(398,1232,1)},daughter
    if gap==720:assert daughter=={'AD':(803,1501,1),'DA':(794,1502,1)},daughter
    return {'label':'COMPUTED finite horizon only','q':q,'gap':gap,'steps':steps,
            'initial_digits':len(src),'final_digits':len(str(ns[0])),'seeds':7,
            'nonlinear':nonlinear,'daughter':daughter,'sha256':checkpoints}
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--q',type=int,default=140)
    ap.add_argument('--gap',type=int,default=360)
    ap.add_argument('--steps',type=int,default=1000)
    a=ap.parse_args();print(json.dumps(check(a.q,a.gap,a.steps),indent=2))
