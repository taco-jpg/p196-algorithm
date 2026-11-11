import re, glob, os, collections, sys
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
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
            res[(mode,clk,V,int(T),int(M),int(tau),int(R))].append(st)
for clk in ['1000','10','00001110001']:
    lp=set(); rp=set(); rs=set(); lall=set(); rall=set()
    for (mode,c,V,T,M,tau,R),sts in res.items():
        if c!=clk: continue
        if mode=='L' and M==1 and tau==0 and R==12:
            if 'PASS' in sts: lp.add(V)
            if 'ALLUNSAT' in sts: lall.add(V)
        if mode=='R':
            if 'PASS' in sts: rp.add(V)
            if 'ALLUNSAT' in sts: rall.add(V)
        if mode=='R*' and 'PASS' in sts: rs.add(V)
    print(clk,'L PASS',len(lp),'R PASS',len(rp),'L&R',len(lp&rp),'L&R&R*-PASS',len(lp&rp&rs),'L-ALLUNSAT',len(lall),'R-ALLUNSAT',len(rall))
