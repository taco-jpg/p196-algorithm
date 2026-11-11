#!/usr/bin/env python3
"""sweep.py (r14a): run a list of (class, orbit) jobs with a bounded pool.
usage: sweep.py MODE(scc|run) NPAR RSSGB SEC  [classfilter ids or 'all'] [maxT] [threads per job]
Logs: logs/sw_<mode>_c<id>_o<orbit>.log; summary lines appended to logs/sweep_<mode>.txt.
A job is skipped if its .status file already says END rc=0."""
import sys, os, json, subprocess, time, threading, collections
mode, npar, rss, sec = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
filt = sys.argv[5] if len(sys.argv) > 5 else 'all'
maxT = int(sys.argv[6]) if len(sys.argv) > 6 else 10**9
tpj = int(sys.argv[7]) if len(sys.argv) > 7 else 1
kmax = int(sys.argv[8]) if len(sys.argv) > 8 else 200
os.chdir(os.path.expanduser('~/p196_run/r14a'))
table = json.load(open('class/classes.json'))
jobs = []
for rec in table:
    if rec['T'] < 256:
        continue
    if filt != 'all' and str(rec['id']) not in filt.split(','):
        continue
    if rec['T'] > maxT:
        continue
    for oc in rec['orbit_classes']:
        jobs.append((rec['T'], rec['id'], oc[0], rec['rep'], rec['L']))
jobs.sort(key=lambda x: (x[0], x[1], x[2]))
print('jobs', len(jobs), flush=True)
lock = threading.Lock()
done = []
next_i = [0]
mcmd = 'runscc' if mode == 'scc' else 'run'
def worker():
    while True:
        with lock:
            if next_i[0] >= len(jobs):
                return
            T, cid, o, rep, L = jobs[next_i[0]]
            next_i[0] += 1
        name = f'sw_{mode}_c{cid}_o{o}'
        logf = f'logs/{name}.log'
        st = f'logs/{name}.status'
        if os.path.exists(st) and 'rc=0' in open(st).read():
            continue
        t0 = time.time()
        env = dict(os.environ, R14_RSS_GB=str(rss), R14_SEC=str(sec))
        cmd = ['perl', '-e', 'alarm shift; exec @ARGV', str(int(sec) + 300), './bin_mc14a', mcmd, rep, str(o), str(kmax), str(tpj), '1']
        with open(logf, 'w') as f:
            f.write('# cmd ' + ' '.join(cmd) + '\n'); f.flush()
            rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, env=env)
        el = time.time() - t0
        txt = open(logf, errors='ignore').read()
        status = 'EMPTY' if 'EMPTY at' in txt else ('BUDGET' if 'BUDGET' in txt else 'OTHER')
        exact = txt.count('PERIODIC exact orbit') + txt.count('# exact orbit')
        ks = [l for l in txt.splitlines() if l.startswith('K ')]
        kmaxrun = ks[-1].split()[1] if ks else '-'
        peak = max((int(l.split()[3]) for l in ks), default=0)
        line = f'{mode} class {cid} L={L} T={T} orbit {o} rep {os.path.basename(rep)} rc={rc} status={status} lastK={kmaxrun} peak={peak} exactlines={exact} time={el:.0f}s'
        with lock:
            with open(f'logs/sweep_{mode}.txt', 'a') as f:
                f.write(line + '\n')
            with open(st, 'w') as f:
                f.write(f'END rc={rc}\n')
threads = [threading.Thread(target=worker) for _ in range(npar)]
for th in threads: th.start()
for th in threads: th.join()
print('sweep done', flush=True)
