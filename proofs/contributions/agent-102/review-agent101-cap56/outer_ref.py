# Agent #102: outer map (c,B) -> (c',B',gamma) written from METHOD_AND_PROOF.md (3),(4),(6),(7)
# and the sec. 6 suffix trim, plus literal-integer controls. Independent of Agent #101's code.
import random, json, sys
def N(W,e):
    D=[]
    for x in W: D.append((x+e)%10); e=(x+e)//10
    return D,e
k=lambda x:1 if x>=10 else 0
t=lambda x:x-9*k(x)
def outer(c,B):
    DB,e0=N(B,0); DRB,gam=N(B[::-1],k(c)); u0=c+e0-10*k(c); tc=t(c)
    X=DB+[u0]; Y=(DRB[::-1]+[tc]) if gam==0 else ([1]+DRB[::-1])
    Br=[a+b for a,b in zip(X,Y)]; c2=2*tc
    while Br and Br[-1]==c2: Br.pop()
    return c2,Br,gam
def pairw(D): return [a+b for a,b in zip(D,D[::-1])]
def realize(q):
    L=len(q); dig=[0]*L
    for i in range((L+1)//2):
        j=L-1-i
        if i==j: dig[i]=q[i]//2; continue
        hi=min(9,q[i]); dig[j],dig[i]=hi,q[i]-hi
    return int(''.join(map(str,dig[::-1])))
def control(n_rand=20000, seed=1020):
    random.seed(seed); phases=[x for x in range(1,18) if x!=9]; cnt=0
    for _ in range(n_rand):
        c=random.choice(phases); d=18-c
        B=[random.randint(0,18) for _ in range(random.randint(0,7))]
        if B: B[0]=random.randint(1,18)
        while B and B[-1]==c: B.pop()
        A=[random.randint(0,18) for _ in range(random.randint(0,3))]
        half=[random.randint(0,18) for _ in range(random.randint(0,2))]
        C=half+([2*random.randint(0,9)] if random.random()<.5 else [])+half[::-1]
        g=random.randint(12,16); h=random.randint(2,6)
        q=B+[c]*g+A+[d]*h+C+[d]*h+A[::-1]+[c]*g+B[::-1]
        n=realize(q); m=n+int(str(n)[::-1]); w=pairw([int(x) for x in str(m)[::-1]])
        c2,Bp,gam=outer(c,B)
        assert len(str(m))==len(str(n))+gam
        # w must be B' followed by a run of c2 that is at least g-2+gam-(|B|+1-|B'|) long... check prefix and band start
        assert w[:len(Bp)]==Bp, (c,B)
        j=len(Bp)
        while w[j]==c2: j+=1
        assert j-len(Bp) >= g-2+gam, (c,B)   # band (incl. absorbed trailing c2) is genuinely there
        assert not Bp or Bp[-1]!=c2
        cnt+=1
    return cnt
if __name__=="__main__":
    print(json.dumps(dict(literal_controls=control(),status="PASS")))
