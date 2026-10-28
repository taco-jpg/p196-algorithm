#!/usr/bin/env python3
"""Split a merged census DB into one file per p:  split_db.py IN.jsonl OUTDIR   ->  OUTDIR/b10_p{p}.jsonl  (best record per word: decisive > larger cap)."""
import sys,json,os,collections
inp,outdir=sys.argv[1],sys.argv[2]; os.makedirs(outdir,exist_ok=True)
def score(r):
    if r['status'] in('EXHAUSTED','ACCEPT'): return (2,0,0)
    return (1, r.get('cap',0) if r['status']=='CAPPED_states' else 0, r.get('depth',0))
best={}
for l in open(inp):
    try: r=json.loads(l)
    except: continue
    k=(r['b'],r['p'],r['g']); o=best.get(k)
    if o is None or score(r)>=score(o): best[k]=r
byp=collections.defaultdict(list)
for k,r in best.items(): byp[(r['b'],r['p'])].append(r)
for (b,p),rs in sorted(byp.items()):
    rs.sort(key=lambda r:(r['G'],r['g']))
    with open(os.path.join(outdir,f'b{b}_p{p}.jsonl'),'w') as fo:
        for r in rs: fo.write(json.dumps(r)+'\n')
    print(f'b={b} p={p}: {len(rs)} words')
