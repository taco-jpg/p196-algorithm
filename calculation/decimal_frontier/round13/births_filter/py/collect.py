#!/usr/bin/env python3
"""collect.py: summarize tower runs per word directory (KHR / KHR_BULK lines, HIST).  usage: collect.py [dirs...]; prints a markdown table."""
import sys, re, glob, os
root=os.path.expanduser('~/p196_run/r13c/out')
dirs = sys.argv[1:] or ['L16','L24r','L32','L40','L48','L56','N24','N36','N48','N60','CTRL_N12d4','CTRL_p11','CTRL_b9','CTRL_01d4']
rows=[]
for d in dirs:
    files=sorted(glob.glob(os.path.join(root,d,'*.out')))
    if not files: continue
    tot=0; dies=0; surv=0; shards=0; maxk=0; maxn=0; sec=0; emitted=0; ifaces=''; a0=''; births=''; word=''
    hist={}
    tsurv=[]
    for f in files:
        txt=open(f,errors='ignore').read()
        for m in re.finditer(r'^(KHR|KHR_BULK) g=(\S+) d0=(\d+) L=(\d+) interfaces=(\d+) a0=(\d+)(?: births=(\d+))?(?: shard=(\S+))?.*?(?:emitted=(\d+) )?ran=(\d+) dies=(\d+) surv=(\d+).*?secs=([\d.]+)', txt, flags=re.M):
            word=f"{m.group(2)} L={m.group(4)}"; ifaces=m.group(5); a0=m.group(6)
            if m.group(9): emitted+=int(m.group(9))
            tot+=int(m.group(10)); dies+=int(m.group(11)); surv+=int(m.group(12)); sec=max(sec,float(m.group(13))); shards+=1
        for m in re.finditer(r'^HIST(.*)$', txt, flags=re.M):
            for kv in m.group(1).split():
                k,v=kv.split(':'); hist[int(k)]=hist.get(int(k),0)+int(v)
        for m in re.finditer(r'^TSURV.*$', txt, flags=re.M): tsurv.append(m.group(0)[:120])
        for m in re.finditer(r'maxn=(\d+)', txt): maxn=max(maxn,int(m.group(1)))
    maxk=max(hist) if hist else 0
    rows.append((d,word,shards,ifaces,a0,tot,dies,surv,maxk,maxn,sec,hist,tsurv))
print('| dir | word | shards done | interfaces (a0) | towers run | die | survive (cap) | max death level | widest level | max secs |')
print('|---|---|--:|--:|--:|--:|--:|--:|--:|--:|')
for r in rows:
    print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} ({r[4]}) | {r[5]} | {r[6]} | {r[7]} | {r[8]} | {r[9]} | {r[10]:.0f} |")
for r in rows:
    if r[12]:
        print(f"\nSurvivors in {r[0]} ({len(r[12])}):")
        for s in r[12][:20]: print('  ',s)
