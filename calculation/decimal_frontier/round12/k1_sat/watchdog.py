#!/usr/bin/env python3
"""r12d global RSS watchdog: every 30 s sum the RSS of all r12d compute processes (python processes whose command
line contains tsrun.py / wallscan.py / survscan.py / retsat.py / survall.py / verify_hit.py and whose cwd is r12d);
if the sum exceeds LIMIT_GB, kill the process group of the largest one and log it (watchdog.log), and append a
KILLED line to its log if the log path can be found.  Exits when no such process has existed for 30 minutes.
usage: watchdog.py [LIMIT_GB]"""
import os, sys, time, signal, subprocess
LIMIT = float(sys.argv[1]) if len(sys.argv) > 1 else 39.0
here = os.path.dirname(os.path.abspath(__file__))
KEYS = ('tsrun.py', 'wallscan.py', 'survscan.py', 'retsat.py', 'survall.py', 'verify_hit.py')
log = open(os.path.join(here, 'watchdog.log'), 'a')
idle_since = None
while True:
    out = subprocess.run(['ps', '-Ao', 'pid=,pgid=,rss=,command='], capture_output=True, text=True).stdout
    procs = []
    for line in out.split('\n'):
        p = line.split(None, 3)
        if len(p) < 4: continue
        pid, pgid, rss, cmd = int(p[0]), int(p[1]), int(p[2]), p[3]
        if any(k in cmd for k in KEYS) and 'watchdog' not in cmd:
            procs.append((rss / 1048576.0, pid, pgid, cmd))
    tot = sum(x[0] for x in procs)
    now = time.strftime('%Y-%m-%dT%H:%M:%S')
    if procs: idle_since = None
    elif idle_since is None: idle_since = time.time()
    elif time.time() - idle_since > 1800:
        log.write(f'{now} no r12d jobs for 30 min, exit\n'); log.flush(); break
    if tot > LIMIT and procs:
        big = max(procs)
        try: os.killpg(big[2], signal.SIGKILL)
        except Exception: os.kill(big[1], signal.SIGKILL)
        log.write(f'{now} total {tot:.1f} GB > {LIMIT} GB: killed pgid {big[2]} ({big[0]:.1f} GB) {big[3][:160]}\n'); log.flush()
    with open(os.path.join(here, 'watchdog.state'), 'w') as f:
        f.write(f'{now} n={len(procs)} total={tot:.1f}GB limit={LIMIT}\n')
    time.sleep(30)
