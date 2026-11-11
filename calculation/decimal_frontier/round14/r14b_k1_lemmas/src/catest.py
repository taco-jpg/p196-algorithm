# Validate the local CA form of reverse-and-add on pair words (genuine big-integer arithmetic).
import random
random.seed(20261108)
def pairs(N,n):
    d=[(N//10**i)%10 for i in range(n)]
    return [d[i]+d[n-1-i] for i in range(n)]
def step_int(N,n):
    M=N+int(str(N).zfill(n)[::-1])
    g=len(str(M))-n
    return M,g
def ca_step(P,g):
    """P: full palindromic pair word (list length n). Local rule with 9-transparency applied on the full line.
    returns new pair word of length n+g."""
    n=len(P)
    # c, a, b via 9-transparent rule (b computed from the mirrored a, i.e. the true carry chains on the full line)
    a=[0]*(n+1)
    for x in range(n):
        if P[x]!=9: a[x+1]=1 if P[x]>=10 else 0
        else: a[x+1]=a[x]
    # descending in folded picture: b_x = carry into mirror position; on the full line b_x = a[n-1-x]
    # local check: for non-9 P_x, b_{x-1} = c_x
    b=[a[n-1-x] for x in range(n)]
    for x in range(1,n):
        if P[x]!=9:
            assert b[x-1]==(1 if P[x]>=10 else 0)
        else:
            assert b[x-1]==b[x]
    Q=[]
    for x in range(n+g):
        if g==0:
            # P'_x = e_x + r_x with e=(P+a)%10, r=(P+b)%10
            v=(P[x]+a[x])%10+(P[x]+b[x])%10
            if P[x]!=9:
                d=P[x]%10; assert v==2*d+a[x]+b[x]
            else:
                assert v==18-9*(a[x]+b[x])
        else:
            # new position x has e_x (x<n) and r_{x-1}; on the full line: digit at x + digit at n-x
            ex=(P[x]+a[x])%10 if x<n else a[n]  # top digit when g=1: a[n]=1
            if x==0:
                rm=g  # r_{-1} = carry out = g (the new leading digit 1 pairs with position 0)
                # new digit at position n is g; pair with position 0 digit
            else:
                rm=(P[x-1]+b[x-1])%10
            v=ex+rm
        Q.append(v)
    return Q
ok=0; tot=0
for it in range(200000):
    n=random.randint(4,40)
    N=random.randrange(10**(n-1),10**n)
    P=pairs(N,n)
    M,g=step_int(N,n)
    n2=n+g
    if g==1:
        # P' full word of length n+1
        Q=ca_step(P,1)
    else:
        Q=ca_step(P,0)
    P2=pairs(M,n2)
    tot+=1
    if Q==P2: ok+=1
    else:
        print("MISMATCH",n,N,g,P,Q,P2); break
print("big-integer test of CA local rule (g=0 and g=1, palindromic pair words incl. 9 cells):",ok,"of",tot)
# Now validate R-form for non-9 neighbour cells on random pair words (g=1 interior cells):
bad=0
for it in range(200000):
    n=random.randint(6,40)
    N=random.randrange(10**(n-1),10**n)
    P=pairs(N,n)
    M,g=step_int(N,n)
    P2=pairs(M,n+g)
    # choose interior x
    h=(n+1)//2
    for x in range(1,h-1):
        if g==1 and P[x]!=9 and P[x-1]!=9:
            R=lambda p: (p-9 if p>=10 else p)
            if P2[x]!=R(P[x])+R(P[x-1]):
                bad+=1
        if g==0 and P[x]!=9 and P[x-1]!=9 and P[x+1]!=9:
            c=lambda p:1 if p>=10 else 0
            if P2[x]!=2*(P[x]%10)+c(P[x-1])+c(P[x+1]):
                bad+=1
print("R-form interior mismatches (non-9 neighbourhoods):",bad)
