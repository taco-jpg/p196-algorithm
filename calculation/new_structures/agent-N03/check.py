#!/usr/bin/env python3
"""Independent decimal carry and genuine-integer checks of branching morphic bulk.
No reliance on the automaton's state encoding or transition generator.
"""
import sys
from pathlib import Path

DIG = '0123456789ABCDEFGHI'

def parse(path):
    rows = {}
    for line in Path(path).read_text().splitlines():
        t = line.split()
        if t and t[0] in ('ROOTPATH', 'LOOPA', 'LOOPB'):
            rows[t[0]] = [[DIG.index(d) for d in col] for col in t[2:]]
            assert len(rows[t[0]]) == int(t[1][2:])
    assert set(rows) == {'ROOTPATH','LOOPA','LOOPB'}
    assert len(rows['ROOTPATH']) == 27 and len(rows['LOOPA']) == 119 and len(rows['LOOPB']) == 48
    assert rows['LOOPA'] != rows['LOOPB']
    return rows

def fib(n):
    w='A'
    while len(w)<n: w=''.join('AB' if c=='A' else 'A' for c in w)
    return w[:n]

def thue(n):
    return ''.join('AB'[i.bit_count()%2] for i in range(n))

def columns(rows, word):
    return rows['ROOTPATH']+sum((rows['LOOP'+c] for c in word),[])

def test_bulk(cols, name):
    K=len(cols)
    assert K>90
    x=[[cols[k][t] for k in range(K)] for t in range(8)]
    g=[1,0,1,0,1,0,1,0]
    for t in range(8):
        lower=[0]*(K+1)
        for k in range(K): lower[k+1]=(x[t][k]+lower[k])//10
        assert lower[K] in (0,1)
        upper=[0]*(K+1)
        for k in range(K-1,-1,-1): upper[k]=(x[t][k]+upper[k+1])//10
        for k in range(K-64):
            dl=(x[t][k]+lower[k])%10
            dr=1 if (g[t] and k==0) else (x[t][k-1]+upper[k])%10 if g[t] else (x[t][k]+upper[k+1])%10
            expected=dl+dr
            actual=x[(t+1)%8][k]
            if expected!=actual:
                raise AssertionError((name,t,k,x[t][k],expected,actual))
        assert upper[0]==g[t], (name,t,'overflow',upper[0],g[t])
    print('BULK-PASS',name,'columns',K,'8 phases, validated cells',K-64)

def integer_control(cols,name,steps=32):
    x0=[v[0] for v in cols]
    lo=[u//2 for u in x0]
    hi=[u-u//2 for u in reversed(x0)]
    digits=lo+hi
    assert digits[-1]>0 and digits!=digits[::-1]
    n0=len(digits)
    for t in range(steps):
        assert digits!=digits[::-1],(name,t,'palindrome')
        K=min(len(cols)-64, len(digits)//2)
        for k in range(K):
            if digits[k]+digits[-1-k]!=cols[k][t%8]:
                raise AssertionError((name,t,k,'real-integer pairing',digits[k]+digits[-1-k],cols[k][t%8]))
        carry=0; out=[]
        for k in range(len(digits)):
            y=digits[k]+digits[-1-k]+carry
            out.append(y%10); carry=y//10
        if carry:out.append(carry)
        digits=out
    print('INTEGER-PASS',name,'steps',steps,'n0',n0,'final_n',len(digits),'checked initial pair-word cells through',K)

if __name__=='__main__':
    data=parse(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name('witness.txt'))
    controls={'A': 'A'*4, 'B':'B'*4, 'ABBA':'ABBA', 'Fibonacci':fib(64), 'Thue-Morse':thue(64), 'Fibonacci uniform macro':''.join('AB' if c=='A' else 'BA' for c in fib(64)), 'Thue-Morse uniform macro':''.join('AB' if c=='A' else 'BA' for c in thue(64))}
    for name,word in controls.items():
        cols=columns(data,word)
        test_bulk(cols,name)
        integer_control(cols,name,min(32,len(cols)//2))
    print('ALL INDEPENDENT CHECKS PASSED')
