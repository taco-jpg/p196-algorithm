#!/usr/bin/env python3
"""Independent decimal big-integer check of the first mixed-phase packet collision."""
import subprocess,sys
sys.set_int_max_str_digits(1000000)
BINARY=sys.argv[1]
def coefficients(n):
 s=str(n)
 return [ord(s[i])+ord(s[-1-i])-96 for i in range(len(s))]
def realize(p):
 n=len(p);d=[0]*n
 for i in range(n//2):
  x=p[i];lo=min(x,9);hi=x-lo
  if i==0 and hi==0:lo-=1;hi+=1
  assert 0<=lo<=9 and 0<=hi<=9
  d[i],d[n-1-i]=lo,hi
 assert d[-1]>0
 return int(''.join(map(str,d[::-1])))
def run():
 r=subprocess.run([BINARY],capture_output=True,text=True,check=True)
 frames={}
 for line in r.stdout.splitlines():
  if line.startswith('SNAP '):
   _,t,j,packed=line.split(' ')
   assert len(packed)%2==0
   p=[int(packed[i:i+2]) for i in range(0,len(packed),2)]
   frames[int(t),int(j)]=p
  else:assert line=='SUMMARY first_overlap=22503 first_nonlinear=22506 initial_residual=3 residual_22644=86',line
 assert len(frames)==8
 end_numbers=[]
 for j in range(4):
  n=realize(frames[22500,j]);assert coefficients(n)==frames[22500,j]
  for step in range(6):
   assert str(n)!=str(n)[::-1]
   n+=int(str(n)[::-1])
  assert str(n)!=str(n)[::-1]
  assert coefficients(n)==frames[22506,j],('independent-bigint mismatch',j)
  end_numbers.append(n)
 p=[frames[22506,j] for j in range(4)]
 bad=[i for i in range(len(p[0])//2) if p[0][i]+p[3][i]!=p[1][i]+p[2][i]]
 assert bad==[17781,17782,17783]
 predicted=[p[1][i]+p[2][i]-p[0][i] for i in bad]
 observed=[p[3][i] for i in bad]
 assert predicted==[4,26,8] and observed==[5,6,9]
 assert [y-x for x,y in zip(predicted,observed)]==[1,-20,1]
 original=frames[22506,3][17782]
 frames[22506,3][17782]=(original+1)%19
 assert coefficients(end_numbers[3])!=frames[22506,3]
 frames[22506,3][17782]=original
 assert coefficients(end_numbers[3])==frames[22506,3]
 print('BIGINT_COLLISION_PASS t=22500..22506, four 75k+ digit decimal integers, full pairword equality, 3-cell correction (1,-20,1)')
 print('CORRUPTED_COEFFICIENT_NEGATIVE_CONTROL_PASS')
 print('\n'.join(x for x in r.stderr.splitlines() if x.startswith(('TRACE','CORRECTION'))))
if __name__=='__main__':run()
