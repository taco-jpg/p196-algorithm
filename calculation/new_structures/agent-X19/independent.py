#!/usr/bin/env python3
"""Independent Python bigint + base100 insertion oracle for X19 commuting square.
No calls to the C++ implementation, no coordinate sharing, no digit-vector stepping.
"""
import sys
sys.set_int_max_str_digits(0)

def seed(q,r):
    return int('12'+'99'*q+'34'+'99'*r+'56'+'99'*q+'78')

def norm_step(n):
    return n+int(str(n)[::-1])

def coefficients(n):
    a=[int(x) for x in str(n)[::-1]]
    return [a[i]+a[len(a)-1-i] for i in range(len(a))]

def insertions(a,b,insert_count,letter):
    if len(b)!=len(a)+insert_count:return False
    reachable={(0,0)}
    for i,symbol in enumerate(b):
        nxt=set()
        for j,k in reachable:
            if k<insert_count and symbol==letter: nxt.add((j,k+1))
            if j<len(a) and symbol==a[j]: nxt.add((j+1,k))
        reachable=nxt
    return (len(a),insert_count) in reachable

def blocks(n):
    s=str(n)[::-1]
    return [int(s[i:i+2][::-1]) for i in range(0,len(s),2)]

def replay(q,r,steps):
    ns=[seed(q,r),seed(q+1,r),seed(q,r+1),seed(q+1,r+1)]
    minodd=10**9
    pair_square_step=-1
    for t in range(steps+1):
        ss=[str(n) for n in ns]
        assert all(s!=s[::-1] for s in ss), ('pal',t)
        aa=list(map(blocks,ns))
        for i,j,count in [(0,1,2),(2,3,2),(0,2,1),(1,3,1)]:
            assert insertions(aa[i],aa[j],count,99), ('digit insertion',t,i,j)
        cc=list(map(coefficients,ns))
        for c in cc:minodd=min(minodd,sum(v&1 for v in c))
        # Optional stronger test: insertions of 18 in the symmetric pair coefficient word.
        if pair_square_step<0 and not all(insertions(cc[i],cc[j],2*count,18) for i,j,count in [(0,1,2),(2,3,2),(0,2,1),(1,3,1)]):
            pair_square_step=t
        if t<steps:ns=list(map(norm_step,ns))
    return {'Q':q,'R':r,'steps':steps,'pairword_18_insertion_break':pair_square_step,'min_odd_coefficients':minodd,'base_digits_final':len(str(ns[0]))}

def mutation():
    x=blocks(seed(7,11));y=blocks(seed(8,11));assert insertions(x,y,2,99)
    y[-3]=(y[-3]+1)%100
    assert not insertions(x,y,2,99)

if __name__=='__main__':
    mutation()
    for q,r,t in [(5,5,13),(10,20,25),(20,20,50),(100,100,300)]:
        print(replay(q,r,t))
