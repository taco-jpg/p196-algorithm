#!/usr/bin/env python3
"""Universal no-overflow first-defect carry gate; p12/m9 phase exclusions.
Standalone stdlib checker using the repository's existing lattice data.
"""
import sys
from pathlib import Path

def load(path):
    a=list(map(int,Path(path).read_text().split()));p,nb,m,base=a[:4]; i=4
    gam=a[i:i+p];i+=p
    def read_rows(count,width):
        nonlocal i
        z=[a[i+t*width:i+(t+1)*width] for t in range(count)];i+=count*width;return z
    W=read_rows(p,m); C=read_rows(p,m); B=read_rows(p,nb)
    assert i==len(a) and (p,m,base)==(12,9,10)
    return p,nb,m,gam,W,C,B

def step(P):
    c=0;out=[];car=[0]
    for q in P:
        v=q+c;out.append(v%10);c=v//10;car.append(c)
    if c:out.append(c)
    return [out[i]+out[-i-1] for i in range(len(out))],out,car

def full(H,odd):return H+H[-2::-1] if odd else H+H[::-1]


def ordinary_numeric_step(P):
    """Independent canonical-digit reverse-and-add, not pair_step(P)."""
    n=len(P); d=[0]*n
    for i in range(n//2):
        q=P[i]; hi=min(9,q); lo=q-hi
        d[i]=lo; d[n-1-i]=hi
        assert 0<=lo<=9 and 1<=hi<=9 if i==0 else 0<=lo<=9 and 0<=hi<=9
    if n%2:
        assert P[n//2]%2==0;d[n//2]=P[n//2]//2
    assert d[-1]>0
    c=0;O=[]
    for i in range(n):
        x=d[i]+d[n-1-i]+c;O.append(x%10);c=x//10
    if c:O.append(c)
    return [O[i]+O[-1-i] for i in range(len(O))]

def gate_options(q,cl,cu):
    ans=[]
    for p in range(19):
        delta=p-q
        if delta not in (-5,5):continue
        dl=((p+cl)//10)-((q+cl)//10)
        dh=((p+cu)//10)-((q+cu)//10)
        if dl==delta//5 and dh==0:ans.append(p)
    return ans

# Exhaustively check the UNIVERSAL 19x19x2x2 carry-gate arithmetic.
gates=[]
for q in range(19):
  for q2 in range(19):
    if q2==q:continue
    for cl in (0,1):
      for cu in (0,1):
        delta=q2-q
        A=((q2+cl)//10)-((q+cl)//10)
        B=((q2+cu)//10)-((q+cu)//10)
        if 2*delta==10*A and B==0:gates.append([q,q2,cl,cu])
assert sorted(gates)==sorted([[4,9,1,0],[9,4,1,0],[9,14,0,1],[14,9,0,1]])
print('UNIVERSAL_GATE',gates)
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'data'/'lat_p12m9.txt'
p,nb,m,g,W,C,B=load(path)
assert g==[1,0,0,0]*3
assert all(any(w!=9 for w in row) for row in W)
for t in range(p):
 if g[t]:continue
 possibilities=[]
 for r,q in enumerate(W[t]):
  # one 9-run maximum, so the reversed (upper) carry entering j' is
  # fixed by the nearest non-9 coefficient after the lower site j.
  nx=W[t][(r+1)%m]
  next_non9=nx if nx!=9 else W[t][(r+2)%m]
  assert next_non9!=9
  cl=C[t][r];cu=int(next_non9>=10)
  for q2 in gate_options(q,cl,cu):possibilities.append([r,q,q2,cl,cu])
 # Compare exact incoming carries from the complete finite pair words,
 # for both parities and two different band lengths.
 for odd in (0,1):
  for k in (0,1):
   n=400+18*k+odd;h=(n+1)//2
   H=[B[t][i] if i<nb else W[t][(i-nb)%m] for i in range(h)]
   if odd and H[-1]%2:H[-1]-=1
   P=full(H,odd);_,out,carry=step(P)
   assert len(out)==n,(t,odd,k)
   for r,q in enumerate(W[t]):
    j=nb+3*m+r;j2=n-1-j
    cl=carry[j];cu=carry[j2]
    assert (cl,cu)==(C[t][r], int((W[t][(r+1)%m] if W[t][(r+1)%m]!=9 else W[t][(r+2)%m])>=10)),(t,odd,k,r,cl,cu)
 print('PHASE',t,'GAMMA0','POSSIBLE_FIRST_DEFECTS',possibilities)
 if t in (3,7,11): assert not possibilities

# Independent positive controls: real no-overflow collisions in the centre.
controls=[(True,[1,9,10,0],[1,14,9,10]),(False,[1,9,9,10],[1,14,14,0]),(True,[1,0,9,10,0],[1,0,14,9,10])]
for odd,L,R in controls:
 PA=full(L,odd);PB=full(R,odd)
 QA,OA,_=step(PA);QB,OB,_=step(PB)
 assert len(OA)==len(PA) and len(OB)==len(PB) and QA==QB and PA!=PB
 assert ordinary_numeric_step(PA)==QA and ordinary_numeric_step(PB)==QB
 print('COLLISION_CONTROL n',len(PA),'PASS')
print('GATE_AND_NO_GATE_PHASES_3_7_11_PASS')
