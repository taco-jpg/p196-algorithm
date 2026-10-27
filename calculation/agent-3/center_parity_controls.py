#!/usr/bin/env python3
"""PAPER center-parity lemma: independent integer controls, NOT Lean-verified."""
from random import Random

def value(s,b):
    n=0
    for x in s:n=n*b+x
    return n

def word(p,g,h):
    A,B,M,D,E,x,y,u,v=p
    return A+(x,)*g+B+(u,)*h+M+(v,)*h+D+(y,)*g+E

def fixed_add(s,t,c,b):
    n=value(s,b)+value(t,b)+c
    return tuple(n//b**(len(s)-i-1)%b for i in range(len(s))),n//b**len(s)

def image(b,p):
    A,B,M,D,E,x,y,u,v=p
    s0,c1=fixed_add(E,A[::-1],0,b)
    s1,c2=fixed_add(D,B[::-1],c1,b)
    s2,c3=fixed_add(M,M[::-1],c2,b)
    s3,c4=fixed_add(B,D[::-1],c3,b)
    s4,f=fixed_add(A,E[::-1],c4,b)
    z=b-1
    return ((1,)*f+s4,s3,s2,s1,s0),(z*(1-c4),z*(1-c3),z*(1-c2),z*(1-c1)),f,(c2,c3)

def demo():
    phases=[
       ((1,0),(1,1),(1,1,0,1),(0,0),(0,0),1,0,1,0),
       ((1,1),(0,0),(1,0,0,0),(1,1),(0,1),0,1,0,1),
       ((1,0),(1,1),(1,0,1),(0,0),(0,0),1,0,1,0),
       ((1,1),(0,0),(0,1,0),(1,1),(0,1),0,1,0,1)
    ]
    gains=((0,0),(0,1),(0,0),(0,0))
    carry=[]
    for i,p in enumerate(phases):
       q=phases[(i+1)%4]
       z,r,f,_=image(2,p)
       carry.append(f)
       F=lambda t:2*len(t[0])+2*len(t[1])+len(t[2])
       dg,dh=gains[i]
       assert F(q)-F(p)==f-2*(dg+dh)
       assert (len(q[2])-len(p[2])-f)%2==0
       for g,h in ((2,2),(3,4),(10,7)):
          out=z[0]+(r[0],)*g+z[1]+(r[1],)*h+z[2]+(r[2],)*h+z[3]+(r[3],)*g+z[4]
          assert out==word(q,g+dg,h+dh)
    assert carry==[0,1,0,1]
    print("positive_binary_parity_controls 4 EDGES PASS carry",carry)
    p=((9,),(0,9,7),(7,0,2,7,2),(2,7,9),(0,),5,4,2,7)
    q=((1,),(0,6),(9,7,4,8),(0,6),(9,),0,9,9,0)
    z,r,f,_=image(10,p)
    assert f==1 and len(p[2])==5 and len(q[2])==4
    for g,h in ((0,0),(2,3),(11,9)):
       out=z[0]+(r[0],)*g+z[1]+(r[1],)*h+z[2]+(r[2],)*h+z[3]+(r[3],)*g+z[4]
       assert out==word(q,g+1,h+1)
       assert value(out,10)==value(word(p,g,h),10)+value(word(p,g,h)[::-1],10)
    print("base10_nonclosed_parity_control 3 LENGTHS PASS")
    rng=Random(19603);tested=0;empty_reject=0
    for b in (2,3,10,11,17,26):
      for _ in range(4000):
       a=rng.randint(1,4);d=rng.randint(0,3);m=rng.randint(0,5)
       make=lambda n:tuple(rng.randrange(b) for _ in range(n))
       A=(rng.randrange(1,b),)+make(a-1)
       x=rng.randrange(b);u=rng.randrange(b)
       p=(A,make(d),make(m),make(d),make(a),x,b-1-x,u,b-1-u)
       z,r,f,(c2,c3)=image(b,p)
       if m==0:
           assert c3==c2 and r[1]+r[2]!=b-1
           empty_reject+=1
       g=rng.randint(0,12);h=rng.randint(0,12)
       raw=z[0]+(r[0],)*g+z[1]+(r[1],)*h+z[2]+(r[2],)*h+z[3]+(r[3],)*g+z[4]
       w=word(p,g,h)
       assert value(raw,b)==value(w,b)+value(w[::-1],b)
       tested+=1
    print("independent_bigint_crosschecks",tested,"PASS; empty_center_rejections",empty_reject)

if __name__=="__main__":demo()
