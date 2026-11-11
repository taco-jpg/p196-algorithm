#!/usr/bin/env python3
"""r13a job pool: pool.py JOBFILE NWORKERS TAG.  Each job line is a shell command (run with nice 10 by the worker).
Output of job i goes to logs/TAG/iNNNNN.log; finished jobs are recorded in logs/TAG/done.txt so restarts skip them.
Lines starting with # are skipped."""
import sys, os, subprocess, threading, time
DEADLINE=float(os.environ.get('DEADLINE','0'))
jobfile, nw, tag = sys.argv[1], int(sys.argv[2]), sys.argv[3]
root=os.path.expanduser('~/p196_run/r13a')
logdir=f'{root}/logs/{tag}'
os.makedirs(logdir,exist_ok=True)
donef=f'{logdir}/done.txt'
done=set()
if os.path.exists(donef):
    done=set(l.strip() for l in open(donef))
lines=[l.rstrip('\n') for l in open(jobfile) if l.strip() and not l.startswith('#')]
lock=threading.Lock()
idx=[0]
def worker():
    while True:
        with lock:
            while idx[0]<len(lines) and (f'{idx[0]}' in done):
                idx[0]+=1
            if idx[0]>=len(lines): return
            if DEADLINE and time.time()>DEADLINE: return
            i=idx[0]; idx[0]+=1
        cmd=lines[i]
        lf=f'{logdir}/i{i:05d}.log'
        with open(lf,'w') as f:
            f.write(f'# {cmd}\n'); f.flush()
            t0=time.time()
            r=subprocess.run(['nice','-n','10','bash','-c',cmd],stdout=f,stderr=subprocess.STDOUT)
            f.write(f'# exit {r.returncode} elapsed {time.time()-t0:.1f}\n')
        with lock:
            with open(donef,'a') as f: f.write(f'{i}\n')
ths=[threading.Thread(target=worker) for _ in range(nw)]
for t in ths: t.start()
for t in ths: t.join()
print('pool done',flush=True)
