import sys, itertools, collections
sys.path.insert(0,'/home/claude/rev101')
from outer_ref import outer
k=lambda x:1 if x>=10 else 0
t=lambda x:x-9*k(x)
def rsuf(c,B):
    tc=t(c); r=0
    for x in reversed(B):
        if x in (tc,tc+9): r+=1
        else: break
    return r
def phi(c,B): return len(B)-rsuf(c,B)
hist=collections.Counter(); hist2=collections.Counter(); worst=None
for c in range(2,17,2):
    for L in range(0,5):
        for B in itertools.product(range(19),repeat=L):
            if L and (B[0]<1 or B[-1]==c): continue
            c1,B1,g=outer(c,list(B))
            d=phi(c1,B1)-phi(c,list(B)); hist[d]+=1
            # two-step
            c2,B2,g2=outer(c1,B1)
            d2=phi(c2,B2)-phi(c,list(B)); hist2[d2]+=1
            if worst is None or d2<worst[0]: worst=(d2,c,B)
print("one-step dPhi",sorted(hist.items()))
print("two-step dPhi",sorted(hist2.items()), "worst",worst)
