from itertools import product
from collections import Counter
from functools import lru_cache

def T(n): return n+int(str(n)[::-1])
def D(v): return int(''.join(x*2 for x in str(v)))
def I(v): return int('0'.join(str(v)))
def ds(n): return tuple(map(int,str(n)[::-1]))
def q(n):
 a=ds(n);return tuple(x+y for x,y in zip(a,a[::-1]))
def normalize(s):
 a=[];carry=0
 for x in s:
  carry,x=divmod(x+carry,10);a.append(x)
 if carry:a.append(carry)
 return tuple(a)
def F(s):
 a=normalize(s);return tuple(x+y for x,y in zip(a,a[::-1]))
def feasible(s):
 return bool(s) and s[0]>0 and s==s[::-1] and all(0<=x<=18 for x in s) and (len(s)%2==0 or s[len(s)//2]%2==0)
def representative(s):
 a=[0]*len(s)
 for i in range(len(s)//2):
  a[-1-i]=max(1 if i==0 else 0,s[i]-9);a[i]=s[i]-a[-1-i]
 if len(s)%2:a[len(s)//2]=s[len(s)//2]//2
 return sum(d*10**i for i,d in enumerate(a))

@lru_cache(maxsize=10000)
def inverse(qt):
 # Exact inverse of F on feasible symmetric digit-sum words.
 L=len(qt);ans=set()
 for grow in (0,1):
  n=L-grow
  if n<1:continue
  half=(n+1)//2
  if not grow:
   states=[((),0,0)]
   for p in qt[:half]:
    nxt=[]
    for word,x,y in states:
     for u in range(1 if not word else 0,19):
      xx=(u+x)//10
      for yy in (0,1):
       if (u+yy)//10==y and 2*u+x+yy-10*(xx+y)==p:
        nxt.append((word+(u,),xx,yy))
    states=nxt
   words=[word for word,_,_ in states]
  else:
   if qt[0]>10:continue
   u=qt[0]+9 if qt[0]<=9 else 9
   states=[((u,),u//10,1)]
   for p in qt[1:half]:
    nxt=[]
    for word,x,y in states:
     for yy in (0,1):
      if (word[-1]+yy)//10!=y:continue
      b=p-word[-1]-yy+10*y
      if 0<=b<=9:
       for xx in (0,1):
        u=b+10*xx-x
        if 0<=u<=18:nxt.append((word+(u,),xx,yy))
    states=nxt
   words=[word for word,_,_ in states]
  for word in words:
   s=word+word[:n//2][::-1]
   if feasible(s) and F(s)==qt:ans.add(s)
 return tuple(sorted(ans))

def v2(n):
 k=0
 while n%2==0:k+=1;n//=2
 return k

def with_gaps(values,gaps):
 # Palindromic nonzero skeleton and its symmetric zero gaps.
 a=len(gaps);allgaps=tuple(gaps)+tuple(gaps)[::-1]
 assert len(values)==2*a+1
 return int(''.join(str(x)+('0'*allgaps[i] if i<len(allgaps) else '') for i,x in enumerate(values)))

def test_local():
 count=0
 for s,x,y,xx,yy in product(range(19),range(2),range(2),range(2),range(2)):
  if (s+x)//10!=xx or (s+yy)//10!=y:continue
  p=2*s+x+yy-10*(xx+y)
  if p!=9:
   assert xx==y
   assert (xx^yy)==(x^y^(p%2))
  count+=1
 total=0
 for n in range(1,8):
  if n==1:words=[(c,) for c in range(2,19,2)]
  else:
   words=[]
   for first in range(1,19):
    for mid in product(range(19),repeat=n//2-1):
     left=(first,)+mid
     if n%2:
      words.extend(left+(c,)+left[::-1] for c in range(0,19,2))
     else:words.append(left+left[::-1])
  for s in words:
   a=normalize(s);p=F(s)
   if len(a)==n and all(x%2==0 for x in p):assert a==a[::-1]
   # The inverse algorithm must recover every actual source.
   assert s in inverse(p)
   total+=1
 print('local carry transitions:',count,'actual raw words:',total,flush=True)

def test_sparse_height():
 count=0
 for h in (3,5,7):
  for gaps in product(range(3),repeat=(h-1)//2):
   B=with_gaps((1,)*h,gaps);U=I(B)
   for d in range(1,10):
    p=ds(d*U)
    states={p} if feasible(p) else set();height=0
    while states:
     height+=1
     states={s for z in states for s in inverse(z)}
     assert height<=4
    assert height==v2(d),(B,d,height)
    count+=1
   for c in (10,12,14,16,18):
    raw=tuple(c*x for x in ds(U));states={raw};height=-1
    while states:
     height+=1;states={s for z in states for s in inverse(z)}
     assert height<=4
    assert height==v2(c//2),(B,c,height)
 print('sparse palindrome height cases:',count,flush=True)

def test_eleven():
 cases=0
 for gaps in product(range(2),repeat=5):
  B=with_gaps((1,)*11,gaps);U=I(B)
  for d in range(1,9):
   p=D(d*B);raw=ds(p);parents=inverse(raw)
   nn={s for s in parents if len(s)==len(raw)}
   gn={s for s in parents if len(s)==len(raw)-1 and representative(s)%11==0}
   assert nn==({tuple(x//2 for x in raw)} if d%2==0 else set()),(d,B,'NN')
   expected=tuple((d+9)*x for x in ds(U))
   assert gn==({expected} if d%2 else set()),(d,B,'GN')
   f=v2(d);u=d//2**f;a=(u+9)//2;e=v2(a);root=(a//2**e)*U
   assert root%11==0
   n=root
   for _ in range(f+e+2):n=T(n)
   assert n==p,(d,B,'sharpness')
   cases+=1
 print('eleven-one skeletons, exact last-two-step branches and sharp constructions:',cases,flush=True)

def test_mixed():
 cases=0
 for h in (5,7,9,11):
  a=(h-1)//2
  for left in product((1,3,5,7),repeat=a):
   for center in (1,5):
    values=left+(center,)+left[::-1]
    if (sum(values)-2*h)%11:continue
    for gaps in ((0,)*a,tuple((i+sum(left))%3 for i in range(a))):
     v=with_gaps(values,gaps);raw=ds(D(v));parents=inverse(raw)
     assert not any(len(s)==len(raw) for s in parents),(v,'NN')
     gn={s for s in parents if len(s)==len(raw)-1 and representative(s)%11==0}
     expected=tuple(x+9 if x else 0 for x in ds(I(v)))
     assert gn=={expected},(v,'GN')
     assert not inverse(expected),(v,'extra ancestor')
     cases+=1
 print('mixed-digit targets, all two-step branches and third-step obstruction:',cases,flush=True)

def count_skeletons():
 counts=[]
 for h in range(1,22,2):
  c=Counter({0:1})
  for _ in range((h-1)//2):
   nxt=Counter()
   for r,n in c.items():
    for d in (1,3,5,7):nxt[(r+d)%11]+=n
   c=nxt
  count=sum(n for r,n in c.items() for center in (1,5) if (2*r+center-2*h)%11==0)
  counts.append((h,count))
 assert counts==[(1,0),(3,0),(5,7),(7,1),(9,71),(11,167),(13,579),(15,4054),(17,7800),(19,58857),(21,172801)]
 print('mixed-digit skeleton counts:',counts,flush=True)

if __name__=='__main__':
 test_local();test_sparse_height();test_eleven();test_mixed();count_skeletons()
 n=196;early=[]
 for _ in range(9):early.append(n);n=T(n)
 assert early==[196,887,1675,7436,13783,52514,94039,187088,1067869]
 print('196 initial segment:',early,flush=True)
