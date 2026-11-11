#!/usr/bin/env python3
import os
"""r13a job generator.  gen.py MODE CLOCK Tmin Tmax OUTFILE [--R 12] [--epochs M] [--smax 8] [--tau 0] [--timeout 120]
              [--solver kissat404] [--minM] (for R: choose minimal epochs M with delta integer and delta = 0 mod s)
Lines sorted by (T*M, s, V, rot)."""
import sys, argparse, json, re
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
PYB=os.path.expanduser('~/p196_run/venv/bin/python'); RUN=os.path.expanduser('~/p196_run/r13a/bandrun.py'); JOB=os.path.expanduser('~/p196_run/r13a/bandjob.py')
ap=argparse.ArgumentParser()
ap.add_argument('mode'); ap.add_argument('clock'); ap.add_argument('tmin',type=int); ap.add_argument('tmax',type=int); ap.add_argument('out')
ap.add_argument('--R',type=int,default=12); ap.add_argument('--epochs',type=int,default=1)
ap.add_argument('--smax',type=int,default=8); ap.add_argument('--tau',type=int,default=0); ap.add_argument('--timeout',type=int,default=120)
ap.add_argument('--solver',default='kissat404'); ap.add_argument('--minM',action='store_true'); ap.add_argument('--extra',default='')
ap.add_argument('--bands',default='')  # optional file with lines V,T,... restricting bands
a=ap.parse_args()
clk=[int(c) for c in a.clock]; p=len(clk); ones=sum(clk)
bands=MK.parse(a.clock,a.smax)
keep=None
if a.bands:
    keep=set(x.strip() for x in open(a.bands) if x.strip())
jobs=[]
for B in bands:
    if keep is not None and B['V'] not in keep: continue
    s=B['s']; T=B['T']
    # overflows per T steps
    S=sum(clk[t%p] for t in range(T))
    M=a.epochs
    if a.minM:
        M=1
        while not ((S*M)%2==0 and ((S*M)//2)%s==0):
            M+=1
    TT=T*M
    if not (a.tmin<=TT<=a.tmax): continue
    for r in range(s):
        extra=a.extra
        cmd=f"perl -e 'alarm shift; exec @ARGV' {a.timeout} {PYB} {RUN} {a.mode} --b 10 --clock {a.clock} --V {B['V']} --T {T} --tau {a.tau} --rot {r} --R {a.R} --epochs {M} --solver {a.solver} {extra}"
        jobs.append((TT,s,B['V'],r,cmd))
jobs.sort()
open(a.out,'w').write('\n'.join(j[4] for j in jobs)+'\n')
print(len(jobs),'jobs written',a.out)

# (band-job file is written when --bandjobs is given)
