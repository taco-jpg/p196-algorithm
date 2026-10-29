#!/usr/bin/env python3
"""Independent actual Python integers; does NOT call the cone evolution code."""
import hashlib
import random
from affine_cone import B,W,shield


def make_pairs(Z, mutate=False):
 A=shield(144)
 if mutate: A[3+13]=6
 P=B+W+A+Z+A[::-1]+W[::-1]+B[::-1]
 assert P==P[::-1]
 digs=[0]*len(P)
 for i in range(len(P)//2):
  a=min(P[i],9);digs[i]=a;digs[-1-i]=P[i]-a
 if len(P)%2:
  assert P[len(P)//2]%2==0
  digs[len(P)//2]=P[len(P)//2]//2
 assert digs[-1]!=0
 return ''.join(str(x) for x in digs[::-1])


def replay(Z, mutate=False):
 s=make_pairs(Z,mutate)
 assert s[0]!='0'
 n0=len(s)
 expected_phase={}
 for t in range(265):
  p=[int(s[-1-i])+int(s[i]) for i in range(min(59,len(s)//2))]
  if t<8:expected_phase[t]=p[:39]
  if not mutate:
   assert p[:39]==expected_phase[t%8], (len(Z),t,'root')
   assert any(x%2 for x in p[:39]),(len(Z),t,'odd')
   if t in (88,176,264):assert p[:59]==B+W,(len(Z),t,'renewal')
  elif t in (88,176,264) and p[:59]!=B+W:
   return {'mutant_break':t}
  assert s!=s[::-1] or mutate,(len(Z),t,'palindrome')
  if t==264:break
  s=str(int(s)+int(s[::-1]))
  assert len(s)==n0+(t//2+1), (len(Z),t,'growth')
 if mutate: return {'mutant_break':None}
 return {'initial_length':n0,'final_length':len(s),'sha256':hashlib.sha256((s+'\n').encode()).hexdigest()}

if __name__=='__main__':
 rng=random.Random(808808)
 total=0
 for L in (0,1,2,3,7,17,47,180,600):
  for k in range(5):
   Z=[0]*L
   for i in range(L//2):Z[i]=Z[L-1-i]=rng.randrange(19)
   if L%2:Z[L//2]=2*rng.randrange(10)
   result=replay(Z)
   total+=1
   if k==0:print('length',L,'seed_digits',result['initial_length'],'finish_sha256',result['sha256'][:16])
 print('PASS',total,'independent ordinary-integer orbits, 0 palindrome, all three renewals')
 print('mutation',replay([],True))
