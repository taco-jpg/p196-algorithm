#!/usr/bin/env python3
"""r12f: minimal return period of each U3 band row under the forced clock gamma_t=[t%4==0] (T multiple of 4),
and the admissible return times T of the template (B/W rows 12-periodic, length growth T/4 digits = T/8 columns per
half must be a multiple of 3, U row back to U_0)."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import mdefect as md
from math import lcm
out = []
for i, U in enumerate(md.us()):
    rows, _, _ = md.band_bg(U, 480)
    p = next(T for T in range(4, 481, 4) if rows[T] == tuple(U))
    out.append(p)
    print(f"U{i} {U}: minimal period {p}")
print("set of minimal periods:", sorted(set(out)))
print("admissible template return times T = multiples of lcm(12, 24, p):", sorted(set(lcm(12, 24, p) for p in out)))
