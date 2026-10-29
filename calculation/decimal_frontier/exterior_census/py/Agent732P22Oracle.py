#!/usr/bin/env python3
"""Independent, uncompressed integer-state oracle for first two cut positions.

This intentionally uses Python tuples (lower bits, upper bits, individual decimal
partner digits) rather than the 128-bit C++ packing or its hash structure.
"""
import collections
import sys


def successors(g, state, first):
    lower, upper, partners = state
    p = len(g)
    indices = {}
    j = 0
    for t,bit in enumerate(g):
        if bit:
            indices[t] = j
            j += 1
    for initial in range(1 if first else 0,19):
        def rec(t, x, lo, hi, digs):
            if t == p:
                if x == initial:
                    yield (lo, hi, digs)
                return
            if first and x == 0:
                return
            low_carry = (lower >> t) & 1
            required = (upper >> t) & 1
            for upper_carry in (0,1):
                if (x+upper_carry >= 10) != bool(required):
                    continue
                lower_digit = (x+low_carry) % 10
                upper_digit = (x+upper_carry) % 10
                next_x = lower_digit + (partners[indices[t]] if g[t] else upper_digit)
                next_digits = digs + ((upper_digit,) if g[t] else ())
                yield from rec(t+1,next_x,lo | (((x+low_carry)//10) << t),hi | (upper_carry << t), next_digits)
        yield from rec(0,initial,0,0,())


def initial(g):
    return (0,sum(bit<<t for t,bit in enumerate(g)),(1,)*sum(g))


def run(pattern, depth=2):
    g=tuple(map(int,pattern))
    current=collections.Counter({initial(g):1})
    for d in range(depth+1):
        print(f'depth={d} states={len(current)} mass={sum(current.values())}', flush=True)
        if d==depth:
            path=sys.argv[3] if len(sys.argv)>3 else None
            if path:
                with open(path,'w') as f:
                    for (L,H,Y),cnt in sorted(current.items()):
                        # Y little-endian nibble pack for comparison with C++ (not used in enumeration)
                        yi=sum(y<<(4*i) for i,y in enumerate(Y))
                        f.write(f'{L},{H},{yi},{cnt}\n')
        else:
            nxt=collections.Counter()
            for state,weight in current.items():
                for next_state in successors(g,state,d==0):
                    nxt[next_state]+=weight
            current=nxt
if __name__=='__main__':
    if len(sys.argv)<3:raise SystemExit('usage: oracle.py overflow-bits depth [output.csv]')
    run(sys.argv[1], int(sys.argv[2]))
