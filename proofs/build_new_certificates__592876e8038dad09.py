from prefix_inverse_fast import pred_prefix
from prefix_graph_forward import forward,raw_words
from collections import defaultdict,deque
from itertools import product
from pathlib import Path
import json,time
out=Path('p196_seven_column_progress');out.mkdir(exist_ok=True)
k=7
short=defaultdict(set)
for n in range(1,k):
 for s in raw_words(n):short[forward(s)].add(s)

def make_initial(abc):
 head=tuple(map(int,abc));starts={head+tail for tail in product(range(10),repeat=k-3)}
 for n in range(3,k):
  for half in product(range(10),repeat=(n+1)//2):
   p=half+half[:n//2][::-1]
   if p[:3]==head and (n%2==0 or p[n//2]%2==0):starts.add(p)
 return starts

def run(abc):
 starts=make_initial(abc);todo=list(starts);seen=set(starts);back={};fwd=defaultdict(list)
 while todo:
  p=todo.pop();ps=(pred_prefix(p) if len(p)==k else set())|short[p];back[p]=ps
  for s in ps:
   fwd[s].append(p)
   if s not in seen:seen.add(s);todo.append(s)
  if len(seen)>2000000:raise RuntimeError('CAP '+abc)
 rank={p:0 for p in seen if not back[p]};degree={p:len(back[p]) for p in seen};queue=deque(rank)
 while queue:
  s=queue.popleft()
  for p in fwd[s]:
   degree[p]-=1
   if not degree[p]:rank[p]=1+max(rank[q] for q in back[p]);queue.append(p)
 assert len(rank)==len(seen),(abc,len(rank),len(seen))
 layers=[];S=set(starts)
 while S:
  layers.append(len(S));S={s for p in S for s in back[p]}
 layers.append(0)
 # A separate long-prefix-only replay matches the C++ discovery transcript.
 longlayers=[];S={p for p in starts if len(p)==k}
 while S:
  longlayers.append(len(S));S={s for p in S for s in back[p] if len(s)==k}
 longlayers.append(0)
 bound=1+max(rank[p] for p in starts)
 cert={'schema':1,'width':k,'prefix':abc,'initial':[list(p) for p in sorted(starts)],'nodes':[{'word':list(p),'rank':rank[p]} for p in sorted(seen)],'layer_counts':layers,'long_only_layer_counts':longlayers,'palindrome_height_bound':bound}
 path=out/('certificate_'+abc+'.json');path.write_text(json.dumps(cert,separators=(',',':'))+'\n')
 print(abc,'nodes',len(seen),'edges',sum(map(len,back.values())),'counts',layers,'bound',bound,flush=True)
 return cert
for abc in ['217','218','620','777']:run(abc)
