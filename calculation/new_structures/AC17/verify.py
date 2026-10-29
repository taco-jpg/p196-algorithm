#!/usr/bin/env python3
"""Independent ordinary-decimal bigint and schoolbook replay for AC17."""
import random
import sys
sys.set_int_max_str_digits(0)
B=[10,4,15,4,1,7,9,11,11,18,0,18,6,9,17,4,0,12,0,2,10,1,12,4,2,15,0,13,4,8,4,8,10,15]
W=[4,0,5,5,18,4,8,1,15]
def U_rank(rank):
    a=2*(rank//3)
    x=[9,a,18-a]
    r=rank%3
    return x[r:]+x[:r]
def template(q,k,J,U,C):
    h=B+W*q+J+U*k
    return h+C+h[::-1]
def realize(P):
    D=[0]*len(P)
    for i in range(len(P)//2):
        D[i]=min(9,P[i])
        D[-1-i]=P[i]-D[i]
        assert 0<=D[-1-i]<=9
    if len(P)%2:
        assert P[len(P)//2]%2==0
        D[len(P)//2]=P[len(P)//2]//2
    assert D[-1]>0 and D[0]>=0
    return int(''.join(map(str,D[::-1])))
def pair(D):
    return [D[i]+D[-1-i] for i in range(len(D))]
def digit_step(D):
    P=pair(D); O=[]; carry=0
    for z in P:
        z+=carry
        O.append(z%10)
        carry=z//10
    if carry: O.append(carry)
    return O,carry
def first_mismatch(A,B):
    return next((i for i,(a,b) in enumerate(zip(A,B)) if a!=b),None)
def run(q,k,J,U,C):
    P=template(q,k,J,U,C)
    N=realize(P)
    D=[int(x) for x in str(N)[::-1]]
    assert pair(D)==P
    g=[]; nonpal=0
    for t in range(120):
        assert pair(D)==P, (q,k,t,'pair source')
        nonpal += (D!=D[::-1])
        D_next,gamma=digit_step(D)
        N=N+int(str(N)[::-1])
        D_bigint=[int(x) for x in str(N)[::-1]]
        assert D_next==D_bigint,(q,k,J,U,C,t,'independent bigint/digits')
        P=pair(D_bigint)
        g.append(gamma)
        D=D_bigint
    assert ''.join(map(str,g))=='1000'*30
    assert nonpal==120
    expected=template(q,k+5,J,U,C)
    assert len(expected)==len(P)
    mismatch=first_mismatch(P,expected)
    assert mismatch is not None and mismatch<34+9*q, (q,k,J,U,C,mismatch)
    assert sum(g)==30
    return mismatch,P[mismatch],expected[mismatch]
def main():
    rng=random.Random(91728)
    controls=[]
    for rank in [0,3,8,11,16,19,24,29]:
        jlen=3 if rank%2==0 else 4
        J=[rng.randrange(19) for _ in range(jlen)]
        C=[4,4] if rank%2==0 else [4,14,4]
        controls.append((rank,J,C))
    widths=[(14,100),(20,100),(40,160),(80,320),(160,640)]
    for rank,J,C in controls:
        U=U_rank(rank)
        for q,k in widths:
            at,got,want=run(q,k,J,U,C)
            print('INDEPENDENT_BIGINT',f'rank={rank}',f'q={q}',f'k={k}',f'J={J}',f'C={C}',f'first={at}',f'got={got}',f'want={want}')
    print(f'AC17_BIGINT_AND_SCHOOLBOOK_PASS controls={len(controls)*len(widths)} transitions={120*len(controls)*len(widths)}')
if __name__=='__main__':main()
