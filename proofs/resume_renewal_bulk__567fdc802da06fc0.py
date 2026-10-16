"""Exact periodic-bulk dynamics; no finite-seed existence conclusion."""
from itertools import product
from collections import Counter
import json

def transform(q, overflow):
 n=len(q)
 if all(a==9 for a in q): return None
 j=next(i for i,a in enumerate(q) if a!=9)
 left=[0]*n;right=[0]*n
 left[j]=right[j]=int(q[j]>=10)
 for k in range(1,n):
  i=(j+k)%n; left[i]=(q[i]+left[(i-1)%n])//10
 for k in range(1,n):
  i=(j-k)%n;right[i]=(q[i]+right[(i+1)%n])//10
 lo=[q[i]+left[(i-1)%n]-10*left[i] for i in range(n)]
 hi=[q[i]+right[(i+1)%n]-10*right[i] for i in range(n)]
 return tuple(lo[i]+hi[(i-1)%n if overflow else i] for i in range(n))
def F(q):
 x=transform(q,False)
 return None if x is None else transform(x,True)
def canon(q):return min(q[i:]+q[:i] for i in range(len(q)))
def run(n):
 seen=set();cycles=[]
 for q in product(range(19),repeat=n):
  if q in seen:continue
  path=[];index={}
  while q is not None and q not in seen:
   index[q]=len(path);path.append(q);seen.add(q);q=F(q)
  if q in index:
   cycle=path[index[q]:]
   cycles.append(cycle)
 unique={tuple(sorted(canon(q) for q in c)):c for c in cycles}
 data={'width':n,'cycle_counts':dict(Counter(len(c) for c in cycles)),'cycles_mod_rotation':list(unique.values())}
 print(json.dumps(data),flush=True)
 return data
if __name__=='__main__':
 result=[run(i) for i in range(1,5)]
 json.dump(result,open('resume_renewal_bulk_results.json','w'),indent=2)
