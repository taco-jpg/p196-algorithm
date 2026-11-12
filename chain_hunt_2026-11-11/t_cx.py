from cx import *
import time
# base 2 fold frame
B=2; g=(1,0,1,0)
F0=Frame(B,(0,)*4,g)
r=run_closure(F0,expand(F0,root_node(B,g)),dump=True)
print('base2 outer:',r['nodes'],r['live'],r['cyc'])
wire=((1,0,1,0),(0,1,0,1),(1,0,1,0),(0,1,0,1))
F,phi=make_frame(B,g,{2})
pars=[(1,parity_seq(g,F.alpha,'i')),(2,parity_seq(g,F.alpha,'ii'))]
r=run_closure(F,[sheared_node(B,F,phi,lattice_cells(B,[wire]),0)],pars=pars,dump=True)
print('base2 fold:',r['nodes'],r['complete'],len(r['cands']),[ (c['case'],c['i'],c['w']) for c in r['cands']])
# base 10 clock 10 outer
B=10; g=(1,0)*4
F0=Frame(B,(0,)*8,g)
t0=time.time()
r=run_closure(F0,expand(F0,root_node(B,g)),dump=False)
print('base10 clock10:',r['nodes'],r['live'],sorted(c['size'] for c in r['cyc']),'dfs',r['dfs'],'time %.2f'%(time.time()-t0))
