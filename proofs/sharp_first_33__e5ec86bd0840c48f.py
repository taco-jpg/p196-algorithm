from inverse_original import inverse,ds,representative,T,feasible
from itertools import product

def paths(q,depth):
 if depth==0:yield q;return
 for p in inverse(q):yield from paths(p,depth-1)
for n in range(4,14):
 h=(n+1)//2;checked=0
 for tail in product(range(10),repeat=h-2):
  half=(3,3)+tail;q=half+half[:n//2][::-1]
  if not feasible(q):continue
  checked+=1
  for root in paths(q,4):
   a=representative(root);vals=[a]
   for _ in range(5):vals.append(T(vals[-1]))
   if all(str(v)!=str(v)[::-1] for v in vals[:-1]):
    print('FOUND FIRST5',vals,'qroot',root,flush=True);raise SystemExit
 print('n',n,'checked',checked,flush=True)
