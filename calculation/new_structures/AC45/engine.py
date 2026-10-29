#!/usr/bin/env python3
"""Bounded exact endpoint ROBDD. NOT the unbounded pi185 120-track product."""
import argparse,itertools,json
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)
U=(9,0,18)
def template(j,c,q=14,k=100):
 h=B+W*q+tuple(j)+U*k
 return h+tuple(c)+h[::-1]
def realize(p):
 assert p==p[::-1]
 d=[0]*len(p)
 for i in range(len(p)//2):
  d[i]=max(0,p[i]-9);d[-i-1]=p[i]-d[i]
 if len(p)%2:
  assert p[len(p)//2]%2==0
  d[len(p)//2]=p[len(p)//2]//2
 assert d[-1]>0
 return d
def step_digits(d):
 out=[];carry=0
 for a,b in zip(d,reversed(d)):
  s=a+b+carry;out.append(s%10);carry=s//10
 if carry:out.append(carry)
 return out
def pair(d):return tuple(a+b for a,b in zip(d,reversed(d)))
def exact(j,c,q=14,k=100,independent=False):
 d=realize(template(j,c,q,k))
 n=int(''.join(map(str,reversed(d)))) if independent else None
 total_gamma=0
 for t in range(120):
  nxt=step_digits(d);total_gamma+=len(nxt)-len(d);d=nxt
  if independent:
   n=n+int(str(n)[::-1])
   assert d==[int(x) for x in str(n)[::-1]],(j,c,q,k,t)
 target=template(j,c,q,k+5);got=pair(d)
 mismatch=next((i for i,(a,b) in enumerate(zip(got,target)) if a!=b),min(len(got),len(target)))
 return got==target,total_gamma,mismatch
def robdd(truth):
 unique={}
 def go(v,depth):
  if all(x==v[0] for x in v):return int(v[0])
  half=len(v)//2;lo=go(v[:half],depth+1);hi=go(v[half:],depth+1)
  if lo==hi:return lo
  key=(depth,lo,hi)
  if key not in unique:unique[key]=len(unique)+2
  return unique[key]
 return go(tuple(truth),0),len(unique)
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--jlen',type=int,default=2);p.add_argument('--centre',type=int,default=4)
 p.add_argument('--q',type=int,default=14);p.add_argument('--k',type=int,default=100)
 p.add_argument('--prefix',type=int);p.add_argument('--independent',action='store_true')
 a=p.parse_args();assert 0<=a.jlen<=2 and 0<=a.centre<=18
 bits=[];valid=returns=clock=0;hist={}
 for codes in itertools.product(range(32),repeat=a.jlen):
  if any(x>=19 for x in codes):
   bits.append(False);continue
  valid+=1;ok,g,m=exact(codes,(a.centre,a.centre),a.q,a.k,a.independent)
  returns+=ok;clock+=g==30;hist[m]=hist.get(m,0)+1
  bits.append(ok if a.prefix is None else (m>=a.prefix and g==30))
 root,nodes=robdd(bits)
 print(json.dumps(dict(label='COMPUTED' if a.independent else 'UNDECIDED',
  scope='fixed even C=(c,c), U=(9,0,18), bounded J; no all-length decision',
  q=a.q,k=a.k,jlen=a.jlen,c=a.centre,valid=valid,returns=returns,
  correct_overflow_count=clock,prefix_threshold=a.prefix,accepted=sum(bits),
  robdd_nonterminal_nodes=nodes,robdd_root=root,first_mismatch_histogram=hist),
  sort_keys=True))
if __name__=='__main__':main()
