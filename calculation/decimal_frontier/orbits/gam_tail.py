import sys, numpy as np
sys.argv=['x','data/gam_b10_rnd5.npz','8']
exec(open('gam_markov.py').read().split("real = {p")[0])
c1,c = fit(g,8)
thr=[30,40,50,60,70,80,100]
def cnt(x): 
    L=np.array(alt_stretches(x,30)); return [int((L>=t).sum()) for t in thr]
print('thr',thr); print('real',cnt(g))
S=np.array([cnt(simulate(c1,c,8,N)) for _ in range(20)])
print('sur mean',S.mean(0).round(1)); print('sur max ',S.max(0))
