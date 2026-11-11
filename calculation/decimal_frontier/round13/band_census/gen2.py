#!/usr/bin/env python3
"""r13a stage-2 generator: for bands whose BANDRESULT at (mode L, M=1, tau=0, R=12) is PASS (or any status given),
emit L* multi-epoch band jobs: M = ceil(Tgoal/T), T' = M T <= Tcap, --allepochs, sorted by T'.
usage: gen2.py CLOCK OUT [--Tgoal 96] [--Tcap 168] [--status PASS] [--smax 8] [--timeout 300] [--logs DIR ...]"""
import sys, argparse, math, re, glob, os
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
ROOT=os.path.expanduser('~/p196_run/r13a')
ap=argparse.ArgumentParser()
ap.add_argument('clock'); ap.add_argument('out')
ap.add_argument('--Tgoal',type=int,default=96); ap.add_argument('--Tcap',type=int,default=168); ap.add_argument('--status',default='PASS')
ap.add_argument('--smax',type=int,default=8); ap.add_argument('--timeout',type=int,default=300); ap.add_argument('--solver',default='kissat404'); ap.add_argument('--R',type=int,default=12); ap.add_argument('--enc',type=int,default=1)
a=ap.parse_args()
status={}
for d in glob.glob(ROOT+'/logs/*'):
    if not os.path.isdir(d): continue
    for f in glob.glob(d+'/i*.log'):
        for line in open(f):
            if not line.startswith('BANDRESULT L '): continue
            m=re.match(r'BANDRESULT L b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+)(?: Tprime=\d+)? tau=(\d+) R=(\d+) .* : rots=(\S+) status=(\w+)',line)
            if not m: continue
            b,clk,V,T,M,tau,R,rots,st=m.groups()
            if clk==a.clock and int(M)==1 and int(tau)==0 and int(R)==a.R:
                status[V]=st
PY=sys.executable
JOB=ROOT+'/bandjob.py'
jobs=[]
cl=[int(c) for c in a.clock]; p=len(cl)
for B in MK.parse(a.clock,a.smax):
    st=status.get(B['V'])
    if a.status and st!=a.status: continue
    if B['s']>6: continue  # restricted (time budget): s>=7 multi-epoch not attempted
    T=B['T']
    M=max(2,math.ceil(a.Tgoal/T))
    TT=M*T
    if TT>a.Tcap:
        M=1 if T>=a.Tgoal else None
    if M is None: continue
    TT=M*T
    if M==1: continue  # already done as M=1
    mk = B['Trot'] if B['Trot'] < T else T
    cmd=f"{sys.executable} {JOB} L --clock {a.clock} --V {B['V']} --T {T} --epochs {M} --R {a.R} --solver {a.solver} --enc {a.enc} --timeout {a.timeout} --budget 600 --markevery {mk}"
    jobs.append((TT,B['s'],B['V'],cmd))
jobs.sort()
open(a.out,'w').write('\n'.join(j[3] for j in jobs)+'\n')
print(len(jobs),'jobs',a.out, 'status counts', {k:sum(1 for v in status.values() if v==k) for k in set(status.values())})
