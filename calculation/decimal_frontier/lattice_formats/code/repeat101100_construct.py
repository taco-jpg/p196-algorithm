#!/usr/bin/env python3
"""Independent direct all-k coefficient/carry construction, not matrix DP."""

def row(b,k,mode):
    assert b in (4,5,6) and k>=1
    if b==4: x=[4,1,3,4,1,2]; fixed=[1,1,0,0]
    if b==5: x=[6,2,4,5,1,3]; fixed=[0,1,1,0]
    if b==6: x=[7,2,5,6,1,3]; fixed=[1,1,1,1]
    g=[int(z) for z in ('101100'*k)]
    xs=x*k;cs=[]
    for q in range(k):
        a,d=mode(q)
        assert a in (0,1) and d in (0,1)
        cs.extend([a,fixed[0],fixed[1],d,fixed[2],fixed[3]])
    assert len(xs)==len(cs)==len(g)
    for t in range(len(g)):
        y=xs[t]%b + (1 if g[t] else (xs[t]+cs[t])%b)
        assert (xs[t]+cs[t])//b==g[t]
        assert y==xs[(t+1)%len(g)]
        assert 1<=xs[t]<=2*b-2
    return xs,cs

def main():
    for b in (4,5,6):
        for k in (1,2,3,4,7,20,100,1000):
            for seed in range(16):
                xs,cs=row(b,k,lambda q:(((q*7+seed)//3)&1,((q*11+seed)//5)&1))
                for shift in range(6):
                    X=xs[shift:]+xs[:shift]
                    C=cs[shift:]+cs[:shift]
                    G=('101100'*k)[shift:]+('101100'*k)[:shift]
                    assert X[0]>0
                    for t in range(len(G)):
                        assert (X[t]+C[t])//b==int(G[t])
                        assert (X[t]%b+(1 if G[t]=='1' else (X[t]+C[t])%b))==X[(t+1)%len(G)]
        print('PASS explicit construction',b,'k<=1000, 16 assignments, six rotations')
if __name__=='__main__':main()
