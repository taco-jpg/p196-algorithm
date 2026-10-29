#!/usr/bin/env python3
"""Independent Python big-integer census of 10..999 under the F32 rule."""
import sys

def raa(n: int) -> int:
    s = str(n)
    return n + int(s[::-1])

def odd_witness(n:int,k:int) -> bool:
    s=str(n)
    m=len(s)//2
    return any(((ord(s[i])-48)+(ord(s[-1-i])-48))%2 for i in range(min(k,m)))

def main():
    horizon=int(sys.argv[1]) if len(sys.argv)>1 else 5000
    survivors=[]
    first_fail={}
    for start in range(10,1000):
        n=start
        for t in range(horizon+1):
            if not odd_witness(n,32):
                first_fail[start]=t
                break
            if t<horizon: n=raa(n)
        else: survivors.append(start)
    assert survivors==[879,978], survivors
    assert raa(879)==raa(978)==1857
    print('PYTHON FULL-INTEGER CENSUS PASS: starts=10..999, horizon=',horizon,
          'survivors=',survivors, 'failures=',len(first_fail),'shared successor=',raa(879))
    for x in (196,295,394,493,592):
        print('control',x,'first_parity_failure',first_fail[x])

if __name__=='__main__':main()
