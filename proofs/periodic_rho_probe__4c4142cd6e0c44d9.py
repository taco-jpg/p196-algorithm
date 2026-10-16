from itertools import product
from pathlib import Path
import numpy as np,sys,time,json
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from astra_counting_nooverflow_depth import layers
j=list(product(tuple(product((0,1),repeat=2)),repeat=3));ix={st:i for i,st in enumerate(j)};ms=[]
for y in range(1,9):
 M=np.zeros((64,64))
 for i,st in enumerate(j):
  for x in(y,y+9):
   for ns,_ in layers(st,x):M[i,ix[ns]]+=1
 ms.append(M)
rows=[]
for k in range(1,7):
 best=(0,None);t0=time.time();ct=0
 for w in product(range(8),repeat=k):
  if w[0]!=min(w):continue
  if any(w>w[i:]+w[:i] for i in range(1,k)):continue
  M=np.eye(64)
  for i in w:M=M@ms[i]
  r=float(max(abs(np.linalg.eigvals(M)))**(1/k));ct+=1
  if r>best[0]:best=(r,tuple(y+1 for y in w))
 row=dict(period=k,best_radius=best[0],best_word=best[1],checked=ct,seconds=time.time()-t0);rows.append(row);print(row,flush=True)
json.dump(rows,open(Path(__file__).with_name('periodic_rho_probe.json'),'w'),indent=2)
