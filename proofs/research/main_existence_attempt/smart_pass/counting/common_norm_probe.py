from itertools import product
from pathlib import Path
import numpy as np,sys,time,json
from scipy.optimize import minimize
from scipy.special import logsumexp
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from astra_counting_nooverflow_depth import layers
j=list(product(tuple(product((0,1),repeat=2)),repeat=3));ix={st:i for i,st in enumerate(j)};ms=[]
for y in range(1,9):
 M=np.zeros((64,64))
 for i,st in enumerate(j):
  for x in(y,y+9):
   for ns,_ in layers(st,x):M[i,ix[ns]]+=1
 ms.append(M)
x=np.zeros(64)
for tau in (.03,.01,.003,.001):
 def obj(x):
  d=np.exp(x);v=[];gs=[]
  for m in ms:
   A=(d[:,None]*m)/d[None,:]
   vals,vec=np.linalg.eigh(A.T@A);s=np.sqrt(vals[-1]);vr=vec[:,-1];ul=A@vr/s
   v.append(np.log(s));gs.append(ul*ul-vr*vr)
  z=np.array(v)/tau;weights=np.exp(z-logsumexp(z))
  return tau*logsumexp(z),np.array(gs).T@weights
 r=minimize(obj,x,jac=True,method='L-BFGS-B',options={'maxiter':300,'ftol':1e-13,'gtol':1e-9})
 x=r.x-x.mean();norms=[np.linalg.norm(np.exp(x[:,None]-x[None,:])*m,2) for m in ms]
 print('tau',tau,'success',r.success,'norms',norms,flush=True)
json.dump(dict(x=x.tolist(),norms=norms),open(Path(__file__).with_name('common_norm_probe.json'),'w'),indent=2)
