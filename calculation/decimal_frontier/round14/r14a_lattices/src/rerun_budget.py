#!/usr/bin/env python3
"""rerun_budget.py (r14a): rerun (mode scc or run) all (class, orbit) jobs whose sweep result was BUDGET, in increasing T, with larger caps.
usage: rerun_budget.py MODE RSSGB SEC THREADS_PER_JOB WORKERS [kmax] [maxjobs]
Results appended to logs/rerun_<mode>.txt; logs logs/rr_<mode>_c<id>_o<o>.log"""
import sys, os, re, json, subprocess, time, threading
os.chdir(os.path.expanduser('~/p196_run/r14a'))
mode, rss, sec, thr, workers = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
kmax = sys.argv[6] if len(sys.argv) > 6 else '120'
maxjobs = int(sys.argv[7]) if len(sys.argv) > 7 else 10**9
tab = json.load(open('class/classes.json'))
sweep = f'logs/sweep_{mode}.txt'
rrf = f'logs/rerun_{mode}.txt'
done = set()
if os.path.exists(rrf):
    for ln in open(rrf):
        m = re.match(r'(\w+) class (\d+) .* orbit (\d+)', ln)
        if m: done.add((int(m.group(2)), int(m.group(3))))
if os.environ.get('R14_FORCE'):
    done=set()
jobs = []
seen = set()
for ln in open(sweep):
    m = re.match(r'(scc|run) class (\d+) L=(\d+) T=(\d+) orbit (\d+) rep (\S+) rc=(-?\d+) status=(\w+)', ln)
    if not m: continue
    cid, L, T, o, rep, rc, st = int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), m.group(6), m.group(7), m.group(8)
    if st != 'BUDGET': continue
    if (cid, o) in seen or (cid, o) in done: continue
    seen.add((cid, o))
    jobs.append((T, cid, o, tab[cid]['rep'], L))
jobs.sort()
if os.environ.get('R14_ONLY'):
    only=set(tuple(map(int,l.split())) for l in open(os.environ['R14_ONLY']) if l.strip())
    jobs=[j for j in jobs if (j[1],j[2]) in only]
jobs = jobs[:maxjobs]
print('jobs', len(jobs), flush=True)
lock = threading.Lock(); nxt = [0]
mcmd = 'runscc' if mode == 'scc' else 'run'
def worker():
    while True:
        with lock:
            if nxt[0] >= len(jobs): return
            T, cid, o, rep, L = jobs[nxt[0]]; nxt[0] += 1
        name = f'rr_{mode}_c{cid}_o{o}'
        logf = f'logs/{name}.log'
        env = dict(os.environ, R14_RSS_GB=rss, R14_SEC=sec)
        t0 = time.time()
        with open(logf, 'w') as f:
            rc = subprocess.call(['perl', '-e', 'alarm shift; exec @ARGV', str(int(float(sec)) + 300), './bin_mc14a', mcmd, rep, str(o), kmax, thr, '1'], stdout=f, stderr=subprocess.STDOUT, env=env)
        el = time.time() - t0
        txt = open(logf, errors='ignore').read()
        status = 'EMPTY' if 'EMPTY at' in txt else ('BUDGET' if 'BUDGET' in txt else 'OTHER')
        ks = [l for l in txt.splitlines() if l.startswith('K ')]
        peak = max((int(l.split()[3]) for l in ks), default=0)
        lastK = ks[-1].split()[1] if ks else '-'
        exact = txt.count('PERIODIC') + txt.count('# exact orbit')
        line = f'{mode} class {cid} L={L} T={T} orbit {o} rep {os.path.basename(rep)} rc={rc} status={status} lastK={lastK} peak={peak} exactlines={exact} time={el:.0f}s rss={rss}'
        with lock:
            with open(rrf, 'a') as f:
                f.write(line + '\n')
ths = [threading.Thread(target=worker) for _ in range(workers)]
for th in ths: th.start()
for th in ths: th.join()
print('rerun done', flush=True)
