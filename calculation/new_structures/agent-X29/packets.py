#!/usr/bin/env python3
"""Independently verify 128 interlaced p3 packet variants by native Python bigint."""
import argparse, hashlib, json, sys
sys.set_int_max_str_digits(1000000)
from construct import B1,W1,split,string,pairs

def packet_seed(k,m,q,mask):
 H=list(B1)+list(W1)*k+[5,5,2]*m+[18]*q
 for v,j in enumerate([8,16,24,32,40,48,56]):
  if mask>>v&1:
   s=len(B1)+20*k+3*j+1
   assert H[s:s+3]==[5,2,5]
   H[s:s+3]=[7,7,7]
 return int(string(split(H+[18]+H[::-1])))
def run(k=300,m=80,q=6500):
 base=None;step4=None
 for mask in range(128):
  n=packet_seed(k,m,q,mask)
  assert len(str(n))==2*(39+20*k+3*m+q)+1
  for t in range(6):
   s=str(n);assert s!=s[::-1]
   if t==4:
    pair=bytes((int(a)+int(b) for a,b in zip(s,s[::-1])))
    if step4 is None:step4=pair
    assert pair==step4,(mask,'pair mismatch')
   if t==5:
    if base is None:base=n
    assert n==base,(mask,'num mismatch')
   if t<5:n+=int(s[::-1])
 print(json.dumps({'k':k,'m':m,'q':q,'variants':128,'merge_step':5,'pair_merge_step':4,'nonpals':768,'merged_sha256':hashlib.sha256(str(base).encode()).hexdigest(),'merged_digits':len(str(base))}))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--k',type=int,default=300);parser.add_argument('--m',type=int,default=80);parser.add_argument('--q',type=int,default=6500);a=parser.parse_args();run(a.k,a.m,a.q)
