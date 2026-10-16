"""Exact folded-pair transducer and ICE/CEGIS regular invariant synthesis.
No finite sample success is reported as a proof: universal product checks required.
Input representation: (pairs, center), center=None for even length; odd center 0,2,...,18.
Pairs are q_i=d_i+d_{L-1-i}, outermost first.
"""
from collections import deque
import json, time, sys

def C(q,c): return (q+c)//10
def D(q,c): return (q+c)%10

def fold(q):
 return (tuple(q[:len(q)//2]), None if len(q)%2==0 else q[len(q)//2])
def unfold(w):
 p,c=w; return p+(() if c is None else (c,))+p[::-1]
def qstep(w):
 q=unfold(w); carry=0; out=[]
 for x in q:
  out.append(D(x,carry)); carry=C(x,carry)
 if carry: out.append(carry)
 return fold(tuple(x+y for x,y in zip(out,out[::-1])))
def valid(w):
 p,c=w
 return bool(p or c is not None) and (not p or 1<=p[0]<=18) and all(0<=q<=18 for q in p) and (c is None or c in range(0,19,2)) and (bool(p) or c is not None and c>0)
def bad(w):
 p,c=w; q=unfold(w)
 return all(x<=9 for x in q) or q[0]==11 and all(x in (0,11) for x in q)
def trans(w):
 """Enumerate exact finite transducer paths. Must yield one unique output."""
 p,c=w; results=[]
 for overflow in (0,1):
  paths=[(0,overflow,1 if overflow else -1,())]
  for q in p:
   new=[]
   for a,b,t,out in paths:
    for bn in (0,1):
     if C(q,bn)!=b: continue
     an=C(q,a); lo=D(q,a); hi=D(q,bn)
     new.append((an,bn,hi if overflow else -1,out+((lo+t) if overflow else (lo+hi),)))
   paths=new
  for a,b,t,out in paths:
   if c is None:
    if a==b: results.append((out,2*t if overflow else None))
   elif C(c,a)==b:
    if overflow: results.append((out+(D(c,a)+t,),None))
    else: results.append((out,2*D(c,a)))
 return results

def terminal_index(c): return 0 if c is None else c//2+1

def accepted(dfa,w):
 delta,finish=dfa; s=0
 for q in w[0]: s=delta[s][q]
 return finish[s][terminal_index(w[1])]

def safety_counterexample(dfa):
 delta,finish=dfa
 # state DFA, still low-only, still exceptional, length category
 init=(0,True,True,False); todo=deque([init]); paths={init:()}
 while todo:
  s,low,exc,started=todo.popleft(); p=paths[(s,low,exc,started)]
  for c in [None]+list(range(0,19,2)):
   if not started and (c is None or c==0): continue
   isbad=(low and (c is None or c<=9)) or (exc and started and (c is None or c==0))
   if isbad and finish[s][terminal_index(c)]: return (p,c)
  for q in range(0 if started else 1,19):
   nxt=(delta[s][q],low and q<=9,exc and (q in (0,11) if started else q==11),True)
   if nxt not in paths: paths[nxt]=p+(q,);todo.append(nxt)
 return None

def closure_counterexample(dfa):
 delta,finish=dfa
 for overflow in (0,1):
  init=(0,0,0,overflow,1 if overflow else -1,False)
  todo=deque([init]); paths={init:()}
  while todo:
   st=todo.popleft(); si,so,a,b,t,started=st;p=paths[st]
   for c in [None]+list(range(0,19,2)):
    if not started and (c is None or c==0): continue
    if c is None:
     if a!=b: continue
     oc=2*t if overflow else None; sout=so
    else:
     if C(c,a)!=b: continue
     if overflow: sout=delta[so][D(c,a)+t];oc=None
     else: sout=so;oc=2*D(c,a)
    if finish[si][terminal_index(c)] and not finish[sout][terminal_index(oc)]:
     w=(p,c); out=qstep(w)
     assert accepted(dfa,w) and not accepted(dfa,out)
     return w,out
   for q in range(0 if started else 1,19):
    for bn in (0,1):
     if C(q,bn)!=b: continue
     an=C(q,a);lo=D(q,a);hi=D(q,bn);r=lo+t if overflow else lo+hi
     nxt=(delta[si][q],delta[so][r],an,bn,hi if overflow else -1,True)
     if nxt not in paths: paths[nxt]=p+(q,);todo.append(nxt)
 return None

def validate(limit=100000):
 for n in range(1,limit+1):
  ds=tuple(map(int,str(n)[::-1]));q=tuple(a+b for a,b in zip(ds,ds[::-1]));w=fold(q)
  assert valid(w)
  actual=n+int(str(n)[::-1]);ds2=tuple(map(int,str(actual)[::-1]));expected=fold(tuple(a+b for a,b in zip(ds2,ds2[::-1])))
  assert trans(w)==[expected],(n,w,trans(w),expected)
  assert qstep(w)==expected
  assert bad(w)==(str(actual)==str(actual)[::-1])
 print(json.dumps({'validation':limit}),flush=True)

def synth(N,seconds=40,maxiters=10000,seed=((7,),18),shared=None):
 import z3
 started=time.time();solver=z3.Solver();solver.set(timeout=int(seconds*1000))
 delta=[z3.Array('d%d'%s,z3.IntSort(),z3.IntSort()) for s in range(N)]
 # Single two-dimensional flattened lookup via array; keeps state term compact.
 d=z3.Array('delta',z3.IntSort(),z3.IntSort());f=z3.Array('final',z3.IntSort(),z3.BoolSort())
 for s in range(N):
  for q in range(19): solver.add(d[19*s+q]>=0,d[19*s+q]<N)
 def mem(w):
  s=z3.IntVal(0)
  for q in w[0]: s=d[19*s+q]
  return f[11*s+terminal_index(w[1])]
 if seed is not None:
  solver.add(mem(seed))
 else:
  # Every nonempty canonical regular language has a folded word with at most N pairs.
  # One-digit-only cases cannot be closed and avoid palindrome predecessors.
  state=z3.IntVal(0)
  for j in range(N):
   symbol=z3.Int('witness_q%d'%j)
   solver.add(symbol>=(1 if j==0 else 0),symbol<=(18 if j==0 else 19))
   state=z3.If(symbol==19,state,d[19*state+symbol])
  terminal=z3.Int('witness_terminal');solver.add(terminal>=0,terminal<11)
  solver.add(f[11*state+terminal])
 if shared is None: shared={'negative':set(),'implications':set()}
 for w in shared['negative']:solver.add(z3.Not(mem(w)))
 for a,b in shared['implications']:solver.add(z3.Implies(mem(a),mem(b)))
 for iteration in range(maxiters):
  remaining=seconds-(time.time()-started)
  if remaining<=0:return {'states':N,'status':'time','iterations':iteration,'constraints':len(shared['negative'])+len(shared['implications'])}
  solver.set(timeout=max(1,int(remaining*1000)))
  status=solver.check()
  if status!=z3.sat:return {'states':N,'status':str(status),'iterations':iteration,'seconds':time.time()-started,'negative':len(shared['negative']),'implications':len(shared['implications'])}
  m=solver.model();dfa=([[m.eval(d[19*s+q],model_completion=True).as_long() for q in range(19)] for s in range(N)],[[z3.is_true(m.eval(f[11*s+j],model_completion=True)) for j in range(11)] for s in range(N)])
  ce=safety_counterexample(dfa)
  if ce is not None:
   shared['negative'].add(ce);solver.add(z3.Not(mem(ce)));continue
  ce=closure_counterexample(dfa)
  if ce is not None:
   shared['implications'].add(ce);solver.add(z3.Implies(mem(ce[0]),mem(ce[1])));continue
  return {'states':N,'status':'CERTIFICATE','iterations':iteration,'seconds':time.time()-started,'dfa':dfa}
 return {'states':N,'status':'iterations','iterations':maxiters}

if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='validate':validate(int(sys.argv[2]) if len(sys.argv)>2 else 100000)
 else:
  shared={'negative':set(),'implications':set()};results=[]
  for N in range(1,13):
   result=synth(N,40,shared=shared);results.append(result);print(json.dumps(result),flush=True)
   with open('creative_regular_results.json','w') as f:json.dump(results,f,indent=2)
   if result['status']=='CERTIFICATE':break
  with open('creative_regular_constraints.json','w') as f:json.dump({k:list(v) for k,v in shared.items()},f)
