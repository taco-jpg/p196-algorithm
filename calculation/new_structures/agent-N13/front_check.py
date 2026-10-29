#!/usr/bin/env python3
"""Independent check of the measured first-disagreement-front recurrence.
No arithmetic recurrence is fitted: the law is checked at every eligible t.
"""
import sys
path=sys.argv[1]
vals=[]
with open(path) as f:
    for i,line in enumerate(f):
        t,p=map(int,line.split());assert t==i
        vals.append(p)
assert len(vals)==20001,len(vals)
assert vals[0]==5100 and vals[20000]==556
for t in range(18,20001-22):
    assert vals[t+22]==vals[t]-5,(t,vals[t],vals[t+22])
for t in range(18,20001-88):
    assert vals[t+88]==vals[t]-20,(t,vals[t],vals[t+88])
bad=[t for t in range(0,20001-22) if vals[t+22]!=vals[t]-5]
assert bad==[0,1,2,3,10,11,14,15,16,17],bad
print('FRONT_PHASE_22_TRANSLATION_20000_PASS; first failure list:',bad)
