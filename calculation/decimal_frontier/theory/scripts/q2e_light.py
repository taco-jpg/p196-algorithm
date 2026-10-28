#!/usr/bin/env python3
"""Q2e: all-repetition centre decision with the PR #411 regular-language engine for every exterior (g,e) of a base (p<=PM).
Unit = stream if G even else stream doubled (odd G needs even k).  V = K=G/2 trims spread evenly.
usage: q2e.py base PM tmo"""
import sys, subprocess, re, time, json
b=int(sys.argv[1]); PM=int(sys.argv[2]); TMO=int(sys.argv[3])
D="/home/claude/research/w2_theory"
gl=f"/tmp/q2e_gl_{b}.txt"
subprocess.run(f"{D}/own/gamlist {b} 1 {PM} emit > {gl}",shell=True)
r=subprocess.run(f"ulimit -v 700000; timeout 12 {D}/own/bauto4 {b} {gl} -cap 300000 2>/dev/null",shell=True,capture_output=True,text=True)
for l in r.stdout.splitlines():
    m=re.search(r"p=(\d+) g=([01]+) e=([01]+)",l)
    if not m: continue
    p,g,e=int(m[1]),m[2],m[3]; G=g.count('1')
    prim=all(not(p%d==0 and g[:d]*(p//d)==g and e[:d]*(p//d)==e) for d in range(1,p))
    if not prim: continue
    ug,ue=(g,e) if G%2==0 else (g*2,e*2)
    P=len(ug); GG=ug.count('1'); K=GG//2
    v=['0']*P
    for i in range(K): v[(P-1-(i*P)//K)%P]='1'
    v=''.join(v)
    t0=time.time()
    try:
        rr=subprocess.run(['sh','-c',f'ulimit -v 700000; nice -n 10; exec {D}/own/bin/a113_regular {b} {ue} {ug} {v} --depth 30 --states 250000 --edges 3000000 --ops 150000000 --seconds {TMO}'],capture_output=True,text=True,timeout=TMO+10)
        out=rr.stdout.strip().splitlines()
        last=json.loads(out[-1]) if out else {}
        st=last.get('status','?'); extra=last.get('initial_width','') if st=='CENTER_LANGUAGE_ACCEPTS' else last.get('reason','')
    except Exception as ex:
        st='ERR'; extra=str(ex)[:40]
    print(f"b={b} p0={p} G0={G} g={g} e={e} unit_p={P} v={v}: {st} {extra} ({time.time()-t0:.1f}s)",flush=True)
