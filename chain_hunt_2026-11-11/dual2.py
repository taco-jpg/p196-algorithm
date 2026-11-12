from dual import *
g=(0,0,0,0,1,1,1,0,0,0,1)
leftH,wireH=setup(g)[0]
T=11
def stats(digs):
    L=len(digs); h=L//2
    ps=[digs[i]+digs[L-1-i] for i in range(h)]
    return ps
for (n,k) in ((3,100),(3,101)):
    digs,K=build(leftH,wireH,n,k,0)
    t=0; dev=None; log=[]
    while t<2600:
        L=len(digs)
        ok=all(digs[i]==leftH[i][0][t%T] and digs[L-1-i]==leftH[i][1][t%T] for i in range(K))
        if not ok and dev is None: dev=t
        ps=stats(digs)
        n18=sum(1 for s in ps if s==18); n9=sum(1 for s in ps if s==9); n0=sum(1 for s in ps if s==0); n13=sum(1 for s in ps if s>=13)
        # longest run of 9-sums and of 18-sums
        def longest(v):
            best=cur=0
            for s in ps:
                cur=cur+1 if s==v else 0; best=max(best,cur)
            return best
        if t%50==0 or (dev is not None and dev<=t<dev+3) or (t>=600 and t<760 and t%10==0):
            log.append((t,L,n18,longest(18),n9,longest(9),n0,longest(0),n13))
        if is_pal(digs): print('PAL at',t); break
        digs=ra_step(digs,B); t+=1
    print('n=%d k=%d exterior first deviates at t=%s'%(n,k,dev))
    print('   t  L  #18 run18  #9 run9  #0 run0  #>=13')
    for x in log: print('  ',x)
