from itertools import product
from functools import lru_cache
from prefix_graph_forward import raw_words,forward
from inverse_original import inverse
from collections import defaultdict
NG={}
for v,x,y in product(range(19),range(2),range(2)):
 NG[(v,x,y)]=[(s,(s+x)//10,yy) for s in range(19) for yy in (0,1) if (s+yy)//10==y and 2*s+x+yy-10*((s+x)//10+y)==v]

def pred_prefix(p):
 states={((),0,0)}
 for v in p:
  states={(w+(s,),xx,yy) for w,x,y in states for s,xx,yy in NG[(v,x,y)] if w or s}
 out={w for w,x,y in states}
 if p[0]>10:return out
 first=p[0]+9 if p[0]<=9 else 9
 states={((first,),first//10,1)}
 for v in p[1:]:
  ns=set()
  for w,x,y in states:
   for yy in (0,1):
    if (w[-1]+yy)//10!=y:continue
    d=v-w[-1]-yy+10*y
    if not 0<=d<=9:continue
    for xx in (0,1):
     s=d+10*xx-x
     if 0<=s<=18:ns.add((w+(s,),xx,yy))
  states=ns
 out.update(w for w,x,y in states if any((w[-1]+z)//10==y for z in (0,1)))
 return out

def inverse_graph(k):
 sm=defaultdict(set)
 for s in raw_words(k-1):
  p=forward(s)
  if len(p)==k:sm[p].add(s)
 @lru_cache(maxsize=100000)
 def pred(p):
  if len(p)<k:return frozenset(inverse(p))
  return frozenset(pred_prefix(p)|sm[p])
 return pred
if __name__=='__main__':
 import sys
 k=int(sys.argv[1]);pred=inverse_graph(k)
 S={(7,7,c)+tail for c in range(1,10) for tail in product(range(10),repeat=k-3)}
 for h in range(60):
  print('k',k,'depth',h,'states',len(S),'cache',pred.cache_info(),flush=True)
  if not S:break
  if len(S)>1_000_000:break
  S={s for p in S for s in pred(p)}
