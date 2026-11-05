#!/usr/bin/env python3
"""r11d summary.  Wire (9-wire exterior) status per word = best over out/db (bx3) and out/dbB (bxb, same BFS);
band status only from out/dbB (bxb).  Writes out/residue_wire.txt, out/residue_band.txt and prints the funnel.
usage: report_r11d.py"""
import json,glob,re,collections,os
DEC=('EXHAUSTED','ACCEPT')
def load(files):
    db={}
    for f in files:
        for l in open(f):
            try: r=json.loads(l)
            except: continue
            k=(r['p'],r['g']); o=db.get(k)
            if o and o['status'] in DEC: continue
            if o and r['status'].startswith('CAPPED') and o.get('cap',0)>r.get('cap',0): continue
            db[k]=r
    return db
W=load(sorted(glob.glob('out/db/b10_p*.jsonl')))
Bd=load(sorted(glob.glob('out/dbB/b10_p*.jsonl')))
allk=set(W)|set(Bd)
def root(g):
    p=len(g)
    for d in range(1,p+1):
        if p%d==0 and g[:d]*(p//d)==g: return d
print('p  words  wire:EXH ACC CAP | band-checked:decided CAP hits | maxcap(capped)')
rw=open('out/residue_wire.txt','w'); rb=open('out/residue_band.txt','w')
for p in sorted({k[0] for k in allk}):
    ks=[k for k in allk if k[0]==p]
    c=collections.Counter(); bc=collections.Counter(); hits=[]; mc=0
    for k in ks:
        a=W.get(k); b=Bd.get(k)
        st=[x['status'] for x in (a,b) if x]
        ws='ACCEPT' if 'ACCEPT' in st else ('EXHAUSTED' if 'EXHAUSTED' in st else 'CAPPED')
        c[ws]+=1
        if ws=='CAPPED':
            caps=[x.get('cap',0) for x in (a,b) if x]; mc=max(mc,max(caps))
            rw.write(f"{p} {k[1]} G={k[1].count('1')} root={root(k[1])} cap={max(caps)}\n")
        if b:
            if b['status'] in DEC: bc['dec']+=1
            else: bc['cap']+=1; rb.write(f"{p} {k[1]} G={k[1].count('1')} root={root(k[1])} cap={b.get('cap')}\n")
            if b.get('band'): hits.append((k[1],b['band']))
    print(f"{p:2d} {len(ks):8d}  {c['EXHAUSTED']:8d} {c['ACCEPT']:3d} {c['CAPPED']:5d} | {bc['dec']:8d} {bc['cap']:5d} {len(hits):3d} | {mc}")
    for h in hits: print('   BANDHIT',p,h)
