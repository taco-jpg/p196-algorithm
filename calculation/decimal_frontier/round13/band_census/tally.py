#!/usr/bin/env python3
"""r13a: print a compact tally of all results (for the FINAL.md summary)."""
import sys, re, glob, os, collections
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
ROOT=os.path.expanduser('~/p196_run/r13a')
res=collections.defaultdict(list)
for d in glob.glob(ROOT+'/logs/*'):
    if not os.path.isdir(d): continue
    for f in glob.glob(d+'/i*.log'):
        for line in open(f):
            if not line.startswith('BANDRESULT'): continue
            m=re.match(r'BANDRESULT (\S+) b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+)(?: Tprime=\d+)? tau=(\d+) R=(\d+) Rfree=(\d+) solver=(\w+) enc=(\d) : rots=(\S+) status=(\w+)',line)
            if not m: continue
            mode,b,clk,V,T,M,tau,R,Rf,solver,enc,rots,st=m.groups()
            res[(mode,clk,V,int(T),int(M),int(tau))].append((st,rots,solver,enc,os.path.basename(d)))
CL=['1000','10','00001110001']
for clk in CL:
    bands={B['V']:B for B in MK.parse(clk,8)}
    print(f'--- clock {clk}: {len(bands)} bands')
    # L M=1 tau=0
    lres={}
    for (mode,c,V,T,M,tau),rs in res.items():
        if c==clk and mode=='L' and M==1 and tau==0:
            lres[V]=[r[0] for r in rs]
    cnt=collections.Counter()
    for V,B in bands.items():
        st=lres.get(V)
        if st is None:
            cnt['NOTRUN(T=%d..)'%(0 if B['T']<=120 else 1)]+=1
        elif 'ALLUNSAT' in st: cnt['ALLUNSAT']+=1
        elif 'PASS' in st: cnt['PASS']+=1
        else: cnt['UNDEC']+=1
    print(' L(M=1,tau=0):',dict(cnt))
    # by T buckets for bands with T<=120
    # L* results
    excl=set(V for (mode,c,V,T,M,tau),rs in res.items() if c==clk and mode.startswith('L') and any(r[0]=='ALLUNSAT' for r in rs))
    print(' bands with some ALLUNSAT at (M,tau) in L/L*:',len(excl))
    ls=[(V,M,tau,mode) for (mode,c,V,T,M,tau),rs in res.items() if c==clk and mode.startswith('L') and (M>1 or tau>0)]
    print(' multi-epoch/tau records:',len(ls))
    # R
    rres={}
    for (mode,c,V,T,M,tau),rs in res.items():
        if c==clk and mode=='R': rres[V]=(M,[r[0] for r in rs])
    cntR=collections.Counter()
    for V,B in bands.items():
        if V not in rres: cntR['NOTRUN']+=1
        else:
            st=rres[V][1]
            cntR['ALLUNSAT' if 'ALLUNSAT' in st else ('PASS' if 'PASS' in st else 'UNDEC')]+=1
    print(' R:',dict(cntR))
    # R*
    rsres={}
    for (mode,c,V,T,M,tau),rs in res.items():
        if c==clk and mode=='R*': rsres[V]=(M,[r[0] for r in rs])
    cntRs=collections.Counter()
    for V,(M,st) in rsres.items():
        cntRs['ALLUNSAT' if 'ALLUNSAT' in st else ('PASS' if 'PASS' in st else 'UNDEC')]+=1
    print(' R*:',dict(cntRs))
