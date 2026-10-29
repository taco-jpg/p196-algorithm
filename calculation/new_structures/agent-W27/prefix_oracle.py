#!/usr/bin/env python3
"""Independent genuine Python integers, reversing decimal strings."""
import sys
if hasattr(sys,"set_int_max_str_digits"): sys.set_int_max_str_digits(0)
for name,s,steps,expected in [
    ("196","196",1000,(11,105)),
    ("hybrid","196"+"9"*12010+"196",160,(6,12))
]:
    n=int(s)
    best,when=-1,-1
    for t in range(steps+1):
        v=str(n)
        m=len(v)//2
        idx=next((i for i in range(m)
                  if (int(v[i])+int(v[-i-1]))%2),m)
        if idx==m:
            assert name=="196" and t in (8,13,19),(name,t)
        elif idx>best:
            best,when=idx,t
        if t<steps:
            n+=int(v[::-1])
    assert (best,when)==expected,(name,best,when)
    print("PYTHON_INT",name,steps,best,when,"PASS")
