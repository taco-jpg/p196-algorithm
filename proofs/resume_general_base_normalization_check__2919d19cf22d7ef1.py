"""Checks the repaired protected endpoint-class extension; not a proof."""
import random,json
from itertools import product
from resume_even_base_normalization_check import carry_word,digits,val,step,pal,image,realize

def normalized(q,b):
 c=carry_word(q,b);low=0 if c[-1] else 2;alpha=b+b%2
 return [b-1 if c[i+1]!=c[len(q)-i] else(alpha if c[i+1] else low)for i in range(len(q))]
def check(q,b):
 qn=normalized(q,b);assert carry_word(qn,b)==carry_word(q,b)
 n=realize(qn,b);x=n
 for t in range(1,5):
  x=step(x,b)
  if pal(x,b):return t
 raise AssertionError((b,q,qn,n))
def sharp_check(b,r):
 alpha=b+b%2;v=alpha-b+2*r
 q=[b-1,b-1,alpha+2*r,b-1,b-1]
 n=realize(q,b);assert carry_word(q,b)==[0,0,0,1,1,1]
 x=step(n,b);assert digits(x,b)==[b-1,b-1,v,0,0,1] and not pal(x,b)
 x=step(x,b);assert digits(x,b)==[0,0,v+1,v,b-1,0,1] and not pal(x,b)
 x=step(x,b);assert digits(x,b)==[1,0,v,(2*v+1)%b,v+(2*v+1)//b,1,1] and not pal(x,b)
 if r==0:
  expected=[2,1,0,2,0,1,2]if b%2==0 else[2,1,2,6,2,1,2]
  assert digits(step(x,b),b)==expected

def main():
 rng=random.Random(2026101301);random_count=0;sharp_count=0;trace_count=0
 bases=[17,19,21,23,25,27,35,99,255,999,1000001]
 for b in bases:
  alpha=b+b%2
  for _ in range(2500):
   L=rng.randrange(1,101);d=[rng.randrange(b)for _ in range(L)];d[-1]=rng.randrange(1,b)
   q=[x+y for x,y in zip(d,d[::-1])];check(q,b);random_count+=1
  maxr=(2*b-2-alpha)//2
  rs=list(range(maxr+1))if b<=1000 else[0,maxr]+[rng.randrange(maxr+1)for _ in range(1000)]
  for r in rs:sharp_check(b,r);sharp_count+=1
  for L in range(1,13):
   for tail in product((0,1),repeat=L):
    c=(0,)+tail
    if not c[-1]:continue
    q=[b-1 if c[i+1]!=c[L-i] else(alpha if c[i+1] else 0)for i in range(L)]
    if carry_word(q,b)!=list(c):continue
    if L%2 and q[L//2]%2:continue
    check(q,b);trace_count+=1
 out={'odd_bases':bases,'random_original_integers':random_count,'normalized_overflow_trace_checks':trace_count,'sharpness_parameter_checks':sharp_count,'status':'all passed','arbitrary_base_Lean_formalization':False}
 print(json.dumps(out,indent=2));json.dump(out,open('resume_general_base_normalization_results.json','w'),indent=2)
if __name__=='__main__':main()
