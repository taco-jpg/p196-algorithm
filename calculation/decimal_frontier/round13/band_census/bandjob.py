#!/usr/bin/env python3
import os
"""r13a band job: one band, all rotations of one test (L or R), sequentially, each rotation run in a subprocess with a
per-instance timeout.  Stops at the first SAT rotation unless --all.
usage: bandjob.py MODE --b 10 --clock 1000 --V 18,9,0 --T 120 [--epochs M] [--tau t] [--R 12] [--Rfree F] [--solver S] [--enc E]
       [--timeout SEC] [--all] [--extra "..."]
Output: one line per rotation (from bandrun.py) and a final summary line:
BANDRESULT mode=L clock=.. V=.. T=.. epochs=.. tau=.. solver=.. enc=.. R=.. : rots=SUSTU... status=PASS/ALLUNSAT/UNDECIDED firstSAT=r times=[..]
(S SAT, U UNSAT, T timeout, ? not run after early stop)."""
import sys, subprocess, argparse, time, re
ap=argparse.ArgumentParser()
ap.add_argument('mode'); ap.add_argument('--b',type=int,default=10); ap.add_argument('--clock',required=True); ap.add_argument('--V',required=True)
ap.add_argument('--T',type=int,required=True); ap.add_argument('--epochs',type=int,default=1); ap.add_argument('--tau',type=int,default=0)
ap.add_argument('--R',type=int,default=12); ap.add_argument('--Rfree',type=int,default=0); ap.add_argument('--solver',default='kissat404')
ap.add_argument('--enc',type=int,default=1); ap.add_argument('--timeout',type=int,default=120); ap.add_argument('--all',action='store_true'); ap.add_argument('--extra',default='')
ap.add_argument('--budget',type=int,default=0,help='overall time limit (s) for this band job (remaining rotations are marked B)'); ap.add_argument('--tag',default=''); ap.add_argument('--allepochs',action='store_true'); ap.add_argument('--comoving',action='store_true'); ap.add_argument('--markevery',type=int,default=0); ap.add_argument('--Tprime',type=int,default=0)
a=ap.parse_args()
PY=os.path.expanduser('~/p196_run/venv/bin/python'); RUN=os.path.expanduser('~/p196_run/r13a/bandrun.py')
n=len(a.V.split(','))
t00=time.time()
status=[]; times=[]; first=None
for r in range(n):
    if a.budget and time.time()-t00>a.budget:
        print(f'BUDGET rot={r}: budget {a.budget}s exhausted',flush=True); status.append('B'); times.append(0.0); continue
    cmd=[PY,RUN,a.mode,'--b',str(a.b),'--clock',a.clock,'--V',a.V,'--T',str(a.T),'--epochs',str(a.epochs),'--tau',str(a.tau),'--rot',str(r),'--R',str(a.R),'--solver',a.solver,'--enc',str(a.enc)]
    if a.Rfree: cmd+=['--Rfree',str(a.Rfree)]
    cmd+=a.extra.split()
    if a.allepochs: cmd+=['--allepochs']
    if a.comoving: cmd+=['--comoving']
    if a.markevery: cmd+=['--markevery',str(a.markevery)]
    if a.Tprime: cmd+=['--Tprime',str(a.Tprime)]
    t0=time.time()
    try:
        out=subprocess.run(cmd,capture_output=True,text=True,timeout=a.timeout)
        ans=None
        for line in out.stdout.splitlines():
            if line.startswith('RESULT'):
                print(line,flush=True)
                ans='S' if ': SAT' in line else ('U' if ': UNSAT' in line else None)
            elif line.startswith('NOTE'):
                print(line,flush=True); ans='N'
        if ans is None:
            print(f'ERROR rot={r}: {out.stderr[-300:]}',flush=True); ans='E'
    except subprocess.TimeoutExpired:
        ans='T'
        print(f'TIMEOUT rot={r} after {a.timeout}s',flush=True)
    dt=time.time()-t0
    status.append(ans); times.append(round(dt,1))
    if ans=='S' and first is None:
        first=r
        if not a.all:
            break
st=''.join(status)+'?'*(n-len(status))
if 'S' in st: bs='PASS'
elif st=='U'*n: bs='ALLUNSAT'
else: bs='UNDECIDED'
tag=f'{a.mode}{"r" if a.Tprime else ""}{"D" if "--ret" in a.extra else ""}{"*" if a.allepochs or a.comoving or a.markevery else ""} b={a.b} clock={a.clock} V={a.V} T={a.T} epochs={a.epochs} Tprime={a.Tprime or a.epochs*a.T} tau={a.tau} R={a.R} Rfree={a.Rfree} solver={a.solver} enc={a.enc}'
print(f'BANDRESULT {tag} : rots={st} status={bs} firstSAT={first} times={times} total={sum(times):.1f}s',flush=True)
