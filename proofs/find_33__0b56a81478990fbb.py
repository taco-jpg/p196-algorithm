from inverse_original import inverse,ds,representative,T,feasible
from prefix_original import inv_prefix
from functools import lru_cache
from itertools import product
from collections import defaultdict

def group(layer):
 d=defaultdict(list)
 for a,b,c in sorted(layer):d[(a,b)].append(c)
 return dict(d)
layer={(3,3,c) for c in range(10)}
for k in range(9):
 print('layer',k,group(layer),flush=True)
 if not layer:break
 layer={s for p in layer for s in inv_prefix(p)}

@lru_cache(maxsize=50000)
def getpath(q,depth):
 if depth==0:return (q,)
 for p in inverse(q):
  r=getpath(p,depth-1)
  if r:return (q,)+r
 return None

for n in range(6,17):
 h=(n+1)//2;checked=0
 for tail in product(range(10),repeat=h-3):
  for c in (7,8):
   half=(3,3,c)+tail
   q=half+half[:n//2][::-1]
   if len(q)!=n or not feasible(q):continue
   checked+=1
   path=getpath(q,7)
   if path:
    a=representative(path[-1]);vals=[a]
    for _ in range(8):vals.append(T(vals[-1]))
    assert vals[-1]==int(''.join(map(str,q)))
    print('FOUND',vals,'qpath',path,'pal_flags',[str(v)==str(v)[::-1] for v in vals],flush=True)
    raise SystemExit
 print('n',n,'checked',checked,flush=True)
