from fractions import Fraction
from itertools import product
import json

def norm(B,e):
 D=[]
 for b in B: D.append((b+e)%10);e=(b+e)//10
 return tuple(D),e
def step(c,B):
 k=int(c>=10);t=c-9*k
 L,e=norm(B,0);R,g=norm(B[::-1],k)
 u=c+e-10*k
 rhs=R[::-1]+(t,) if g==0 else (1,)+R[::-1]
 raw=tuple(x+y for x,y in zip(L+(u,),rhs))
 C=raw
 while C and C[-1]==2*t:C=C[:-1]
 return 2*t,C,g
def z(c,B):return 9*sum(b*10**i for i,b in enumerate(B))-c*(10**len(B)-1)
def x(c,B):return sum(Fraction(b-c,10**(i+1)) for i,b in enumerate(B))
def clean(c,B):
 while B and B[-1]==c:B=B[:-1]
 return B
if __name__=="__main__":
 out=[]
 for c in range(2,18,2):
  for b in range(1,4):
   for B in product(range(19),repeat=b):
    if not B[0] or B[-1]==c:continue
    d,C,g=step(c,B)
    if abs(z(d,C))<=abs(z(c,B)) and z(c,B)!=0:
     out.append(dict(c=c,B=B,d=d,C=C,g=g,z=z(c,B),nextz=z(d,C)))
     break
 print(json.dumps(out,indent=2))
