from prefix_inverse_fast import pred_prefix,NG
from prefix_graph_forward import raw_words,forward
from functools import lru_cache
from itertools import product
from collections import defaultdict
import sys,time,json

def nongrowth(p):
 states={((),0,0)}
 for v in p:states={(w+(s,),xx,yy) for w,x,y in states for s,xx,yy in NG[(v,x,y)] if w or s}
 return {w for w,x,y in states}

def run(abc,k,cap=400000):
 short=defaultdict(set)
 for n in range(1,k):
  for s in raw_words(n):short[forward(s)].add(s)
 @lru_cache(maxsize=100000)
 def pred(p):return frozenset((pred_prefix(p) if len(p)==k else set())|short[p])
 init=tuple(map(int,abc));S={init+tail for tail in product(range(10),repeat=k-3)}
 # All short feasible palindrome digit words with the specified decimal prefix.
 for n in range(3,k):
  for half in product(range(10),repeat=(n+1)//2):
   if not half[0]:continue
   p=half+half[:n//2][::-1]
   if p[:3]==init and (n%2==0 or p[n//2]%2==0):S.add(p)
 counts=[];seenlayers={}
 for h in range(100):
  counts.append(len(S))
  if not S:
   print(abc,k,'FINITE',h,counts,flush=True);return h
  if len(S)>cap:
   print(abc,k,'CAP',h,counts,flush=True);return None
  signature=hash(frozenset(S))
  if signature in seenlayers:
   print(abc,k,'REPEAT',h,seenlayers[signature],counts,flush=True);return None
  seenlayers[signature]=h
  if h==0 and init[1]<init[0]:
   S={q for p in S for q in ((nongrowth(p) if len(p)==k else {q for q in short[p] if len(q)==len(p)}))}
  else:S={q for p in S for q in pred(p)}
 print(abc,k,'DEPTH',counts,flush=True)
if __name__=='__main__':
 k=int(sys.argv[1])
 for s in sys.argv[2:]:run(s,k)
