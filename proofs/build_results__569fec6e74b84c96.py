from prefix_inverse_fast import pred_prefix
from prefix_graph_forward import forward,raw_words
from collections import defaultdict,deque,Counter
from itertools import product
from pathlib import Path
import json
out=Path('p196_continuation');out.mkdir(exist_ok=True)

def run(k,starts,title):
 short=defaultdict(set)
 for n in range(1,k):
  for s in raw_words(n):short[forward(s)].add(s)
 def parents(p):return (pred_prefix(p) if len(p)==k else set())|short[p]
 todo=list(starts);seen=set(starts);back={};fwd=defaultdict(list)
 while todo:
  p=todo.pop();ps=parents(p);back[p]=ps
  for s in ps:
   fwd[s].append(p)
   if s not in seen:seen.add(s);todo.append(s)
 rank={p:0 for p in seen if not back[p]};degree={p:len(back[p]) for p in seen};queue=deque(rank)
 while queue:
  s=queue.popleft()
  for p in fwd[s]:
   degree[p]-=1
   if not degree[p]:rank[p]=1+max(rank[q] for q in back[p]);queue.append(p)
 assert len(rank)==len(seen)
 layers=[];S=set(starts)
 while S:
  layers.append(len(S));S={s for p in S for s in back[p]}
 layers.append(0)
 cert={'schema':1,'width':k,'title':title,'initial':[list(p) for p in sorted(starts)],'nodes':[{'word':list(p),'rank':rank[p]} for p in sorted(seen)],'layer_counts':layers,'palindrome_height_bound':1+max(rank[p] for p in starts)}
 if k==5:cert['third_digit_bounds']={str(c):1+max(rank[p] for p in starts if len(p)>=3 and p[2]==c) for c in range(1,10)}
 path=out/('certificate_33.json' if k==4 else 'certificate_77.json');path.write_text(json.dumps(cert,separators=(',',':'))+'\n')
 print(path,'nodes',len(seen),'edges',sum(map(len,back.values())),'counts',layers,'bound',cert['palindrome_height_bound'],'details',cert.get('third_digit_bounds'))
 return cert
run(4,{(3,3,c,d) for c,d in product(range(10),repeat=2)}|{(3,3)},'All palindromes beginning with 33')
run(5,{(7,7,c,d,e) for c in range(1,10) for d,e in product(range(10),repeat=2)}|{(7,7,7,7)},'Palindromes beginning with 77 whose third digit is nonzero')
