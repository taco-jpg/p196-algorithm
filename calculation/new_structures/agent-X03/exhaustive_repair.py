#!/usr/bin/env python3
"""Independent arbitrary-precision check of delayed full-word bridge repair.
No dependency on the spatial graph engine or C++ digit-array replayer.
"""
import itertools,collections,csv,sys
from pathlib import Path
AL='0123456789ABCDEFGHI'

def parse(filename):
  out={}
  for line in Path(filename).read_text().splitlines():
    t=line.split()
    if t and t[0] in ('ROOTPATH','LOOPA','LOOPB'):
      out[t[0]]=[tuple(AL.index(x) for x in c) for c in t[2:]]
      assert len(out[t[0]])==int(t[1][2:])
  return out

def trial(w,cut):
  C=list(w['ROOTPATH']);A=w['LOOPA'];B=w['LOOPB'];hist=trial.history
  for s in hist:C+=(A if s=='A' else B)
  # The centre cut is inside A, whose untruncated continuation is the phase oracle.
  C+=A+A # 2*92 columns of lookahead, enough for 16 steps.
  h=len(C)-len(A)*2+cut
  x=[a[0] for a in C[:h]]
  assert x[-1]%2==0 and cut in (2,63)
  digits=[z//2 for z in x[:-1]]+[x[-1]//2]+[z-z//2 for z in x[-2::-1]]
  assert digits[-1]>0
  n=int(''.join(map(str,digits[::-1])))
  full=[];off=[];notpal=[];overflow=[]
  for t in range(17):
    s=str(n);nlen=len(s);need=(nlen+1)//2
    p=[int(s[i])+int(s[-1-i]) for i in range(need)]
    e=[col[t%8] for col in C[:need]]
    assert len(e)==len(p)
    full.append(p==e)
    off.append(next((i for i,(a,b) in enumerate(zip(p,e)) if a!=b),need)-need)
    notpal.append(s!=s[::-1])
    if t<16:
      m=n+int(s[::-1]);overflow.append(len(str(m))-len(s));n=m
  return full,off,notpal,overflow
trial.history=''

def main():
  w=parse(sys.argv[1] if len(sys.argv)>1 else 'bridge_witness_generated.txt')
  assert (len(w['ROOTPATH']),len(w['LOOPA']),len(w['LOOPB']))==(45,92,97)
  cases=0;failures=[];recovery=collections.Counter();profiles=collections.Counter()
  with open('exhaustive_repair.csv','w') as f:
    writer=csv.writer(f);writer.writerow(['word','cut','seed_half','full_times_0_to_16','first_mismatch_offsets_0_to_16','overflow_0_to_15'])
    for k in range(0,8):
      for seq in itertools.product('AB',repeat=k):
        trial.history=''.join(seq)
        for cut in (2,63):
          ful,off,nopal,ov=trial(w,cut)
          cases+=1
          expected=([0,1,2,9,10] if cut==2 else [0,1,2,5,6,7,8,9,10])
          success=all(ful[t] for t in expected) and all(nopal) and ov==[1,0]*8
          if not success:failures.append((trial.history,cut,expected,[i for i,b in enumerate(ful) if b]))
          recovery[cut]+=ful[9] and ful[10]
          profiles[(cut,tuple(ful))]+=1
          writer.writerow([trial.history,cut,len(w['ROOTPATH'])+sum(len(w['LOOPA' if a=='A' else 'LOOPB']) for a in trial.history)+cut,
                           ''.join('1' if z else '0' for z in ful),' '.join(str(z) for z in off),''.join(map(str,ov))])
  print('words',sum(2**k for k in range(8)),'cases',cases,'positive reentry',recovery,'profiles',len(profiles),'failures',failures[:5]);
  assert not failures
  print('PASS: all 510 base-10 big integers have the predicted genuine full-word phase reentry (t=9,10)')
if __name__=='__main__':main()
