# Collision types of the Theta-dual family: N = [P][9^j][~P], P = [top(B)][wire][~low(B)]
import sys, zlib
from pipeline import *
from dual import setup
B=10
def build_phys(leftH,wireH,n,j,t0):
    Bc=[(H[0][t0],H[1][t0]) for H in leftH]
    w=(wireH[0][t0],wireH[1][t0])
    top=[b for (a,b) in Bc]+[w[1]]*n           # high->low order of the top part
    lowHL=[a for (a,b) in Bc][::-1]            # low part, high->low
    P=top+[9-x for x in lowHL]                 # [T][w_b][~Lo]  (high->low)
    Pc=[9-x for x in P]
    hl=P+[9]*j+Pc                              # high->low
    return hl[::-1]                            # digits low->high
def stats(d):
    L=len(d); h=L//2
    s=[d[i]+d[L-1-i] for i in range(h)]
    n9=sum(1 for x in s if x==9); n18=sum(1 for x in s if x==18); n0=sum(1 for x in s if x==0)
    runs=1+sum(1 for i in range(1,L) if d[i]!=d[i-1])
    return L,n9,n18,n0,runs
def run(g,label,steps=2500):
    T=len(g)
    for leftH,wireH in setup(g):
        K=len(leftH)
        for j in range(60,60+2*sum(g)):
            for t0 in (0,):
                d=build_phys(leftH,wireH,3,j,t0)
                t=0; dev=None; pal=None; log=[]
                while t<steps:
                    if is_pal(d): pal=t; break
                    L=len(d)
                    ok=all(d[i]==leftH[i][0][(t0+t)%T] and d[L-1-i]==leftH[i][1][(t0+t)%T] for i in range(K))
                    if not ok and dev is None: dev=t
                    if dev is not None and (t-dev) in (0,1,2,5,10,20,50,100,200,400,800,1600): log.append((t-dev,)+stats(d))
                    d=ra_step(d,B); t+=1
                print('%s K=%d j=%d t0=%d: exterior breaks at t=%s, palindrome=%s'%(label,K,j,t0,dev,pal))
                for e in log: print('    +%d: L=%d  #9=%d #18=%d #0=%d  runs/L=%.2f'%(e[0],e[1],e[2],e[3],e[4],e[5]/e[1]))
if __name__=='__main__':
    run((0,0,0,0,1,1,1,0,0,0,1),'p11')
    run((0,0,0,1)*3,'p12')
