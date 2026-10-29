#!/usr/bin/env python3
"""Independent Python-bigint controls for the R18 fixed-seam centre extension.
The all-q,k>=512 seed mismatch is from calculation/new_structures/S08/verify.py.
"""
import sys
sys.set_int_max_str_digits(0)
B=[10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4]
W=[8,1,15,4,0,5,5,18,4]
J=[17,5,5,9,6,6,6,14,5,11,7,10,14,7,8,15,9,6,4,18,9,10,17,2]
U=[18,0,9]
CENTRES=[[1,1],[12,4,4,12],[2,8,12,12,8,2],[4,0,8,12,12,8,0,4]]
def P(q,k,C):
 h=B+W*q+J+U*k
 return h+C+h[::-1]
def src(p):
 h=len(p)//2;lo=[max(x-9,0) for x in p[:h]];hi=[x-y for x,y in zip(p,lo)];d=lo+hi[::-1]
 assert [d[i]+d[-1-i] for i in range(len(d))]==p
 return int(''.join(map(str,d[::-1])))
def digits(n):return list(map(int,str(n)[::-1]))
def pair(n):
 d=digits(n);return [d[i]+d[-1-i] for i in range(len(d))]
def firstdiff(a,b):
 for i,(x,y) in enumerate(zip(a,b)):
  if x!=y:return i
 return -1 if len(a)==len(b) else min(len(a),len(b))
def main():
 count=0
 for C in CENTRES:
  for q in (20,40,80,160):
   for k in (20,40,80,160):
    p0=P(q,k,C);n=src(p0);palcount=0
    assert n+int(str(n)[::-1])==sum(x*10**i for i,x in enumerate(p0))
    for t in range(240):
     s=str(n)
     if s==s[::-1]:palcount+=1
     n1=n+int(s[::-1]);g=len(str(n1))-len(s)
     assert g==(1 if t%4==0 else 0),(q,k,t,g)
     n=n1
     if t+1==120:
      m=firstdiff(pair(n),P(q,k+5,C));assert m==9*q+35 and pair(n)[m]==9 and P(q,k+5,C)[m]==5,(q,k,C,m)
     if t+1==240:
      m=firstdiff(pair(n),P(q,k+10,C));assert m==9*q+12 and pair(n)[m]==6 and P(q,k+10,C)[m]==5,(q,k,C,m)
    assert palcount==0
    count+=1
 assert count==64
 print(f'PASS: {count} genuine Python-bigint 240-step controls; 16 independent (q,k) pairs x 4 even centres.')
 print('All overflow clocks match; no palindromes; endpoint mismatches are 9q+35 at 120 and 9q+12 at 240.')
if __name__=='__main__':main()
