#!/usr/bin/env python3
"""Independent controls for Y12's all-width neutral-nine proof (not proof by replay)."""
import json,sys
sys.set_int_max_str_digits(1000000)
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
F={0:0,2:4,4:8,6:12,8:16,10:2,12:6,14:10,16:14,18:18}
EXPECT={0:(3,18),2:(3,18),4:(3,18),6:(7,0),8:(5,0),10:(1,0),12:(1,0),14:(1,0),16:(1,0),18:(1,0)}
def step(d):
 c=0;z=[]
 for i in range(len(d)):
  u=d[i]+d[-1-i]+c;z.append(u%10);c=u//10
 if c:z.append(c)
 return z
def pair(d):return [d[i]+d[-1-i] for i in range(len(d))]
def seed(Q,L,C):
 h=B+W*Q+[9]*L;p=h+[C]+h[::-1];n=len(p);d=[0]*n
 for i in range(n//2):d[i]=min(9,p[i]);d[-1-i]=p[i]-d[i]
 d[n//2]=C//2
 assert d[-1]!=0 and pair(d)==p
 return d
def run():
 table={}
 for k in [*range(0,19,2),9]:
  out=set()
  for a in (0,1):
   for b in (0,1):
    def norm(c):
     digits=[]
     for _ in range(5):
      z=k+c;digits.append(z%10);c=z//10
     return digits
    z=norm(a)[3]+norm(b)[3];out.add(z)
    assert z==(18-9*(a+b) if k==9 else F[k])
  table[k]=sorted(out)
 assert table[9]==[0,9,18]
 tests=0;first={}
 for Q in (8,12,19):
  for L in (30,47,81,161):
   for C in EXPECT:
    d=seed(Q,L,C);v=int(''.join(map(str,d[::-1])));pos=len(B)+20*Q+L//2
    seen=[]
    for t in range(9):
     assert int(''.join(map(str,d[::-1])))==v
     k=pair(d)[pos];seen.append(k)
     if t<8:
      d=step(d);v+=int(str(v)[::-1]);tests+=1
    when=next(i for i,x in enumerate(seen) if x!=9)
    assert (when,seen[when])==EXPECT[C],(Q,L,C,seen)
    assert all(x!=9 for x in seen[when:])
    first[C]=(when,seen[when])
 print(json.dumps({'label':'PAPER PROOF with COMPUTED controls','local_table':table,
    'p8_single_centre_first_even':first,'independent_full_integer_steps':tests,
    'tested_Q':[8,12,19],'tested_L':[30,47,81,161],
    'scope_warning':'Controls sample lengths only; all-width proof is in report.'},sort_keys=True))
if __name__=='__main__':run()
