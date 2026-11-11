#!/usr/bin/env python3
"""r13a: time-origin scan jobs: for bands with L(M=1,tau=0) PASS and T <= Tmax: one bandjob line per nonzero phase-0 origin tau < Trot.
usage: gentau.py CLOCK Tmax OUT [--timeout 60]"""
import sys, re, glob, os, argparse
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
ap=argparse.ArgumentParser(); ap.add_argument('clock'); ap.add_argument('Tmax',type=int); ap.add_argument('out'); ap.add_argument('--timeout',type=int,default=60); ap.add_argument('--smax',type=int,default=8)
a=ap.parse_args()
ROOT=os.path.expanduser('~/p196_run/r13a')
status={}
for d in glob.glob(ROOT+'/logs/*'):
    if not os.path.isdir(d): continue
    for f in glob.glob(d+'/i*.log'):
        for line in open(f):
            if not line.startswith('BANDRESULT L '): continue
            m=re.match(r'BANDRESULT L b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+)(?: Tprime=\d+)? tau=(\d+) R=(\d+) .* : rots=(\S+) status=(\w+)',line)
            if not m: continue
            b,clk,V,T,M,tau,R,rots,st=m.groups()
            if clk==a.clock and int(M)==1 and int(tau)==0: status[V]=st
p=len(a.clock); PY=sys.executable; J=ROOT+'/bandjob.py'; jobs=[]
for B in MK.parse(a.clock,a.smax):
    if B['T']>a.Tmax or status.get(B['V'])!='PASS': continue
    for tau in range(p,B['Trot'],p):
        jobs.append((B['T'],B['s'],f"{PY} {J} L --clock {a.clock} --V {B['V']} --T {B['T']} --epochs 1 --tau {tau} --R 12 --solver kissat404 --timeout {a.timeout}"))
jobs.sort(key=lambda x:(x[0],x[1]))
open(a.out,'w').write('\n'.join(x[2] for x in jobs)+'\n')
print(len(jobs),'tau-scan jobs',a.out)
