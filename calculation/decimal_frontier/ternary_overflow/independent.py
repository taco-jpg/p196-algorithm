#!/usr/bin/env python3
"""Independent checker for Agent13TernaryOverflowObstruction.

Does not import proof.py. Generates substitution prefixes directly, computes
ordinary reverse-and-add using Python big integers and direct divmod, and
validates published b9/b13 periodic controls via independent arithmetic.
"""
import random
MU={'0':'01','1':'02','2':'00'}

B9=[8, 9, 10, 13, 14, 12, 3, 14, 10, 0, 11, 7, 10, 9, 7, 8, 8, 14, 15, 2, 9, 7, 0, 5, 8, 3, 8, 11, 8, 6, 8, 7, 5, 14, 11, 3, 9, 3, 8, 14, 7, 12, 8, 2, 0, 12, 1, 5, 13, 8, 1, 16, 15, 9, 1, 7, 6, 2, 1, 15, 15]
B13A=[19, 9, 8, 19, 13, 19, 11, 9, 14, 1, 23, 12, 7, 21, 3, 10, 12, 0, 1, 17, 0, 1, 10, 16, 9, 2, 5, 23, 14, 14, 1, 11, 22, 9, 12, 11, 18, 4, 19, 19, 19, 21, 21, 23, 19, 1, 17, 4, 21, 17, 3, 22, 24, 23, 17, 19, 12, 1, 14, 6, 3, 16, 15, 9, 16, 1, 23, 12, 20, 23, 6, 12, 16, 16, 16]
B13B=[19, 9, 8, 19, 13, 6, 16, 11, 11, 10, 23, 13, 2, 15, 12, 13, 6, 20, 5, 5, 5, 3, 3, 1, 5, 23, 7, 20, 3, 7, 21, 2, 0, 1, 7, 5, 12, 23, 10, 18, 21, 8, 9, 15, 8, 23, 1, 12, 4, 1, 18, 12, 8, 8, 8]

def fixed_word(depth):
    w='0'
    for _ in range(depth):w=''.join(MU[c] for c in w)
    return w

def factors_direct(n):
    w=fixed_word(16)
    return {w[j:j+n] for j in range(len(w)-n+1)}

def norm_direct(b,p):
    c=0; out=[]
    for x in p:
        value=x+c
        c,d=divmod(value,b)
        out.append(d)
    if c:out.append(c)
    return out

def to_int(b,p):
    n=0
    for v in p[::-1]:n=n*b+v
    return n

def to_digits(b,n):
    out=[]
    while n:
        n,d=divmod(n,b)
        out.append(d)
    return out

def published_controls():
    # These are reproductions of known results, not novel results.
    for b,B,W,C,g in (
        (9,B9,[1,1,15,15],[1,1],'1100011000'),
        (13,B13A,[16],[16],'1010010000'),
        (13,B13B,[8],[8],'1010010000')):
        assert len(B) in (61,75,55)
        p=B+W*3+C+W[::-1]*3+B[::-1]
        s='';n=to_int(b,p)
        for k in range(30):
            dig=to_digits(b,n)
            assert dig !=dig[::-1]
            s+=str(len(dig)-len(p))
            p=[x+y for x,y in zip(dig,dig[::-1])]
            n+=to_int(b,dig[::-1])
            assert n==to_int(b,p)
        assert s==g*3,(b,s)
        print('CONTROL PASS: base',b,'B',len(B),'overflow',s[:10])
        # Continue plain integer reverse-add without relying on pair templating.
        for k in range(470):
            d=to_digits(b,n)
            assert d!=d[::-1]
            n+=to_int(b,d[::-1])

def letter_local_test(samples=2500):
    rng=random.Random(130474)
    w=fixed_word(15)
    for k in range(samples):
        b=rng.randrange(2,30)
        pool=[v for v in range(2*b-1) if v!=b-1]
        if len(pool)<3:continue
        a=rng.sample(pool,3)
        j=rng.randrange(len(w)-125)
        source=w[j:j+120]
        L=[a[ord(t)-48] for t in source]
        gamma=k%2
        B=[2*b-2 if gamma else 1]+[rng.randrange(2*b-1) for _ in range(rng.randrange(1,5))]
        p=B+L+L[::-1]+B[::-1]
        digits=norm_direct(b,p)
        assert len(digits)-len(p)==gamma
        ref=to_digits(b,to_int(b,p))
        assert digits==ref
        pairs=[ref[i]+ref[len(ref)-1-i] for i in range(len(ref))]
        hi=[int(x>=b) for x in a]
        lo=[x%b for x in a]
        x=[ord(t)-48 for t in source]
        if gamma:
            expected=[lo[x[i]]+lo[x[i-1]]+hi[x[i]]+hi[x[i-1]] for i in range(1,119)]
        else:
            expected=[2*lo[x[i]]+hi[x[i-1]]+hi[x[i+1]] for i in range(1,119)]
        assert pairs[len(B)+1:len(B)+119]==expected,(k,b,a,gamma)
        assert to_int(b,p)+to_int(b,ref[::-1])==to_int(b,pairs)
    return samples

def equality_pattern(word):
    map={};result=[]
    for x in word:
        if x not in map:map[x]=len(map)
        result.append(map[x])
    return tuple(result)

def independent_symbolic():
    from itertools import product
    F8=factors_direct(8);F6=factors_direct(6)
    assert len(F8)==20 and len(F6)==16
    patterns={equality_pattern(z) for z in F6}
    count=0
    # All assignments of pair types 00,01/10,02/20 to <=3 output symbols.
    # This covers all collisions without assuming any numeric base.
    for assignment in product(range(3),repeat=3):
        for src in F8:
            seq=[]
            for i in range(1,7):
                p=src[i-1:i+1]
                assert p in ('00','01','10','02','20')
                typ=0 if p=='00' else (1 if '1' in p else 2)
                seq.append(assignment[typ])
            assert equality_pattern(seq) not in patterns,(src,assignment)
            count+=1
    print('INDEPENDENT FINITE CHECK PASS:',count,'raw maps, no compatible L6 factors')

if __name__=='__main__':
    independent_symbolic()
    published_controls()
    print('INDEPENDENT ARITHMETIC CHECK PASS:',letter_local_test())
