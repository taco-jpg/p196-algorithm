from itertools import product
BASES=(2,4,8,10,11,17,26)
def alt(xs):
    return sum(x if i%2==0 else -x for i,x in enumerate(xs))
def norm(b,C,e):
    out=[];carry=e
    for x in C:
        z=x+carry;out.append(z%b);carry=z//b
    return out,carry
def candidates(b,m):
    for h in product(range(2*b-1),repeat=(m+1)//2):
        yield list(h)+list(reversed(h[:m//2]))
def next_raw(b,C,e,g):
    d,out=norm(b,C,e)
    assert out==1-e
    if g:
        y=(b-1)*e
        return [a+c for a,c in zip(d+[y],[y]+d[::-1])]
    return [a+c for a,c in zip(d,d[::-1])]
def trims(b,raw):
    v=0
    while raw:
        yield v,raw
        if len(raw)<3 or raw[0]!=b-1 or raw[-1]!=b-1:break
        raw=raw[1:-1];v+=1
for b in BASES:
    total=odd=0
    for m in range(1,5):
        for C in candidates(b,m):
            for e in (0,1):
                if norm(b,C,e)[1]!=1-e:continue
                for g in (0,1):
                    for v,T in trims(b,next_raw(b,C,e,g)):
                        total+=1
                        if len(T)%2==0:continue
                        odd+=1
                        assert T[len(T)//2]%2==0
                        if (m%2==0 and g==1) or (m%2==1 and g==0 and (alt(C)-(b-1))%(b+1)==0):
                            assert (alt(T)-(b-1))%(b+1)==0
    print('base',b,'checked_edges',total,'odd_outputs',odd,'PASS')
