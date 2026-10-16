#!/usr/bin/env python3
"""Literal integer prefix oracle and independent sink-deletion rank audit."""
import gzip, hashlib, json
from collections import Counter, deque
from pathlib import Path
HERE=Path(__file__).resolve().parent

def sha(data):return hashlib.sha256(data).hexdigest()
def value(q):return sum(x*10**i for i,x in enumerate(q))
def normalize(q):
 n=value(q); width=len(q)+(n>=10**len(q))
 ds=[n//10**i%10 for i in range(width)]
 assert ds[-1]>0
 return ds

def pair_step(q):
 ds=normalize(q)
 return [a+b for a,b in zip(ds,reversed(ds))]

def main():
 compressed=(HERE/'prefix_certificate.json.gz').read_bytes()
 raw=gzip.decompress(compressed);cert=json.loads(raw);rows=cert['vertices']
 assert len(rows)==900
 controls=[]; predecessors=[[] for _ in rows];outdegree=[0]*len(rows)
 for idx,row in enumerate(rows):
  A,B,C=row['word'];assert row['id']==idx==100*(A-10)+10*(B-9)+C-9
  assert 10<=A<=18 and 9<=B<=18 and 9<=C<=18
  assert [r['incoming'] for r in row['controls']]==[0,1]
  for t,saved in enumerate(row['controls']):
   a,p,z=A-9,A+B-18,B+C-18
   # The central 0 or 18 forces the selected carry, regardless of its input.
   word=[a,p,z,18*t,z,p,a];n=value(word)
   digits=[n//10**i%10 for i in range(7)]
   carry=[value(word[:i])//10**i for i in range(8)]
   assert carry[4]==t
   overflow=n//10**7
   candidate=[digits[0]+digits[6]+10*overflow,digits[1]+digits[5],digits[2]+digits[4]]
   reasons=[]
   if overflow:reasons.append('second_overflow_excluded_by_neutral_exterior_theorem')
   if not 10<=candidate[0]<=18:reasons.append('exterior_outside_high_region')
   if not all(9<=x<=18 for x in candidate[1:]):reasons.append('next_two_coefficients_outside_high_region')
   accepted=not reasons
   target=100*(candidate[0]-10)+10*(candidate[1]-9)+candidate[2]-9 if accepted else None
   expected={'incoming':t,'p_prefix':[a,p,z], 'low_carry_into_p2':carry[2],
    'high_carry_into_p1':carry[5],'high_carry_into_p0':carry[6],
    'second_overflow':overflow,'no_overflow_candidate':candidate,
    'accepted':accepted,'rejection_reasons':reasons,'target':target}
   assert saved==expected,(idx,t,saved,expected)
   if not overflow:assert pair_step(word)[:3]==candidate
   controls.append({'source':idx,'incoming':t,'literal_word':word,'integer':n,
    'fixed_width_digits':digits,'actual_carries':carry,'accepted':accepted,'target':target})
   if accepted:predecessors[target].append(idx);outdegree[idx]+=1
 ranks=[0]*len(rows);queue=deque(i for i,x in enumerate(outdegree) if x==0);order=[]
 while queue:
  v=queue.popleft();order.append(v)
  for u in predecessors[v]:
   ranks[u]=max(ranks[u],ranks[v]+1);outdegree[u]-=1
   if outdegree[u]==0:queue.append(u)
 assert len(order)==900 and not any(outdegree)
 assert ranks==[r['rank'] for r in rows]
 assert Counter(ranks)=={0:760,1:123,2:14,3:3}
 output={'controls':controls,'sink_deletion_order':order,'ranks':ranks}
 packed=gzip.compress((json.dumps(output,separators=(',',':'))+'\n').encode(),mtime=0)
 (HERE/'independent_prefix_controls.json.gz').write_bytes(packed)
 report={'result':'PASS_INDEPENDENT_LITERAL_PREFIX_AND_DAG_AUDIT','vertices':900,
  'all_controls':len(controls),'accepted_edges':sum(c['accepted'] for c in controls),
  'rank_counts':dict(sorted(Counter(ranks).items())),'max_path_edges':max(ranks),
  'method':'Exact integer evaluation of seven-coefficient symmetric test words with a forced central carry; independently computed sink-deletion DAG ranks. No producer import.',
  'scope':'Audits the complete necessary no-overflow graph; neutral-overflow exclusion and actual-orbit projection are separate written proofs. Abstract edges need not arise from high-region words.',
  'pins':{'producer':sha((HERE/'build_prefix_certificate.py').read_bytes()),'certificate_gzip':sha(compressed),'certificate_recovered':sha(raw),'producer_report':sha((HERE/'prefix_verification.json').read_bytes()),'independent_source':sha(Path(__file__).read_bytes()),'independent_controls_gzip':sha(packed)}}
 (HERE/'independent_prefix_audit.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()
