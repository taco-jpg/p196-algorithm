from inverse_original import inverse,ds,representative,T,feasible
from prefix_original import inv_prefix
from functools import lru_cache
from itertools import product
from collections import defaultdict
@lru_cache(maxsize=50000)
def getpath(q,depth):
 if depth==0:return (q,)
 for p in inverse(q):
  r=getpath(p,depth-1)
  if r:return (q,)+r
 return None
for n in range(4,11):
 h=(n+1)//2;checked=0
 for tail in product(range(10),repeat=h-2):
  half=(3,3)+tail;q=half+half[:n//2][::-1]
  if not feasible(q):continue
  checked+=1
  path=getpath(q,4)
  if path:
   a=representative(path[-1]);vals=[a]
   for _ in range(5):vals.append(T(vals[-1]))
   print('FOUND 5',vals,'pal_flags',[str(v)==str(v)[::-1] for v in vals],flush=True)
   raise SystemExit
 print('n',n,'checked',checked,flush=True)
