#!/usr/bin/env python3
"""Independent genuine Python bigint + LSD-schoolbook audit of phase-6 census."""
import random,sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
B=[2,11,3,6,0,1,17,7,2,14,9,14,1,2,9,5,9,17,14,4,17,4,12,15,9,18,9,7,10,16,10,6,12,8]
W=[5,9,16,0,9,11,1,10,8]
US=[]
for a in range(0,19,2):
 b=[9,a,18-a]
 for r in range(3):US.append(b[r:]+b[:r])
assert len(set(map(tuple,US)))==30
def template(q,k,J,U,C):
 h=B+W*q+J+U*k
 return h+C+h[::-1]
def start_num(p):
 d=[0]*len(p)
 for i in range(len(p)//2):
  hi=min(9,p[i]);d[i]=p[i]-hi;d[-1-i]=hi
 if len(p)%2:d[len(p)//2]=p[len(p)//2]//2
 assert d[-1]!=0 and all(0<=v<=9 for v in d)
 return int(''.join(map(str,d[::-1])))
def schoolbook(d):
 out=[];c=0
 for x,y in zip(d,d[::-1]):
  s=x+y+c;out.append(s%10);c=s//10
 if c:out.append(c)
 return out
def run(q,k,J,U,C,verify):
 p=template(q,k,J,U,C);n=start_num(p)
 d=list(map(int,str(n)[::-1]));gam=[]
 for t in range(120):
  s=str(n);n2=n+int(s[::-1])
  gam.append(len(str(n2))-len(s))
  if verify:
   assert any(x&1 for x in p)
   d=schoolbook(d)
   assert d==list(map(int,str(n2)[::-1]))
   p=[d[i]+d[-1-i] for i in range(len(d))]
  n=n2
 assert gam==[0,0,1,0]*30
 s=str(n);got=[int(x)+int(y) for x,y in zip(s[::-1],s)]
 if verify:assert got==p
 tgt=template(q,k+5,J,U,C)
 assert len(got)==len(tgt)
 first=next((i for i,(x,y) in enumerate(zip(got,tgt)) if x!=y),None)
 assert first is not None and 34<=first<34+9*q
 return first-(34+9*q)
def main():
 r=random.Random(2706)
 cases=[(U,[r.randrange(19) for _ in range(5)]) for U in US]
 cases.append(([9,14,4],[14,5,14,16,4]))
 widths=[(14,100),(20,100),(40,200),(80,400),(160,800)]
 cnt=0
 for U,J in cases:
  for C in ([4,4],[4,14,4]):
   offsets=[run(q,k,J,U,C,q==14) for q,k in widths]
   assert len(set(offsets))==1,(J,U,C,offsets)
   cnt+=len(widths)
 print('AC27_INDEPENDENT_BIGINT_DIGITARRAY_PASS',cnt,'runs',cnt*120,'steps')
if __name__=='__main__':main()
