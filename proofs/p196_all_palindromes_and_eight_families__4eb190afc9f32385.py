# Python 3; standard library only.
# This verifies the stated finite cross-checks, not the complete 196 conjecture.
from itertools import product
import re

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

def represent(s):
 L=len(s);a=[0]*L
 for i in range(L//2):
  a[L-1-i]=max(1 if i==0 else 0,s[i]-9)
  a[i]=s[i]-a[L-1-i]
 if L%2:a[L//2]=s[L//2]//2
 return int(''.join(map(str,a[::-1])))

from itertools import product
import re

def T(n):return n+int(str(n)[::-1])
def pal(n):return str(n)==str(n)[::-1]
def exception(p):
 return p in (22,44,66,88,242) or re.fullmatch(r'22(?:00)*22',str(p)) is not None

def growth_condition(p):return p%11==0 and pal(p//11) and not exception(p)

def nongrowth_source(p):
 digits=tuple(map(int,str(p)))
 L=len(digits)
 states={(0,0):()}
 for i,d in enumerate(digits[:L//2]):
  nxt={}
  for (x,y),word in states.items():
   xx=y;yy=x^(d%2)
   u=10*y+(d-x-yy)//2
   if 0<=u<=18 and (i>0 or u>0):
    assert (u+x)//10==xx and (u+yy)//10==y
    nxt[(xx,yy)]=word+(u,)
   if d==9 and x!=y:
    nxt[(x,y)]=word+(9,)
  states=nxt
 for (x,y),word in states.items():
  if L%2==0:
   if x==y:return represent(word+word[::-1])
  else:
   d=digits[L//2]
   if d%2==0 and x==(d//2)%2:
    u=d//2-x+10*y
    if L>1 or u>0:return represent(word+(u,)+word[::-1])
 return None

def nongrowth_condition(p):
 return any(int(d)%2 for d in str(p)) and nongrowth_source(p) is not None

def growth_source(p):
 u=tuple(map(int,str(p//11)[::-1]));n=len(u)
 if n%2==0 or u[n//2]%2:
  c=[1]*n
  if all(d==2 for d in u):
   assert n>=4
   c=[1]+[0]*(n-2)+[1]
 else:
  assert n>=3
  c=[1]+[0]*(n-2)+[1]
 s=tuple(d+9*e for d,e in zip(u,c))
 return represent(s)

def pals(max_len):
 for L in range(1,max_len+1):
  for d in '123456789':
   for rest in product('0123456789',repeat=(L+1)//2-1):
    h=d+''.join(rest)
    yield int(h+h[::-1][L%2:])

if __name__=='__main__':
 count=0;g_count=0;ng_count=0;both_count=0
 for p in pals(9):
  inv=inverse(tuple(map(int,str(p)[::-1])))
  actual_g=any(len(s)==len(str(p))-1 for s in inv)
  actual_ng=any(len(s)==len(str(p)) for s in inv)
  g=growth_condition(p);ng=nongrowth_condition(p)
  assert g==actual_g,('G',p,p//11,g,inv)
  assert ng==actual_ng,('NG',p,ng,inv)
  if g:
   n=growth_source(p);m=T(n)
   assert len(str(m))==len(str(n))+1 and not pal(m) and T(m)==p,(p,n,m)
  if ng:
   n=nongrowth_source(p);m=T(n)
   assert len(str(m))==len(str(n)) and not pal(m) and T(m)==p,(p,n,m)
  g_count+=g;ng_count+=ng;both_count+=(g and ng);count+=1
 print('Targets',count,'growth branch',g_count,'nongrowth branch',ng_count,'overlap',both_count,'union',g_count+ng_count-both_count)
 for p in [11,22,121,242,303,3113,3223,4444,22022,220022,2442,545,9999,99999,11111111011111111]:
  print(p,'growth',growth_condition(p),'nongrowth',nongrowth_condition(p))
 print('All targets, both branches, and constructive sources passed.')

 # Verify the exact two-step predecessor shapes of the infinite family
 # on a finite range. The text gives a proof for all r.
 for r in range(31):
  for d in range(1,10):
   p=11*d*(10**(2*r+2)+1)
   actual=set(inverse(tuple(map(int,str(p)[::-1]))))
   expected=set()
   if d!=2:expected.add((d+9,)+(0,)*(2*r+1)+(d+9,))
   if d in (3,5,7,9):
    a=(d-1)//2
    expected.add((a,a+10)+(9,)*(2*r)+(a+10,a))
   assert actual==expected,(d,r,actual,expected)
 print('Family predecessor shapes checked for all 9 digits and 0 <= r <= 30.')

 # Enumerate all feasible pair-sum words through length 7 and check
 # the universal prefix obstruction (1, 16) used in the proof.
 checked=0
 for L in range(1,8):
  h=L//2
  halves=[()] if h==0 else (
   (a,)+tail for a in range(1,19) for tail in product(range(19),repeat=h-1))
  for half in halves:
   centers=[None] if L%2==0 else range(2 if h==0 else 0,19,2)
   for center in centers:
    s=half+(() if center is None else (center,))+half[::-1]
    q=step(s)
    if len(q)>=2 and q[0]==1:assert q[1]<=10,(s,q)
    checked+=1
 assert checked==75447,checked
 print('Universal prefix obstruction cross-check:',checked,'pair-sum words.')

 # Check the actual 196 orbit over a modest finite range as a guard
 # against a transcription error. This is not the infinite proof.
 n=196
 excluded=set((1,2,3,4,6,7,8,9))
 for t in range(1,1001):
  n=T(n)
  if t>=3:assert n%11==0
  assert n%3!=0
  s=str(n)
  match=re.fullmatch(r'([1-9])\1(?:00)*\1\1',s)
  assert match is None or int(match.group(1)) not in excluded,(t,n)
 print('196 orbit cross-check: 1000 steps.')

 # A remaining d=5 target is compatible with the same mod-99 cycle.
 n=71647625487907287180977453773517
 assert n%99==11
 for t in range(6):
  assert not pal(n)
  assert n%99==(11*pow(2,t,9))%99
  n=T(n)
 assert n==55*(10**32+1) and pal(n) and n%99==11
 print('Six-step d=5 example verified:',n)
 print('All checks passed. These results do not prove the complete 196 conjecture.')

