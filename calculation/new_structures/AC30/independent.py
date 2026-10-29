#!/usr/bin/env python3
"""Completely separate unbounded Python integer reverse-and-add for phase9 controls."""
import sys, pathlib
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)

def read(path, phase=9):
    lines=[list(map(int, l.split())) for l in pathlib.Path(path).read_text().splitlines()]
    assert lines[0]==[12,34,9,10]
    return lines[26+phase],lines[2+phase]

def ulist():
    return [([9,a,18-a][i:]+[9,a,18-a][:i]) for a in range(0,19,2) for i in range(3)]

def templ(B,W,J,U,C,q,k):
    h=B+W*q+J+U*k
    return h+C+h[::-1]

def realize(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(d)//2):
        d[i]=max(p[i]-9,0)
        d[-1-i]=min(p[i],9)
    if len(d)%2:
        assert p[len(d)//2]%2==0
        d[len(d)//2]=p[len(d)//2]//2
    assert d[-1]>0
    return int(''.join(map(str,d[::-1])))

def check(B,W,J,U,C,q,k):
    p=templ(B,W,J,U,C,q,k)
    expected=templ(B,W,J,U,C,q,k+5)
    n=realize(p)
    gamma=[]
    for _ in range(120):
        s=str(n)
        n2=n+int(s[::-1])
        gamma.append(len(str(n2))-len(s))
        n=n2
    s=str(n)
    observed=[int(a)+int(b) for a,b in zip(s[::-1],s)]
    first=next((i for i,(a,b) in enumerate(zip(observed,expected)) if a!=b), min(len(observed),len(expected)))
    if first==len(observed)==len(expected):first=None
    return dict(q=q,k=k,first=first,length=len(s),expected=len(expected),gamma=''.join(map(str,gamma)),return_=observed==expected)

if __name__=='__main__':
    B,W=read(sys.argv[1]);J=[int(x) for x in sys.argv[2].split(',')]
    U=[int(x) for x in sys.argv[3].split(',')]
    C=[int(x) for x in sys.argv[4].split(',')]
    for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:print(check(B,W,J,U,C,q,k))
