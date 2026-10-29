#!/usr/bin/env python3
"""Independent Python arbitrary-integer test of W27 centre insertion."""
import sys
if hasattr(sys,"set_int_max_str_digits"): sys.set_int_max_str_digits(0)
def step(s):
    return str(int(s)+int(s[::-1]))
def pump(s):
    k=len(s)//2
    return s[:k]+"99"+s[k:]
def middle9(s):
    k=len(s)//2
    i,j=k-1,k
    while i>=0 and s[i]=="9": i-=1
    while j<len(s) and s[j]=="9": j+=1
    return j-i-1
count=0
for a in (1,2):
    for b in (1,2):
        for left in range(10**(a-1),10**a):
            for right in range(10**(b-1),10**b):
                for length in (6,7):
                    x=str(left)+"9"*length+str(right)
                    y=step(x)
                    if middle9(y)<5: continue
                    assert step(pump(x))==pump(y),(x,y)
                    count+=1
print("LEMMA_CHECK exhaustive qualifying cases =",count)
q=6005
s="196"+"9"*(2*q)+"196"
u=pump(s)
for t in range(161):
    assert u==pump(s),t
    assert s!=s[::-1],t
    assert middle9(s)>=5,t
    if t<160: s,u=step(s),step(u)
print("PYTHON_INTEGER_REPLAY through step 160 PASS; centre9 =",middle9(s))
