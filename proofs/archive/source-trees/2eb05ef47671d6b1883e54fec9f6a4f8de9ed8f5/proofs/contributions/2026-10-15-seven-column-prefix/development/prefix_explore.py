from prefix_original import *
from collections import defaultdict,deque,Counter
nodes=[(a,b,c) for a in range(1,19) for b in range(19) for c in range(19)]
inv={p:set(inv_prefix(p)) for p in nodes}
# Include the only missing length-two sources of a length-three output.
for s in range(10,19): inv[(s-9,2*(s-9),s-9)].add((s,s))
for s in range(1,19): inv[(s,s)]=set()
for s in range(2,19,2): inv[(s,)]=set()
for s in range(1,19): inv[forward((s,s))].add((s,s))
for s in range(2,19,2): inv[forward((s,))].add((s,))
children=defaultdict(set)
for p,parents in inv.items():
 for q in parents:children[q].add(p)
left={p:len(q) for p,q in inv.items()}
queue=deque(p for p in inv if not left[p]);rank={p:0 for p in queue}
while queue:
 q=queue.popleft()
 for p in children[q]:
  left[p]-=1
  if not left[p]:
   rank[p]=1+max(rank[x] for x in inv[p]);queue.append(p)
print('states',len(inv),'finite',len(rank),'max rank',max(rank.values()),'counts',dict(sorted(Counter(rank.values()).items())))
print('Bounded palindrome prefixes ignoring descending-pair extra constraint:')
for a in range(1,10):
 for b in range(10):
  vals={c:rank[(a,b,c)]+1 for c in range(10) if (a,b,c) in rank}
  if vals:print(a,b,vals)
print('Descending two-digit families:')
for a in range(1,10):
 for b in range(a):
  rs=[]
  for c in range(10):
   ps=inv_nongrowth((a,b,c))
   if not ps:r=1
   elif all(p in rank for p in ps):r=2+max(rank[p] for p in ps)
   else:r=None
   rs.append(r)
  print(a,b,rs)
