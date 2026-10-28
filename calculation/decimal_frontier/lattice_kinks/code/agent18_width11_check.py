#!/usr/bin/env python3
"""Independent ordinary-integer replay of finite centre SAT witness, not a certificate."""
import sys
from pathlib import Path
from agent18_width11_z3 import load_lat

def bdigit(n):
 d=[]
 while n:d.append(n%10);n//=10
 return d or [0]
def number(d):
 n=0
 for v in d[::-1]:n=n*10+v
 return n

def run(o,cent,H=40,w=11,M=6):
 lat=load_lat();a=list(map(int,(Path(__file__).parent.parent/'data'/'lat2.txt').read_text().split()));p,nB,m,gam,W=lat['p'],lat['nB'],lat['m'],lat['gam'],lat['W']; K=M+w
 B=[a[4+p+2*p*m+i*nB:4+p+2*p*m+(i+1)*nB] for i in range(p)]
 assert len(cent)==K
 n=400+o;h=(n+1)//2
 lo=[B[0][i] if i<nB else W[0][(i-nB)%m] for i in range(h-K)]+cent[:]
 pair=lo+(lo[::-1] if n%2==0 else lo[-2::-1]);assert len(pair)==n
 d=[0]*n
 for i in range(n//2):
  v=pair[i];a_i=min(9,v);b_i=v-a_i;d[i]=a_i;d[n-1-i]=b_i
 if n%2:d[n//2]=pair[n//2]//2
 assert d[-1]>0
 N=number(d)
 for t in range(H+1):
  d=bdigit(N);actualn=len(d)
  assert actualn==n,(t,'length',actualn,n)
  h=(n+1)//2
  pp=[d[i]+d[n-1-i] for i in range(n)]
  assert pp==pp[::-1]
  for i in range(h-K):
   expected=B[t%p][i] if i<nB else W[t%p][(i-nB)%m]
   assert pp[i]==expected,(t,'outer',i,pp[i],expected)
  if t==0:assert pp[h-K:h]==cent
  assert d!=d[::-1],('palindrome',t)
  if t<H:
   NN=N+number(d[::-1]);n+=gam[t%p]
   assert len(bdigit(NN))==n,(t,'overflow')
   N=NN
 print('BIGINT_REPLAY_PASS',H,'steps','seed_digits',400+o,'final_digits',n,'all exterior template rows and no palindromes checked')

if __name__=='__main__':
 o=int(sys.argv[1]);H=int(sys.argv[2]);vals=list(map(int,sys.argv[3].split(',')));run(o,vals,H)
