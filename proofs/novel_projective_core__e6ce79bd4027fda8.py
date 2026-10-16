"""Exact checks for a protected central high-carry core and outer growth bound.
Research only: no decimal Lychrel number is established.
"""
from itertools import product

def step(q):
    c=0; out=[]
    for a in q:
        a+=c;out.append(a%10);c=a//10
    if c:out.append(c)
    return tuple(a+b for a,b in zip(out,reversed(out)))

def edges(q):
    if q<9:return [(2*q,0),(2*q+1,0)]
    if q==9:return [(18,0),(10,1)]
    return [(q-9,1)]

POTENTIAL=(0,0,0,0,1,0,1,1,1,2,1,1,1,2,1,2,2,2,3)

def core_len(q):
    L=len(q)
    if L%2:
        a=L//2;b=a+1
        if q[a]!=18:return 0
    else:
        a=b=L//2
    while a>0 and q[a-1]==18 and q[b]==18:a-=1;b+=1
    return b-a

def verify():
    for q in range(1,19):
        for r,h in edges(q):
            assert 2*h-1<=POTENTIAL[q]-POTENTIAL[r]
    count=0
    for k in range(1,4):
        for p in product(range(19),repeat=k):
            if p[0]==0 or p[-1]==18:continue
            for m in (1,2,3,4,5):
                q=p+(18,)*m+p[::-1]; r=step(q); h=len(r)-len(q)
                assert (r[0],h) in edges(q[0])
                cm=core_len(r)
                if h:assert cm==m-1,(q,r,cm)
                else:assert cm in (m,max(0,m-2)),(q,r,cm)
                count+=1
    return count

if __name__=='__main__':
    print({'verified_core_cases':verify(),'potential':POTENTIAL[1:],
           'claimed_decimal_lychrel_witness':None})


def two_pair_step(a,b,u):
    low=a//10
    high=(b+u)//10
    h=(a+high)//10
    if h:
        return (a%10+1,(b+low)%10+(a+high)%10,h)
    return (a%10+(a+high)%10,(b+low)%10+(b+u)%10,h)


def critical_clock_check():
    graph={(a,b): sorted(set((aa,bb) for u in (0,1)
                for aa,bb,h in (two_pair_step(a,b,u),)
                if aa==27-a))
           for a in (9,18) for b in range(19)}
    def depth(s,stack=()):
        assert s not in stack, ('unexpected cycle',stack,s)
        return max([0]+[1+depth(t,stack+(s,)) for t in graph[s]])
    depths={s:depth(s) for s in graph}
    assert max(depths.values())==4
    assert depths[9,4]==4
    return depths

if __name__=='__main__':
    depths=critical_clock_check()
    print({'maximum_9_18_alternating_transitions':max(depths.values())})
