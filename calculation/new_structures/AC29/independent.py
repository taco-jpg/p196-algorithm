#!/usr/bin/env python3
"""Independent Python unbounded-number n+reverse(n) endpoint oracle for AC29."""
import sys,subprocess
from pathlib import Path
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)
B=[10,4,15,4,1,7,9,11,11,18,0,18,6,9,17,4,0,12,0,2,10,1,12,4,2,15,0,13,4,8,4,8,10,15]
W=[4,0,5,5,18,4,8,1,15]
U=[v[s:]+v[:s] for a in range(0,19,2) for v in [[9,a,18-a]] for s in range(3)]
def decode(z):
 j=[]
 for _ in range(5):j.append(z%19);z//=19
 return j
def check(ui,z,centre,q,k):
 j=decode(z);u=U[ui];C=[4,14,4] if centre=="ODD" else [4,4]
 h=B+W*q+j+u*k;source=h+C+h[::-1]
 D=[0]*len(source)
 for i in range(len(D)//2):
  hi=min(9,source[i]);D[i]=source[i]-hi;D[-1-i]=hi
 if len(D)%2:D[len(D)//2]=source[len(D)//2]//2
 assert D[-1]>0
 n=int(''.join(map(str,D[::-1])))
 g=[];pal=0
 for t in range(120):
  s=str(n);pal+=s==s[::-1]
  v=n+int(s[::-1]);g.append(len(str(v))-len(s));n=v
 H=B+W*q+j+u*(k+5);target=H+C+H[::-1]
 d=list(map(int,str(n)[::-1]));obs=[d[i]+d[-1-i] for i in range(len(d))]
 mismatch=next((i for i,(a,b) in enumerate(zip(obs,target)) if a!=b),None)
 if mismatch is None and len(obs)!=len(target):mismatch=min(len(obs),len(target))
 exe=Path(__file__).with_name("census")
 lines=subprocess.check_output([str(exe),centre,str(z+1),str(ui),str(z),str(q),str(k)],text=True).splitlines()
 fields=lines[0].split()
 assert fields[0]=="tested" and fields[1]=="1" and fields[6]=="clockbad" and fields[7]=="0",lines
 hist={int(k):int(v) for k,v in (line.split() for line in lines[1:])}
 assert hist=={-1 if mismatch is None else mismatch:1},(hist,mismatch)
 assert g==[int(t%4==0) for t in range(120)] and pal==0
def main():
 cases=[(0,6,"ODD"),(28,17,"ODD"),(0,26,"ODD"),(1,5,"EVEN"),(4,100,"EVEN"),(20,280,"EVEN"),(28,800,"EVEN")]
 for ui,z,C in cases:
  for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
   check(ui,z,C,q,k)
 print("PASS: independent Python bigint vs C++ endpoint, 35 controls / five width pairs")
if __name__=="__main__":main()
