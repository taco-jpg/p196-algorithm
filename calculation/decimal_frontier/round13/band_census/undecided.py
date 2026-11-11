#!/usr/bin/env python3
"""r13a: list UNDECIDED/NOTRUN status per clock for FINAL.md sec. 8."""
import re, glob, os, collections, sys
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
ROOT=os.path.expanduser('~/p196_run/r13a')
res=collections.defaultdict(list)
for d in glob.glob(ROOT+'/logs/*'):
    if not os.path.isdir(d): continue
    for f in glob.glob(d+'/i*.log'):
        for line in open(f):
            if not line.startswith('BANDRESULT'): continue
            m=re.match(r'BANDRESULT (\S+) b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+)(?: Tprime=(\d+))? tau=(\d+) R=(\d+) Rfree=(\d+) solver=(\w+) enc=(\d) : rots=(\S+) status=(\w+)',line)
            if not m: continue
            mode,b,clk,V,T,M,TP,tau,R,Rf,solver,enc,rots,st=m.groups()
            res[(mode,clk,V,int(M),int(tau),int(R))].append((st,rots))
print('## 8.1 Per-clock status of the census bands (generated)\n')
for clk in ['1000','10','00001110001']:
    bands=MK.parse(clk,8)
    notL=[];undL=[];okL=0
    notR=[];undR=[]
    for B in bands:
        V=B['V']
        l=[s for k,v in res.items() if k[0]=='L' and k[1]==clk and k[2]==V and k[3]==1 and k[4]==0 and k[5]==12 for s in v]
        if not l: notL.append(B)
        elif all(x[0]=='UNDECIDED' for x in l): undL.append((B,l[0][1]))
        r=[s for k,v in res.items() if k[0]=='R' and k[1]==clk and k[2]==V for s in v]
        if not r: notR.append(B)
        elif all(x[0]=='UNDECIDED' for x in r): undR.append((B,r[0][1]))
    print(f'**clock {clk}** ({len(bands)} bands).  L(M=1,tau=0,R=12): {len(notL)} not run, {len(undL)} UNDECIDED (all rotations timed out or not decided).  R: {len(notR)} not run, {len(undR)} UNDECIDED.')
    ts=collections.Counter(B['T'] for B in notL)
    print('  not run (T distribution): '+', '.join(f'T={t}x{ts[t]}' for t in sorted(ts)))
    if undL:
        print('  L UNDECIDED: '+'; '.join(f"({B['V']}) T={B['T']} [{rots}]" for B,rots in undL))
    if undR:
        print('  R UNDECIDED: '+'; '.join(f"({B['V']}) T={B['T']} [{rots}]" for B,rots in undR))
    print()
