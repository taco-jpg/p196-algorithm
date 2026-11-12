from front import *
k=679
left,walk=setup(k)
K0=len(left)
for n in (1,2,3,5,10):
    digs,ncols=number_at(left,walk,n,0,0,None)
    N0=''.join(map(str,digs[::-1]))
    t=0; first_dev=None; pal=None
    H0=order[left[0]]
    while t<4000:
        if is_pal(digs): pal=t; break
        L=len(digs)
        if first_dev is None and (digs[0]!=H0[0][t%8] or digs[L-1]!=H0[1][t%8]): first_dev=t
        digs=ra_step(digs,10); t+=1
    print('n=%d digits=%d rigorous bound %d steps; column 0 follows its period-8 history until t=%s; palindrome within 4000 steps: %s'%(n,len(N0),(K0+20*n)//2,first_dev,pal))
    if n==1: print('   N =',N0)
