"""Independent checks of the even-base >=10 generalization.
The arbitrary-base theorem is justified algebraically in the companion note;
these finite checks are implementation validation, not its proof.
"""
import random,json
from itertools import product

def carry_word(q,b):
 c=[0]
 for x in q:c.append((x+c[-1])//b)
 return c

def digits(n,b):
 d=[]
 while n:d.append(n%b);n//=b
 return d or[0]

def val(d,b):return sum(a*b**i for i,a in enumerate(d))
def step(n,b):
 d=digits(n,b)
 return n+val(d[::-1],b)
def pal(n,b):
 d=digits(n,b);return d==d[::-1]
def image(q,b):
 c=0;d=[]
 for a in q:
  z=a+c;d.append(z%b);c=z//b
 if c:d.append(c)
 return [x+y for x,y in zip(d,d[::-1])]
def realize(q,b):
 d=[0]*len(q)
 for i,a in enumerate(q):
  j=len(q)-1-i
  if i<j:d[i]=max(a-(b-1),0);d[j]=min(a,b-1)
  elif i==j:assert a%2==0;d[i]=a//2
 assert d[-1]>0 and all(0<=x<b for x in d)
 return val(d,b)
def normalized(q,b):
 c=carry_word(q,b);low=0 if c[-1] else 2
 return [b-1 if c[i+1]!=c[len(q)-i] else (b if c[i+1] else low) for i in range(len(q))]
def check(q,b):
 qn=normalized(q,b);assert carry_word(qn,b)==carry_word(q,b)
 n=realize(qn,b);x=n
 for t in range(1,5):
  x=step(x,b)
  if pal(x,b):return t
 raise AssertionError((b,q,qn,n))
def sharp_check(b,r):
 q=[b-1,b-1,b+2*r,b-1,b-1]
 n=realize(q,b);assert carry_word(q,b)==[0,0,0,1,1,1]
 x=step(n,b);assert digits(x,b)==[b-1,b-1,2*r,0,0,1] and not pal(x,b)
 x=step(x,b);assert digits(x,b)==[0,0,2*r+1,2*r,b-1,0,1] and not pal(x,b)
 x=step(x,b);assert digits(x,b)==[1,0,2*r,(4*r+1)%b,2*r+(4*r+1)//b,1,1] and not pal(x,b)
 if r==0:assert digits(step(x,b),b)==[2,1,0,2,0,1,2]

def main():
 rng=random.Random(20261013);random_count=0;sharp_count=0;trace_count=0
 bases=[10,12,14,16,18,20,26,36,100,256,1000,1000000]
 for b in bases:
  for _ in range(2500):
   L=rng.randrange(1,101);d=[rng.randrange(b) for _ in range(L)];d[-1]=rng.randrange(1,b)
   q=[x+y for x,y in zip(d,d[::-1])];check(q,b);random_count+=1
  rs=list(range(b//2)) if b<=1000 else[0,b//2-1]+[rng.randrange(b//2)for _ in range(1000)]
  for r in rs:sharp_check(b,r);sharp_count+=1
  for L in range(1,13):
   for tail in product((0,1),repeat=L):
    c=(0,)+tail
    if not c[-1]:continue
    q=[b-1 if c[i+1]!=c[L-i] else(b if c[i+1] else 0)for i in range(L)]
    if carry_word(q,b)!=list(c):continue
    if L%2 and q[L//2]%2:continue
    check(q,b);trace_count+=1
 out={'bases':bases,'random_original_integers':random_count,'normalized_overflow_trace_checks':trace_count,'sharpness_parameter_checks':sharp_count,'status':'all passed','arbitrary_base_Lean_formalization':False}
 print(json.dumps(out,indent=2));json.dump(out,open('resume_even_base_normalization_results.json','w'),indent=2)
if __name__=='__main__':main()
