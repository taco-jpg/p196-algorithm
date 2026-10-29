#!/usr/bin/env python3
"""Independently construct all eight 39-cell B phases with ordinary integers."""
import sys
from sft import B0, W
from validate import numeral_from_folded, integer_pairs
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)
N=numeral_from_folded(B0+W[0]*100)
for t in range(8):
    row=integer_pairs(N)[:39]
    assert len(row)==39 and any(p%2 for p in row)
    print(" ".join(map(str,row)))
    N+=int(str(N)[::-1])
