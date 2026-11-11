#!/usr/bin/env python3
import os
"""Extract control bands: p8 lattice rows from p8_scc.txt; base-9 w_t rows from the cert JSONs; verify the row map."""
import json, re, sys
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import bandsat as BS
fn=sys.argv[1] if len(sys.argv)>1 else os.path.expanduser('~/p196_run/r13a/ctrl/p8_scc.txt')
txt=open(fn).read()
blocks=re.findall(r'SCC p=8 g=(\d+) size=(\d+) cyclen=(\d+) depth=(\d+) path=(.*?) cyc=(\[.*?\])\n',txt,re.S)
out=[]
for gs,size,cyclen,depth,path,cyc in blocks:
    cols=[[int(x) for x in c.split(',')] for c in re.findall(r'\[([\d,]+)\]',cyc)]
    p=len(cols[0]); m=len(cols)
    clk=[int(ch) for ch in gs]
    # rows V_t[c] = cols[c][t]
    rows=[[cols[c][t] for c in range(m)] for t in range(p)]
    ok=True
    for t in range(p):
        y,_,_,_,_=BS.rowstep(rows[t],clk[t],10)
        if y!=rows[(t+1)%p]: ok=False
    print(f'p8 SCC cyclen={cyclen} size={size} m={m} p={p}: rowmap check {"OK" if ok else "FAIL"}  V0={rows[0]}')
    out.append(dict(clock=gs,T=p,m=m,V0=rows[0],rows=rows,cyclen=int(cyclen),size=int(size)))
json.dump(out,open(os.path.expanduser('~/p196_run/r13a/ctrl/p8_bands.json'),'w'))
for name in ['cert_b9_rec0','cert_b9_rec1']:
    d=json.load(open(os.path.expanduser(f'~/p196_run/r12d/ctrl/{name}.json')))
    b=d['base']; gam=d['gam']; w=d['w_t']; p=d['p']; B_t=d['B_t']
    ok=True
    for t in range(p):
        y,_,_,_,_=BS.rowstep(w[t],gam[t],b)
        if y!=w[(t+1)%p]: ok=False
    print(name,'p',p,'gam',gam,'s',len(w[0]),'w0',w[0],'rowmap',"OK" if ok else "FAIL",'S=',sum(gam),'nB',d['nB'],'B0 tail',B_t[0][-8:])
    # determine the maximal band start in B_0 (band continuation leftwards)
    V=w[0]; n=len(V)
    # phase: band column at index nB has letter V[0] (band starts right after B)
    y=d['nB']
    while y>0 and B_t[0][y-1]==V[(y-1-d['nB'])%n]: y-=1
    print('   band start y* at t=0:',y,'(nB=%d)'%d['nB'],'foreign letter before:',B_t[0][y-1] if y>0 else None,'band coord of y*:',(y-d['nB'])%n)
