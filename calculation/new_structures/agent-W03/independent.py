#!/usr/bin/env python3
"""Independent genuine Python bigint oracle, all possible insertion indices."""
import csv,random,sys
sys.set_int_max_str_digits(0)
def groups(n):
 s=str(n)
 return [int(s[max(i-2,0):i]) for i in range(len(s),0,-2)]
def insertion(x,y):
 return any(y[:p]==x[:p] and y[p:p+1]==[99] and y[p+1:]==x[p:] for p in range(len(x)+1))
def replay(q,first0,repair0):
 a=int('12'+'99'*q+'34');b=int('12'+'99'*(q+1)+'34')
 first=None;repairs=[]
 for t in range(first0+81):
  ok=insertion(groups(a),groups(b))
  if t==0:assert ok
  if first is None and not ok:first=t
  if first is not None and t>first and ok:repairs.append(t)
  assert str(a)!=str(a)[::-1] and str(b)!=str(b)[::-1],(q,t)
  a+=int(str(a)[::-1]);b+=int(str(b)[::-1])
 assert first==first0,(q,first,first0)
 assert repairs==repair0,(q,repairs,repair0)
def main(table,events):
 rows=list(csv.DictReader(open(table)))
 assert len(rows)==436
 positives=[r for r in rows if int(r['repair_count'])>0]
 negatives=[r for r in rows if not int(r['repair_count'])]
 assert len(positives)==17 and sum(int(r['repair_count']) for r in rows)==21
 assert max(int(r['max_repair_run']) for r in rows)==3
 assert [(r['Q'],r['first'],r['repair_times'],r['first_old'],r['first_new']) for r in positives]==[(r['Q'],r['first'],r['repair_times'],r['first_old'],r['first_new']) for r in csv.DictReader(open(events))]
 for r in positives+random.Random(20261028).sample(negatives,24):
  replay(int(r['Q']),int(r['first']),[int(t) for t in r['repair_times'].split(':') if t])
 r=next(x for x in positives if x['Q']=='21')
 try:replay(21,70,[75,70])
 except AssertionError:pass
 else:raise AssertionError('mutation control failed')
 print('PASS: 436 Q scanned, 17 repaired Q, 21 restored states, 41 independent bigint controls, mutation rejected')
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
