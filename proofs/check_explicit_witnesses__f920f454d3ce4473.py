#!/usr/bin/env python3
"""Preserve the sharp actual witness and all bounded completion attempts."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def value(ds):return sum(d*10**i for i,d in enumerate(ds))
def digits(n):
 out=[]
 while n:n,d=divmod(n,10);out.append(d)
 return out

def inspect(q):
 assert q==q[::-1] and min(q)>=9 and q[0]>=10
 ds=[0]*len(q)
 for i in range(len(q)//2):ds[i]=min(9,q[i]);ds[-i-1]=q[i]-ds[i]
 if len(q)%2:assert q[len(q)//2]%2==0;ds[len(q)//2]=q[len(q)//2]//2
 n=value(ds);assert ds[-1]>0
 states=[];carries=[]
 for t in range(9):
  actual=digits(n);p=[x+y for x,y in zip(actual,reversed(actual))]
  if t==0:assert p==q
  states.append({'time':t,'integer':n,'pair_word':p,'palindrome':actual==actual[::-1],
    'high':p[0]>=10 and min(p)>=9 and max(p)<=18})
  if t<8:
   carries.append([value(p[:i])//10**i for i in range(len(p)+1)])
   next_n=n+value(actual[::-1]);assert next_n==value(p);n=next_n
 return {'initial_pair_word':q,'states':states,'normalization_carries':carries,
  'consecutive_two_step_returns':next((i-1 for i in range(1,5) if not states[2*i]['high']),4),
  'six_positive_outputs_safe':not any(s['palindrome'] for s in states[1:7])}

def main():
 attempts=[
 ('minimal_sharp',[17,9,18,9,17]),('other_width5',[17,16,10,16,17]),
 ('width6_a',[17,9,18,18,9,17]),('width6_b',[17,16,9,9,16,17]),('width6_c',[17,16,10,10,16,17]),
 ('bulk17_a',[17,16,9,17,17,9,16,17]),('bulk17_b',[17,16,10,17,17,10,16,17]),
 ('bulk16',[17,16,10,16,16,10,16,17]),('bulk18_initial',[17,16,9,18,18,9,16,17]),
 ('repeated_minimal',[17,9,18,9,17,17,9,18,9,17]),
 ('alternating_center',[17,9,18,9,18,9,18,9,17]),
 ('single_central18',[17,9,18,9,17,18,17,9,18,9,17]),
 ('double_central18',[17,9,18,9,17,18,18,17,9,18,9,17]),
 ]
 attempts += [('uniform18_m'+str(m),[17,16,9]+[18]*m+[9,16,17]) for m in (2,4,6,8,10,12)]
 rows=[];seen={}
 for label,q in attempts:
  key=tuple(q)
  if key not in seen:
   seen[key]=len(rows);row=inspect(q);row['labels']=[];rows.append(row)
  rows[seen[key]]['labels'].append(label)
 sharp=rows[0]
 assert [sharp['states'][i]['pair_word'] for i in (0,2,4,6)]==[
  [17,9,18,9,17],[16,16,18,18,16,16],[15,9,14,18,14,9,15],[12,12,11,9,9,11,12,12]]
 assert sharp['states'][0]['integer']==80999
 assert sharp['consecutive_two_step_returns']==3 and sharp['states'][2]['palindrome']
 for row in rows:
  assert not(row['consecutive_two_step_returns']>=3 and row['six_positive_outputs_safe'])
  for label in row['labels']:
   if label.startswith('uniform18_m'):
    m=int(label.split('_m')[1]);s=row['states']
    assert s[2]['pair_word'][:4]==[17,10,16,9]
    assert s[2]['pair_word'][4]==(16 if m==2 else 17)
    assert s[4]['pair_word'][:4]==[16,18,16,14]
    assert s[6]['pair_word'][3]==6 and not s[6]['high']
 output={'scope':'All explicit finite completions tried in this review, including failures. No broad search and no negative result for every completion.',
  'sharp_high_only_witness_seed':80999,'safe_three_return_sharpness':'UNKNOWN',
  'records':rows}
 raw=(json.dumps(output,indent=2,sort_keys=True)+'\n').encode()
 (HERE/'explicit_witnesses.json').write_bytes(raw)
 report={'result':'PASS_SHARP_HIGH_ONLY_WITNESS_AND_RETAINED_COMPLETIONS',
  'distinct_words':len(rows),'labeled_attempts':len(attempts),'transitions_per_word':8,
  'sharp_seed':80999,'sharp_returns':3,'sharp_witness_second_output_is_palindrome':True,
  'safe_three_return_sharpness':'UNKNOWN','uniform18_parameters':[2,4,6,8,10,12],
  'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'records_sha256':hashlib.sha256(raw).hexdigest()}
 (HERE/'explicit_witness_verification.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()
