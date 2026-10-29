#!/usr/bin/env python3
"""Arithmetic controls for the X05 affine-RLE engine, including an external base-9 orbit."""
import random,json,sys
from affine_rle import L,cat,symbolic_step,expand,ordinary_step,coeff_digits
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)

def test_random():
    r=random.Random(57829);total=0
    for b in [3,7,9,10,13,16]:
        for j in range(180):
            half=[r.randrange(2*b-1) for i in range(r.randrange(1,21))]
            half[0]=r.randrange(1,2*b-1)
            p=half+(r.choice([[],[r.randrange(2*b-1)]]))+list(reversed(half))
            w=cat([(v,L(1)) for v in p],1,1)
            nw,pal,d=symbolic_step(w,b,1,1)
            od=ordinary_step(p,b)[1]
            assert expand(nw,1,1)==ordinary_step(p,b)[0]
            assert expand(d,1,1)==od
            assert pal==(od==od[::-1]);total+=1
    return total

def control9():
    # Base-9 known 10-edge lattice certificate seed from cert_b9_rec0.json.
    seed='4557762750645544478154034246434437625247464106137418851431188107701330478046206014637414157234345414203417744345350571676544'
    n=int(seed,9)
    for t in range(300):
        digits=[];m=n
        while m:digits.append(m%9);m//=9
        assert digits!=digits[::-1],t
        rev=0
        for d in digits:rev=rev*9+d
        n+=rev
    return {'base':9,'steps':300,'initial_digits':len(seed),'palindrome_encountered':False}

if __name__=='__main__':
    print(json.dumps({'random_exact_one_step':test_random(),'known_base9_control':control9()},indent=2))
