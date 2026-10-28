#!/usr/bin/env python3
"""Independent ordinary-integer/carry checks for T=24 rec2 transfer.
Compares the existing lattice file and committed column-formatted input,
and checks 48 time-24 unperturbed spatial continuation controls.
"""
import sys
from pathlib import Path
z=list(map(int,Path(sys.argv[1]).read_text().split()))
p,nb,m,b=z[:4]
assert (p,nb,m,b)==(8,11,48,10)
k=4
G=z[k:k+p];k+=p
W=[z[k+t*m:k+(t+1)*m] for t in range(p)];k+=p*m
C=[z[k+t*m:k+(t+1)*m] for t in range(p)];k+=p*m
B=[z[k+t*nb:k+(t+1)*nb] for t in range(p)]
assert k+p*nb==len(z) and G==[1,0,1,0,1,0,1,0]
rows=[[W[t][j] for t in range(p)] for j in range(m)]
rows.extend([[B[t][j] for t in range(p)] for j in range(nb)])
assert rows==[list(map(int,line.split())) for line in Path(sys.argv[2]).read_text().splitlines()]
def cell(t,x):
    return B[t%8][x] if x<nb else W[t%8][(x-nb)%m]
def ascending(t,x):
    for d in range(1,97):
        v=cell(t,x-d)
        if v!=9:return int(v>=10)
    raise ValueError('ambiguous ascending carry')
def descending(t,x):
    for d in range(1,97):
        v=cell(t,x+d)
        if v!=9:return int(v>=10)
    raise ValueError('ambiguous descending carry')
for t in range(8):
    for j in range(48):
        assert ascending(t,nb+2*m+j)==C[t][j]
for j in range(48):
    x=nb+2*m+j
    for t in range(24):
        v=cell(t,x)
        a=ascending(t,x)
        d=descending(t,x)
        prev=cell(t,x-1)
        prev_d=descending(t,x-1)
        assert prev_d==int(v+d>=10)
        lo=(v+a)%10
        hi=((prev+prev_d)%10) if G[t%8] else ((v+d)%10)
        assert lo+hi==cell(t+1,x)
        assert int(v+a>=10)==ascending(t,x+1)
        assert int(v+d>=10)==descending(t,x-1)
print('CONTROL: lattice source, 48 T=24 periodic bulk traces, ascending/descending carries all match')
