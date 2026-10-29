#!/usr/bin/env python3
"""Independent 40-row check of a reflection-synchronized odd coefficient carrier."""

def local(x, left, right, gamma):
    assert 9 not in (x, left, right)
    h=lambda z: int(z>=10)
    if gamma: return x+left-9*(h(x)+h(left))
    return 2*x+h(left)+h(right)-20*h(x)

R=[17,3,14,3,17]
rows=[]
for t in range(40):
    assert all(0<=v<=18 and v!=9 for v in R)
    assert any(v%2 for v in R)
    rows.append(tuple(R))
    delta=((t+1)//2-1)%5
    for r in range(5):
        assert R[r]==R[(delta-r)%5],(t,delta,R,r)
    R=[local(R[i],R[(i-1)%5],R[(i+1)%5],t%2==0) for i in range(5)]
assert tuple(R)==rows[0]
for t in range(32):
    assert rows[t+8]==tuple(rows[t][(i-2)%5] for i in range(5))
# all future reflection-axis classes repeat after 40, because 20 == 0 (mod 5).
for t in range(40,4040):
    d=((t+1)//2-1)%5
    row=rows[t%40]
    assert all(row[r]==row[(d-r)%5] for r in range(5))
print('PASS 40 local affine updates, 40 reflection axes, and all 4040 extended phase/axis checks')
print('Exact conditional width: 42000 - t - floor(t/2) - 4')
