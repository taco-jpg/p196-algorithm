# Agent #102 independent control for the review of Agent #109 (written from METHOD_AND_PROOF.md
# eqs (1),(3)-(8) only, without reading Agent #109's controls.py). Semantics check, not proof.
import random, json
random.seed(102)
def N(W,e):
    D=[]
    for x in W: D.append((x+e)%10); e=(x+e)//10
    return D,e
def pair(D): return [a+b for a,b in zip(D,D[::-1])]
def Q(c,B,A,C,g,h):
    d=18-c; return B+[c]*g+A+[d]*h+C+[d]*h+A[::-1]+[c]*g+B[::-1]
def realize(q):  # canonical integer with mirrored-sum word q (q symmetric, positive exterior, even middle)
    L=len(q); dig=[0]*L
    for i in range((L+1)//2):
        j=L-1-i
        if i==j: dig[i]=q[i]//2; continue
        hi=min(9,q[i]); lo=q[i]-hi
        dig[j],dig[i]=hi,lo   # most significant gets the larger part, positive since q[0]>0
    return int(''.join(map(str,dig[::-1])))
def G(n):
    m=n+int(str(n)[::-1]); D=[int(x) for x in str(m)[::-1]]; return pair(D)
k=lambda x:1 if x>=10 else 0
t=lambda x:x-9*k(x)
phases=[x for x in range(1,18) if x!=9]
cnt=0
for _ in range(20000):
    c=random.choice(phases); d=18-c
    B=[random.randint(0,18) for _ in range(random.randint(0,3))]
    if B: B[0]=random.randint(1,18)
    A=[random.randint(0,18) for _ in range(random.randint(0,3))]
    half=[random.randint(0,18) for _ in range(random.randint(0,2))]
    mid=[2*random.randint(0,9)] if random.random()<.5 else []
    C=half+mid+half[::-1]
    g,h=random.randint(2,6),random.randint(2,6)
    q=Q(c,B,A,C,g,h); n=realize(q); assert pair([int(x) for x in str(n)[::-1]])==q
    DB,e0=N(B,0); DA,e1=N(A,k(c)); DC,e2=N(C,k(d)); DRA,e3=N(A[::-1],k(d)); DRB,gam=N(B[::-1],k(c))
    u0=c+e0-10*k(c); u1=d+e1-10*k(d); u2=d+e2-10*k(d); u3=c+e3-10*k(c)
    w5=DB+[u0]+[t(c)]*(g-1)+DA+[u1]+[t(d)]*(h-1)+DC+[u2]+[t(d)]*(h-1)+DRA+[u3]+[t(c)]*(g-1)+DRB+([1] if gam else [])
    m=n+int(str(n)[::-1]); assert [int(x) for x in str(m)[::-1]]==w5
    add=lambda X,Y:[a+b for a,b in zip(X,Y)]
    if gam==0:
        Br=add(DB+[u0],DRB[::-1]+[t(c)]); Ar=add([t(c)]+DA+[u1],[u3]+DRA[::-1]+[t(d)]); Cr=pair([t(d)]+DC+[u2])
    else:
        Br=add(DB+[u0],[1]+DRB[::-1]); Ar=add(DA+[u1],[u3]+DRA[::-1]); Cr=pair(DC+[u2])
    assert G(n)==Q(2*t(c),Br,Ar,Cr,g-2+gam,h-2+gam)
    cnt+=1
print(json.dumps(dict(cases=cnt,seed=102,status="PASS")))
