#!/usr/bin/env python3
"""Independent exhaustive census of period-three growing-band bulk cycles."""
from itertools import product
import json
from pathlib import Path
G=[1,0,0,0,1,0,0,0,1,0,0,0]
US=[(6,12,9),(9,18,0)]
def alt(x): return sum((1 if i%2==0 else -1)*v for i,v in enumerate(x))
def step(w,g):
 n=len(w); a=None; b=None
 for s in (0,1):
  c=s;v=[s]
  for x in w:c=(x+c)//10;v.append(c)
  if c==s:a=v;break
 for s in (0,1):
  v=[0]*(n+1);v[n]=s
  for i in range(n-1,-1,-1):v[i]=(w[i]+v[i+1])//10
  if v[0]==s:b=v;break
 if a is None or b is None:raise AssertionError('carry fixed point missing')
 return [(w[i]+a[i])%10+((w[(i-1)%n]+b[i])%10 if g else (w[i]+b[i+1])%10) for i in range(n)]
rows=[]
allw=list(product(range(19),repeat=3))
charge=[r for r in allw if sum(r)%9==0]
assert len(allw)==19**3==6859 and len(charge)==763
for U in US:
 gated=[r for r in charge if alt(r)%11==alt(U)%11]
 cycles=[]; hit999=[]; double9=[]
 for r in gated:
  x=list(r);seen=[]
  for t in range(120):
   seen.append(tuple(x));x=step(x,G[t%12])
  if tuple(x)==r:
   cycles.append(r)
   if any(y==(9,9,9) for y in seen):hit999.append(r)
   if any(any(y[i]==9 and y[(i+1)%3]==9 for i in range(3)) for y in seen):double9.append(r)
 assert len(gated)==72
 assert len(cycles)==(7 if U==US[0] else 11)
 assert not hit999
 assert not double9, (U,double9)
 nondeg=[r for r in cycles if r!=U and r!=(9,9,9)]
 rows.append({'U':U,'A_U_mod11':alt(U)%11,'all_R_words':len(allw),'charge_zero':len(charge),'charge_and_alt_gate':len(gated),'120_cycle_count_including_degenerate':len(cycles),'cycles_through_999':hit999,'phase_words_with_adjacent_9':double9,'excluded_R_equals_U':U in cycles,'nondegenerate_R_count':len(nondeg),'R':nondeg})
print(json.dumps({'clock':'1000 repeated 30 times','all_R_words':6859,'charge_zero_R':763,'results':rows},indent=2))
with Path(__file__).with_name('bulk_cycle_census.json').open('w') as f:json.dump({'clock':'1000 repeated 30 times','all_R_words':6859,'charge_zero_R':763,'results':rows},f,indent=2)
