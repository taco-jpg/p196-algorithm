#!/usr/bin/env python3
"""Independent Python arbitrary-precision control for X20 unequal-band seeds."""
import re
import sys
from pathlib import Path
sys.set_int_max_str_digits(0)
source = Path(__file__).with_name('two_counter.cpp').read_text()
def block(key):
    s = re.search(r'const V '+key+r'=\{([^}]+)\}', source).group(1)
    return [int(x) for x in s.split(',')]
B, W, V = block('B'), block('W'), block('Q')
def seed(m,n):
    half = B+W*m+[9]+V*n
    p=half+[9]+half[::-1]
    carry=0
    digits=[]
    for x in p:
        x+=carry
        digits.append(x%10)
        carry=x//10
    if carry: digits.append(carry)
    return int(''.join(map(str,digits[::-1])))
def check(m,n,tmax):
    x=seed(m,n)
    length0=len(str(x))
    for t in range(tmax+1):
        s=str(x)
        assert s!=s[::-1], (m,n,t,'palindrome')
        assert len(s)==length0+t//2, (m,n,t,'length')
        if t<tmax:x+=int(s[::-1])
    print('PASS Python int', m,n,'steps',tmax,'digits',len(str(x)))
if __name__=='__main__':
    for mn in [(40,41),(41,40),(43,58),(58,43)]:check(*mn,128)
