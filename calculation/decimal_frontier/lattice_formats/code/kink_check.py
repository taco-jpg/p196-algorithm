import sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from kink_sat import *
recs=parse('/home/claude/research/w3_formats/out/p8_scc.txt')
for ri in range(3):
    L=lattice_data(recs[ri]); p,nB,m,gam=L['p'],L['nB'],L['m'],L['gam']
    K=90; bad=0; tot=0
    for o in range(0,2*m*2):
        for T0 in range(p):
            # simulate time T0 with n = o+... ; use hm from n
            n=o+400 # n_t fixed residue; but need consistent phases across t: use direct arithmetic
            S=[0]
            for t in range(p+1): S.append(S[-1]+gam[(T0+t)%p])
            n_t=[n+S[t] for t in range(p+1)]
            hm=[((x+1)//2)%m for x in n_t]
            t=T0
            def lat(tt,idx,hmm): return L['Wt'][tt%p][(hmm-K+idx-nB)%m]
            Pw=[lat(t,i,hm[0]) for i in range(K)]
            c0=L['cup'][t%p][(hm[0]-K-nB)%m]
            Pn,delta,_,_=fwd_window(Pw,n_t[0],gam[t%p],c0)
            for i2 in range(2,K-30):
                tot+=1
                exp=L['Wt'][(t+1)%p][(hm[1]-K+i2-nB)%m]
                if Pn[i2]!=exp: bad+=1
    print('rec',ri,'cyclen',m,'checks',tot,'bad',bad)
