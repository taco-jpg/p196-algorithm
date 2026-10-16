"""Independent arithmetic replay of the 16-column variable-rho witness.
No imports from previous inverse/DFA implementations are used.
"""
from itertools import product
from collections import deque
from functools import lru_cache
from pathlib import Path
import json
BASE=Path(__file__).parent
STATES=list(product(tuple(product((0,1),repeat=2)),repeat=3))
INDEX={s:i for i,s in enumerate(STATES)}

@lru_cache(None)
def one(state,target):
 a,b=state;out=[]
 for coefficient in range(19):
  low_out,low_digit=divmod(coefficient+a,10)
  for high_in in (0,1):
   high_out,high_digit=divmod(coefficient+high_in,10)
   if high_out==b and low_digit+high_digit==target:
    out.append(((low_out,high_in),coefficient))
 return tuple(out)

@lru_cache(None)
def three(state,target):
 out=[]
 for t0,x0 in one(state[0],target):
  for t1,x1 in one(state[1],x0):
   for t2,x2 in one(state[2],x1):
    out.append(((t0,t1,t2),(x0,x1,x2)))
 return tuple(out)

@lru_cache(None)
def advance(mask,symbol):
 out=0
 for i in range(64):
  if mask>>i&1:
   for ns,_ in three(STATES[i],symbol):out|=1<<INDEX[ns]
 return out

def initial(symbol):
 return sum(1<<INDEX[ns] for ns in set(ns for ns,labels in three(((0,0),)*3,symbol) if all(labels)))

ALPHABET=tuple(range(1,9))+tuple(range(10,18))
paths={}
for s in range(10,18):
 mask=initial(s)
 if mask and mask not in paths:paths[mask]=(s,)
queue=deque(paths)
while queue:
 mask=queue.popleft()
 for symbol in ALPHABET:
  new=advance(mask,symbol)
  if new and new not in paths:paths[new]=paths[mask]+(symbol,);queue.append(new)
assert len(paths)==240
expected={sub<<(4*g) for g in range(16) for sub in range(1,16)}
assert set(paths)==expected
# Check the saved compact transition table independently.
saved=[list(map(int,line.split())) for line in(BASE/'compact_transitions.txt').read_text().splitlines()]
for g in range(16):
 for sub in range(1,16):
  mask=sub<<(4*g);i=15*g+sub-1
  for j,s in enumerate(ALPHABET):
   new=advance(mask,s)
   if new:
    ng=(new.bit_length()-1)//4;assert new==(new>>(4*ng))<<(4*ng)
    value=15*ng+(new>>(4*ng))-1
   else:value=-1
   assert value==saved[i][j]

rows=json.loads((BASE/'rho_horizon_sat.json').read_text());satrows=[r for r in rows if r['status']=='sat'];best=max(satrows,key=lambda r:r['depth'])
assert best['depth']==16
short_witnesses=[]
for row in satrows:
 gg=row['viable_initial_groups'][0];mm=15<<(4*gg)
 ww=tuple(reversed(row['rho_word_read_inside_to_outside']));cc={mm};counts=[1]
 for yy in ww:
  cc={advance(v,x) for v in cc for x in(yy,yy+9)}
  assert 0 not in cc
  counts.append(len(cc))
 short_witnesses.append(dict(depth=row['depth'],starting_group=gg,positive_outer_prefix=paths[mm],rho_word_outside_to_inside=ww,collection_sizes=counts))
g=best['viable_initial_groups'][0];mask=15<<(4*g);prefix=paths[mask]
word=tuple(reversed(best['rho_word_read_inside_to_outside']))
collection={mask};levels=[sorted(collection)]
for rho in word:
 collection={advance(s,x) for s in collection for x in(rho,rho+9)}
 assert 0 not in collection
 levels.append(sorted(collection))

# Every nonempty inverse subset reached by the witness can be completed to
# the all-one carry state, allowing an actual reflected finite center.
TARGET=63
completion={};max_suffix=0
for start in collection:
 q=deque([(start,())]);seen={start}
 while q:
  state,path=q.popleft()
  if state>>TARGET&1:
   completion[start]=path;max_suffix=max(max_suffix,len(path));break
  for symbol in range(19):
   new=advance(state,symbol)
   if new and new not in seen:seen.add(new);q.append((new,path+(symbol,)))
 else:raise AssertionError(('no finite completion',start))
# q=18 preserves all-one carries at each backward layer. Pad to common width.
completion={s:w+(18,)*(max_suffix-len(w)+1) for s,w in completion.items()}
assert all(advance(1<<63,18)==1<<63 for _ in range(1))

def inverse_half(half):
 paths_now={((0,0),)*3: ((),(),())}
 for s in half:
  nxt={}
  for state,words in paths_now.items():
   for ns,labels in three(state,s):
    if not words[0] and not all(labels):continue
    nxt[ns]=tuple(words[i]+(labels[i],) for i in range(3))
  paths_now=nxt
 assert STATES[63] in paths_now
 return paths_now[STATES[63]]

def canonical_number(q):
 digs=[0]*len(q)
 for i in range(len(q)//2):
  digs[i]=max(0,q[i]-9);digs[-i-1]=min(9,q[i])
 assert digs[-1]>0
 return sum(d*10**i for i,d in enumerate(digs))

def pairword(n):
 digs=list(map(int,str(n)))[::-1]
 return tuple(a+b for a,b in zip(digs,reversed(digs)))

def G(q):
 carry=0;digs=[]
 for x in q:
  carry,d=divmod(x+carry,10);digs.append(d)
 if carry:digs.append(carry)
 return tuple(a+b for a,b in zip(digs,reversed(digs))),carry

samples=[];checked=0
for bits in product((0,1),repeat=16):
 free=tuple(rho+9*b for rho,b in zip(word,bits))
 state=mask
 for s in free:state=advance(state,s)
 half=prefix+free+completion[state]
 inv=inverse_half(half)
 q3=half+half[::-1];q2=inv[0]+inv[0][::-1];q1=inv[1]+inv[1][::-1];q0=inv[2]+inv[2][::-1]
 assert G(q0)==(q1,0) and G(q1)==(q2,0) and G(q2)==(q3,0)
 assert all(18 in q for q in(q0,q1,q2,q3))
 # Only a few literal integer examples are needed: all 65536 cases above
 # are independently checked by the exact digit/carry equations.
 if bits in ((0,)*16,(1,)*16,tuple(i%2 for i in range(16))):
  n=canonical_number(q0);orbit=[n]
  for _ in range(4):orbit.append(orbit[-1]+int(str(orbit[-1])[::-1]))
  assert pairword(orbit[3])==q3
  assert all(str(n)!=str(n)[::-1] for n in orbit)
  samples.append(dict(bits=bits,q0=q0,q3=q3,seed=str(n),orbit=list(map(str,orbit))))
 checked+=1
result=dict(status='independent exact arithmetic replay passed',dfa_states=240,compact_transitions_checked=240*16,depth=16,starting_group=g,starting_mask=mask,shortest_positive_outer_prefix=prefix,rho_word_outside_to_inside=word,collection_sizes=list(map(len,levels)),collections=levels,completion_suffix_length=max_suffix+1,completion_table=[dict(state=s,suffix=w) for s,w in sorted(completion.items())],finite_canonical_pairword_width=2*(len(prefix)+16+max_suffix+1),finite_words_checked=checked,samples=samples,prefix_witnesses=short_witnesses,last_solver_result=rows[-1],scope='No uniform killing block of length at most 16 exists for arbitrary rho sequences under three no-overflow inverse layers. Length 17 remains UNKNOWN; no asymptotic contraction or Lychrel existence follows.')
json.dump(result,open(BASE/'independent_witness_audit.json','w'),indent=2)
print(json.dumps({k:v for k,v in result.items() if k not in('collections','completion_table','samples','prefix_witnesses')},indent=2),flush=True)
