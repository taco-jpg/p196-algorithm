from chain import *
B=2
# orbit of 22 = 10110
n=22
digs=[int(ch) for ch in bin(n)[2:]][::-1]
gs=[]
for t in range(24):
    nd=ra_step(digs,B)
    gs.append(len(nd)-len(digs))
    print(t, ''.join(map(str,digs[::-1])), 'ov', gs[-1])
    digs=nd
for g in ((1,0,1,0),(0,1,0,1)):
    F=Frame(B,(0,)*4,g)
    R=root_node(B,g)
    starts=expand(F,R)
    print('clock',g,'roots',len(starts))
    order,edges,ok=closure(F,starts)
    live,comps,cyc=live_nodes(len(order),edges)
    print(' nodes',len(order),'ok',ok,'live',sum(live))
    for k,cm in enumerate(comps):
        if cyc[k]:
            print('  cyclic comp size',len(cm),[psums(order[v]) for v in cm][:6])
    for i,H in enumerate(order):
        if live[i]:
            print('  ',i,'a',H[0],'b',H[1],'c',H[2],'d',H[3],'->',edges[i])
