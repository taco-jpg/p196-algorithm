#!/usr/bin/env python3
"""Compile chunk modules with at most 2 concurrent lean processes (6 GB cap each)."""
import json, subprocess, os, time, sys
mods=json.load(open(sys.argv[1] if len(sys.argv)>1 else "chunk_modules.json"))
env=dict(os.environ, LEAN_PATH=os.getcwd())
running=[]; failed=[]; t0=time.time()
def start(m):
    log=open(m+".log","w")
    p=subprocess.Popen(["bash","-c",f"ulimit -v 6000000; exec lean -o {m}.olean {m}.lean"],env=env,stdout=log,stderr=subprocess.STDOUT)
    return (m,p,time.time())
queue=list(mods)
while queue or running:
    while queue and len(running)<2: running.append(start(queue.pop(0)))
    time.sleep(0.5)
    for r in list(running):
        m,p,ts=r
        if p.poll() is not None:
            running.remove(r)
            print(f"{m} exit={p.returncode} {time.time()-ts:.1f}s", flush=True)
            if p.returncode: failed.append(m)
print("FAILED:",failed," total %.0fs"%(time.time()-t0))
sys.exit(1 if failed else 0)
