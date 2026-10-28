#!/usr/bin/env python3
"""Merge census DBs (jsonl).  usage: merge_db.py OUT.jsonl IN1.jsonl IN2.jsonl ...   (OUT may also be one of the inputs)
Per (p,g): a decisive record (EXHAUSTED/ACCEPT) beats everything; otherwise keep the CAPPED record with the largest cap
(CAPPED_states: cap; CAPPED_time: sec) -- ties: the one that got furthest (depth).  Output sorted by (p,G,g).
Memory-light: keeps raw lines + a small score tuple per word."""
import sys,json
out=sys.argv[1]; best={}
def score(r):
    if r['status'] in('EXHAUSTED','ACCEPT'): return (2,0,0)
    return (1, r.get('cap',0) if r['status']=='CAPPED_states' else 0, r.get('depth',0))
n=0
for f in sys.argv[2:]:
    try: fh=open(f)
    except FileNotFoundError: continue
    for l in fh:
        try: r=json.loads(l)
        except: continue
        n+=1; k=(r['p'],r['g']); sc=score(r); o=best.get(k)
        if o is None or sc>=o[0]: best[k]=(sc,r['G'],l if l.endswith('\n') else l+'\n')
tmp=out+'.tmp'
with open(tmp,'w') as fo:
    for k in sorted(best,key=lambda k:(k[0],best[k][1],k[1])): fo.write(best[k][2])
import os; os.replace(tmp,out)
print(f'{n} records -> {len(best)} words in {out}')
