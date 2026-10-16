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


def high_words(max_length):
 C=(10,12,14,16)
 for n in range(1,max_length+1,2):
  if n==1:
   for c in C:yield (c,)
   continue
  h=n//2;places=list(range(0,h,2))
  for vals in product(C,range(1)): # outer entry is nonzero
   first=vals[0]
   for tail in product((0,)+C,repeat=len(places)-1):
    left=[0]*h
    for i,c in zip(places,(first,)+tail):left[i]=c
    centers=((0,)+C) if h%2==0 else (0,)
    for c in centers:yield tuple(left)+(c,)+tuple(left[::-1])

def check_prefix_certificate():
 C=(10,12,14,16)
 states={(c,0,a,0,b,0,d) for c in C for a,b,d in product((0,)+C,repeat=3)}
 counts=[len(states)]
 for _ in range(5):
  states={p for q in states for p in inverse_prefix(q)};counts.append(len(states))
 assert counts==[500,100,56,17,2,0],counts
 print('prefix certificate:',counts,flush=True)

def check_full_high_words():
 count=0;maximum=0
 for q0 in high_words(17):
  states={q0};height=-1
  while states:
   height+=1
   assert height<=4,(q0,states)
   if len(q0)>=5 and height==4:
    assert all(s[:3] in ((1,0,0),(1,0,1)) for s in states)
   states={p for q in states for p in inverse(q)}
  count+=1;maximum=max(maximum,height)
 assert count==3748,(count,maximum)
 print('full high-word cases:',count,'maximum depth:',maximum,flush=True)

def all_raw_words(max_length):
 for n in range(1,max_length+1):
  if n==1:
   for c in range(2,19,2):yield (c,)
   continue
  for first in range(1,19):
   for tail in product(range(19),repeat=n//2-1):
    left=(first,)+tail
    centers=range(0,19,2) if n%2 else (None,)
    for c in centers:yield left+(c,)+left[::-1] if c is not None else left+left[::-1]

def check_growth_rules():
 count=0
 for s in all_raw_words(7):
  a=normalize(s);p=F(s);growth=len(a)>len(s)
  if not growth:assert p[0]>=2
  elif p[0]<=9 and len(p)>=3:
   j=p[0];assert j-1<=p[1]<=j+9
   if j==1 and p[1]==0:assert p[2]>=9
   if j==1 and p[1]==5:assert p[2]>=3
   if j==1 and p[1]==10:assert p[2]>=8
   if j in (2,3) and p[1]==10:assert p[2]>=6
  count+=1
 assert count==75447
 print('actual integer carry-rule checks:',count,flush=True)

def check_generalized_targets():
 count=0;by_h=[]
 for h in (3,5,7,9,11,13):
  skeletons=0;a=(h-1)//2
  for left in product((1,3,5,7),repeat=a):
   for center in (1,3,5,7):
    values=left+(center,)+left[::-1]
    if (sum(values)-2*h)%11:continue
    skeletons+=1
    for gaps in ((0,)*a,tuple(i%2 for i in range(a))):
     v=with_gaps(values,gaps);target=D(v);raw=ds(target)
     parents=inverse(raw)
     assert not any(len(s)==len(raw) for s in parents)
     gn={s for s in parents if len(s)==len(raw)-1 and representative(s)%11==0}
     expected=tuple(x+9 if x else 0 for x in ds(I(v)))
     assert gn=={expected},(v,gn)
     roots={expected}
     for _ in range(5):roots={p for q in roots for p in inverse(q)}
     assert not roots,v
     # Every target has a first-hit two-step source divisible by 11.
     root=representative(expected)
     assert root%11==0 and str(root)!=str(root)[::-1]
     middle=T(root)
     assert str(middle)!=str(middle)[::-1] and T(middle)==target
     count+=1
  by_h.append((h,skeletons))
 print('generalized target cases:',count,'skeleton counts:',by_h,flush=True)

def check_sharpness_and_196():
 root=1003100101010909090299000;n=root;path=[]
 for k in range(7):path.append(n);assert n%11==0;n=T(n)
 assert path==[1003100101010909090299000,1013021010101010100312001,2015151020202020201515102,4030302040404040403030204,8050605080808080805060508,16101210161616161610121016,77113311777777777711331177]
 V=7131777771317
 assert len(str(V))==13 and sum(map(int,str(V)))==59 and D(V)==path[-1]
 q0=q(path[4]);assert all(x==0 if i%2 else x in (0,10,12,14,16) for i,x in enumerate(q0))
 states={q0}
 for _ in range(4):states={p for z in states for p in inverse(z)}
 assert q(root) in states
 states={p for z in states for p in inverse(z)};assert not states
 n=196;early=[]
 for _ in range(10):early.append(n);n=T(n)
 assert early[-1]==10755470 and all(n not in (557755,773377) for n in early)
 print('sharp six-step 11-multiple source:',root,flush=True)
 print('196 initial segment:',early,flush=True)

if __name__=='__main__':
 check_growth_rules();check_prefix_certificate();check_full_high_words();check_generalized_targets();check_sharpness_and_196()
