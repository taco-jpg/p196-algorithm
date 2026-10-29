#!/usr/bin/env python3
"""Independent digit/integer checker: generates long fixed-word prefix, runs
all neutral-containing injective coefficient tables in ordinary base-10
integer arithmetic (no calls to neutral_proof.py or its factor recursion).
"""
from itertools import permutations
MU={'0':'01','1':'02','2':'00'}

def forward_word():
    w='0'
    for _ in range(16): w=''.join(MU[c] for c in w)
    return w

def to_integer(digits):
    z=0
    for d in digits[::-1]:z=z*10+d
    return z

def digits(x):
    ds=[]
    while x>0:
        x,d=divmod(x,10);ds.append(d)
    return ds

def equality(word):
    d={};return_values=[]
    for v in word:
        if v not in d:d[v]=len(d)
        return_values.append(d[v])
    return tuple(return_values)

def test():
    w=forward_word()
    F16={w[i:i+16] for i in range(len(w)-15)}
    F6={w[i:i+6] for i in range(len(w)-5)}
    F4={w[i:i+4] for i in range(len(w)-3)}
    assert len(F16)==40 and len(F6)==16 and len(F4)==10
    targets={equality(t) for t in F6}
    count=0
    for a in permutations(range(19),3):
        if 9 not in a:continue
        for s in F16:
            c=[a[ord(t)-48] for t in s]
            P=[18]+c+c[::-1]+[18]
            N=to_integer(P)
            D=digits(N)
            assert len(D)==len(P)+1
            N2=N+to_integer(D[::-1]);D2=digits(N2)
            # Pair word of the NEXT number's predecessor: reverse-add digits.
            pair=[D[i]+D[-1-i] for i in range(len(D))]
            assert N2==to_integer(pair)
            six=pair[1+5:1+11]
            assert len(six)==6
            assert equality(six) not in targets, (a,s,six)
            count+=1
    assert count==36720
    return count

if __name__=='__main__':
    print('INDEPENDENT BIG-INT PASS:',test(),'source/table cases; zero compatible target factors')
