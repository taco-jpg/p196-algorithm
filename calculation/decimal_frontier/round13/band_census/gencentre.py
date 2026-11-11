#!/usr/bin/env python3
"""r13a centre-sweep job generator.  gencentre.py CLOCK Nmax Lmax OUT [--timeout 60] [--budget 900] [--smax 8] [--status PASS]"""
import sys, argparse, re, glob, os, math
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
ap=argparse.ArgumentParser()
ap.add_argument('clock'); ap.add_argument('Nmax',type=int); ap.add_argument('Lmax',type=int); ap.add_argument('out')
ap.add_argument('--timeout',type=int,default=60); ap.add_argument('--budget',type=int,default=900); ap.add_argument('--status',default='PASS'); ap.add_argument('--smax',type=int,default=8); ap.add_argument('--allstatus',action='store_true')
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
            if clk==a.clock and int(M)==1: status[V]=st
PY=sys.executable; CJ=ROOT+'/centrejob.py'
cl=[int(c) for c in a.clock]; p=len(cl)
jobs=[]
for B in MK.parse(a.clock,a.smax):
    if not a.allstatus and status.get(B['V'])!=a.status: continue
    s=B['s']; T=B['T']
    S=sum(cl[t%p] for t in range(T))
    M=1
    while not ((S*M)%2==0 and ((S*M)//2)%s==0): M+=1
    N=T*M
    if N>a.Nmax: continue
    cmd=f"{PY} {CJ} --clock {a.clock} --V {B['V']} --T {T} --Trot {B['Trot']} --Lmax {a.Lmax} --timeout {a.timeout} --budget {a.budget}"
    jobs.append((N,s,B['V'],cmd))
jobs.sort()
open(a.out,'w').write('\n'.join(j[3] for j in jobs)+'\n')
print(len(jobs),'centre jobs',a.out)
