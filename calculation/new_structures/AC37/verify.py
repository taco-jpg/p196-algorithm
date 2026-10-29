#!/usr/bin/env python3
"""Independent ordinary Python big-integer checks of a phase-4 template."""
import sys
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)
B=[10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4]
W=[8,1,15,4,0,5,5,18,4]
def template(J,U,C,q,k):
 H=B+W*q+J+U*k
 return H+C+H[::-1]
def realize(p):
 d=[0]*len(p)
 for i,x in enumerate(p[:len(p)//2]):
  hi=min(9,x);d[i]=x-hi;d[-1-i]=hi
 if len(p)%2:
  assert p[len(p)//2]%2==0
  d[len(p)//2]=p[len(p)//2]//2
 assert p==p[::-1] and d[-1]!=0
 return int(''.join(str(v) for v in d[::-1]))
def run(J,U,C,q,k):
 n=realize(template(J,U,C,q,k));g=[]
 for t in range(120):
  v=int(str(n)[::-1]);next_n=n+v
  g.append(len(str(next_n))-len(str(n)));n=next_n
 d=[int(x) for x in str(n)[::-1]]
 got=[d[i]+d[-1-i] for i in range(len(d))]
 want=template(J,U,C,q,k+5)
 ix=next((i for i,(x,y) in enumerate(zip(got,want)) if x!=y),None)
 if ix is None and len(got)!=len(want):ix=min(len(got),len(want))
 return {'return':got==want,'first_mismatch':ix,'gamma':''.join(map(str,g)),'digits':len(d)}
if __name__=="__main__":
 J=list(map(int,sys.argv[1].split(',')));U=list(map(int,sys.argv[2].split(',')))
 C=list(map(int,sys.argv[3].split(',')))
 for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
  print(q,k,run(J,U,C,q,k))
