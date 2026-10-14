from __future__ import annotations
import importlib.util, json, sys
from collections import Counter, defaultdict
from pathlib import Path
ARCHIVE_ROOT = Path(__file__).resolve().parent.parent
p = ARCHIVE_ROOT / 'astra_moving_boundary_check.py'
if not p.exists():
 p = ARCHIVE_ROOT / 'research' / 'astra_moving_boundary_check.py'
s=importlib.util.spec_from_file_location('wall',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)

def qstep(q):
 c=0; d=[]
 for x in q:
  z=x+c; d.append(z%10); c=z//10
 if c:d.append(c)
 return tuple(x+y for x,y in zip(d,d[::-1])), tuple(d)

def balance(q):
 assert sum(q)%18==0
 C=sum(q)//18
 if C<1 or any(sum(q[j::C])!=18 for j in range(C)): return None
 w=len(q)-C; W=[]
 for i in range(w):W.append(q[i]+(W[i-C] if i>=C else 0))
 assert m.word_valid(q) and m.difference_word(W,C)==q
 assert all(W[i]+W[-1-i]==18 for i in range(w))
 return tuple(W),C

def canonical(q):
 return ''.join('0123456789ABCDEFGHI'[x] for x in q)

def run():
 counts=Counter(); examples=defaultdict(list); events=[]
 for W in m.wall_words(3):
  for C in range(1,len(W)+3):
   q=m.difference_word(W,C)
   if not m.word_valid(q):continue
   counts['valid']+=1
   V,h,r=m.wall_step(W)
   if m.digit_monotone(r,C):continue
   counts['failures']+=1
   Q,d=qstep(q); z=balance(Q)
   E=sum(Q)//18-C
   pal=d==d[::-1]
   typ=('pal_' if pal else 'safe_')+('balance' if z else 'unbalanced')
   counts[typ]+=1
   key=(C,E,len(W),len(Q),pal,bool(z))
   if len(examples[str(key)])<3:
    examples[str(key)].append(dict(W=W,C=C,q=q,Q=Q,d=d,ret=z))
   if z and not pal:
    events.append(dict(W=W,C=C,newW=z[0],newC=z[1],q=q,Q=Q,d=d))
 chainbest=[]; chainhist=Counter()
 for ev in events:
  W=ev['W']; C=ev['C']; q=ev['q']; chain=[]
  for t in range(100):
   Q,d=qstep(q); z=balance(Q)
   if d==d[::-1] or z is None:break
   if z[1]>C:chain.append((t,C,z[1],z[0]))
   W,C=z; q=Q
  chainhist[len(chain)]+=1
  if len(chain)>=2:chainbest.append(dict(seed=ev,chain=chain,steps=t,stop='pal' if d==d[::-1] else 'unbalanced'))
 empty=[]
 for C0 in range(1,65):
  q=(18,)*C0; rec=[]
  for t in range(300):
   Q,d=qstep(q); z=balance(Q)
   if z is not None and (sum(Q)>sum(q) or balance(q) is None):rec.append(dict(t=t+1,C=z[1],W=z[0]))
   if d==d[::-1]:break
   q=Q
  empty.append(dict(C0=C0,steps=t+1,pal=d==d[::-1],returns=rec))
 out=dict(counts=counts,chain_histogram=chainhist,events=events,chains=chainbest,examples=dict(examples),empty=empty)
 dest=Path(__file__).with_name('renewal_search_scan_results.json');dest.write_text(json.dumps(out,indent=2))
 print(json.dumps(dict(counts=counts,chain_histogram=chainhist,event_count=len(events),chains=chainbest[:10],empty=[e for e in empty if e['returns']]),indent=2))
if __name__=='__main__':run()
