#!/usr/bin/env python3
"""Independent Python BIGINT checker for decimal central-18 front."""
import sys
sys.set_int_max_str_digits(0)
def normalize(x,c):
 out=[]
 for a in x:
  y=a+c
  out.append(y%10)
  c=y//10
 return out,c
def step(B,C,g):
 low,e1=normalize(B,0)
 mid,e2=normalize(C,e1)
 assert e1!=e2
 hi,gam=normalize(B[::-1],e2)
 if gam:
  b2=[a+b for a,b in zip(low+[9*(1-e1)],[1]+hi[::-1])]
  y=9*(1-e2)
  c2=[a+b for a,b in zip(mid+[y],[y]+mid[::-1])]
 else:
  b2=[a+b for a,b in zip(low,hi[::-1])]
  c2=[a+b for a,b in zip(mid,mid[::-1])]
 u=0
 while b2 and b2[-1]==9:
  b2.pop()
  u+=1
 v=0
 while len(c2)>=2 and c2[0]==c2[-1]==9:
  c2=c2[1:-1]
  v+=1
 return b2,c2,g+u+v-gam,gam
def central18(C):
 n=len(C)
 l=(n-1)//2
 r=n//2
 if C[l]!=18 or C[r]!=18:return 0
 while l>0 and C[l-1]==18:l-=1
 while r+1<n and C[r+1]==18:r+=1
 return r-l+1
def seed(P):
 d=[0]*len(P)
 for j in range(len(d)//2):
  k=len(d)-j-1
  d[j]=min(P[j],9)
  d[k]=P[j]-d[j]
  if j==0 and d[k]==0:
   d[j]-=1
   d[k]+=1
 if len(d)%2:d[len(d)//2]=P[len(d)//2]//2
 assert d[-1]!=0 and all(d[j]+d[-1-j]==P[j] for j in range(len(P)))
 return int(''.join(map(str,d[::-1])))
def run(m,g=1000,cap=2000):
 B=[12,9]
 C=[6]+[9]*m+[6]
 def pw():return B+[9]*g+C+[9]*g+B[::-1]
 N=seed(pw())
 S=0
 eq=0
 collision=-1
 for t in range(cap+1):
  s=str(N)
  assert s!=s[::-1]
  d=[int(x) for x in s[::-1]]
  actual=[d[j]+d[-1-j] for j in range(len(d))]
  assert actual==pw(),(t,"pairword mismatch")
  if t>0 and S<m:
   assert central18(C)==m-S,(t,S,central18(C))
   eq+=1
  if t>0 and S>=m:
   collision=t
   break
  B,C,g,gam=step(B,C,g)
  N+=int(s[::-1])
  S+=gam
  assert len(str(N))-len(s)==gam
 assert collision>=0
 print("INDEPENDENT PASS","m",m,"collision",collision,"equalities",eq,"overflows",S,"digits",len(str(N)))
 return collision,eq
if __name__=="__main__":
 run(*(int(x) for x in sys.argv[1:]))
