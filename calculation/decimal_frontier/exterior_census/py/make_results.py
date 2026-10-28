#!/usr/bin/env python3
"""Markdown results section from the census DB.  usage: make_results.py [--files F...]  (default out/db_b10.jsonl)"""
import json,sys,re,os,collections
from math import comb,gcd
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args=sys.argv[1:]; files=[os.environ.get('DB') or f'{ROOT}/out/db_b10.jsonl']
if '--files' in args: files=args[args.index('--files')+1:]
def phi(n): return sum(1 for k in range(1,n+1) if gcd(k,n)==1)
def neck(p,G): return sum(phi(d)*comb(p//d,G//d) for d in range(1,gcd(p,G)+1) if p%d==0 and G%d==0)//p
def neck_all(p): return sum(phi(d)*2**(p//d) for d in range(1,p+1) if p%d==0)//p
DEC=('EXHAUSTED','ACCEPT'); db={}
for f in files:
    for l in open(f):
        try: r=json.loads(l)
        except: continue
        k=(r['p'],r['g']); o=db.get(k)
        if o and o['status'] in DEC: continue
        if o and r['status'].startswith('CAPPED') and o.get('cap',0)>r.get('cap',0): continue
        db[k]=r
F1={}; byG={}
for l in open(f'{ROOT}/out/fc_counts_b10.txt'):
    m=re.match(r'p=(\d+) total_necklaces=(\d+)\s+byG:(.*)',l)
    if m: F1[int(m[1])]=int(m[2]); byG[int(m[1])]={int(a):int(c) for a,c in re.findall(r'(\d+):(\d+)',m[3])}
ps=sorted({p for p,g in db})
print('| p | all necklaces | with 2G<=p<=4G | F1 survivors (NFA) | EXHAUSTED | ACCEPT | CAPPED = UNDECIDED |')
print('|--:|--:|--:|--:|--:|--:|--:|')
for p in ps:
    rs=[r for (pp,g),r in db.items() if pp==p]
    c=collections.Counter(r['status'].split('_')[0] for r in rs)
    nb=sum(neck(p,G) for G in range(-(-p//4),p//2+1))
    print(f"| {p} | {neck_all(p):,} | {nb:,} | {F1.get(p,0):,} | {c['EXHAUSTED']:,} | {c['ACCEPT']} | {c['CAPPED']} |")
print()
print('By (p,G): decided/F1-survivors, [c] = capped words\n')
for p in ps:
    if p<16: continue
    row=[]
    for G in sorted(byG.get(p,{})):
        rs=[r for (pp,g),r in db.items() if pp==p and r['G']==G]
        nd=sum(r['status'] in DEC for r in rs); nc=sum(r['status'].startswith('CAPPED') for r in rs)
        row.append(f"G{G}: {nd}/{len(rs)}"+(f" [{nc}c]" if nc else ''))
    print(f'* p={p}: '+'; '.join(row))
print()
print('Accepted streams (all are repetitions of the known p11 / p12 streams, see py/check_accepts.py):\n')
for (p,g),r in sorted(db.items()):
    if r['status']=='ACCEPT' or r.get('acc'): print(f"* p={p} g={g} status={r['status']} e={r.get('acc')} states={r['states']} depth={r['depth']}")
print()
print('UNDECIDED (CAPPED) words; `wdone` = B-positions completely processed (no cycle of width <= wdone); cap in visited states (quotient states if m>1):\n')
print('| p | G | word g | m | cap | states | depth reached | wdone |')
print('|--:|--:|---|--:|--:|--:|--:|--:|')
n=0
for (p,g),r in sorted(db.items(),key=lambda kv:(kv[0][0],kv[1]['G'],kv[0][1])):
    if r['status'].startswith('CAPPED'):
        n+=1; print(f"| {p} | {r['G']} | `{g}` | {r.get('m','')} | {r.get('cap',0):,} | {r['states']:,} | {r['depth']} | {r.get('wdone','')} |")
print(f'\n(total {n} undecided words)')
