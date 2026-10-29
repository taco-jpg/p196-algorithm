#!/usr/bin/env python3
"""Independent Python ordinary-integer tests of two-wall 9-band transfer formulas."""
import random
r=random.Random(23)
def val(a):return sum(x*10**i for i,x in enumerate(a))
def digits(n):
 z=[]
 while n:z.append(n%10);n//=10
 return z or [0]
def edge(U,V,L):
 a=len(U);c=0;lo=[];hi=[]
 for i in range(a):
  s=U[i]+V[a-1-i]+c;lo.append(s%10);c=s//10
 z=8+c;c=1
 for j in range(a):
  s=V[j]+U[a-1-j]+c;hi.append(s%10);c=s//10
 gamma=c;Un=lo+[z]
 if gamma==0:Vn=[9]+hi;Ln=L-2
 else:Vn=hi+[1];Ln=L-1
 while Un and Vn and Un[-1]==9 and Vn[0]==9:
  Un.pop();Vn.pop(0);Ln+=2
 return Un,Vn,Ln
for t in range(10000):
 a=r.randint(1,12);L=r.randint(2,26)
 U=[r.randrange(10) for _ in range(a)];V=[r.randrange(10) for _ in range(a)]
 V[-1]=r.randint(1,9)
 orig=U+[9]*L+V
 x=val(orig);y=x+int(str(x)[::-1]);actual=digits(y)
 Un,Vn,Ln=edge(U,V,L)
 assert Ln>=0
 assert actual==Un+[9]*Ln+Vn,(t,a,L,U,V,actual,Un,Ln,Vn)
print('PASS 10,000 independently evaluated random two-wall transfer cases, both parities and gamma values')
