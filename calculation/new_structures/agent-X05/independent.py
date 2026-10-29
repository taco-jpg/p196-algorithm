#!/usr/bin/env python3
"""Independent ordinary Python big-int replay against all X05 symbolic pairwords.
No symbolic carry rules are used to advance the actual integer orbit.
"""
import sys,hashlib,json,argparse
from affine_rle import seed, symbolic_step, expand
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)

def normalize_coefficients(p,b=10):
    out=[];carry=0
    for x in p:
        y=x+carry;out.append(y%b);carry=y//b
    if carry:out.append(carry)
    while len(out)>1 and out[-1]==0:out.pop()
    return out

def replay(A=2000,B=2017,steps=2000):
    w=seed(A,B)
    p=expand(w,A,B)
    d=normalize_coefficients(p)
    n=int(''.join(str(x) for x in reversed(d)))
    lengths=[]
    for t in range(steps):
        dd=str(n)
        assert dd!=dd[::-1],('PALINDROME',t)
        d=normalize_coefficients(expand(w,A,B))
        assert dd==''.join(str(x) for x in reversed(d)),('PAIRWORD_MISMATCH',t)
        q,pal,_=symbolic_step(w,10,A,B)
        assert not pal,('SYMBOLIC_PAL',t)
        n+=int(dd[::-1])
        w=q
        if t%100==0:lengths.append([t,len(dd),hashlib.sha256(dd.encode()).hexdigest()[:16]])
    d=normalize_coefficients(expand(w,A,B))
    assert str(n)==''.join(str(x) for x in reversed(d)),('PAIRWORD_FINAL_MISMATCH',steps)
    v={'A':A,'B':B,'steps':steps,'last_digit_length':len(str(n)),
       'all_numeric_replays_and_pairword_matches':True,'sample_hashes':lengths}
    print(json.dumps(v,indent=2))
    return v

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--a',type=int,default=2000)
    ap.add_argument('--b',type=int,default=2017);ap.add_argument('--steps',type=int,default=2000)
    x=ap.parse_args();replay(x.a,x.b,x.steps)
