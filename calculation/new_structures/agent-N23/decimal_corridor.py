#!/usr/bin/env python3
"""Mine an actual decimal affine-band corridor, later proved for ALL q by polynomial_checker."""
import json,sys
from mine_decimal import groups,nextn,infer
def make(qbase=50,nsteps=174):
 vals={q:int('12'+'99'*(qbase+q+2)+'34') for q in range(5)}
 phases=[]
 for t in range(nsteps+1):
  words={q:groups(n) for q,n in vals.items()}
  x=infer(words)
  if not x:raise RuntimeError('loss of one-band shape at step '+str(t))
  phase=x[0]
  for q in words:
   arr=[]
   for p in phase['parts']:
    if 'digits' in p:arr+=p['digits']
    else:arr+=p['motif']*(p['slope']*q+p['offset'])
   assert arr==words[q]
  phases.append(phase)
  vals={q:nextn(n) for q,n in vals.items()}
 return {'base':100,'decimal_block_digits':2,'qmin':0,'origin':'N_0(r) = 12 (99)^(qbase+2+r) 34; all phases exact decimal reverse-add; open corridor','qbase':qbase,'phases':phases}
if __name__=='__main__':
 j=make(int(sys.argv[2]),int(sys.argv[3]));json.dump(j,open(sys.argv[1],'w'),separators=(',',':'))
 print('generated',len(j['phases']),'states')
