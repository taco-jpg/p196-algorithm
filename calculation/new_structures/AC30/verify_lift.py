#!/usr/bin/env python3
"""Phase-9 conditional 120-step T12 insertion audit, independent decimal integer controls."""
from pathlib import Path
from random import Random
from phase9_cones import B,W,F,g
from independent import templ,realize,ulist
import sys
if hasattr(sys, 'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
def pair(n):
 s=str(n);return [int(x)+int(y) for x,y in zip(s[::-1],s)]
def step(n):
 return n+int(str(n)[::-1])
def ins(p,w,cut):
 return p[:cut]+list(w)+p[cut:len(p)-cut]+list(w)[::-1]+p[len(p)-cut:]
def run(U,J,C,q,k,typ):
 b,w=B[9],W[9]
 p=templ(b,w,J,U,C,q,k)
 qq=q+(typ=='W');kk=k+(typ=='U')
 p2=templ(b,w,J,U,C,qq,kk)
 x,y=realize(p),realize(p2)
 c=52 if typ=='W' else 34+9*q+len(J)+165
 v=[tuple(U)]
 for t in range(120):v.append(F(v[-1],g(t)))
 for t in range(121):
  row=W[(9+t)%12] if typ=='W' else v[t]
  px,py=pair(x),pair(y)
  assert py==ins(px,row,c),(typ,U,q,k,J,C,t,next((i for i,(a,b) in enumerate(zip(py,ins(px,row,c))) if a!=b),None))
  if t==120:break
  xx,yy=step(x),step(y)
  assert len(str(xx))-len(str(x))==g(t),(t,typ,U,'base-gamma')
  assert len(str(yy))-len(str(y))==g(t),(t,typ,U,'insert-gamma')
  x,y=xx,yy
 return True

if __name__=='__main__':
 start=int(sys.argv[1]) if len(sys.argv)>1 else 0
 stop=int(sys.argv[2]) if len(sys.argv)>2 else 30
 rr=Random(20261029)
 n=0
 for uix in range(start,stop):
  U=ulist()[uix]
  for q,k in [(14,100),(20,160)]:
   J=[rr.randrange(19) for _ in range(5)]
   for C in ([4,14,4],[4,4]):
    for typ in ('W','U'):
     run(U,J,C,q,k,typ);n+=1
 print('PHASE9_INSERTION_BIGINT_PASS',start,stop,'cases',n,'steps',n*120)
