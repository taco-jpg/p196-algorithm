import creative_regular_invariant as r
import z3,json,time,sys

def safety_batch(dfa):
 from collections import deque
 delta,finish=dfa;init=(0,True,True,False);todo=deque([init]);paths={init:()};result=[]
 while todo:
  st=todo.popleft();s,low,exc,started=st;p=paths[st]
  for c in [None]+list(range(0,19,2)):
   if not started and (c is None or c==0):continue
   isbad=(low and (c is None or c<=9)) or (exc and started and (c is None or c==0))
   if isbad and finish[s][r.terminal_index(c)]:result.append((p,c))
  for q in range(0 if started else 1,19):
   nxt=(delta[s][q],low and q<=9,exc and (q in (0,11) if started else q==11),True)
   if nxt not in paths:paths[nxt]=p+(q,);todo.append(nxt)
 return result

class Learner:
 def __init__(self,N,seed=((7,),18)):
  self.N=N; self.s=z3.Solver();self.count=0
  self.d=[[[z3.Bool('d_%d_%d_%d'%(s,q,t)) for t in range(N)] for q in range(19)] for s in range(N)]
  self.f=[[z3.Bool('f_%d_%d'%(s,j)) for j in range(11)] for s in range(N)]
  for row in self.d:
   for dest in row:self.s.add(z3.PbEq([(v,1) for v in dest],1))
  # Symbolic reachability of the product with the exact bad-language monitor.
  reach=[[z3.Bool('reach_%d_%d'%(s,m)) for m in range(4)] for s in range(N)]
  self.s.add(reach[0][0])
  for a in range(N):
   for m in range(4):
    for q in range(1 if m==0 else 0,19):
     if m==0:nm=1 if q<=9 else (2 if q==11 else 3)
     elif m==1:nm=1 if q<=9 else 3
     elif m==2:nm=2 if q in (0,11) else 3
     else:nm=3
     for b in range(N):self.s.add(z3.Or(z3.Not(reach[a][m]),z3.Not(self.d[a][q][b]),reach[b][nm]))
    for c in [None]+list(range(0,19,2)):
     if m==0 and (c is None or c==0):continue
     bad=(m==0 and c<=9) or (m==1 and (c is None or c<=9)) or (m==2 and (c is None or c==0))
     if bad:self.s.add(z3.Or(z3.Not(reach[a][m]),z3.Not(self.f[a][r.terminal_index(c)])))
  self.prefix={():[z3.BoolVal(t==0) for t in range(N)]};self.members={}
  if seed is not None:
   # These labels are forced by the requested invariant, not by conjectured termination.
   w=seed
   for k in range(50):
    self.s.add(self.mem(w));w=r.qstep(w)
  else:
   syms=[z3.Int('witness_symbol_%d'%j) for j in range(N)]
   states=[[z3.Bool('witness_state_%d_%d'%(j,t)) for t in range(N)] for j in range(N+1)]
   for t in range(N):self.s.add(states[0][t]==(t==0))
   for j in range(N):
    self.s.add(z3.PbEq([(v,1) for v in states[j+1]],1));self.s.add(syms[j]>=(1 if j==0 else 0),syms[j]<=(18 if j==0 else 19))
    for a in range(N):
     for b in range(N):
      self.s.add(z3.Implies(z3.And(states[j][a],syms[j]==19),states[j+1][a]))
      for q in range(19):self.s.add(z3.Implies(z3.And(states[j][a],syms[j]==q,self.d[a][q][b]),states[j+1][b]))
   self.s.add(z3.Or([z3.And(states[N][a],self.f[a][j]) for a in range(N) for j in range(11)]))
  # Terminating seeds give unconditional negative labels, retaining their q words.
  neg=set()
  for n in range(1,1001):
   ds=tuple(map(int,str(n)));w=r.fold(tuple(a+b for a,b in zip(ds,ds[::-1])))
   chain=[]
   for k in range(15):
    if r.bad(w):neg.update(chain+[w]);break
    chain.append(w);w=r.qstep(w)
  for w in neg:self.s.add(z3.Not(self.mem(w)))
  self.initialneg=len(neg)
 def pref(self,p):
  if p in self.prefix:return self.prefix[p]
  parent=self.pref(p[:-1]);q=p[-1];index=len(self.prefix)
  col=[z3.Bool('prefix_%d_%d'%(index,t)) for t in range(self.N)]
  self.prefix[p]=col;self.s.add(z3.PbEq([(v,1) for v in col],1))
  for a in range(self.N):
   for b in range(self.N):self.s.add(z3.Or(z3.Not(parent[a]),z3.Not(self.d[a][q][b]),col[b]))
  return col
 def mem(self,w):
  if w in self.members:return self.members[w]
  index=len(self.members);v=z3.Bool('membership_%d'%index);self.members[w]=v
  col=self.pref(w[0]);j=r.terminal_index(w[1]);self.s.add(v==z3.Or([z3.And(col[a],self.f[a][j]) for a in range(self.N)]));return v
 def model(self):
  m=self.s.model();delta=[[next(b for b in range(self.N) if z3.is_true(m.eval(self.d[a][q][b],model_completion=True))) for q in range(19)] for a in range(self.N)];finish=[[z3.is_true(m.eval(v,model_completion=True)) for v in row] for row in self.f];return delta,finish

def run(N,seconds=30,seed=((7,),18)):
 start=time.time();L=Learner(N,seed);neg=imp=0
 for i in range(10000):
  remain=seconds-(time.time()-start)
  if remain<=0:return {'states':N,'status':'time','iterations':i,'seconds':time.time()-start,'negative':neg,'implications':imp,'initialnegative':L.initialneg}
  L.s.set(timeout=int(remain*1000));status=L.s.check()
  if status!=z3.sat:return {'states':N,'status':str(status),'iterations':i,'seconds':time.time()-start,'negative':neg,'implications':imp,'initialnegative':L.initialneg}
  dfa=L.model();ces=safety_batch(dfa)
  if ces:
   for ce in ces:L.s.add(z3.Not(L.mem(ce)));neg+=1
   continue
  ce=r.closure_counterexample(dfa)
  if ce is not None:L.s.add(z3.Implies(L.mem(ce[0]),L.mem(ce[1])));imp+=1;continue
  return {'states':N,'status':'CERTIFICATE','iterations':i,'seconds':time.time()-start,'dfa':dfa}

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description='Synthesize a regular reverse-add invariant; no certificate is assumed to exist.')
 parser.add_argument('objective',nargs='?',choices=['196','any'],default='196')
 parser.add_argument('--min-states',type=int,default=2)
 parser.add_argument('--max-states',type=int,default=8)
 parser.add_argument('--seconds',type=float,default=35)
 parser.add_argument('--output')
 args=parser.parse_args()
 if args.min_states<1 or args.max_states<args.min_states:parser.error('invalid state bounds')
 results=[];anyseed=args.objective=='any';kind=args.objective
 for n in range(args.min_states,args.max_states+1):
  result=run(n,args.seconds,seed=None if anyseed else ((7,),18));results.append(result);print(json.dumps(result),flush=True)
  with open(args.output or 'creative_regular_boolean_%s_results.json'%kind,'w') as f:json.dump(results,f,indent=2)
  if result['status']=='CERTIFICATE':break
