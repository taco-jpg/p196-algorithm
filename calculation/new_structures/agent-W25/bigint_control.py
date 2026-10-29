#!/usr/bin/env python3
"""Independent ordinary Python bigint reverse/add control for W25."""
import sys
sys.set_int_max_str_digits(0)
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
U=[9,18,9,0]
k=int(sys.argv[1]) if len(sys.argv)>1 else 150
r=int(sys.argv[2]) if len(sys.argv)>2 else 500
steps=int(sys.argv[3]) if len(sys.argv)>3 else 1000
q=B+W*k+U*r
s=''.join(str(v-min(v,9)) for v in q)+''.join(str(min(v,9)) for v in q[::-1])
n=int(s)
pals=0
for t in range(steps+1):
    v=str(n)
    pals+=v==v[::-1]
    if t<steps:n+=int(v[::-1])
h=1469598103934665603
for d in str(n)[::-1]:
    h^=int(d);h=(h*1099511628211)%(1<<64)
print(f'PYTHON_CONTROL k={k} r={r} steps={steps} initial_digits={len(s)} final_digits={len(str(n))} pal={pals} fnv64={h:x}')
if (k,r,steps)==(150,500,1000):assert (len(str(n)),pals,h)==(10578,0,0x2e3b04ac35eb421)
