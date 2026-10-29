#!/usr/bin/env python3
"""Independent exact decimal-bigint and fresh-buffer digit-array controls for Z07."""
import sys
if hasattr(sys, "set_int_max_str_digits"): sys.set_int_max_str_digits(1000000)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
US={7:[6,9,12],19:[9,16,2]}
JS=[[0,0,0,0,0],[18,18,18,18,18],[1,2,3,4,5],[5,18,4,8,1],[18,0,9,12,3]]
WIDTHS=[(20,100),(40,160),(80,320),(160,640)]
def value(d):
 n=0
 for x in reversed(d):n=10*n+x
 return n
def realize(p):
 assert p==p[::-1];d=[0]*len(p)
 for i in range(len(p)//2):
  hi=min(9,p[i]);lo=p[i]-hi;assert 0<=lo<=9
  d[i]=lo;d[-1-i]=hi
 if len(p)%2:
  assert p[len(p)//2]%2==0;d[len(p)//2]=p[len(p)//2]//2
 assert d[-1]>0 and value(d)>0
 return d
def pairword(d):return [d[i]+d[-1-i] for i in range(len(d))]
def pair_step(p):
 d=[];c=0
 for x in p:
  z=x+c;d.append(z%10);c=z//10
 if c:d.append(c)
 return [d[i]+d[len(d)-1-i] for i in range(len(d))],c
def schoolbook_step(d):
 out=[];c=0
 for i in range(len(d)):
  z=d[i]+d[len(d)-1-i]+c;out.append(z%10);c=z//10
 if c:out.append(c)
 return out,c
def template(q,k,J,U):
 h=B+W*q+J+U*k
 return h+[0,0,0]+h[::-1]
def check(q,k,J,U):
 p=template(q,k,J,U);d=realize(p);n=value(d);assert pairword(d)==p
 target_prefix=B+W*q;gamma=[]
 for t in range(120):
  p2,g=pair_step(p);d2,overflow=schoolbook_step(d)
  assert g==overflow,(q,k,J,U,t,"overflow disagreement")
  assert p2==pairword(d2),(q,k,J,U,t,"pairword vs digit-array disagreement")
  n2=n+int(str(n)[::-1])
  assert value(d2)==n2,(q,k,J,U,t,"digit-array vs genuine bigint disagreement")
  assert d2==list(map(int,str(n2)[::-1])),(q,k,J,U,t,"digit-array representation disagreement")
  assert len(str(n2))-len(str(n))==overflow,(q,k,J,U,t,"bigint length/overflow disagreement")
  p,d,n=p2,d2,n2;gamma.append(g)
 assert gamma==[1,0,0,0]*30,(q,k,J,U,"wrong 120-step overflow clock")
 mismatch=next((i for i,(a,b) in enumerate(zip(p,target_prefix)) if a!=b),min(len(p),len(target_prefix)))
 restored=len(p)>=len(target_prefix) and p[:len(target_prefix)]==target_prefix
 assert not restored,(q,k,J,U,"unexpected W9-prefix restoration; investigate")
 assert p!=template(q,k+5,J,U)
 return mismatch-len(target_prefix),len(d),sum(gamma)
def main():
 total=0
 for rank,U in US.items():
  for q,k in WIDTHS:
   for J in JS:
    off,digits,overflows=check(q,k,J,U);total+=1
    print(f"PASS U_rank={rank} U={U} q={q} k={k} J={J} first_W9_mismatch_offset={off} digits={digits} overflows={overflows}")
 print(f"PASS independent genuine-bigint/digit-array/pairword replay: {total} cases x 120 steps; all exact clocks and endpoint failures agree.")
if __name__=="__main__":main()
