#!/usr/bin/env python3
"""Independent Python ordinary-integer merger checks for 4q+1 carry gates."""
import random,sys
sys.set_int_max_str_digits(0)
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
def pair(q,mask):
 h=B+W*q
 for k in range(q):
  for jidx,j in enumerate((0,4,8,12)):
   if mask&(1<<(4*k+jidx)):
    v=h[39+20*k+j];h[39+20*k+j]=v-9 if v>=9 else v+9
 if mask&(1<<(4*q)):h[-1]=4
 return h+h[::-1]
def source(p):
 h=p[:len(p)//2]
 l=[min(x,9) for x in h]
 u=[x-y for x,y in zip(h,l)]
 return int(''.join(map(str,u))+''.join(map(str,l[::-1])))
def step(n):return n+int(str(n)[::-1])
def pairword(n):
 s=str(n);return tuple(int(a)+int(b) for a,b in zip(s,s[::-1]))
def main():
 r=random.Random(4729)
 for q in (1,2,3,300):
  baseline=source(pair(q,0));target=pairword(step(baseline));second=step(step(baseline))
  bits=4*q+1
  masks=range(1<<bits) if q<=2 else [r.getrandbits(bits) for _ in range(1024 if q==3 else 64)]
  count=0
  for m in masks:
   x=source(pair(q,m));y=step(x)
   assert pairword(y)==target
   assert step(y)==second
   assert str(x)!=str(x)[::-1]
   count+=1
  print('q',q,'ordinary Python-bigint mask controls',count,'PASS')
  if q==1:
   p=pair(q,0);pos=39+11;p[pos]=p[-1-pos]=p[pos]-9 if p[pos]>=9 else p[pos]+9
   assert pairword(step(source(p)))!=target
 print('W07_MULTI_BIGINT_PASSED')
if __name__=='__main__':main()
