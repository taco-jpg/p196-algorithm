#!/usr/bin/env python3
"""Finite toroidal hint: arithmetic mod 10^k-1, NOT ordinary decimal RAA."""
from collections import Counter

def rev(x,k):
    v=0
    for _ in range(k):
        v=10*v+x%10
        x//=10
    return v

def cycles(k):
    modulus=10**k-1
    visited=set();nonpal=[];counts=Counter()
    for start in range(modulus):
        if start in visited:continue
        path=[];index={};x=start
        while x not in visited and x not in index:
            index[x]=len(path);path.append(x)
            x=(x+rev(x,k))%modulus
        if x in index:
            c=path[index[x]:]
            pal=any(v==rev(v,k) for v in c)
            counts[(len(c),pal)]+=1
            if not pal:nonpal.append(c)
        visited.update(path)
    return counts,nonpal
if __name__=='__main__':
    c,f=cycles(4)
    print('modulus=9999; cycle_counts=',sorted(c.items()))
    print('cycles_without_4digit_palindromes=',f)
    assert f==[[5346,1782,4653,8217]],f
    print('PASS: unique nonpalindromic 4-digit cycle, not a decimal certificate')
