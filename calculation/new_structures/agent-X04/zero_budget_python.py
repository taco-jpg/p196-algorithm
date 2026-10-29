#!/usr/bin/env python3
"""Independent ordinary-Python-integer checks of the exact zero-corridor budget."""
import random
rng = random.Random(4404)

def width(s):
    n=len(s); i=(n-1)//2; z=0
    while i>=0 and int(s[i])+int(s[n-1-i])==0:
        z += 1 if i==n-1-i else 2
        i-=1
    return z

def carry_into(s,a):
    n=len(s); c=0
    for i in range(a):
        c=(int(s[i])+int(s[n-1-i])+c)//10
    return c

samples=0; g1=0
for _ in range(100000):
    a=rng.randrange(1,30); z=rng.randrange(1,80)
    s=''.join(str(rng.randrange(10)) for _ in range(a))+'0'*z+''.join(str(rng.randrange(10)) for _ in range(a))
    if s[0]=='0': s='1'+s[1:]
    actual_z=width(s); a0=(len(s)-actual_z)//2
    c=carry_into(s,a0)
    value=int(s)+int(s[::-1]); next_s=str(value); gamma=len(next_s)-len(s)
    assert gamma in (0,1)
    observed=width(next_s)
    predicted=actual_z-1 if gamma else max(0,actual_z-2*c)
    assert observed==predicted, (s, gamma, actual_z, c, observed, predicted)
    samples+=1;g1+=gamma
print(f'PYTHON_INTEGER_PASS samples={samples} overflow={g1}')
