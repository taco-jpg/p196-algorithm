#!/usr/bin/env python3
"""W25 band-first exact periodic bulk checker, LSB-first pair coefficients.
This checks the bulk ONLY. Cyclic carries need not match any rooted exterior.
"""
def carries(w,b):
    m=len(w)
    for c0 in (0,1):
        c=[c0]
        for x in w:c.append((x+c[-1])//b)
        if c[-1]!=c0:continue
        for hm in (0,1):
            h=[None]*(m+1);h[m]=hm
            for i in range(m-1,-1,-1):h[i]=(w[i]+h[i+1])//b
            if h[0]==hm:yield c[:-1],h

def advance(w,b,g):
    for c,h in carries(w,b):
        lo=[(x+ci)%b for x,ci in zip(w,c)]
        hi=[(x+h[i+1])%b for i,x in enumerate(w)]
        yield tuple(lo[i]+hi[(i-g)%len(w)] for i in range(len(w)))

def test():
    w=(1,1,15,15)
    assert tuple(advance(w,9,1))==((8,2,8,14),) # existing base-9 control
    w=(9,18,9,0)
    rows=[w]
    for t in range(8):
        opts=list(advance(w,10,1 if t%2==0 else 0))
        assert len(opts)==1
        w=opts[0];rows.append(w)
    assert rows==[(9,18,9,0),(10,8,8,10),(1,17,17,1),
                  (2,9,16,9),(6,9,12,9),(16,16,2,2),
                  (13,13,5,5),(9,8,9,10),(9,18,9,0)]
    print("PASS base9 control and decimal p8/m4 bulk cycle, g=10101010")
if __name__=="__main__":test()
