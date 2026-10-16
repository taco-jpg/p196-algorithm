#!/usr/bin/env python3
"""Independent literal arithmetic controls, supplementary to the all-width proofs."""
from __future__ import annotations
import argparse,hashlib,itertools,json,time
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True)
OUT=parser.parse_args().output.resolve()
if OUT.exists():raise ValueError('Refusing to overwrite prior evidence')
OUT.parent.mkdir(parents=True,exist_ok=True)
def digits(n,b=10):
 d=[]
 while n:d.append(n%b);n//=b
 return d or [0]
def value(d,b=10):return sum(x*b**i for i,x in enumerate(d))
def step(n,b=10):return n+value(digits(n,b)[::-1],b)
def pal(n,b=10):d=digits(n,b);return d==d[::-1]
def pair(d):return tuple(x+y for x,y in zip(d,d[::-1]))
def carryword(n):
 d=digits(n);q=pair(d);c=[0]
 for s in q:c.append((s+c[-1])//10)
 return tuple(c),q
start=time.monotonic();report={'agent':'Agent #1','role':'independent finite controls, not replacements for universal Lean proofs','status':'RUNNING'}
# Canonical inputs in bases 3..12, including widths one and palindromic seeds.
threshold=interval=firstone=firsttwo=alln=0
for b in range(3,13):
 for n in range(1,b**4):
  alln+=1;d=digits(n,b);q=pair(d)
  if q[0]<b or not all(b-1<=x<=2*b-2 for x in q):continue
  threshold+=1;a=step(n,b);z=step(a,b)
  assert pal(z,b)==all(x+y<=3*b-3 for x,y in zip(q,q[1:])),(b,n,'threshold')
  assert pal(a,b)==all(x==b+1 for x in q),(b,n,'first output')
  if all(x<=b+(b-1)//2-1 for x in q):
   interval+=1
   if pal(a,b):firstone+=1;assert all(x==b+1 for x in q)
   else:firsttwo+=1;assert pal(z,b)
report['high_base']={'bases':list(range(3,13)),'positive_canonical_seeds':alln,'max_width':4,'threshold_hypotheses_satisfied':threshold,'interval_hypotheses_satisfied':interval,'first_positive_one':firstone,'first_positive_two':firsttwo,'continued_after_initial_or_earlier_palindromes':True}
# Full carry histories for ordinary decimal seeds. Test collisions in identical
# initial width, not the erroneous assertion that initial integers are unique.
seen={};collisions=0;next_equal_not_seed_equal=0
for n in range(1,100000):
 v=n;history=[]
 for t in range(9):
  cw,q=carryword(v);history.append(cw);v=step(v)
 key=(len(digits(n)),tuple(history));q0=pair(digits(n));nextn=step(n)
 if key in seen:
  p,pq,pnext=seen[key];collisions+=1
  assert q0==pq and nextn==pnext,(p,n,'nine-carry collision')
  if p!=n:next_equal_not_seed_equal+=1
 else:seen[key]=(n,q0,nextn)
report['carry_observability']={'seeds':[1,99999],'time_indices':[0,8],'complete_carries_include_initial_and_terminal':True,'equal_history_collisions':collisions,'distinct_seed_same_next_collisions':next_equal_not_seed_equal,'history_classes':len(seen),'conclusion':'pair-sum equality and equal next integer, not equal initial integer'}
# Recompute necessary two-column graph with divmod and actual next-digit pair
# formulas, independent of the author's packed rank literal.
states=[(p,q) for p in range(1,19) for q in range(19)]
def edge(s,e):
 p,q=s;a=p//10;u=(q+e)//10;b=(q+a)//10;h=(p+u)//10
 if not h: nxt=(p%10+(p+u)%10,(q+a)%10+(q+e)%10)
 else:nxt=(p%10+1,(q+a)%10+(p+u)%10)
 assert nxt in state_set and h in (0,1)
 return nxt,1-h
state_set=set(states);dp={s:0 for s in states};mins=[]
for t in range(1,10):
 dp={s:min(cost+dp[nxt] for nxt,cost in [edge(s,0),edge(s,1)]) for s in states}
 mins.append(min(dp.values()))
 if t==8:assert dp[(13,6)]==3
assert mins[-1]>=4
report['carry_necessary_graph']={'states':len(states),'edges':len(states)*2,'minimum_nonoverflow_by_steps_1_through_9':mins,'eight_step_obstruction_state':[13,6]}
# Outer charge: independent straightforward list arithmetic, no external decimal
# bridge assumed. Every B of length <=3, alphabet0..18, positive outer digit.
def normalize(w,e):
 d=[]
 for x in w:e,a=divmod(x+e,10);d.append(a)
 return d,e
def outer(c,w):
 k=int(c>=9);t=c-9*k;ld,le=normalize(w,0);rd,re=normalize(w[::-1],k)
 r=[1]+rd[::-1] if re==1 else rd[::-1]+[t]
 nxt=[a+b for a,b in zip(ld+[c+le-10*k],r)];c=2*t
 while nxt and nxt[-1]==c:nxt.pop()
 return c,nxt
def charge(c,w):return (2*sum((-1)**i*x for i,x in enumerate(w))+(-1)**len(w)*c)%11
outer_count=0;witness=None
for c0 in range(1,18):
 if c0==9:continue
 for L in range(4):
  for tup in itertools.product(range(19),repeat=L):
   if tup and tup[0]==0:continue
   c,w=c0,list(tup);zs=[charge(c,w)]
   for t in range(7):
    c,w=outer(c,w)
    assert 1<=c<=17 and c!=9 and all(0<=x<=18 for x in w) and (w[0] if w else c)>0
    zs.append(charge(c,w))
   assert zs[5:]==[0,0,0],(c0,tup,zs)
   if c0==1 and not tup:witness=zs;assert zs[4]!=0 and zs[5]==0
   outer_count+=1
report['outer_charge']={'initial_phases':16,'max_initial_exterior_length':3,'alphabet':[0,18],'valid_initial_states_checked':outer_count,'verified_through_time':7,'sharpness_charge_history_c1_empty':witness,'ordinary_integer_semiconjugacy_used':False}
report['status']='PASS';report['elapsed_seconds']=round(time.monotonic()-start,6);report['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();OUT.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
