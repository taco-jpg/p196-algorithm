#!/usr/bin/env python3
"""Independent ordinary decimal-bigint oracle for compact 9-rail certificates.
Does NOT import reproduce.py or use its carry/centre recurrence. The next
centre is extracted from an actual decimal N+reverse(N) integer each phase.
"""
import json
from pathlib import Path

def canonical_source(P):
    n=len(P)
    digits=[0]*n
    for i in range(n//2):
        digits[i]=max(0,P[i]-9)
        digits[-1-i]=min(9,P[i])
    if n%2:
        assert P[n//2]%2==0
        digits[n//2]=P[n//2]//2
    assert digits[-1]>0
    return int(''.join(map(str,digits[::-1])))

def pairs(N):
    d=[int(x) for x in str(N)[::-1]]
    return [d[i]+d[-1-i] for i in range(len(d))]

def revadd(N):
    return N+int(str(N)[::-1])

def carry_after(word,start):
    c=start
    for x in word:c=(x+c)//10
    return c

def outer_for(a,g):
    for x in range(1,19):
        for y in range(19):
            H=[x,y]
            if carry_after(H,0)==a and carry_after(H[::-1],1-a)==g:
                return H
    raise AssertionError((a,g))

def main():
    data=json.loads(Path(__file__).with_name('cert.json').read_text())
    checks=0
    for cert in data['certificates']:
        core=cert['core']
        H=cert['period']
        assert len(cert['ports'])==H
        assert core==core[::-1]
        C=core[:]
        for t in range(H):
            a=int(cert['ports'][t]);g=int(t%4==0)
            assert carry_after(C,a)==1-a,(cert['name'],t,'port')
            Hword=outer_for(a,g)
            expected_next=None
            for k in (6,9,20,80):
                for extra in (0,3):
                    padded=[9]*extra+C+[9]*extra
                    P=Hword+[9]*k+padded+[9]*k+Hword[::-1]
                    N=canonical_source(P)
                    assert pairs(N)==P
                    M=revadd(N)
                    assert len(str(M))==len(str(N))+g
                    Q=pairs(M)
                    start=len(Hword)+k
                    next_length=len(padded)+g
                    D=Q[start:start+next_length]
                    assert len(D)==next_length and D==D[::-1]
                    assert len(D)%2==0 or D[len(D)//2]%2==0
                    assert all(Q[len(Hword)+i]==9 for i in range(2,k-2))
                    if extra==0:
                        if expected_next is None:expected_next=D
                        else:assert D==expected_next
                    else:
                        assert D==[9]*extra+expected_next+[9]*extra
                    checks+=1
            C=expected_next
        delta=cert['gain_per_side']
        assert H==8*delta
        assert C==[9]*delta+core+[9]*delta,(cert['name'],'closure',C)
    print('ALL CHECKS PASSED: independent literal decimal bigint controls',checks)

if __name__=='__main__':main()
