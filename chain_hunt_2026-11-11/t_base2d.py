from tools import *
B=2
g=(1,0,1,0)
F0=Frame(B,(0,)*4,g)
R=root_node(B,g)
order,edges,ok=closure(F0,expand(F0,R))
wire=[i for i,H in enumerate(order) if all(s==B-1 for s in psums(H)) and i in edges[i]][0]
left=find_path(edges,[0],wire)[:-1]
left_cols=[(order[i][0][0],order[i][1][0]) for i in left]
wcol=[(order[wire][0][0],order[wire][1][0])]
good=0;tot=0
for adv in ({2},{0}):
    F,phi=make_frame(B,g,adv)
    cells=lattice_cells(B,[order[wire]])
    sn=sheared_node(B,F,phi,cells,0)
    o2,e2,ok2=closure(F,[sn])
    for case in ('i','ii'):
        par=parity_seq(g,F.alpha,case)
        if par is None: continue
        for i,H in enumerate(o2):
            for w in e2[i]:
                if mirror_edge(H,o2[w],par,case):
                    path=find_path(e2,[0],i)
                    chain=[o2[v] for v in path[1:]]   # columns after the wire, up to K=H
                    Hn=o2[w]
                    if case=='i':
                        if par[0]==0: cc=[(X[0][0],X[1][0]) for X in chain]; mid=None
                        else: cc=[(X[0][0],X[1][0]) for X in chain]; mid=Hn[0][0]
                    else:
                        if par[0]==1: cc=[(X[0][0],X[1][0]) for X in chain[:-1]]; mid=H[0][0]
                        else: cc=[(X[0][0],X[1][0]) for X in chain]; mid=None
                    if case=='ii' and par[0]==1 and len(chain)==0: continue
                    mk=lambda n: build_number(left_cols,wcol,n,cc,mid)
                    res=check_template(B,mk,3,1,4)
                    tot+=1
                    if res[0]:
                        good+=1
                        print('OK  adv',adv,'case',case,'edge',i,w,'N(3)=',digits_to_str(mk(3)), int(digits_to_str(mk(3)),2))
                    else:
                        print('bad adv',adv,'case',case,'edge',i,w,res[1])
print(good,'/',tot)
