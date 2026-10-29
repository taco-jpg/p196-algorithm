#!/usr/bin/env python3
"""Independent scalar carry oracle. Run from any cwd: python3 check.py"""
import itertools,random,re,subprocess,tempfile
from pathlib import Path
D=Path(__file__).resolve().parent
def read(path):
 v=list(map(int,path.read_text().split()));p,nb,m,b=v[:4];i=4
 G=v[i:i+p];i+=p
 W=[v[i+j*m:i+(j+1)*m] for j in range(p)];i+=p*m
 C=[v[i+j*m:i+(j+1)*m] for j in range(p)];i+=p*m
 assert i==len(v)
 return p,nb,m,b,G,W,C
def exact(L,w,H,o,digits):
 p,nb,m,b,G,W,C=L;K=w+10
 n=2*m*((max(400,2*nb+2*K)+2*m-1)//(2*m))+o;h=(n+1)//2
 def cell(t,x):return W[t%p][(x-nb)%m]
 x=[cell(0,h-K+i) for i in range(K-w)]+list(digits)
 if n%2 and x[-1]%2:return 0
 for t in range(H):
  carry=C[t%p][(h-K-nb)%m];up=[]
  for z in x:
   v=z+carry;up.append(v%b);carry=v//b
  dn=[0]*K;dc=[0]*K
  if n%2:
   dn[K-1]=up[K-1];dc[K-2]=carry;hi=K-2
  else:dc[K-1]=carry;hi=K-1
  for i in range(hi,-1,-1):
   v=x[i]+dc[i];dn[i]=v%b
   if i:dc[i-1]=v//b
  g=G[t%p];nn=n+g;hh=(nn+1)//2;dh=hh-h;z=[]
  for j in range(K):
   if j<2:z.append(cell(t+1,hh-K+j));continue
   i=j+dh
   if g==0:
    a=up[i];q=up[i] if (n%2 and i==K-1) else dn[i]
   else:a=up[i] if i<K else dn[K-1];q=dn[i-1]
   v=a+q
   if j<K-w and v!=cell(t+1,hh-K+j):return 0
   z.append(v)
  if nn%2 and z[-1]%2:return 0
  x=z;n=nn;h=hh
 return 1
def run(exe,file,w,H,o,prefix=None):
 cmd=[str(exe),str(file),str(w),str(H),str(o),str(o+1)]
 if prefix is not None:cmd.append(','.join(map(str,prefix)))
 r=subprocess.run(cmd,capture_output=True,text=True,check=True)
 m=re.search(r'survivors=(\d+)',r.stdout)
 assert m and f'w={w} H={H} o={o}' in r.stdout,r.stdout
 return int(m[1])
def main():
 with tempfile.TemporaryDirectory() as t:
  exe=Path(t)/'solver'
  subprocess.run(['g++','-O3','-std=c++17','-DNDEBUG',str(D/'kinkdfs_mask.cpp'),'-o',str(exe)],check=True)
  rng=random.Random(4740426);n=0
  for name,w,H in [('neutral_p11',13,110),('neutral_p12',11,90),('neutral_b26_control',3,30)]:
   file=D/'data'/f'{name}.txt';L=read(file);b=L[3]
   for o in (0,1):
    for k in range(120):
     digits=[rng.randrange(2*b-1) for _ in range(w)]
     if o%2:digits[-1]&=~1
     a=exact(L,w,H,o,digits);z=run(exe,file,w,H,o,digits)
     assert a==z,(name,o,k,digits,a,z)
     n+=1
  assert n==720
  print('PASS: 720 independent scalar full-width checks')
  n=0
  for name in ('neutral_p11','neutral_p12','neutral_b26_control'):
   file=D/'data'/f'{name}.txt';L=read(file);b=L[3]
   for w in (1,2):
    for H in (1,3):
     for o in (0,1):
      a=sum(exact(L,w,H,o,d) for d in itertools.product(range(2*b-1),repeat=w))
      z=run(exe,file,w,H,o)
      assert a==z,(name,w,H,o,a,z)
      n+=1
  assert n==24
  print('PASS: 24 independent complete small-width checks')
  file=D/'data'/'neutral_b26_control.txt'
  assert (run(exe,file,3,30,0),run(exe,file,3,30,1))==(4,2)
  print('PASS: base26 positive control (4,2)')
  n=0
  for name in ('neutral_p11','neutral_p12','neutral_b26_control'):
   file=D/'data'/f'{name}.txt';L=read(file)
   for H,o in ((1,0),(3,1)):
    a=run(exe,file,2,H,o)
    z=sum(run(exe,file,2,H,o,(d,)) for d in range(2*L[3]-1))
    assert a==z,(name,H,o,a,z);n+=1
  assert n==6
  print('PASS: 6 complete first-digit partition identities')
if __name__=='__main__':main()
