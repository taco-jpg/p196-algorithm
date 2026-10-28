#!/usr/bin/env python3
"""Summarise census DB(s): funnel by p (and p,G), capped / accepted list.
usage: summarize.py [b] [--g] [--files F1 F2 ...]        (default file: $DB or out/db_b{b}.jsonl; with --files, e.g.  out/db/b10_p*.jsonl)"""
import json,sys,re,collections,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args=sys.argv[1:]
b=int(args[0]) if args and args[0].isdigit() else 10
files=[os.environ.get('DB') or f'{ROOT}/out/db_b{b}.jsonl']
if '--files' in args: files=args[args.index('--files')+1:]
DEC=('EXHAUSTED','ACCEPT')
db={}      # (p,g) -> small tuple (status,G,states,depth,secs,cap,wdone,m,acc)
for f in files:
    for l in open(f):
        try: r=json.loads(l)
        except: continue
        k=(r['p'],r['g']); o=db.get(k)
        if o and o[0] in DEC: continue
        if o and r['status'].startswith('CAPPED') and o[5]>r.get('cap',0): continue
        db[k]=(r['status'],r['G'],r['states'],r['depth'],r['secs'],r.get('cap',0),r.get('wdone'),r.get('m'),tuple(r.get('acc',[])))
F1={}; byG={}
for l in open(f'{ROOT}/out/fc_counts_b{b}.txt'):
    m=re.match(r'p=(\d+) total_necklaces=(\d+)\s+byG:(.*)',l)
    if m:
        F1[int(m[1])]=int(m[2]); byG[int(m[1])]={int(a):int(c) for a,c in re.findall(r'(\d+):(\d+)',m[3])}
ps=sorted({p for p,g in db})
print('p   F1-surv   in-DB  EXHAUSTED  ACCEPT  CAPPED   maxstates(exh)  sumsecs')
tot=collections.Counter()
for p in ps:
    rs=[r for (pp,g),r in db.items() if pp==p]
    c=collections.Counter(r[0].split('_')[0] for r in rs)
    ms=max([r[2] for r in rs if r[0]=='EXHAUSTED']+[0]); ss=sum(r[4] for r in rs)
    print(f"{p:2d} {F1.get(p,0):9d} {len(rs):7d} {c['EXHAUSTED']:9d} {c['ACCEPT']:7d} {c['CAPPED']:7d} {ms:14d} {ss:9.0f}")
    tot.update(c)
print('TOTAL',dict(tot))
if '--g' in args:
    print('\nby (p,G): EXHAUSTED/ALL words  [c = capped, A = accepted]')
    for p in ps:
        row=[]
        for G in sorted(byG.get(p,{})):
            rs=[r for (pp,g),r in db.items() if pp==p and r[1]==G]
            ne=sum(r[0]=='EXHAUSTED' for r in rs); nc=sum(r[0].startswith('CAPPED') for r in rs); na=sum(r[0]=='ACCEPT' for r in rs)
            row.append(f"G{G}:{ne}/{len(rs)}"+(f"[{nc}c]" if nc else '')+(f"[{na}A]" if na else ''))
        print(f'p={p}: '+' '.join(row))
print('\nCAPPED / ACCEPT words:')
for (p,g),r in sorted(db.items(),key=lambda kv:(kv[0][0],kv[1][1],kv[0][1])):
    if r[0]!='EXHAUSTED':
        print(f"p={p} G={r[1]} {g} {r[0]} states={r[2]} depth={r[3]} wdone={r[6]} m={r[7]} cap={r[5]} acc={list(r[8])}")
