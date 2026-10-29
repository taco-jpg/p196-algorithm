#!/usr/bin/env python3
"""Independent native Python bigint verification of the four-orbit interference."""
import csv,sys
sys.set_int_max_str_digits(1000000)
PATH=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
CYC=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)
def seed(first=False,second=False):
 H=5200;arr=[0]*(2*H)
 for j in range(H):
  p=PATH[j] if j<39 else CYC[(j-39)%20]
  if first and 1800<=j<1850:p=(7*j+11)%19
  if second and 2600<=j<2650:p=(3*j+7)%19
  arr[j]=min(p,9);arr[2*H-1-j]=p-arr[j]
 return int(''.join(map(str,reversed(arr))))

def analyze(a,b,c,d):
 sa,sb,sc,sd=[str(x).encode() for x in (a,b,c,d)]
 assert len(sa)==len(sb)==len(sc)==len(sd)
 lo1=hi1=lo2=hi2=-1
 ov=nonlin=out=0;umin=umax=-1
 for j in range(len(sa)//2):
  x=sa[j]+sa[-1-j];x1=sb[j]+sb[-1-j];x2=sc[j]+sc[-1-j];y=sd[j]+sd[-1-j]
  q1=x1!=x;q2=x2!=x
  if q1:
   if lo1<0:lo1=j
   hi1=j
  if q2:
   if lo2<0:lo2=j
   hi2=j
  if q1 and q2:ov+=1
  elif y!=(x1 if q1 else x2 if q2 else x):nonlin+=1
  if not q1 and not q2 and y!=x:
   out+=1
   if umin<0:umin=j
   umax=j
 return lo1,hi1,lo2,hi2,ov,nonlin,out,umin,umax,len(sa)

def main():
 data=list(csv.DictReader(open(sys.argv[1]),delimiter='\t'))
 a,b,c,d=seed(),seed(first=True),seed(second=True),seed(first=True,second=True)
 cols=('lo1','hi1','lo2','hi2','overlap','nonlinear','unexpected','umin','umax','alllen')
 for t in range(901):
  obs=analyze(a,b,c,d)
  exp=tuple(int(data[t][field]) for field in cols)
  assert obs==exp,(t,obs,exp)
  if t<900:
   a,b,c,d=(v+int(str(v)[::-1]) for v in (a,b,c,d))
 print('INDEPENDENT_BIGINT_TWO_PULSE_PASS four_native_orbits steps=0..900 all_901_rows_exact')
if __name__=='__main__':main()
