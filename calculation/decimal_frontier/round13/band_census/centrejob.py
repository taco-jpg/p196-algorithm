#!/usr/bin/env python3
import os
"""r13a: centre sweep for one band: loop over time origins tau (phase-0 rows up to Trot), rotations r, centre widths Lc=Lmin..Lmax;
N = T*M (M minimal with delta integer and = 0 mod s, unless --epochs is given), shift j = delta/s.
Runs centregen.py with timeouts.  Stops at the first SAT unless --all.
usage: centrejob.py --clock 1000 --V v --T T --Trot Tr [--Lmax 6] [--timeout 120] [--budget 900] [--epochs M] [--b 10]"""
import sys, subprocess, argparse, time
ap=argparse.ArgumentParser()
ap.add_argument('--b',type=int,default=10); ap.add_argument('--clock',required=True); ap.add_argument('--V',required=True); ap.add_argument('--T',type=int,required=True); ap.add_argument('--Trot',type=int,default=0)
ap.add_argument('--Lmax',type=int,default=6); ap.add_argument('--Lmin',type=int,default=0); ap.add_argument('--timeout',type=int,default=120); ap.add_argument('--budget',type=int,default=900); ap.add_argument('--epochs',type=int,default=0); ap.add_argument('--all',action='store_true'); ap.add_argument('--solver',default='cadical195')
a=ap.parse_args()
PY=sys.executable; CG=os.path.expanduser('~/p196_run/r13a/centregen.py')
import bandsat as BS
V=[int(x) for x in a.V.split(',')]; s=len(V)
cl=[int(c) for c in a.clock]; p=len(cl)
M=a.epochs
S=sum(cl[t%p] for t in range(a.T))
if M==0:
    M=1
    while not ((S*M)%2==0 and ((S*M)//2)%s==0): M+=1
N=a.T*M; delta=S*M//2; j=delta//s
Trot=a.Trot if a.Trot else a.T
taus=list(range(0,Trot,p))
# rows at phase-0 times
rows=[list(V)]
for t in range(max(taus)+1 if taus else 1):
    y,_,_,_,_=BS.rowstep(rows[-1],cl[t%p],a.b); rows.append(y)
t00=time.time(); nrun=0; nuns=0; ntime=0; found=False
for Lc in range(a.Lmin,a.Lmax+1):
    for tau in taus:
        for r in range(s):
            if time.time()-t00>a.budget:
                print(f'CENTREBAND budget hit V={a.V} Lc={Lc} tau={tau} r={r} ran={nrun} unsat={nuns} timeouts={ntime}',flush=True); sys.exit(0)
            Vt=rows[tau][r:]+rows[tau][:r]
            cmd=[PY,CG,'--b',str(a.b),'--clock',a.clock,'--V',','.join(map(str,Vt)),'--N',str(N),'--j',str(j),'--Lc',str(Lc),'--solver',a.solver]
            try:
                out=subprocess.run(cmd,capture_output=True,text=True,timeout=a.timeout)
                nrun+=1
                txt=out.stdout
                if 'RESULT SAT' in txt:
                    print(f'CENTRE-SAT V={a.V} T={a.T} N={N} j={j} tau={tau} r={r} word={Vt} Lc={Lc}: '+txt.replace('\n',' | '),flush=True); found=True
                    if not a.all:
                        print(f'CENTREBAND FOUND V={a.V} Lc={Lc} tau={tau} r={r}',flush=True); sys.exit(0)
                elif 'RESULT UNSAT' in txt: nuns+=1
                else:
                    print('ERROR',out.stderr[-300:],flush=True)
            except subprocess.TimeoutExpired:
                ntime+=1
                print(f'TIMEOUT V={a.V} Lc={Lc} tau={tau} r={r}',flush=True)
print(f'CENTREBAND done V={a.V} T={a.T} N={N} j={j} Lmax={a.Lmax} ran={nrun} unsat={nuns} timeouts={ntime} found={found} elapsed={time.time()-t00:.0f}s',flush=True)
