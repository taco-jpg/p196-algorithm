#!/usr/bin/env python3
"""r13a: charge analysis: band charge Q = sum(V) - 9s over a row; compare with L status."""
import sys, re, glob, os, collections
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK, bandsat as BS
ROOT=os.path.expanduser('~/p196_run/r13a')
status={}
for d in glob.glob(ROOT+'/logs/*'):
    if not os.path.isdir(d): continue
    for f in glob.glob(d+'/i*.log'):
        for line in open(f):
            if not line.startswith('BANDRESULT'): continue
            m=re.match(r'BANDRESULT (\S+) b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+)(?: Tprime=\d+)? tau=(\d+) R=(\d+) Rfree=(\d+) solver=(\w+) enc=(\d) : rots=(\S+) status=(\w+)',line)
            if not m: continue
            mode,b,clk,V,T,M,tau,R,Rf,solver,enc,rots,st=m.groups()
            if mode=='L' and M=='1' and tau=='0' and R=='12':
                status[(clk,V)]=(st,rots)
out=collections.Counter()
for clk in ['1000','10','00001110001']:
    cl=[int(c) for c in clk]; p=len(cl)
    for B in MK.parse(clk,8):
        V=[int(x) for x in B['V'].split(',')]
        s=len(V); T=B['T']
        # charge of row V and of all rows over one F-cycle
        x=list(V); charges=[]
        qs=set()
        t=0
        for t in range(T):
            qs.add(sum(x)-9*s)
            y,*_=BS.rowstep(x,cl[t%p],10)
            x=y
        st=status.get((clk,B['V']),('none',''))
        cz=(0 in qs and len(qs)==1)
        allzero='charge0-all-rows' if cz else ('charge0-some' if 0 in qs else 'nonzero')
        out[(clk,allzero,st[0])]+=1
        if st[0]=='ALLUNSAT' or cz and st[0] not in ('none',):
            print(clk,'s=',s,'T=',T,'V=',B['V'],'charges(over rows)=',sorted(qs)[:6],'L=',st, flush=True)
print()
for k,v in sorted(out.items()):
    print(k,v)
