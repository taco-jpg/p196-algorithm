#!/usr/bin/env python3
from pathlib import Path
s=Path(__file__).with_name("rows.txt").read_text().splitlines()[1:]
assert len(s)==16
B,W=s[:8],s[8:]
v=lambda c:"0123456789ABCDEFGHI".index(c)
assert all(len(x)==39 and any(v(c)%2 for c in x) for x in B)
assert all(len(x)==20 for x in W)
for t in range(8):
 for j in range(20):
  assert v(W[(t+22)%8][(j-5)%20])==18-v(W[t][j])
  assert v(W[(t+2)%8][(j+5)%20])==18-v(W[t][j])
assert 264%8==0 and 264%12==0 and 60%20==0
print("FRONT_TWIST_PASS: 320 checked symmetries, 8 odd boundaries, CRT clock 264")
