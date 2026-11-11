#!/usr/bin/env python3
import os
"""r13a: rooted exterior sweep for one band: loop over time origins (phase-0 rows), rotations and widths w = wmin..wmax; rootseam.py subprocess with a timeout.  Stops at the first SAT (for each word) unless --all; budget per word.
usage: rootjob.py --V v --T T --Trot Tr --clock 1000 --N 24 [--taus 0,4,...] [--wmin 0] [--wmax 60] [--timeout 90] [--budget 900]"""
import sys, subprocess, argparse, time
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import bandsat as BS
ap=argparse.ArgumentParser(); ap.add_argument('--b',type=int,default=10); ap.add_argument('--clock',default='1000'); ap.add_argument('--V',required=True); ap.add_argument('--T',type=int,required=True); ap.add_argument('--Trot',type=int,default=0); ap.add_argument('--N',type=int,required=True); ap.add_argument('--taus',default=''); ap.add_argument('--rots',default=''); ap.add_argument('--wmin',type=int,default=0); ap.add_argument('--wmax',type=int,default=60); ap.add_argument('--timeout',type=int,default=90); ap.add_argument('--budget',type=int,default=900); ap.add_argument('--all',action='store_true'); ap.add_argument('--solver',default='cadical195')
a=ap.parse_args()
PY=sys.executable; RS=os.path.expanduser('~/p196_run/r13a/rootseam.py')
V=[int(x) for x in a.V.split(',')]; s=len(V); cl=[int(c) for c in a.clock]; p=len(cl)
Trot=a.Trot if a.Trot else a.T
taus=[int(x) for x in a.taus.split(',')] if a.taus else list(range(0,Trot,p))
rots=[int(x) for x in a.rots.split(',')] if a.rots else list(range(s))
rows=[list(V)]
for t in range(max(taus)+1):
    y,*_=BS.rowstep(rows[-1],cl[t%p],a.b); rows.append(y)
t00=time.time(); nrun=nuns=nto=0; found=0
for tau in taus:
    for r in rots:
        W=rows[tau][r:]+rows[tau][:r]
        word=','.join(map(str,W))
        for w in range(a.wmin,a.wmax+1):
            if time.time()-t00>a.budget:
                print(f'ROOTJOB budget: V={a.V} tau={tau} r={r} w={w} ran={nrun} unsat={nuns} timeouts={nto} found={found}',flush=True); sys.exit(0)
            cmd=[PY,RS,'--b',str(a.b),'--clock',a.clock,'--V',word,'--N',str(a.N),'--w',str(w),'--solver',a.solver]
            try:
                out=subprocess.run(cmd,capture_output=True,text=True,timeout=a.timeout)
                nrun+=1
                txt=out.stdout
                if ': SAT' in txt:
                    line=[l for l in txt.splitlines() if l.startswith('RESULT')][0]
                    print(f'ROOT-SAT tau={tau} r={r} word=[{word}]: {line}',flush=True); found+=1
                    if not a.all: break
                elif ': UNSAT' in txt: nuns+=1
                else: print('ERROR',out.stderr[-200:],flush=True)
            except subprocess.TimeoutExpired:
                nto+=1; print(f'TIMEOUT tau={tau} r={r} w={w}',flush=True)
print(f'ROOTJOB done V={a.V} T={a.T} N={a.N} taus={taus} wmax={a.wmax} ran={nrun} unsat={nuns} timeouts={nto} found={found} elapsed={time.time()-t00:.0f}s',flush=True)
