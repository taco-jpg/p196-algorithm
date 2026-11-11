#!/usr/bin/env python3
"""r12d job pool with RSS watchdog.  usage: pool.py JOBFILE NPAR [PERJOB_GB] [TOTAL_GB]
JOBFILE lines:  <logfile> <command...>   (lines starting with # ignored; a job whose logfile already has a
'RESULT' or 'DONE' line is skipped, so the pool can be restarted after a network drop).
Each job runs under nice in its own process group; a job whose RSS exceeds PERJOB_GB is killed (logged as
KILLED_RSS); if the summed RSS of running jobs exceeds TOTAL_GB the newest job is killed.  The job file is
re-read whenever a slot frees, so jobs can be appended live.  Writes pool.state (running jobs) and pool.log."""
import os, sys, time, signal, subprocess, shlex

jobfile, npar = sys.argv[1], int(sys.argv[2])
perjob = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0
total = float(sys.argv[4]) if len(sys.argv) > 4 else 38.0
here = os.path.dirname(os.path.abspath(jobfile))
tagn = os.path.splitext(os.path.basename(jobfile))[0]
plog = open(os.path.join(here, f'pool_{tagn}.log'), 'a')

def log(s):
    plog.write(time.strftime('%Y-%m-%dT%H:%M:%S ') + s + '\n'); plog.flush()

def done(logf):
    try:
        with open(logf) as f:
            for l in f:
                if l.startswith('RESULT') or l.startswith('DONE') or l.startswith('KILLED'): return True
    except FileNotFoundError:
        return False
    return False

def rss_tree(pgid):
    """summed RSS (GB) of all processes in the process group"""
    try:
        out = subprocess.run(['ps', '-Ao', 'pgid=,rss='], capture_output=True, text=True).stdout
    except Exception:
        return 0.0
    s = 0
    for line in out.split('\n'):
        p = line.split()
        if len(p) == 2 and int(p[0]) == pgid: s += int(p[1])
    return s / 1048576.0

running = {}   # pgid -> (proc, logf, start)
started = set()
while True:
    jobs = []
    with open(jobfile) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            logf, cmd = line.split(None, 1)
            jobs.append((logf, cmd))
    # reap
    for pg in list(running):
        proc, logf, t0 = running[pg]
        if proc.poll() is not None:
            log(f'END rc={proc.returncode} {time.time()-t0:.0f}s {logf}'); del running[pg]
    # watchdog
    tot = 0.0; sizes = {}
    for pg, (proc, logf, t0) in running.items():
        r = rss_tree(pg); sizes[pg] = r; tot += r
        if r > perjob:
            os.killpg(pg, signal.SIGKILL)
            with open(logf, 'a') as f: f.write(f'KILLED_RSS {r:.1f}GB > {perjob}GB\n')
            log(f'KILL perjob {r:.1f}GB {logf}')
    if tot > total and running:
        pg = max(running, key=lambda g: running[g][2])
        os.killpg(pg, signal.SIGKILL)
        with open(running[pg][1], 'a') as f: f.write(f'KILLED_RSS total {tot:.1f}GB > {total}GB\n')
        log(f'KILL total {tot:.1f}GB {running[pg][1]}')
    with open(os.path.join(here, f'pool_{tagn}.state'), 'w') as f:
        f.write(f'{time.strftime("%Y-%m-%dT%H:%M:%S")} running={len(running)} totalRSS={tot:.1f}GB\n')
        for pg, (proc, logf, t0) in running.items():
            f.write(f'  pgid={pg} rss={sizes.get(pg,0):.2f}GB {time.time()-t0:.0f}s {logf}\n')
    # launch
    pending = [(l, c) for (l, c) in jobs if l not in started and not done(l)]
    while len(running) < npar and pending:
        logf, cmd = pending.pop(0); started.add(logf)
        os.makedirs(os.path.dirname(os.path.abspath(logf)), exist_ok=True)
        fo = open(logf, 'a')
        proc = subprocess.Popen(['nice', '-n', '5'] + shlex.split(cmd), stdout=fo, stderr=subprocess.STDOUT,
                                cwd=here, start_new_session=True)
        running[proc.pid] = (proc, logf, time.time())
        log(f'START pgid={proc.pid} {logf} :: {cmd}')
    if not running and not pending:
        log('POOL EMPTY, exit'); break
    time.sleep(20)
