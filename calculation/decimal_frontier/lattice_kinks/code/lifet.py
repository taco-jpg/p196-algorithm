#!/usr/bin/env python3
"""max survival horizon L(w,o) by SAT (hor mode) : largest H with SAT.  usage: lifet.py lat w o [Hstart]"""
import sys, time
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from sat_kink import *
lat=load_lat(sys.argv[1]); w=int(sys.argv[2]); o=int(sys.argv[3]); H=int(sys.argv[4]) if len(sys.argv)>4 else 4*w
# find first UNSAT H, from H upward (assume monotone: SAT at H implies SAT at H-1)
while True:
    E,layers,K,ns=build(lat,w,o,'hor',H)
    r,model,dt=solve(E)
    print(f'w={w} o={o} H={H} {"SAT" if r else "UNSAT"} {dt:.1f}s',flush=True)
    if not r: break
    H+=1
print(f'LIFETIME w={w} o={o}: max SAT horizon = {H-1}',flush=True)
