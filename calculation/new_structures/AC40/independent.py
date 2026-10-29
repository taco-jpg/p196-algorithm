#!/usr/bin/env python3
"""Independent true-decimal bigint replay. Does not call the C++ pairword engine."""
from random import Random
B=[5,2,7,12,0,3,14,15,5,9,0,9,3,4,18,11,9,15,9,10,14,10,5,12,0,17,9,16,1,14,1,14,4,17]
W=[11,9,12,2,9,2,4,0,17]
U=[9,0,18]
if hasattr(__import__('sys'),'set_int_max_str_digits'):__import__('sys').set_int_max_str_digits(0)
def tpl(J,C,q,k):
 h=B+W*q+J+U*k
 return h+C+h[::-1]
def initial(P):
 assert P==P[::-1]
 d=[0]*len(P)
 for i in range(len(P)//2):
  high=min(9,P[i]); low=P[i]-high
  assert 0<=low<=9
  d[i]=low;d[-1-i]=high
 if len(P)%2:assert P[len(P)//2]%2==0;d[len(P)//2]=P[len(P)//2]//2
 assert d[-1]>0
 return int(''.join(map(str,d[::-1])))
def run(J,C,q=14,k=100):
 n=initial(tpl(J,C,q,k)); gamma=[]
 for t in range(120):
  s=str(n);new=n+int(s[::-1]);gamma.append(len(str(new))-len(s));n=new
 d=[int(x) for x in str(n)[::-1]]
 got=[d[i]+d[-1-i] for i in range(len(d))]
 wanted=tpl(J,C,q,k+5)
 first=next((i for i,(x,y) in enumerate(zip(got,wanted)) if x!=y),min(len(got),len(wanted)))
 return (got==wanted,first,sum(gamma),''.join(map(str,gamma)))
if __name__=='__main__':
 rnd=Random(19647640)
 Jcases=[[0]*6,[0]+[18]*5,[0,1,2,3,4,5],[0,18,0,18,0,18]]
 Jcases=Jcases[:4]+[[0]+[rnd.randrange(19) for _ in range(5)] for _ in range(6)]
 for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
  for C in ([4,4],[4,14,4]):
   for j,J in enumerate(Jcases):
    result=run(J,C,q,k)
    assert not result[0]
    assert result[2]==30
    print('control',q,k,len(C),j,result[:3],result[3][:12])