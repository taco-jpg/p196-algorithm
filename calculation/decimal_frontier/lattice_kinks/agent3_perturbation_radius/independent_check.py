#!/usr/bin/env python3
"""Independent digit-normalization check for 12 augmented rec2 covariance rows."""
import itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
raw=list(map(int,(HERE/'lat2.txt').read_text().split()))
assert raw[:12]==[8,11,48,10,1,0,1,0,1,0,1,0]
W=[raw[12+48*t:12+48*(t+1)] for t in range(8)]
F=[sum(1<<m for m in range(64) if m&b==m) for b in range(64)]

def digits(P):
 n=len(P);ups=[];dns=[]
 for seed in (0,1):
  c=seed;aa=[]
  for x in P:aa.append(c);c=(x+c)//10
  if c==seed:ups.append(aa)
  c=seed;dd=[0]*n
  for j in range(n-1,-1,-1):dd[j]=c;c=(P[j]+c)//10
  if c==seed:dns.append(dd)
 assert len(ups)==len(dns)==1
 a,d=ups[0],dns[0]
 return [(P[j]+a[j])%10 for j in range(n)],[(P[j]+d[j])%10 for j in range(n)],a,d

def feature(P):
 _,_,a,d=digits(P);n=len(P);v=0
 for j in range(n):
  k=(j+1)%n
  bits=(P[j]%2)|((P[k]%2)<<1)|(a[j]<<2)|(d[j]<<3)|(a[k]<<4)|(d[k]<<5)
  v^=F[bits]
 return v

def cov(t,P):
 lo,hi,_,_=digits(P);g=1-t%2;n=len(P)
 after=[lo[j]+hi[(j-g)%n] for j in range(n)]
 v=feature(after)<<(64*((t+1)%8))
 if g:v^=feature(P)<<(64*t)
 return v

def tagrow(tag):
 t,j,s,u=tag;P=W[t].copy()
 if j>=0:
  P[j]+=s
  if u:P[(j+1)%48]+=u
 return cov(t,P)

def augrow(tag):
 typ,t,j,*tail=tag;P=W[t].copy()
 if typ=='pair':
  sep,s,u=tail;P[j]+=s;P[(j+sep)%48]+=u
 else:
  s,u,v=tail;P[j]+=s;P[(j+1)%48]+=u;P[(j+2)%48]+=v
 return cov(t,P)

def rank(vs):
 piv={}
 for v in vs:
  while v:
   k=(v&-v).bit_length()-1
   if k not in piv:piv[k]=v;break
   v^=piv[k]
 return len(piv)

def check():
 ref=json.loads((HERE/'rank_witness.json').read_text())
 extra=json.loads((HERE/'augmentation_tags.json').read_text())
 assert len(ref)==388 and len(extra)==12
 assert rank(tagrow(x) for x in ref)==388
 assert rank([*(tagrow(x) for x in ref),*(augrow(x) for x in extra)])==400
 # Independently enumerate every support-in-three-cells perturbation.
 rows=[tagrow(x) for x in ref]
 for t in range(8):
  for j in range(48):
   k=(j+2)%48
   for s,u in itertools.product((-1,1),repeat=2):
    P=W[t].copy();P[j]+=s;P[k]+=u
    if 0<=P[j]<=18 and 0<=P[k]<=18:rows.append(cov(t,P))
 for t in range(8):
  for j in range(48):
   I=(j,(j+1)%48,(j+2)%48)
   for ss in itertools.product((-1,1),repeat=3):
    P=W[t].copy()
    for k,s in zip(I,ss):P[k]+=s
    if all(0<=P[k]<=18 for k in I):rows.append(cov(t,P))
 assert rank(rows)==398
 # All two-site separations cannot reach rank400, even without the triple test.
 rows=[tagrow(x) for x in ref]
 for sep in range(2,25):
  for t in range(8):
   for j in range(48):
    k=(j+sep)%48
    for s,u in itertools.product((-1,1),repeat=2):
     P=W[t].copy();P[j]+=s;P[k]+=u
     if 0<=P[j]<=18 and 0<=P[k]<=18:rows.append(cov(t,P))
 assert rank(rows)==398
 print('INDEPENDENT PASS: physical digit normalization gives ranks 388,398,400 and all-pairs 398')
 print('INDEPENDENT PASS: 12 exact augmented tags, complete 3-cell support and 34236 all-pair controls')
if __name__=='__main__':check()
