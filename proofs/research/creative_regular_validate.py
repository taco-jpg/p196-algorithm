"""Independent checks and witness extraction for the regular-invariant route."""
from itertools import product
from collections import deque
import creative_regular_invariant as r
import json,sys

def realize(w):
 p,c=w
 assert r.valid(w)
 digits=tuple(max(q-9,0) for q in p)+(() if c is None else (c//2,))+tuple(min(q,9) for q in p[::-1])
 return sum(d*10**i for i,d in enumerate(digits))

def witness(dfa):
 delta,finish=dfa;queue=deque([(0,False)]);paths={(0,False):()}
 while queue:
  state,started=queue.popleft();p=paths[state,started]
  for c in [None]+list(range(0,19,2)):
   w=(p,c)
   if r.valid(w) and finish[state][r.terminal_index(c)]:return w,realize(w)
  for q in range(0 if started else 1,19):
   nxt=delta[state][q],True
   if nxt not in paths:paths[nxt]=p+(q,);queue.append(nxt)
 return None

def validate():
 count=0
 for m in range(4):
  for p in product(range(19),repeat=m):
   if p and p[0]==0:continue
   for c in [None]+list(range(0,19,2)):
    w=p,c
    if not r.valid(w):continue
    n=realize(w);actual=n+int(str(n)[::-1]);ds=tuple(map(int,str(actual)));out=r.fold(tuple(a+b for a,b in zip(ds,ds[::-1])))
    assert r.trans(w)==[out],(w,r.trans(w),out)
    assert r.qstep(w)==out
    assert r.bad(w)==(str(actual)==str(actual)[::-1])
    count+=1
 # A verifier must reject the universal language and accept an empty invariant
 # only as safe/closed, never as an existence witness.
 universal=([[0]*19],[[True]*11]);empty=([[0]*19],[[False]*11])
 assert r.safety_counterexample(universal) is not None
 assert r.safety_counterexample(empty) is None and r.closure_counterexample(empty) is None
 assert witness(empty) is None
 result={'canonical_q_words_checked_through_7_digits':count,'transducer_matches_decimal_arithmetic':True,'palindrome_predecessor_matches_actual_palindromicity':True,'empty_language_not_an_existence_witness':True}
 print(json.dumps(result,indent=2))
 with open('creative_regular_validation.json','w') as f:json.dump(result,f,indent=2)

if __name__=='__main__':
 if len(sys.argv)==1:validate()
 else:
  data=json.load(open(sys.argv[1]));dfa=data['dfa']
  assert r.safety_counterexample(dfa) is None,'Not safe'
  assert r.closure_counterexample(dfa) is None,'Not closed'
  found=witness(dfa);assert found is not None,'Empty canonical language'
  w,n=found;print({'accepted_word':w,'representative_integer':n,'lychrel_witness_if_checker_is_correct':n+int(str(n)[::-1])})
