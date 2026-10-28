#!/usr/bin/env python3
"""Q2d: for every exterior cycle (g,e) with p<=PM in base b (bauto4), test the centre for k=1 (G even) or k=2 (G odd) laps and optionally k=2,3 more, with cauto_fast (all widths).
usage: q2d.py base PM tmo kmax"""
import sys, subprocess, re, time, os
b=int(sys.argv[1]); PM=int(sys.argv[2]); TMO=int(sys.argv[3]); KMAX=int(sys.argv[4])
D="/home/claude/research/w2_theory"
gl=f"/tmp/q2d_gl_{b}.txt"
subprocess.run(f"{D}/own/gamlist {b} 1 {PM} emit > {gl}",shell=True)
r=subprocess.run(f"ulimit -v 1500000; timeout 25 {D}/own/bauto4 {b} {gl} -cap 300000 2>/dev/null",shell=True,capture_output=True,text=True)
streams=[]
for l in r.stdout.splitlines():
    m=re.search(r"p=(\d+) g=([01]+) e=([01]+)",l)
    if m: streams.append((int(m[1]),m[2],m[3]))
seen=set()
for p,g,e in streams:
    G=g.count('1')
    # primitive in the pair (g,e)? skip exact repeats of a shorter pair to avoid duplicates
    prim=True
    for d in range(1,p):
        if p%d==0 and g[:d]*(p//d)==g and e[:d]*(p//d)==e: prim=False
    if not prim: continue
    for k in range(1,KMAX+1):
        if (G*k)%2 or p*k>32: continue
        t0=time.time()
        try:
            rr=subprocess.run(['sh','-c',f'ulimit -v 2000000; exec {D}/bin/cauto_fast {b} {e*k} {g*k} 1 1 -vall -allm -sym -cap 2000000'],capture_output=True,text=True,timeout=TMO)
            st={}
            for l in rr.stdout.splitlines():
                mm=re.search(r"^DONE .*status=(\w+)",l)
                if mm: st[mm[1]]=st.get(mm[1],0)+1
            summ=' '.join(f"{a}={c}" for a,c in sorted(st.items()))
        except subprocess.TimeoutExpired:
            summ='TIMEOUT'
        print(f"b={b} p0={p} G0={G} g={g} e={e} k={k}: {summ} ({time.time()-t0:.1f}s)",flush=True)
        if 'hit' in summ: break
