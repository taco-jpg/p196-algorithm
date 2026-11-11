#!/usr/bin/env python3
import os
"""r13a: seam sweep for one band V against exterior E: loop over Lj=0..Lmax, time origins tau (multiples of p up to Trot), rotations r.
Each instance runs seamgen.py with a timeout.  Stops at the first SAT (unless --all).  Overall time limit --budget seconds.
usage: seamjob.py --clock 1000 --E W --ET 12 --V v --VT T --Trot Tr --twist r [--Lmax 12] [--timeout 120] [--budget 1800] [--rotE 0]"""
import sys, subprocess, argparse, time
ap=argparse.ArgumentParser()
ap.add_argument('--b',type=int,default=10); ap.add_argument('--clock',required=True); ap.add_argument('--E',required=True); ap.add_argument('--ET',type=int,required=True); ap.add_argument('--rotE',type=int,default=0)
ap.add_argument('--V',required=True); ap.add_argument('--VT',type=int,required=True); ap.add_argument('--Trot',type=int,default=0)
ap.add_argument('--Lmax',type=int,default=12); ap.add_argument('--Lmin',type=int,default=0); ap.add_argument('--timeout',type=int,default=120); ap.add_argument('--budget',type=int,default=1800); ap.add_argument('--all',action='store_true'); ap.add_argument('--solver',default='kissat404')
ap.add_argument('--Nmul',type=int,default=1)
ap.add_argument('--maxtau',type=int,default=0)
a=ap.parse_args()
PY=sys.executable; SG=os.path.expanduser('~/p196_run/r13a/seamgen.py')
s=len(a.V.split(','))
p=len(a.clock)
Trot=a.Trot if a.Trot else a.VT
taus=list(range(0,Trot,p))
if a.maxtau: taus=taus[:a.maxtau]
t00=time.time(); found=False; nrun=0; nuns=0; ntime=0
for Lj in range(a.Lmin,a.Lmax+1):
    for tau in taus:
        for r in range(s):
            if time.time()-t00>a.budget:
                print(f'SEAMBAND budget hit: V={a.V} done up to Lj={Lj} tau={tau} r={r} ran={nrun} unsat={nuns} timeouts={ntime}',flush=True); sys.exit(0)
            cmd=[PY,SG,'--b',str(a.b),'--clock',a.clock,'--E',a.E,'--ET',str(a.ET),'--rotE',str(a.rotE),'--V',a.V,'--VT',str(a.VT),'--tauV',str(tau),'--rotV',str(r),'--Lj',str(Lj),'--Nmul',str(a.Nmul),'--solver',a.solver]
            try:
                out=subprocess.run(cmd,capture_output=True,text=True,timeout=a.timeout)
                line=[l for l in out.stdout.splitlines() if l.startswith('RESULT')]
                nrun+=1
                if line:
                    if ': SAT' in line[0]:
                        print(line[0],flush=True); found=True
                        if not a.all:
                            print(f'SEAMBAND FOUND V={a.V} Lj={Lj} tau={tau} r={r} ran={nrun}',flush=True); sys.exit(0)
                    else:
                        nuns+=1
                else:
                    print('ERROR',out.stderr[-200:],flush=True)
            except subprocess.TimeoutExpired:
                ntime+=1
                print(f'TIMEOUT V={a.V} Lj={Lj} tau={tau} r={r}',flush=True)
print(f'SEAMBAND done V={a.V} Lmax={a.Lmax} taus={len(taus)} rots={s} ran={nrun} unsat={nuns} timeouts={ntime} found={found} elapsed={time.time()-t00:.0f}s',flush=True)
