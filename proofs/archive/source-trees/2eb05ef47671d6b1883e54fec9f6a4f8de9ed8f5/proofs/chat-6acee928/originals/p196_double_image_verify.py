#!/usr/bin/env python3
"""P196 partial results: exact automaton certificate and finite cross-checks.

Python 3, standard library only. No claim to prove the full 196 conjecture.
The pure two-step theorem is proved in p196_double_image_theorem.md.
The automaton certificate concerns FIRST palindrome hits with final digit growth.
"""
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
     out.append((0,dfa.tr[q][r],xp,yp,0,nf))
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
    if len(queue)>600000:raise RuntimeError('State bound exceeded')
   row.append(index[ss])
  rows.append(row)
 return DFA(rows,ends).minimize()

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

def digits(s):
 d=[];c=0
 for a in s:
  a+=c;d.append(a%10);c=a//10
 if c:d.append(c)
 return d

def step(s):
 d=digits(s)
 return tuple(x+y for x,y in zip(d,d[::-1]))

def inverse(q):
 L=len(q);ans=set()
 for grow in (False,True):
  m=L-int(grow)
  if m<1:continue
  h=(m+1)//2
  if not grow:
   states=[((),0,0)]
   for i in range(h):
    nxt=[]
    for p,x,y in states:
     for u in range(1 if i==0 else 0,19):
      xp=(u+x)//10
      for yp in (0,1):
       if (u+yp)//10==y and 2*u+x+yp-10*(xp+y)==q[i]:nxt.append((p+(u,),xp,yp))
    states=nxt
   ps=[p for p,x,y in states]
  else:
   if q[0]>10:continue
   u0=q[0]+9 if q[0]<=9 else 9
   states=[((u0,),u0//10,1)]
   for i in range(1,h):
    nxt=[]
    for p,x,y in states:
     for yp in (0,1):
      if (p[-1]+yp)//10!=y:continue
      digit=q[i]-p[-1]-yp+10*y
      if not 0<=digit<=9:continue
      for xp in (0,1):
       u=digit+10*xp-x
       if 0<=u<=18:nxt.append((p+(u,),xp,yp))
    states=nxt
   ps=[p for p,x,y in states]
  for p in ps:
   if m%2 and p[-1]%2:continue
   s=p+p[:m//2][::-1]
   d=digits(s)
   if tuple(x+y for x,y in zip(d,d[::-1]))==q and d!=d[::-1]:ans.add(s)
 return tuple(sorted(ans))

def T(n):
 return n+int(str(n)[::-1])

def palindrome(n):
 s=str(n)
 return s==s[::-1]

def leading_one_palindromes(max_length, min_length=1):
 for length in range(min_length,max_length+1):
  half=(length+1)//2
  for tail in product('0123456789',repeat=half-1):
   p='1'+''.join(tail)
   yield int(p+p[::-1][length%2:])

def constructive_source(u):
 return int(''.join(str((int(d)+9*(int(d)%2))//2) for d in str(u)))

def target_two_blocks_growth():
 tr=[[4]*19 for _ in range(5)]
 tr[0][11]=1
 tr[1][0]=2
 tr[2][11]=1
 tr[2][0]=3
 tr[3][0]=3
 return DFA(tr,[0,2,3,3,0])

def feasible_pair_words(max_length):
 for length in range(1,max_length+1):
  half=length//2
  if half==0:
   for center in range(2,19,2):yield (center,)
   continue
  for outer in range(1,19):
   for tail in product(range(19),repeat=half-1):
    p=(outer,)+tail
    if length%2:
     for center in range(0,19,2):yield p+(center,)+p[::-1]
    else:yield p+p[::-1]

def verify_automata():
 import re
 expected=[5,7,15,34,132,506,292,1208,4982,1]
 chain=[target_two_blocks_growth()]
 for _ in range(9):chain.append(preimage(chain[-1]))
 sizes=[len(a.tr) for a in chain]
 assert sizes==expected,sizes
 assert chain[-1].witness() is None
 assert all(a.witness() is not None for a in chain[:-1])
 checked=0
 for s in feasible_pair_words(7):
  q,nonpal=forward(s)
  d=digits(s)
  p=''.join(map(str,d[::-1]))
  target=(len(d)==len(s)+1 and p==p[::-1]
          and re.fullmatch(r'(1+)(0*)\1',p) is not None)
  assert chain[0].accepts(s)==target,(s,p)
  for a,b in zip(chain,chain[1:]):
   assert b.accepts(s)==(nonpal and a.accepts(q)),s
  checked+=1
 assert checked==75447,checked
 print('Exact inverse DFA sizes:',sizes)
 print('Independent transition checks:',checked,'pair words, all 9 transitions')

def verify_pure_theorem():
 checked=0
 for p in leading_one_palindromes(9,2):
  quotient=p//11
  criterion=(p%11==0 and palindrome(quotient))
  # F(s)=digits(P) asks for a source whose intermediate image has
  # these paired sums. It supplies a two-step antecedent with a
  # non-growing final step. The theorem also proves this is enough.
  actual=bool(inverse(tuple(map(int,str(p)[::-1]))))
  assert actual==criterion,p
  if criterion:assert T(T(constructive_source(quotient)))==p,p
  checked+=1
 assert checked==12221,checked
 print('Leading-1 palindrome targets checked through 9 digits:',checked)
 count=0
 for u in leading_one_palindromes(7):
  a=constructive_source(u)
  assert palindrome(a) and T(T(a))==11*u,u
  count+=1
 assert count==1222,count
 print('Constructive identities checked:',count)
 count=0
 for n in range(1,1000000):
  p=T(T(n))
  if str(p).startswith('1') and palindrome(p):
   assert p%11==0 and palindrome(p//11),(n,p)
   count+=1
 assert count==43048,count
 print('Direct integer scan: 999999 inputs;',count,'relevant outputs')

def verify_examples():
 examples=[
  (100819000,9,111100001111),
  (1500006399295,8,11111111011111111),
  (15000323000014699224099994295,8,111111111111111101111111111111111),
 ]
 for seed,steps,target in examples:
  n=seed
  assert not palindrome(n)
  for t in range(1,steps+1):
   previous=n
   n=T(n)
   assert palindrome(n)==(t==steps),(seed,t,n)
  assert n==target,(seed,n)
  if steps==9:assert len(str(n))==len(str(previous))+1
  print('Example:',seed,'first reaches',target,'after',steps,'steps')
 n=196
 for _ in range(9):
  n=T(n)
  assert not palindrome(n)
 assert n==10755470
 assert T(T(1190))==3113 and 3113//11==283
 assert T(T(154))==1111 and 1111//11==101 and 101%11!=0

if __name__=='__main__':
 verify_automata()
 verify_pure_theorem()
 verify_examples()
 print('All checks passed. The full 196 conjecture is NOT proved.')
