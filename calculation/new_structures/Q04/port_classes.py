#!/usr/bin/env python3
"""Only independent-coordinate SPATIAL carry maps; not temporal centres."""
from itertools import product

def port_map(a,b):
    def f(s,c):return c if s=="I" else int(s)
    return tuple(2*f(a,i//2)+f(b,i%2) for i in range(4))

def masks(F,equality=False):
    result=[]
    for mask in range(1,16):
        S={i for i in range(4) if mask&(1<<i)}
        image={F[i] for i in S}
        if (image==S if equality else image<=S):result.append(mask)
    return result

def main():
    modes={a+b:port_map(a,b) for a,b in product("I01",repeat=2)}
    assert len(modes)==9
    for p in range(1,31):
        for F in modes.values():
            y=tuple(range(4))
            for f in [F]+[modes["II"]]*(p-1):
                y=tuple(f[y[i]] for i in range(4))
            assert y==F
    for k,F in sorted(modes.items()):
        f=masks(F);e=masks(F,True)
        assert len(f)==(15 if k=="II" else 8)
        assert len(e)==(15 if k=="II" else 3 if k.count("I")==1 else 1)
        print(k,F,"forward closed:",*[format(s,"x") for s in f],
              "equal return:",*[format(s,"x") for s in e])
    print("PASS complete abstract two-coordinate spatial clock p=1..30.")
    print("NOT a classification of physical temporal centre-return maps.")

if __name__=="__main__":main()
