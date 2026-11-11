#!/usr/bin/env python3
import os
"""r13a band-job generator: genband.py MODE CLOCK Tmin Tmax OUT [--R 12] [--smax 8] [--epochs M] [--minM] [--timeout 200] [--solver S] [--tau t] [--all] [--Rfree F]
Each line = bandjob.py for one band (loops over rotations).  Sorted by (T*M, s)."""
import sys, argparse
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
PY=os.path.expanduser('~/p196_run/venv/bin/python'); JOB=os.path.expanduser('~/p196_run/r13a/bandjob.py')
ap=argparse.ArgumentParser()
ap.add_argument('mode'); ap.add_argument('clock'); ap.add_argument('tmin',type=int); ap.add_argument('tmax',type=int); ap.add_argument('out')
ap.add_argument('--R',type=int,default=12); ap.add_argument('--Rfree',type=int,default=0); ap.add_argument('--epochs',type=int,default=1); ap.add_argument('--minM',action='store_true'); ap.add_argument('--smax',type=int,default=8)
ap.add_argument('--timeout',type=int,default=200); ap.add_argument('--solver',default='kissat404'); ap.add_argument('--tau',type=int,default=0); ap.add_argument('--all',action='store_true'); ap.add_argument('--enc',type=int,default=1)
ap.add_argument('--bands',default=''); ap.add_argument('--extra',default=''); ap.add_argument('--comoving',action='store_true'); ap.add_argument('--rotepoch',action='store_true',help='use epoch Trot (Tprime=Trot), skipping bands with Trot==T'); ap.add_argument('--minbandT',type=int,default=0)
a=ap.parse_args()
clk=[int(c) for c in a.clock]; p=len(clk)
keep=None
if a.bands:
    keep=set(x.strip() for x in open(a.bands) if x.strip())
jobs=[]
for B in MK.parse(a.clock,a.smax):
    if keep is not None and B['V'] not in keep: continue
    s=B['s']; T=B['T']; S=sum(clk[t%p] for t in range(T))
    if T<a.minbandT: continue
    M=a.epochs
    if a.minM:
        M=1
        while not ((S*M)%2==0 and ((S*M)//2)%s==0): M+=1
    TT=T*M
    if a.rotepoch:
        if B['Trot']>=T: continue
        if T<=120 and B['Trot']>48: continue  # restrict (time budget): for T<=120 only short rotating epochs T_rot<=48
        TT=B['Trot']*M
    if not (a.tmin<=TT<=a.tmax): continue
    cmd=f"{PY} {JOB} {a.mode} --clock {a.clock} --V {B['V']} --T {T} --epochs {M} --tau {a.tau} --R {a.R}"
    if a.Rfree: cmd+=f" --Rfree {a.Rfree}"
    if a.rotepoch: cmd+=f" --Tprime {B['Trot']*M}"
    cmd+=f" --solver {a.solver} --enc {a.enc} --timeout {a.timeout}"
    if a.all: cmd+=" --all"
    if a.extra: cmd+=f" --extra \"{a.extra}\""
    if a.comoving: cmd+=" --comoving"
    jobs.append((TT,s,B['V'],cmd))
jobs.sort()
open(a.out,'w').write('\n'.join(j[3] for j in jobs)+'\n')
print(len(jobs),'band jobs',a.out)
