#!/usr/bin/env python3
"""Six antiphase carry-hinge phases, same-phase failure controls, 48 exact transitions."""
A=(8,16,14,10,2,4); B=(10,2,4,8,16,14)
def step(p):
 c=0;d=[]
 for x in p:
  z=x+c;d.append(z%10);c=z//10
 if c:d.append(c)
 return [d[i]+d[-1-i] for i in range(len(d))]
def longest(p,v):
 best=cur=0
 for x in p:
  cur=cur+1 if x==v else 0
  best=max(best,cur)
 return best
for i,(x,y) in enumerate(zip(A,B)):
 k=lambda z:int(z>=10)
 assert k(x)+k(y)==1
 assert 2*(x-9*k(x))==A[(i+1)%6]
 assert 2*(y-9*k(y))==B[(i+1)%6]
 P=[x]*50+[9]*70+[y]*100+[9]*70+[x]*50
 Q=step(P)
 assert longest(Q,9)>=69 and Q[len(Q)//2]==B[(i+1)%6]
for x in (8,16):
 P=[x]*50+[9]*70+[x]*100+[9]*70+[x]*50
 assert longest(step(P),9)==0
P=[8]*300+[9]*250+[10]*800+[9]*250+[8]*300
for i in range(48):
 assert longest(P,9)>=200,(i,longest(P,9))
 assert longest(P,A[i%6])>=250
 assert longest(P,B[i%6])>=500
 P=step(P)
print("unit PASS: 6 antipodal phases, 2 same-phase kills, 48 full transitions")
