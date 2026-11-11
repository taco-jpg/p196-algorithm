#!/usr/bin/env python3
import os
"""r13a: D-type sweep job generator (exact-period free-port junction): for bands listed in a file (or survivors from FINAL_status_auto) and clock: L with --ret for m in M list."""
import sys, argparse
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
ap=argparse.ArgumentParser(); ap.add_argument('clock'); ap.add_argument('Tmax',type=int); ap.add_argument('out'); ap.add_argument('--ms',default='1,2'); ap.add_argument('--timeout',type=int,default=60); ap.add_argument('--bands',default=''); ap.add_argument('--smax',type=int,default=6); ap.add_argument('--R',type=int,default=12)
a=ap.parse_args()
keep=None
if a.bands:
    keep=set(l.strip() for l in open(a.bands) if l.strip())
PY=sys.executable; J=os.path.expanduser('~/p196_run/r13a/bandjob.py')
out=[]
for B in MK.parse(a.clock,a.smax):
    if B['T']>a.Tmax: continue
    if keep is not None and B['V'] not in keep: continue
    for m in [int(x) for x in a.ms.split(',')]:
        out.append((B['T']*m,B['s'],B['V'],f"{PY} {J} L --clock {a.clock} --V {B['V']} --T {B['T']} --epochs {m} --R {a.R} --solver kissat404 --timeout {a.timeout} --extra=--ret --all"))
out.sort()
open(a.out,'w').write('\n'.join(x[3] for x in out)+'\n')
print(len(out),'D jobs',a.out)
