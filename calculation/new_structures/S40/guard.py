#!/usr/bin/env python3
"""Universal conditional p12/m9 decimal nonpalindrome guard.

For canonical source n, P(n)[i]=d_i+d_(L-1-i) is the symmetric
uncarried pairword. Its normalization is exactly n+reverse10(n).
The unknown centre-to-high carry is exhausted by the two cases 0/1.
"""
from random import Random

B0=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W0=(5,18,4,8,1,15,4,0,5)
A=B0+7*W0+W0[:2]  # 99 rooted coefficients
CLOCK=tuple(map(int,"100010001000"))
PHASES=(
 (10,4,6,6,7),(1,5,10,12,13),(2,11,1,6,8),
 (5,2,3,12,16),(10,4,7,5,13),(1,5,11,12,9),
 (2,11,3,6,0),(5,2,7,12,0),(10,4,15,4,1),
 (1,5,10,10,5),(2,11,1,1,11),(5,2,3,3,3))

def guard_next(a):
    """For any n with L>=2len(a) and P(n) prefix a, prove next prefix."""
    m=len(a)
    assert m>=2 and all(0<=v<=18 for v in a)
    low=[]
    carry=0
    for v in a:
        low.append((v+carry)%10)
        carry=(v+carry)//10
    paths=[]
    for incoming in (0,1):
        carry=incoming
        high=[]
        for v in reversed(a):
            high.append((v+carry)%10)
            carry=(v+carry)//10
        gamma=carry
        if gamma:
            new=(low[0]+1,)+tuple(low[i]+high[m-i] for i in range(1,m))
        else:
            new=tuple(low[i]+high[m-1-i] for i in range(m))
        paths.append((gamma,new))
    assert paths[0][0]==paths[1][0], "overflow depends on interior"
    b0,b1=paths[0][1],paths[1][1]
    common=0
    while common<m and b0[common]==b1[common]:
        common+=1
    return b0[:common],paths[0][0]

def universal_guard():
    """Finite two-port check, universal over every allowed middle."""
    a=A
    assert len(a)==99
    trace=[]
    gamma_bits=[]
    for t in range(121):
        assert len(a)>=5,(t,len(a))
        assert a[:5]==PHASES[t%12],(t,a[:5])
        odd=next((i for i,v in enumerate(a[:5]) if v%2),None)
        assert odd is not None,(t,a[:5])
        trace.append((t,len(a),odd,a[:5]))
        if t<120:
            a,gamma=guard_next(a)
            assert gamma==CLOCK[t%12],(t,gamma)
            gamma_bits.append(gamma)
    assert sum(gamma_bits)==30 and trace[-1][1]==5
    return trace,gamma_bits

def step_digits(d):
    """Separate schoolbook LSD-first reverse-and-add engine."""
    c=0
    out=[]
    for i in range(len(d)):
        total=d[i]+d[-1-i]+c
        out.append(total%10)
        c=total//10
    if c:out.append(c)
    return out

def pairs(d):
    return tuple(x+y for x,y in zip(d,reversed(d)))

def realize(p):
    assert p==p[::-1] and all(0<=v<=18 for v in p)
    length=len(p)
    d=[0]*length
    for i in range(length//2):
        d[i]=min(p[i],9)
        d[-1-i]=p[i]-d[i]
    if length%2:
        assert p[length//2]%2==0
        d[length//2]=p[length//2]//2
    assert d[-1]>0
    return int(''.join(map(str,d[::-1])))

def controls():
    """Physical controls only, not used to prove universal quantifiers."""
    rng=Random(40)
    checked=0
    for length in range(4,11):
        for _ in range(300):
            d=[rng.randrange(10) for _ in range(length)]
            d[-1]=rng.randrange(1,10)
            a=pairs(d)[:length//2]
            try:
                b,g=guard_next(a)
            except AssertionError:
                continue
            e=step_digits(d)
            assert len(e)==length+g
            assert pairs(e)[:len(b)]==b
            checked+=1
    assert checked>=1000
    trace,_=universal_guard()
    tested=((8,20),(20,20),(21,41),(40,40),(80,80),(160,160))
    for q,k in tested:
        h=B0+q*W0+(8,)+k*(9,2,16)
        n=realize(h+(12,)+h[::-1])
        d=list(map(int,str(n)[::-1]))
        for t in range(121):
            assert int(''.join(map(str,d[::-1])))==n
            assert pairs(d)[:5]==trace[t][3]
            assert pairs(d)[trace[t][2]]%2==1
            assert d!=d[::-1]
            if t<120:
                n+=int(str(n)[::-1])
                d=step_digits(d)
    return checked,tested

if __name__=="__main__":
    trace,bits=universal_guard()
    checked,tested=controls()
    a=A[:98]
    for _ in range(120):
        a,_=guard_next(a)
    assert a==(10,4,6)  # checker limitation, NOT a palindrome
    print("PAPER PROOF: all n with L>=198 and P(n)[:99]=A")
    print("121 source witnesses; first/last known widths:",trace[0][1],trace[-1][1])
    print("phase odd indices:",[x[2] for x in trace[:12]])
    print("physical overflows:",sum(bits), "of",len(bits))
    print("one-step controls:",checked,"q,k controls:",tested)
    print("CONDITIONAL ONLY: no seam renewal or decimal Lychrel established")
