"""Exact LSD-first schoolbook physical decimal controls for rooted phase 11."""
B=[5,2,3,3,3,16,9,7,18,6,0,1,5,8,13,9,18,12,12,8,12,8,17,9,6,14,5,18,14,11,12,11,9,12]
W=[2,9,2,4,0,17,11,9,12]
assert len(B)==34 and len(W)==9
def template(J,U,C,q=14,k=100):
    h=B+W*q+list(J)+list(U)*k
    return h+list(C)+h[::-1]
def realize(P):
    assert P==P[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        d[i]=P[i]-min(9,P[i])
        d[-1-i]=min(9,P[i])
    if len(P)&1:
        assert P[len(P)//2]%2==0
        d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]!=0
    return d
def step(d):
    out=[];c=0
    for x,y in zip(d,d[::-1]):
        v=x+y+c
        out.append(v%10)
        c=v//10
    if c:out.append(c)
    return out
def pair(d):
    return [a+b for a,b in zip(d,d[::-1])]
def run(J,U,C,q=14,k=100,steps=120):
    P=template(J,U,C,q,k);d=realize(P);gamma=[]
    for _ in range(steps):
        n=step(d);gamma.append(len(n)-len(d));d=n
    t=template(J,U,C,q,k+5);p=pair(d)
    mismatch=next((i for i,(x,y) in enumerate(zip(p,t)) if x!=y),None)
    if mismatch is None and len(p)!=len(t):mismatch=min(len(p),len(t))
    return mismatch,sum(gamma),p,t,''.join(map(str,gamma))
