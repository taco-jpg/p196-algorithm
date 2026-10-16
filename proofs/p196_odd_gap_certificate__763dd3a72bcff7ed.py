from collections import deque
from itertools import product

class DFA:
 def __init__(self,tr,end):self.tr=tr;self.end=end
 def accepts(self,s):
  q=0
  for u in s[:len(s)//2]:q=self.tr[q][u]
  term=0 if len(s)%2==0 else 1+s[len(s)//2]//2
  return bool(self.end[q]>>term&1)
 def minimize(self):
  # Moore partition refinement; end masks distinguish all terminal conditions.
  cls=[];d={}
  for v in self.end:
   if v not in d:d[v]=len(d)
   cls.append(d[v])
  while True:
   nc=[];ids={}
   for i,row in enumerate(self.tr):
    key=(self.end[i],tuple(cls[v] for v in row))
    if key not in ids:ids[key]=len(ids)
    nc.append(ids[key])
   if nc==cls:break
   cls=nc
  reps={}
  for i,c in enumerate(cls):reps.setdefault(c,i)
  # BFS to put initial class first and discard unreachable.
  start=cls[0];index={start:0};queue=[start];rows=[];ends=[]
  for c in queue:
   old=reps[c];row=[]
   for j in self.tr[old]:
    cc=cls[j]
    if cc not in index:index[cc]=len(queue);queue.append(cc)
    row.append(index[cc])
   rows.append(row);ends.append(self.end[old])
  return DFA(rows,ends)
 def witness(self):
  queue=deque([(0,())]);seen={0}
  while queue:
   q,p=queue.popleft()
   if self.end[q]:
    e=(self.end[q]&-self.end[q]).bit_length()-1
    return p+p[::-1] if e==0 else p+(2*(e-1),)+p[::-1]
   for u,r in enumerate(self.tr[q]):
    if r not in seen:seen.add(r);queue.append((r,p+(u,)))
  return None

# state: mode, target state, low carry, high carry, previous sum, flags
# flags encode at least one >=10, and at least one outside {0,11}.
def preimage(dfa, safe=True):
 def fl(u):return int(u>=10)+2*int(u not in (0,11))
 initial=frozenset([(0,0,0,0,-1,0),(1,0,0,1,-1,0)])
 def advance(st,u):
  mode,q,x,y,prev,flags=st
  if prev==-1 and u==0:return []
  nf=flags|fl(u);out=[]
  if mode==0:
   xp=(u+x)//10
   for yp in (0,1):
    if (u+yp)//10==y:
     r=2*u+x+yp-10*(xp+y)
     out.append((0,dfa.tr[q][r],xp,yp,u,nf))
  elif prev==-1:
   if u>=9:out.append((1,dfa.tr[q][u%10+1],u//10,1,u,nf))
  else:
   xp=(u+x)//10
   for yp in (0,1):
    if (prev+yp)//10==y:
     r=(u+x)%10+(prev+yp)%10
     out.append((1,dfa.tr[q][r],xp,yp,u,nf))
  return out
 def mask(st):
  mode,q,x,y,prev,flags=st;m=0
  def okay(f):return not safe or f==3
  if prev!=-1 and okay(flags):
   if mode==0 and x==y and dfa.end[q]&1:m|=1
   if mode==1 and (prev+x)//10==y:
    term=1+(prev+x)%10
    if dfa.end[q]>>term&1:m|=1
  for center in range(0 if prev!=-1 else 2,19,2):
   if not okay(flags|fl(center)):continue
   if mode==0:
    if (center+x)//10!=y:continue
    term=1+(center+x)%10
    if dfa.end[q]>>term&1:m|=1<<(1+center//2)
   elif prev==-1:
    if center>=10:
     r=center-9
     if dfa.end[dfa.tr[q][r]]&1:m|=1<<(1+center//2)
   else:
    xp=(center+x)//10
    if (prev+xp)//10!=y:continue
    r=(center+x)%10+(prev+xp)%10
    if dfa.end[dfa.tr[q][r]]&1:m|=1<<(1+center//2)
  return m
 # NFA states that can never reach target acceptance can be omitted using target liveness.
 live={i for i,e in enumerate(dfa.end) if e}
 while True:
  nxt=live|{i for i,row in enumerate(dfa.tr) if any(j in live for j in row)}
  if nxt==live:break
  live=nxt
 index={initial:0};queue=[initial];rows=[];ends=[]
 for subset in queue:
  end=0
  for st in subset:end|=mask(st)
  ends.append(end);row=[]
  for u in range(19):
   ss=frozenset(t for st in subset for t in advance(st,u) if t[1] in live)
   if ss not in index:
    index[ss]=len(queue);queue.append(ss)
    if len(queue)>100000:raise RuntimeError('State bound exceeded')
   row.append(index[ss])
  rows.append(row)
 return DFA(rows,ends).minimize()

def target_b():
 tr=[[1 if u==11 else 2 for u in range(19)],[1 if u in (0,11) else 2 for u in range(19)],[2]*19]
 return DFA(tr,[0,3,0])

def single_word(s):
 p=s[:len(s)//2];h=len(p);tr=[[h+1]*19 for _ in range(h+2)];end=[0]*(h+2)
 for i,u in enumerate(p):tr[i][u]=i+1
 end[h]=1<<(0 if len(s)%2==0 else 1+s[h]//2)
 return DFA(tr,end)


def family(prefix, minimum_zeros, terminal):
 p=list(prefix)+[0]*minimum_zeros
 n=len(p)
 tr=[[n+1]*19 for _ in range(n+2)]
 end=[0]*(n+2)
 for i,u in enumerate(p):tr[i][u]=i+1
 tr[n][0]=n
 end[n]=1<<terminal
 return DFA(tr,end)

def forward(s):
 digits=[]
 carry=0
 for u in s:
  total=u+carry
  digits.append(total%10)
  carry=total//10
 if carry:digits.append(carry)
 q=tuple(a+b for a,b in zip(digits,digits[::-1]))
 return q,digits!=digits[::-1]

def live_states(a):
 rev=[set() for _ in a.tr]
 for i,row in enumerate(a.tr):
  for j in row:rev[j].add(i)
 live={i for i,e in enumerate(a.end) if e}
 todo=list(live)
 for i in todo:
  for j in rev[i]:
   if j not in live:live.add(j);todo.append(j)
 return live

def prefixes(a,k):
 live=live_states(a)
 states=[(0,())]
 for _ in range(k):
  assert all(a.end[q]==0 for q,p in states), 'An earlier terminal needs separate handling'
  states=[(a.tr[q][u],p+(u,)) for q,p in states for u in range(19) if a.tr[q][u] in live]
 return sorted(p for q,p in states)

def main():
 all_chains=[]
 expected={'A':[6,9,17,43,122,155,637,1],'B':[6,6,9,1]}
 for name,start in [('A',family([1,1,1,1],0,1)),('B',family([11,0,11],1,0))]:
  chain=[start]
  for depth in range(1,len(expected[name])):
   chain.append(preimage(chain[-1]))
  sizes=[len(a.tr) for a in chain]
  assert sizes==expected[name],(name,sizes)
  assert chain[-1].witness() is None
  assert all(a.witness() is not None for a in chain[:-1])
  print(name,'DFA state counts:',sizes)
  if name=='A':
   for i,a in enumerate(chain[:-1]):print('A depth',i,'outer triples:',prefixes(a,3))
   assert prefixes(chain[6],2)==[(1,16)]
  all_chains.append(chain)
 # Independent bounded consistency check against literal column addition.
 # This is a software sanity check, NOT the all-length emptiness certificate.
 checked=0
 for L in range(1,8):
  for p in product(range(19),repeat=(L+1)//2):
   if p[0]==0 or (L%2 and p[-1]%2):continue
   s=p+p[:L//2][::-1]
   q,safe=forward(s)
   for chain in all_chains:
    for i in range(len(chain)-1):
     assert chain[i+1].accepts(s)==(safe and chain[i].accepts(q)),(s,i)
   checked+=1
 print('Independent literal-addition checks:',checked,'feasible pair words, length <= 7')
 # Small arithmetic conclusion independent of the automaton code.
 assert [t for t in range(8) if 7*pow(2,t,9)%9==8]==[5]
 assert 3+5<9
 print('Certified partial conclusion: no 1111 0^(2r+1) 1111 is the FIRST palindrome of the 196 trajectory.')
 print('This does not prove the full 196 conjecture.')

if __name__=='__main__':
 main()
