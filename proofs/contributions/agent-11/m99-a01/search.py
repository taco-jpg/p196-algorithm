#!/usr/bin/env python3
from itertools import product
def K(x): return 1 if x>=10 else 0
def T(x): return x-9*K(x)
def norm(w,e):
 o=[]
 for x in w:o.append((x+e)%10);e=(x+e)//10
 return o,e
def add(a,b): return [x+y for x,y in zip(a,b)]
def lead(w,x):
 n=0
 while n<len(w) and w[n]==x:n+=1
 return n
def trim(c,B,A,C):
 d=18-c;j=lead(B[::-1],c);B=B[:len(B)-j]
 j1=lead(A,c);A=A[j1:];j2=lead(A[::-1],d);A=A[:len(A)-j2]
 q=min(lead(C,d),lead(C[::-1],d),len(C)//2);C=C[q:len(C)-q]
 return c,B,A,C
def step(s):
 c,B,A,C=s;d=18-c
 DB,e0=norm(B,0);DA,e1=norm(A,K(c));DC,e2=norm(C,K(d))
 DRA,e3=norm(A[::-1],K(d));DRB,g=norm(B[::-1],K(c))
 u0=c+e0-10*K(c);u1=d+e1-10*K(d);u2=d+e2-10*K(d);u3=c+e3-10*K(c)
 if g==0:
  Br=add(DB+[u0],DRB[::-1]+[T(c)]);Ar=add([T(c)]+DA+[u1],[u3]+DRA[::-1]+[T(d)]);q=[T(d)]+DC+[u2]
 else:
  Br=add(DB+[u0],[1]+DRB[::-1]);Ar=add(DA+[u1],[u3]+DRA[::-1]);q=DC+[u2]
 return trim(2*T(c),Br,Ar,add(q,q[::-1]))
def key(s):return(s[0],tuple(s[1]),tuple(s[2]),tuple(s[3]))
def states(phases,vals,maxba,maxc,sym):
 mids=range(0,19,2)
 for c in phases:
  for lb in range(maxba+1):
   for la in range(maxba+1):
    for B in product(vals,repeat=lb):
     for A in product(vals,repeat=la):
      for lc in range(maxc+1):
       if not sym:
        for C in product(vals,repeat=lc):yield(c,list(B),list(A),list(C))
       else:
        for h in product(vals,repeat=lc//2):
         if lc%2==0:yield(c,list(B),list(A),list(h+h[::-1]))
         else:
          for m in mids:yield(c,list(B),list(A),list(h+(m,)+h[::-1]))
def scan(S):
 U={key(s) for s in S};F={};out=0;cyc=0
 for s in S:
  q=key(step(s));F[key(s)]=q;out+=q not in U
 seen={}
 for v in F:
  if seen.get(v):continue
  path=[];pos={};u=v
  while u in F and not seen.get(u,0) and u not in pos:
   pos[u]=len(path);path.append(u);u=F[u]
  if u in pos:cyc+=1
  for x in path:seen[x]=2
 return len(U),out,cyc
if __name__=="__main__":
 v1=range(19);v2=(0,1,8,9,10,17,18)
 D=[("all_phases_len1",[1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17],v1,1,1,False),
    ("six_phase_len2",[2,4,8,16,14,10],v2,2,2,True),
    ("two_phase_len2",[6,12],v2,2,2,True)]
 for n,p,v,ba,cc,sy in D:print(n,scan(list(states(p,v,ba,cc,sy))))