from tools import *
B=2
g=(1,0,1,0)
F0=Frame(B,(0,)*4,g)
R=root_node(B,g)
order,edges,ok=closure(F0,expand(F0,R))
live,comps,cyc=live_nodes(len(order),edges)
wire=[i for i,H in enumerate(order) if all(s==B-1 for s in psums(H)) and i in edges[i]][0]
print('wire node',wire,order[wire])
left=find_path(edges,[0],wire)
print('left path',left)
# fold frame, P=4
for adv in ({2},{0}):
    F,phi=make_frame(B,g,adv)
    cells=lattice_cells(B,[order[wire]])
    sn=sheared_node(B,F,phi,cells,0)
    o2,e2,ok2=closure(F,[sn])
    print('adv',adv,'fold-frame nodes',len(o2),ok2)
    for case in ('i','ii'):
        par=parity_seq(g,F.alpha,case)
        print(' case',case,'par',par)
        if par is None: continue
        for i,H in enumerate(o2):
            for w in e2[i]:
                if mirror_edge(H,o2[w],par,case):
                    print('   mirror edge',i,'->',w, 'path from wire', find_path(e2,[0],i))
                    print('     H ',H); print('     Hn',o2[w])
