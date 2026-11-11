#!/usr/bin/env python3
"""r12g RSS watchdog: every 20 s sum the RSS of all processes whose command line contains /r12g/ (except this
watchdog and ssh/shell wrappers); if the sum exceeds LIMIT_GB kill the largest one (SIGKILL) and log it.
Also logs the number of busy r12g processes.  Exits when no r12g compute process has existed for 60 minutes.
usage: watchdog.py [LIMIT_GB]"""
import os, sys, time, signal, subprocess
LIMIT = float(sys.argv[1]) if len(sys.argv) > 1 else 46.0
here = os.path.dirname(os.path.abspath(__file__))
log = open(os.path.join(here, "watchdog.log"), "a")
idle_since = None; peak = 0.0
while True:
    out = subprocess.run(["ps", "-Ao", "pid=,pgid=,rss=,pcpu=,command="], capture_output=True, text=True).stdout
    procs = []
    for line in out.split("\n"):
        p = line.split(None, 4)
        if len(p) < 5: continue
        pid, pgid, rss, cpu, cmd = int(p[0]), int(p[1]), int(p[2]), float(p[3]), p[4]
        if "/r12g/" in cmd and "watchdog" not in cmd and not cmd.startswith(("bash", "sh ", "zsh", "/bin/sh", "/bin/bash", "/bin/zsh", "tail", "grep", "ps ")):
            procs.append((rss / 1048576.0, pid, pgid, cpu, cmd))
    tot = sum(x[0] for x in procs); peak = max(peak, tot)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if procs: idle_since = None
    elif idle_since is None: idle_since = time.time()
    elif time.time() - idle_since > 3600:
        log.write(f"{now} no r12g jobs for 60 min, exit (peak {peak:.1f} GB)\n"); log.flush(); break
    if tot > LIMIT and procs:
        big = max(procs)
        try: os.kill(big[1], signal.SIGKILL)
        except Exception as e: log.write(f"{now} kill failed {e}\n")
        log.write(f"{now} total {tot:.1f} GB > {LIMIT} GB: killed pid {big[1]} ({big[0]:.1f} GB) {big[4][:200]}\n"); log.flush()
    with open(os.path.join(here, "watchdog.state"), "w") as f:
        f.write(f"{now} n={len(procs)} total={tot:.1f}GB peak={peak:.1f}GB cpu={sum(x[3] for x in procs):.0f}% limit={LIMIT}\n")
        for x in sorted(procs, reverse=True)[:12]: f.write(f"  {x[0]:.2f}GB {x[3]:.0f}% {x[4][:150]}\n")
    time.sleep(20)
