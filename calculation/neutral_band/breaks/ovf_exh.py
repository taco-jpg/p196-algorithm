from lib import *
import itertools
def sym(L,b):
    for half in itertools.product(range(2*b-1),repeat=(L+1)//2):
        yield list(half)+list(half[:L//2][::-1])
res=collections.Counter()
for b,LB,LC in ((3,4,5),(4,3,4),(5,3,4),(6,3,4),(7,3,3),(10,3,3),(11,2,3)):
    cnt=collections.Counter()
    for lb in range(1,LB+1):
        for B in itertools.product(range(2*b-1),repeat=lb):
            if B[0]==0: continue
            for lc in range(LC+1):
                for C in sym(lc,b):
                    B_,C_=list(B),C
                    if not hyp(b,B_,C_): continue
                    G=gam(b,B_,C_)
                    B2=nextB(b,B_,C_); C2=nextC(b,B_,C_)
                    F1,F2=e1(b,B2),e2(b,B2,C2)
                    E1,E2=e1(b,B_),e2(b,B_,C_)
                    kind='flip' if (F1==1-E1 and F2==1-E2) else ('same' if (F1==E1 and F2==E2) else 'brk')
                    cnt[(G,kind)]+=1
    print("base",b,dict(cnt))
