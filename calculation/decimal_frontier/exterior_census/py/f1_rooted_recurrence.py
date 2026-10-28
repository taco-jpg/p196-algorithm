#!/usr/bin/env python3
"""Exact finite-state integer certificate for base-10 rooted F1 overflow counts.
No full exterior B-cycle or decimal Lychrel claim; standard library only.
Usage: python3 calculation/decimal_frontier/exterior_census/py/f1_rooted_recurrence.py
"""
B=10; m=2*B-2
E=[]
for g in (0,1):
    row=[]
    for x in range(1,m+1):
        mask=0
        for h in (0,1):
            if (x+h)//B!=g:continue
            y=x%B+(1 if g else (x+h)%B)
            if 1<=y<=m:mask|=1<<(y-1)
        row.append(mask)
    E.append(tuple(row))

def mul(r,s):
    out=[]
    for mask in r:
        t=0
        while mask:
            bit=mask&-mask;mask-=bit
            t|=s[bit.bit_length()-1]
        out.append(t)
    return tuple(out)

def closed(r):
    return any((mask>>i)&1 for i,mask in enumerate(r))
I=tuple(1<<i for i in range(m))
index={I:0};states=[I]
for r in states:
    for g in (0,1):
        s=mul(r,E[g])
        if s not in index:index[s]=len(states);states.append(s)
assert len(states)==434
succ=[tuple(index[mul(r,E[g])] for g in (0,1)) for r in states]
F=[int(closed(r)) for r in states]
V=[F]
for _ in range(26):
    v=V[-1]
    V.append([v[a]+v[b] for a,b in succ])
initial=[v[0] for v in V]
# Exact identity q(T)F = 0 for every of the 434 relation states.
# T acts on a vector of state evaluations as (Tv)(r)=v(rE0)+v(rE1).
# q(T)=T^10-T^8-T^7-T^6-T^5-T^3-2T.
for j in range(len(states)):
    assert V[10][j]==V[8][j]+V[7][j]+V[6][j]+V[5][j]+V[3][j]+2*V[1][j]
for k in range(10,27):
    assert initial[k]==initial[k-2]+initial[k-3]+initial[k-4]+initial[k-5]+initial[k-7]+2*initial[k-9]

def determinant(A):
    # Exact fraction-free Bareiss determinant for the 10x10 Hankel lower bound.
    A=[row[:] for row in A];n=len(A);prev=1;sgn=1
    for k in range(n-1):
        if A[k][k]==0:
            swap=next((i for i in range(k+1,n) if A[i][k]),None)
            if swap is None:return 0
            A[k],A[swap]=A[swap],A[k];sgn=-sgn
        pivot=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numer=A[i][j]*pivot-A[i][k]*A[k][j]
                assert numer%prev==0
                A[i][j]=numer//prev
            A[i][k]=0
        prev=pivot
    return sgn*A[-1][-1]
det=determinant([[initial[i+j] for i in range(10)] for j in range(10)])
assert det==-17378887139328
print('relation states',len(states),'first 10 rooted counts',initial[:10])
print('Hankel determinant',det)
print('recurrence: a(n)=a(n-2)+a(n-3)+a(n-4)+a(n-5)+a(n-7)+2a(n-9), n>=10')
print('GF (1+z^2+2z^3+3z^4+4z^5+6z^7+16z^9)/(1-z^2-z^3-z^4-z^5-z^7-2z^9)')
