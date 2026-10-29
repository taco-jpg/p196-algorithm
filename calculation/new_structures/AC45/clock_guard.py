#!/usr/bin/env python3
"""Independent physical-clock and palindrome guard audit for bounded AC45 controls.
Does not decide the unbounded pi185 language.
"""
import argparse
import itertools
from engine import template, realize, step_digits, pair, U

CLOCK = tuple(int(x) for x in "100010001000" * 10)

def audit(j, c=(4,4), q=14, k=100, steps=120):
    d = realize(template(j,c,q,k))
    n = int("".join(map(str,reversed(d))))
    bits = []
    guarded = d != d[::-1]
    for t in range(steps):
        old = len(d)
        d = step_digits(d)
        bits.append(len(d)-old)
        n += int(str(n)[::-1])
        assert d == [int(x) for x in str(n)[::-1]], (q,k,j,t)
        guarded &= d != d[::-1]
    return tuple(bits), bool(guarded), pair(d) == template(j,c,q,k+5)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--wide",action="store_true")
    args=parser.parse_args()
    widths=[(14,100)] + ([(20,80),(40,160),(80,320),(160,640)] if args.wide else [])
    for q,k in widths:
        count=clock=guard=returns=0
        js=list(itertools.product(range(19),repeat=2)) if q==14 else [(0,0),(5,7),(18,18)]
        for j in js:
            bits,g,r=audit(j,q=q,k=k)
            count+=1
            clock+=bits==CLOCK
            guard+=g
            returns+=r
        print(dict(q=q,k=k,cases=count,exact_clock=clock,nonpalindrome_guard=guard,return_matches=returns))
    # Deliberately planted palindrome: 10 -> 11, so any guard must reject the edge.
    d=[0,1]
    assert step_digits(d)==[1,1]
    assert step_digits(d)==step_digits(d)[::-1]
    print("planted-palindrome guard negative control: PASS")

if __name__=="__main__":
    main()
