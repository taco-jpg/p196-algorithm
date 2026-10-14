"""Exact finite-prefix test for indefinite repetition of a prescribed overflow clock.

The model retains the two outer pair sums.  The unknown carry from deeper
columns is allowed to be either zero or one independently at every step.
Thus it overapproximates every actual decimal reverse-add orbit with at least four decimal digits.
Acyclicity proves a finite bound even when inner digits grow or are aperiodic.
"""
from collections import deque
import json

def transition(a,b,inner):
 # Low-side addition starts with zero carry.
 low0=a%10;carry0=a//10
 low1=(b+carry0)%10
 # High-side addition starts with the unknown carry from the interior.
 high1=(b+inner)%10;carry1=(b+inner)//10
 high0=(a+carry1)%10;overflow=(a+carry1)//10
 if overflow:return (low0+1,low1+high0),overflow
 return (low0+high0,low1+high1),overflow

def primitive(word):
 for p in range(1,len(word)+1):
  if len(word)%p==0 and tuple(word[:p])*(len(word)//p)==tuple(word):return tuple(word[:p])
 raise AssertionError

def check(clock):
 clock=primitive(clock);p=len(clock)
 pairs=[(a,b) for a in range(1,19) for b in range(19)]
 ids={q:i for i,q in enumerate(pairs)};s=len(pairs);n=s*p
 out=[[] for _ in range(n)];ind=[0]*n;edges=0
 for t in range(p):
  for i,(a,b) in enumerate(pairs):
   seen=set()
   for inner in (0,1):
    dest,h=transition(a,b,inner)
    if h==clock[t]:seen.add(((t+1)%p)*s+ids[dest])
   for v in seen:out[t*s+i].append(v);ind[v]+=1;edges+=1
 queue=deque(i for i in range(n) if not ind[i]);removed=0;rank=[0]*n
 while queue:
  u=queue.popleft();removed+=1
  for v in out[u]:
   rank[v]=max(rank[v],rank[u]+1);ind[v]-=1
   if not ind[v]:queue.append(v)
 return {'primitive_clock':clock,'states':n,'edges':edges,'acyclic':removed==n,'cyclic_remainder':n-removed,'maximum_steps':max(rank) if removed==n else None}

def main():
 data=json.load(open('exist_uniform_period4_screen_results.json'));out=[]
 for old in data:
  row=check(old['clock']);row['origins']=old['origins'];out.append(row);print(json.dumps(row),flush=True)
 json.dump(out,open('exist_uniform_clock_obstruction_results.json','w'),indent=2)
if __name__=='__main__':main()
