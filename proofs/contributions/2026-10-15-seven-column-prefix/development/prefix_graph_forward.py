from itertools import product
from collections import deque,Counter
from array import array
import json,sys,time

def normalize(s):
 d=[];c=0
 for u in s:
  c,v=divmod(u+c,10);d.append(v)
 if c:d.append(c)
 return tuple(d)
def forward(s):
 d=normalize(s);return tuple(x+y for x,y in zip(d,d[::-1]))
def outputs(s):
 k=len(s);low=[];c=0
 for u in s:
  c,v=divmod(u+c,10);low.append(v)
 ans=set()
 for cin in (0,1):
  high=[0]*k;c=cin
  for i in range(k-1,-1,-1):c,high[i]=divmod(s[i]+c,10)
  if c:out=(1+low[0],)+tuple(low[i]+high[i-1] for i in range(1,k))
  else:out=tuple(low[i]+high[i] for i in range(k))
  ans.add(out)
 return ans

def raw_words(n):
 if n==1:
  yield from ((c,) for c in range(2,19,2));return
 for first in range(1,19):
  for tail in product(range(19),repeat=n//2-1):
   left=(first,)+tail
   if n%2:
    for c in range(0,19,2):yield left+(c,)+left[::-1]
   else:yield left+left[::-1]

def build(k):
 off=19**(k-1);N=18*off
 short=[q for n in range(1,k) for q in raw_words(n)]
 smap={s:N+i for i,s in enumerate(short)}
 def encode(s):
  if len(s)<k:return smap[s]
  z=0
  for c in s[:k]:z=z*19+c
  return z-off
 def decode(i):
  if i>=N:return short[i-N]
  z=i+off;r=[]
  for _ in range(k):z,c=divmod(z,19);r.append(c)
  return tuple(reversed(r))
 children=[];indeg=array('i',[0])*(N+len(short));edges=0
 for i in range(N):
  out=tuple(sorted(encode(p) for p in outputs(decode(i))))
  children.append(out)
  for p in out:indeg[p]+=1;edges+=1
 for s in short:
  p=encode(forward(s));children.append((p,));indeg[p]+=1;edges+=1
 rank=array('i',[-1])*(N+len(short));best=array('i',[0])*(N+len(short))
 todo=deque(i for i,d in enumerate(indeg) if not d)
 for i in todo:rank[i]=0
 while todo:
  i=todo.popleft()
  for p in children[i]:
   best[p]=max(best[p],rank[i]+1);indeg[p]-=1
   if indeg[p]==0:rank[p]=best[p];todo.append(p)
 print('graph',k,'states',len(children),'edges',edges,'rank_counts',dict(sorted(Counter(rank).items())),flush=True)
 return encode,decode,rank,children
if __name__=='__main__':
 k=int(sys.argv[1]) if len(sys.argv)>1 else 4
 encode,decode,rank,children=build(k)
 from prefix_original import inv_nongrowth
 bounded={}
 for a in range(1,10):
  for b in range(10):
   if (a,b) in ((1,1),(1,2)):continue
   rr=[]
   for tail in product(range(10),repeat=k-2):
    p=(a,b)+tail
    if b<a:
     parents=inv_nongrowth(p)
     r=1 if not parents else (2+max(rank[encode(x)] for x in parents) if all(rank[encode(x)]>=0 for x in parents) else -1)
    else:
     r=rank[encode(p)];r=1+r if r>=0 else -1
    rr.append(r)
   good=[v for v in rr if v>=0]
   if -1 not in rr:
    bounded[str(a)+str(b)]=max(rr);print('ALL',str(a)+str(b),max(rr),Counter(rr),flush=True)
   elif good:print('PARTIAL',str(a)+str(b),len(good),'/',len(rr),'max',max(good),flush=True)
 print('BOUNDED',bounded)
 with open('graph'+str(k)+'_rank.json','w') as f:json.dump({'k':k,'rank':list(rank),'bounded':bounded},f)
