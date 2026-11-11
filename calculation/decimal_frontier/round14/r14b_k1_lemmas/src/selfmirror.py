# enumerate exact cyclic rows of spatial period m (m|4) with 8-step return under clock 10 (g=1,0,1,0,...).
import itertools
BASE=10
def cyc_carry(row):
    m=len(row)
    # ascending carries a_x, x cyclic; solve by fixpoint: for non-all-9 rows unique
    if all(v==BASE-1 for v in row): return None
    a=[0]*m
    for it in range(3*m):
        for x in range(m):
            a[(x+1)%m]=1 if row[x]+a[x]>=BASE else 0
    return a
def step(row,g):
    m=len(row)
    a=cyc_carry(row)
    if a is None: return None
    # descending: b_{x-1} = [P_x + b_x >= 10]
    b=[0]*m
    for it in range(3*m):
        for x in range(m-1,-1,-1):
            b[(x-1)%m]=1 if row[x]+b[x]>=BASE else 0
    e=[(row[x]+a[x])%BASE for x in range(m)]
    r=[(row[x]+b[x])%BASE for x in range(m)]
    new=[e[x]+r[(x-g)%m] for x in range(m)]
    if any(v>18 for v in new): return None
    return tuple(new)
results={}
for m in (1,2,4):
    cnt=0; lst=[]
    for row in itertools.product(range(19),repeat=m):
        r=tuple(row)
        ok=True
        cur=r
        for t in range(8):
            g=1 if t%2==0 else 0
            cur=step(cur,g)
            if cur is None: ok=False;break
        if ok and cur==r:
            lst.append(r)
    # palindromic check: is the row (as a cyclic word) a palindrome under some centre?
    def ispal(row):
        m=len(row)
        for s in range(m):
            rr=row[s:]+row[:s]
            if rr==rr[::-1]: return True
        return False
    # keep canonical under rotation
    canon=set(min(r[i:]+r[:i] for i in range(m)) for r in lst)
    pal=[r for r in canon if ispal(r)]
    print("m",m,"exact 8-step return rows:",len(lst),"up to rotation",len(canon),"palindromic rows up to rotation:",len(pal))
    print("  examples",sorted(canon)[:10])
