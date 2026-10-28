#!/usr/bin/env python3
"""First deviant cell x (all cells below are lattice for all time): enumerate its possible histories over H steps.
Bottom-frame cell identity.  Returns counts per horizon and the number of distinct interface outputs."""
import sys
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from lib7 import *
recs=parse_scc('/home/claude/research/w7_kink/data/p8_scc.txt')
L=Lattice(recs[int(sys.argv[1])]); p=L.p; g=L.g
NB=L.nB
def lat(t,x): return L.cell(t,x)
def lat_asc(t,x):  # steady ascending carry INTO position x at time t
    # compute from B and lattice chain (cached)
    return ASC[t%p][x]
# precompute ascending carries for positions 0..XMAX at each t
XMAX=NB+400
ASC=[]
for t in range(p):
    c=0; arr=[]
    for x in range(XMAX):
        arr.append(c); c=1 if lat(t,x)+c>=10 else 0
    ASC.append(arr)
def lat_desc(t,x):
    """desc carry INTO mirror(x) at time t in the pure lattice: D(x)=[P(x+1)+D(x+1)>=10], scanning up to first non-9."""
    y=x+1
    while True:
        v=lat(t,y)
        if v>=10: return 1
        if v<=8: return 0
        y+=1
def run(x,t0,H):
    # histories: list of (P sequence, D sequence)
    res=[]
    def rec(t,P,Ps,Ds):
        if t==t0+H:
            res.append((tuple(Ps),tuple(Ds))); return
        a=lat_asc(t,x)
        # requirement from lower cell x-1
        r=lat_desc(t,x-1)           # lattice D into mirror(x-1)
        for D in (0,1):
            # D_t(x-1) = [P+D>=10]
            Dlow=1 if P+D>=10 else 0
            if g[t%p]==0:
                if Dlow!=r: continue      # lower cell update uses own D -> must equal lattice
                Pn=(P+a)%10+(P+D)%10
            else:
                # lower cell x-1 (lattice) update uses Odn(x-2): needs D(x-2)=[lat(x-1)+Dlow>=10] to equal lattice
                if lat(t,x-1)==9 and Dlow!=r: continue
                Pn=(P+a)%10+(lat(t,x-1)+Dlow)%10
            if Pn>18: continue
            rec(t+1,Pn,Ps+[Pn],Ds+[D])
    for P0 in range(19):
        rec(t0,P0,[P0],[])
    return res
if __name__=='__main__':
    x=int(sys.argv[2]); t0=int(sys.argv[3]); Hmax=int(sys.argv[4])
    for H in range(1,Hmax+1):
        r=run(x,t0,H)
        # lattice history present?
        latP=tuple(lat(t0+k,x) for k in range(H+1))
        has=any(h[0]==latP for h in r)
        ifs=set()
        for Ps,Ds in r:
            a_out=tuple(1 if Ps[k]+lat_asc(t0+k,x)>=10 else 0 for k in range(H))
            ifs.add((a_out,Ds))
        print('x',x,'H',H,'histories',len(r),'distinct interface',len(ifs),'lattice present',has)
