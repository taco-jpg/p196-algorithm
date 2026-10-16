# Agent #102 literal control for Agent #11 high-region threshold (semantics only).
import random, json
def digs(n,b):
    d=[]
    while n: d.append(n%b); n//=b
    return d
def val(d,b): return sum(x*b**i for i,x in enumerate(d))
def rev(n,b): return val(digs(n,b)[::-1],b)
random.seed(11); cases=0; pal_true=0
for b in range(3,17):
    for _ in range(3000):
        L=random.randint(1,12)
        # choose pair sums q symmetric in [b-1,2b-2], q0>=b, realize digits
        half=[random.randint(b-1,2*b-2) for _ in range((L+1)//2)]
        half[0]=random.randint(b,2*b-2)
        q=half+half[:L//2][::-1]
        if L%2==1 and q[L//2]%2: q[L//2]-=1 if q[L//2]-1>=b-1 else -1
        if L%2==1 and (q[L//2]<b-1 or q[L//2]>2*b-2 or q[L//2]%2): continue
        if L==1 and q[0]<b: continue
        d=[0]*L
        for i in range((L+1)//2):
            j=L-1-i
            if i==j: d[i]=q[i]//2; continue
            hi=min(b-1,q[i]); d[j],d[i]=hi,q[i]-hi
        n=val(d,b); assert [x+y for x,y in zip(d,d[::-1])]==q and d[-1]>0
        m1=n+rev(n,b); D1=digs(m1,b)
        r=[x-b+1 for x in q]
        p1=[x+y for x,y in zip(D1,D1[::-1])]
        expect=[r[0]]+[r[i]+r[i+1] for i in range(L-1)]+[r[0]]
        assert p1==expect,(b,q,p1,expect)
        m2=m1+rev(m1,b); D2=digs(m2,b)
        ispal=D2==D2[::-1]
        assert ispal==all(q[i]+q[i+1]<=3*b-3 for i in range(L-1)),(b,q)
        cases+=1; pal_true+=ispal
print(json.dumps(dict(bases="3..16",cases=cases,second_palindromes=pal_true,status="PASS")))
