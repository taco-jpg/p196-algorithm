#!/usr/bin/env python3
"""W27 symbolic 12-edge decimal centre recharge, all q>=2."""
import sys
if hasattr(sys,'set_int_max_str_digits'): sys.set_int_max_str_digits(0)
# (MSB prefix, exponent=2q+offset, MSB suffix)
PHASES=[
 ('2905',0,'8723'),('6184',0,'3815'),('11368',-1,'88631'),
 ('25057',-1,'74942'),('50005',-1,'49994'),('100000',-2,'899999'),
 ('10',2,'8900000'),('1100098',-3,'8899901'),
 ('2200087',-3,'7799912'),('4400065',-3,'5599934'),
 ('8800021',-3,'1199978'),('17599933',-4,'82400066'),
 ('83600362',-4,'16399637'),
]
def symbolic(A,e,B):
    """N and reverse(N) as (a,b) for a*X+b, X=10**(2q-4)."""
    p,r=len(A),len(B)
    N=((int(A)+1)*10**(e+r+4),int(B)-10**r)
    R=((int(B[::-1])+1)*10**(e+p+4),int(A[::-1])-10**p)
    return N,R
for i in range(12):
    (a,b),(c,d)=symbolic(*PHASES[i])
    (u,v),_=symbolic(*PHASES[i+1])
    assert (a+c,b+d)==(u,v),i
print('SYMBOLIC 12 affine identities PASS for EVERY q >= 2')
def form(q,phase):
    A,e,B=phase
    return A+'9'*(2*q+e)+B
for q in (2,3,4,5,40,100,600):
    s=form(q,PHASES[0])
    for i,phase in enumerate(PHASES):
        assert s==form(q,phase),(q,i)
        assert s!=s[::-1],(q,i)
        assert next((k for k in range(len(s)//2)
                     if s[k]!=s[-1-k]),len(s)//2)<=1,(q,i)
        if i<12: s=str(int(s)+int(s[::-1]))
print('PYTHON_BIGINT all 13 phases and 2-site witness PASS')
print('CENTRE q>=2: g0=2q, g5=2q-2, g6=2q+2, g12=2q-4')
