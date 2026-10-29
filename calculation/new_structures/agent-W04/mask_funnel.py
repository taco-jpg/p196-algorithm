#!/usr/bin/env python3
"""W04: exact one-step carry-gauge erasure on the independent 8/16 rectangle.
All-length theorem is derived from arithmetic identities in report. Controls use
entire pairword normalization AND separate ordinary Python bigint reverse/add.
"""
import itertools, random, sys

def h0(mask,n):
    return [10] + [8+9*z for z in mask] + [5,11] + [16]*n + [8]

def h1(m,n):
    return [1,9] + [16]*(m-1) + [13,7,9] + [14]*(n-1) + [15,16]

def whole(h):
    return h+h[::-1]

def fold(p):
    return p[:(len(p)+1)//2]

def coefficient_step(p):
    carry=0; out=[]
    for x in p:
        y=x+carry;out.append(y%10);carry=y//10
    if carry:out.append(carry)
    return out,fold([out[i]+out[-i-1] for i in range(len(out))])

def physical(h):
    low=[];high=[]
    for x in h:
        a=min(x,9); high.append(a);low.append(x-a)
    return int(''.join(map(str,(low+high[::-1])[::-1])))

def oracle(n):
    s=str(n)
    return n+int(s[::-1])

def check_small():
    total=0; independent=0; distinct=0
    for m in range(1,9):
        for n in range(1,7):
            baseline=None; inputs=set(); successors=set()
            for bits in itertools.product((0,1),repeat=m):
                p=whole(h0(bits,n)); norm,answer=coefficient_step(p)
                assert answer==h1(m,n),(m,n,bits,answer)
                N=physical(h0(bits,n))
                assert str(N)[0]!='0'
                assert str(N)!=str(N)[::-1]
                N1=oracle(N);N2=oracle(N1)
                if baseline is None:baseline=(fold([int(str(N1)[i])+int(str(N1)[-i-1]) for i in range(len(str(N1)))]),N2)
                assert int(''.join(map(str,norm[::-1])))==N1
                assert answer==baseline[0]
                assert N2==baseline[1]
                assert str(N1)!=str(N1)[::-1]
                inputs.add(N); successors.add(N1);total+=1
            assert len(inputs)==2**m and len(successors)==2**m
            distinct+=len(inputs)
    bad=h0([0]*6,7);bad[1]=18
    assert coefficient_step(whole(bad))[1]!=h1(6,7)
    print('CORRUPTED_NON_GAUGE_COEFFICIENT_REJECTED')
    print('EXHAUSTIVE_DECIMAL_MASK_FIBRES_PASS total_seeds=',total,'both_distinct=',distinct)

def check_long():
    rng=random.Random(47405);count=0
    for m,n in [(15,17),(50,40),(120,130),(500,450),(1000,1100)]:
        masks=[[0]*m,[1]*m,[i%2 for i in range(m)]]
        masks += [[rng.randrange(2) for i in range(m)] for _ in range(15)]
        common=None
        for z in masks:
            _,p1=coefficient_step(whole(h0(z,n)))
            assert p1==h1(m,n)
            N=physical(h0(z,n));N1=oracle(N);N2=oracle(N1)
            if common is None:common=N2
            assert N2==common
            assert N!=N1 and str(N1)!=str(N1)[::-1]
            count+=1
    print('INDEPENDENT_BIGINT_MASK_CONTROLS_PASS',count)
if __name__=='__main__':
    sys.set_int_max_str_digits(0)
    check_small();check_long()