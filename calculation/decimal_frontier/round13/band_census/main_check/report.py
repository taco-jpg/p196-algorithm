#!/usr/bin/env python3
import json, os, re, collections, sys
H=os.path.expanduser('~/p196_run')
print('== census recount vs r13a (primitive bands up to rotation)')
clocks=['1000','10','00001110001']
tot=collections.Counter(); totr=collections.Counter(); diff=0
for G in clocks:
    for s in range(1,9):
        fn=f'{H}/mchk13a/logs/bc_{G}_s{s}.txt'
        if not os.path.exists(fn): print('missing',fn); continue
        head=open(fn).readline()
        m=re.search(r'rotation (\d+)',head)
        mine=int(m[1]) if m else -1
        rf=f'{H}/r13a/census/b{G}_s{s}.txt'
        r=sum(1 for l in open(rf) if l.startswith('BAND'))
        # compare band sets too (canonical words + T)
        mset={}
        for l in open(fn):
            if l.startswith('BAND'):
                t=l.split(); mset[t[1]]=int(t[2][2:])
        rset=[]
        for l in open(rf):
            mm=re.match(r'BAND s=\d+ T=(\d+) .* V=([\d,]+)',l)
            if mm: rset.append((mm[2],int(mm[1])))
        same = 'n/a'
        if mset:
            # compare multisets of T only (the representatives may be different rotations)
            same = sorted(mset.values())==sorted(x[1] for x in rset)
        tot[G]+=mine; totr[G]+=r
        if mine!=r or same is False: diff+=1
        print(G,'s',s,'mine',mine,'r13a',r,'T-multiset equal:',same)
    print('  total',G,'mine',tot[G],'r13a',totr[G])
print('differences:',diff)
print('== band centre scan')
for G,fn in [('1000','scan_1000'),('10','scan_10'),('p11','scan_p11')]:
    p=f'{H}/mchk13a/logs/{fn}.jsonl'
    if not os.path.exists(p): continue
    R=[json.loads(l) for l in open(p)]
    closed=0; withper=[]; openb=[]
    for r in R:
        orbs=r['orbits']
        if any(o['nper'] for o in orbs): withper.append(r)
        if all(o['empty'] for o in orbs): closed+=1
        else: openb.append(r)
    print(f'clock {G}: bands scanned {len(R)}; all orbits closed (no centre at depth beyond the listed exact ones) {closed}; some orbit not closed in the time limit {len(openb)}; bands with exact periodic orbits {len(withper)}')
    for r in withper:
        s=' | '.join(f"o{o['o']}: E{o['empty']} nper{o['nper']} "+';'.join('K%s per%s %s'%(x[0],x[2],x[6].strip()) for x in o['periodic'][:3]) for o in r['orbits'] if o['nper'])
        print('  ',r['V'],'T',r['T'],s[:380])
