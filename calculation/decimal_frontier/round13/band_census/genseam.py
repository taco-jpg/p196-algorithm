#!/usr/bin/env python3
"""r13a seam job generator: for bands with L(M=1) status PASS (clock c), one seamjob line (E = exterior word).
usage: genseam.py CLOCK E ET Tmax Lmax OUT [--timeout 120] [--budget 1800] [--status PASS] [--maxlcm N]"""
import sys, argparse, re, glob, os, math
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
ap=argparse.ArgumentParser()
ap.add_argument('clock'); ap.add_argument('E'); ap.add_argument('ET',type=int); ap.add_argument('Tmax',type=int); ap.add_argument('Lmax',type=int); ap.add_argument('out')
ap.add_argument('--timeout',type=int,default=120); ap.add_argument('--budget',type=int,default=1800); ap.add_argument('--status',default='PASS'); ap.add_argument('--maxlcm',type=int,default=10**9); ap.add_argument('--rotE',type=int,default=0); ap.add_argument('--smax',type=int,default=8); ap.add_argument('--allstatus',action='store_true')
a=ap.parse_args()
a.budget=min(a.budget,240)  # clamp (r13a time budget)
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
            if clk==a.clock and int(M)==1: status[V]=st
PY=sys.executable; SJ=ROOT+'/seamjob.py'
jobs=[]
for B in MK.parse(a.clock,a.smax):
    if B['T']>a.Tmax: continue
    if not a.allstatus and status.get(B['V'])!=a.status: continue
    N=B['T']*a.ET//math.gcd(B['T'],a.ET)
    if N>a.maxlcm: continue
    cmd=f"{PY} {SJ} --clock {a.clock} --E {a.E} --ET {a.ET} --rotE {a.rotE} --V {B['V']} --VT {B['T']} --Trot {B['Trot']} --Lmax {a.Lmax} --timeout {a.timeout} --budget {a.budget}"
    jobs.append((N,B['s'],B['V'],cmd))
jobs.sort()
open(a.out,'w').write('\n'.join(j[3] for j in jobs)+'\n')
print(len(jobs),'seam jobs',a.out)
