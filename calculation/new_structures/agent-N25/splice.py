#!/usr/bin/env python3
"""Independent ordinary Python integer verification of two-parameter zero splicing.
Reproduce: python3 splice.py (1000 rounds and 100 random local controls).
"""
import random, sys
sys.set_int_max_str_digits(1000000)

def seed(parts,outer,centre):
    return parts[0]+'0'*outer+parts[1]+'0'*centre+parts[2]+'0'*outer+parts[3]

def raa(s):
    return str(int(s)+int(s[::-1]))

def starts(outer,centre):
    return [4,8+outer,12+outer+centre]

def one_case(parts,o,c,ho,hc,steps):
    small=seed(parts,o,c); large=seed(parts,o+ho,c+hc)
    initial_small=len(small); initial_large=len(large)
    for t in range(steps+1):
        ov_small=len(small)-initial_small
        ov_large=len(large)-initial_large
        assert ov_small==ov_large,(t,'overflow',ov_small,ov_large)
        same=large
        for j,extra in ((2,ho),(1,hc),(0,ho)):
            width=(o+ho if j!=1 else c+hc)-2*t+ov_large
            left=starts(o+ho,c+hc)[j]+t
            assert width>=extra+1
            assert same[left:left+width]=='0'*width,(t,j,'zero loss')
            pos=left+width//2
            assert same[pos:pos+extra]=='0'*extra
            same=same[:pos]+same[pos+extra:]
        assert same==small,(t,'splicing fails')
        assert (small==small[::-1])==(large==large[::-1]),(t,'palindrome changed')
        if t<steps:
            small=raa(small)
            large=raa(large)
    return len(small), len(large),ov_small

def main():
    assert raa('196')=='887' and raa('89')=='187' and raa('1001')=='2002'
    packets=('1789','3141','5926','5358')
    print('MAIN',one_case(packets,2101,2107,13,21,1000))
    rng=random.Random(25)
    for trial in range(100):
        pp=[]
        for k in range(4):
            v=rng.randint(1000,9999)
            if k==3:
                while v%10==0:v=rng.randint(1000,9999)
            pp.append(str(v))
        o=rng.randint(30,60); c=rng.randint(30,60)
        ho=rng.randint(1,18); hc=rng.randint(1,18)
        one_case(pp,o,c,ho,hc,10)
    print('RANDOM 100 cases x 11 time points: PASS')
    print('SPLICING EQUIVALENCE: PASS (full decimal integers, no decimal-digit kernel reuse)')
if __name__=='__main__':main()
