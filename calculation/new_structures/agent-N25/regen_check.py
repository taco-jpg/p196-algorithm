#!/usr/bin/env python3
"""Independent Python integer witness for a two-cell zero-sector recharge at t=1848."""
import sys
sys.set_int_max_str_digits(1000000)
g=4000
s='1789'+'0'*g+'3141'+'0'*g+'5926'+'0'*g+'5358'
seedlen=len(s)

def central_width(s,t):
    G=len(s)-seedlen
    lower=g-2*t+G
    a=8+g+t
    assert lower>0 and s[a:a+lower]=='0'*lower
    l=a;r=a+lower-1
    while l>0 and s[l-1]=='0':l-=1
    while r+1<len(s) and s[r+1]=='0':r+=1
    return (r-l+1,s[max(0,l-16):l],s[r+1:r+17],G)

for t in range(1849):
    if t in (1847,1848):
        print('t=',t,'central_width/left_junction/right_junction/overflows=',central_width(s,t))
    if t<1848:
        s=str(int(s)+int(s[::-1]))
assert central_width(s,1848)[0]==2906
print('RECHARGE +2 at t=1848 confirmed by Python built-in big integers')
