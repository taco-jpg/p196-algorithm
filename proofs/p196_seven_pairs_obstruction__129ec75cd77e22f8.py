from itertools import product
from functools import lru_cache

def digits(s):
 d=[];c=0
 for a in s:
  a+=c;d.append(a%10);c=a//10
 if c:d.append(c)
 return d

def step(s):
 d=digits(s)
 return tuple(x+y for x,y in zip(d,d[::-1]))

@lru_cache(maxsize=200000)
def inverse_all(q):
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
   if tuple(x+y for x,y in zip(d,d[::-1]))==q:ans.add(s)
 return tuple(sorted(ans))

def depth_path(q,depth):
 if depth==0:return [q]
 for p in inverse_all(q):
  ans=depth_path(p,depth-1)
  if ans:return ans+[q]
 return None

def represent(s):
 L=len(s);a=[0]*L
 for i in range(L//2):
  a[L-1-i]=max(1 if i==0 else 0,s[i]-9)
  a[i]=s[i]-a[L-1-i]
 if L%2:a[L//2]=s[L//2]//2
 return int(''.join(map(str,a[::-1])))


from itertools import product
from functools import lru_cache

@lru_cache(None)
def inverse_prefix(q):
 K=len(q);ans=set()
 # Keep K-1 outer layers; the omitted layer certifies the boundary carry.
 states={((),0,0)}
 for i,p in enumerate(q):
  nxt=set()
  for word,x,y in states:
   for u in range(1 if i==0 else 0,19):
    xx=(u+x)//10
    for yy in (0,1):
     if (u+yy)//10==y and 2*u+x+yy-10*(xx+y)==p:
      nxt.add((word+(u,),xx,yy))
  states=nxt
 for word,x,y in states:ans.add(word[:-1])
 if q[0]<=10:
  u=q[0]+9 if q[0]<=9 else 9
  states={((u,),u//10,1)}
  for p in q[1:]:
   nxt=set()
   for word,x,y in states:
    for yy in (0,1):
     if (word[-1]+yy)//10!=y:continue
     digit=p-word[-1]-yy+10*y
     if not 0<=digit<=9:continue
     for xx in (0,1):
      u=digit+10*xx-x
      if 0<=u<=18:nxt.add((word+(u,),xx,yy))
   states=nxt
  for word,x,y in states:
   if any((word[-1]+z)//10==y for z in (0,1)):ans.add(word[:-1])
 return tuple(sorted(ans))

def initial(K):
 return {(14,)+tuple(u for b in bits for u in (9,b))+(9,)*(K%2==0) for bits in product((9,14),repeat=(K-1)//2)}


def T(n): return n+int(str(n)[::-1])
def pal(n): return str(n)==str(n)[::-1]
def D(v): return int(''.join(x*2 for x in str(v)))
def gn_options(v):
 s=str(v);c=int(s[len(s)//2]) if len(s)%2 else 0
 a=sum(x!='0' for x in s[:len(s)//2]);w=sum(map(int,s))
 ks=range(1,2*a+2,2) if c%2 else range(2,2*a+1,2)
 return [k for k in ks if (w-2*k)%11==0]

def construct_gn(v,k):
 u=[]
 for x in str(v)[::-1]:u.extend((int(x),0))
 u.pop();n=len(u);mid=n//2
 support=[i for i,d in enumerate(u) if d]
 left=[i for i in support if i<mid];e=[0]*n
 intervals=[]
 if k%2:
  r=(k-1)//2
  intervals.extend((i,i) for i in left[:r])
  start=left[r] if r<len(left) else mid
  intervals.append((start,n-1-start))
 else:
  r=k//2
  intervals.extend((i,i) for i in left[:r-1])
  intervals.append((left[r-1],left[-1]))
 for lo,hi in intervals:
  for i in range(lo,hi+1):e[i]=e[n-1-i]=1
 s=tuple(d+9*x for d,x in zip(u,e));n0=represent(s)
 assert n0%11==0 and len(str(T(n0)))==len(str(n0))+1
 assert T(T(n0))==D(v)
 return n0

def palindromes(maxlen,alphabet='0123456789'):
 for m in range(1,maxlen+1):
  for first in alphabet[1:]:
   for rest in product(alphabet,repeat=(m+1)//2-1):
    h=first+''.join(rest)
    yield int(h+h[::-1][m%2:])

@lru_cache(None)
def has_ancestor(q,k):
 return k==0 or any(has_ancestor(p,k-1) for p in inverse_all(q))

def check_certificate():
 a=initial(11);counts=[len(a)]
 for _ in range(6):
  a={p for q in a for p in inverse_prefix(q)};counts.append(len(a))
 assert all(q[:2]==(1,12) for q in a)
 a={p for q in a for p in inverse_prefix(q)};counts.append(len(a))
 assert counts==[32,377,1014,1181,136,45,13,0],counts
 short=0
 for halfsize in range(0,11,2):
  words=[()] if halfsize==0 else [(14,)+tuple(u for b in bits for u in (9,b))+(9,) for bits in product((9,14),repeat=halfsize//2-1)]
  for w in words:
   q=w+(14,)+w[::-1]
   assert not has_ancestor(q,7),q
   short+=1
 assert short==32
 print('Universal prefix certificate:',counts,'short words:',short)

def check_general():
 count=0
 for v in palindromes(7):
  q=tuple(map(int,str(D(v))));options=gn_options(v)
  actual=any(len(s)==len(q)-1 and represent(s)%11==0 for s in inverse_all(q))
  assert bool(options)==actual,(v,options,actual)
  for k in options:construct_gn(v,k)
  count+=1
 print('General growth criterion and constructions:',count,'palindromes')

# Independent tests of the two-step binary specialization, both branches.
def check_binary():
 count=0
 for v in palindromes(19,'01'):
  p=D(v);q=tuple(map(int,str(p)));h=str(v).count('1')
  a=bool(gn_options(v));b=all(len(s)%2==0 for s in str(v).split('0') if s)
  gn=any(len(s)==len(q)-1 and represent(s)%11==0 for s in inverse_all(q))
  u=p//11;raw=tuple(11*int(x) for x in str(u));ng=False
  if raw[len(raw)//2]%2==0:
   ng=any(represent(s)%11==0 for s in inverse_all(raw))
  assert (a,b)==(gn,ng),(v,a,b,gn,ng)
  count+=1
 fails=[h for h in range(1,101) if not any((h-k)%2==0 and (h-2*k)%11==0 for k in range(1,h+1))]
 assert fails==[1,2,3,5,6,7,9,10,14,18]
 print('Binary complete criterion:',count,'targets')

# Validate the prefix over-approximation against actual integer addition.
def check_prefix_soundness():
 import random
 rng=random.Random(196)
 for _ in range(3000):
  n=rng.randrange(10**25,10**29);s0=str(n);s=tuple(int(x)+int(y) for x,y in zip(s0,s0[::-1]))
  q=step(s)
  assert s[:10] in inverse_prefix(q[:11])
 print('Prefix soundness cross-check: 3000 integer sources')

def check_orbit_and_sharpness():
 n=196;first=[]
 for t in range(9):first.append(n);assert not pal(n);n=T(n)
 assert first==[196,887,1675,7436,13783,52514,94039,187088,1067869]
 n=13310020608909159190
 assert n%11==0
 for _ in range(8):assert not pal(n);n=T(n)
 assert n==5500555500550055550055 and pal(n)
 print('196 initial segment and sharp eight-step example passed')

if __name__=='__main__':
 check_certificate()
 check_general()
 check_binary()
 check_prefix_soundness()
 check_orbit_and_sharpness()
 print('All checks passed. This is not a proof of the full 196 conjecture.')

