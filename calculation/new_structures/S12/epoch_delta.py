#!/usr/bin/env python3
"""Independent Python-bigint verifier for the S12 K-source insertion law."""
from pathlib import Path
import sys
sys.set_int_max_str_digits(0)
M=101
root=Path(__file__).resolve().parents[3]
rows=[[int(x) for x in s.split()] for s in (root/'calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt').read_text().splitlines() if s.strip()]
assert len(rows)==38 and rows[0]==[12,34,9,10]
W=rows[2];B=rows[26]
def xp(n): return pow(-10,n,M)
def G(k): return sum(pow(10,r,M) for r in range(k))%M
def Pword(q,k,J,U,C):
 h=B+W*q+list(J)+list(U)*k
 return h+list(C)+h[::-1]
def source(P):
 assert len(P)%2==0 and P==P[::-1] and P[0]>0 and P[-1]>0
 lo=[max(x-9,0) for x in P[:len(P)//2]]; hi=[x-y for x,y in zip(P,lo)]
 d=lo+hi[::-1]; assert [d[i]+d[-1-i] for i in range(len(d))]==P
 return d
def nval(d): return int(''.join(map(str,d[::-1])))
def norm(P):
 c=K=0;cs=[];out=[]
 for i,x in enumerate(P):
  z=x+c;c=z//10;out.append(z%10);cs.append(c);K=(K+c*xp(i+1))%M
 if c:out.append(c)
 return K,cs,out,c
def block(V,b):
 c=b;A=0
 for j,x in enumerate(V):c=(x+c)//10;A=(A+c*xp(j+1))%M
 return c,A
def seg(cs,l,r):return sum(cs[i]*xp(i+1) for i in range(l,r))%M
def predict(q,k,J,U,C,P,old):
 V=U[::-1];a=len(B)+9*q+len(J);c=len(C);s=a+3*k;t=s+c;z=t+3*k
 bu=block(U,0)[0];bv=block(V,0)[0]
 assert block(U,1)[0]==bu and block(V,1)[0]==bv
 au=block(U,bu)[1];b=old[1][t-1];av0=block(V,b)[1];avs=block(V,bv)[1]
 assert block(V,b)[0]==bv
 kc=seg(old[1],s,s+c);kz=seg(old[1],z,len(P))
 return (xp(s)*au+9*kc+xp(t)*(9*av0+(1-2*G(k))*avs)-2*kz)%M
def motifs():
 return sorted({tuple(([9,a,18-a][r:]+[9,a,18-a][:r])) for a in range(0,19,2) for r in range(3)})
def collars():
 return [([5],[1,1]),([4,12],[12,4,4,12]),([18,6,10],[2,8,12,12,8,2]),([14,18,1,15,4,16,12,10,4,6,3,9,13,10,1,9,7],[4,0,8,12,12,8,0,4])]
def main():
 widths=[(q,k) for q in range(20,24) for k in range(40,44)]+[(n,n) for n in (20,40,80,160)];checked=0
 for U in motifs():
  assert len(U)==3 and sum(U)==27
  for J,C in collars():
   assert C==C[::-1] and len(C)%2==0
   for q,k in widths:
    P=Pword(q,k,J,U,C);P5=Pword(q,k+5,J,U,C);old=norm(P);new=norm(P5)
    assert old[3]==new[3]==1 and predict(q,k,J,U,C,P,old)==(new[0]-old[0])%M
    d=source(P);n=nval(d);n1=n+int(str(n)[::-1])
    assert n1==sum(x*10**i for i,x in enumerate(P))==nval(old[2])
    assert len(str(n1))-len(str(n))==old[3]
    d5=source(P5);n5=nval(d5);n51=n5+int(str(n5)[::-1])
    assert n51==sum(x*10**i for i,x in enumerate(P5))==nval(new[2])
    checked+=1
 assert checked==2400
 print(f'PASS: {checked} source-delta controls, 30 U motifs x 4 even-centre collars x 20 (q,k) pairs.')
 print('Python native integers independently verify N+reverse(N) at q,k=20,40,80,160; no macro-return claim.')
if __name__=='__main__':main()
