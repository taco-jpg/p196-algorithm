#!/usr/bin/env python3
"""X01 independent arbitrary-precision decimal reverse-and-add oracle.
No symbolic template transition is used."""
import argparse
import sys
sys.set_int_max_str_digits(0)
def central_run(word):
    n=len(word);i=(n-1)//2;j=n//2
    while i>=0 and j<n and word[i]==word[j]=='9':
        i-=1;j+=1
    return j-i-1,i+1
def checksum(word):
    h=0
    for c in word:h=(h*131+ord(c))%1000000007
    return h
def main():
    p=argparse.ArgumentParser()
    p.add_argument('high');p.add_argument('low')
    p.add_argument('q',type=int);p.add_argument('steps',type=int)
    a=p.parse_args()
    assert len(a.high)==len(a.low) and a.high[0]!='0'
    v=int(a.high+'99'*a.q+a.low)
    prevL=None;prevN=None;gam=0;pathhash=0
    cpoints={0,1,2,3,4,5,6,7,8,88,100,300,1000,5000,10000,20000,50000,100000,a.steps}
    for t in range(a.steps+1):
        s=str(v);n=len(s)
        if s==s[::-1]:raise AssertionError(('palindrome',t))
        L,awidth=central_run(s)
        if L<2 or n-L!=2*awidth or awidth==0:
            raise AssertionError(('no centre-run',t,L,awidth,n))
        if prevL is not None:
            gamma=n-prevN
            if gamma not in (0,1):raise AssertionError(('length-growth',t,gamma))
            gam+=gamma
            if L!=prevL-gamma:
                raise AssertionError(('lock failure',t,prevL,L,gamma))
        pathhash=(pathhash*1000003+(L%1000000007)*17+awidth*101+t)%1000000007
        if t in cpoints:
            print(f'STATE t={t} L={L} width={awidth} n={n} checksum={checksum(s)} g1={gam} trim={t-gam} badlock=0',flush=True)
        if t==a.steps:break
        prevL,prevN=L,n
        v+=int(s[::-1])
    print(f'ORACLE PASS high={a.high} low={a.low} Q={a.q} T={a.steps} gamma1={gam} finalL={L} final_digits={len(s)} pathhash={pathhash}',flush=True)
if __name__=='__main__':main()
