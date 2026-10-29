#!/usr/bin/env python3
"""X16 all-width forced-carry reset. Exact algebra plus numerical regressions.
python3 calculation/new_structures/agent-X16/forced_reset.py
"""
from carry_ribbon import tm,seed,pairs,norm,direct
def check(k):
    d0=seed(17,14,k);n=len(d0);h=n//2
    p0=pairs(d0);d1,c0=norm(p0);p1=pairs(d1)
    assert c0==[0]+[1]*n
    assert p1[0]==8 and p1[1]==13
    assert all(10<=x<=16 for x in p1[1:n])
    for i in range(1,h):
        assert p1[i]==16-3*(tm(i)+tm(i-1))
    assert p1[h]==16-6*tm(h-1)
    d2,c1=norm(p1);p2=pairs(d2)
    assert c1==[0,0]+[1]*(n-1)+[0]
    assert p2[0]==17 and p2[1]==7
    assert all(p2[i] in (2,8,14) for i in range(2,n-1))
    for i in range(2,n-1):
        assert p2[i]==2*(p1[i]-9)
    d3,c2=norm(p2);p3=pairs(d3)
    expected=[0,1,0]+[int(p2[i]==14) for i in range(2,n-1)]+[0,1]
    assert c2==expected
    assert [len(d1)-n,len(d2)-len(d1),len(d3)-len(d2)]==[1,0,1]
    assert p3[0]==8 and p3[1]==15 and p3[2]==9
    assert p3.count(9)==2
    assert all(any(x&1 for x in p) for p in (p0,p1,p2,p3))
    assert d1==direct(d0) and d2==direct(d1) and d3==direct(d2)
    return {'k':k,'input_digits':n,'digits_after_three':len(d3),
            'carry_ones_t2':sum(c2),'neutral_port_indices_t3':[2,n-1]}
if __name__=='__main__':
    samples=[]
    for k in range(3001):
        a=check(k)
        if k in (0,1,2,7,31,63,127,511,1023,2047,3000):
            print(a);samples.append(a)
    print('ALL_WIDTH_REGRESSION_PASS k=0..3000')
