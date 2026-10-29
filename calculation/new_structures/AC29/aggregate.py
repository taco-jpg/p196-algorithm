#!/usr/bin/env python3
"""Aggregate 13 disjoint per-J-code C++ windows; require full coverage."""
import sys,collections,json
lines=open(sys.argv[1]).read().splitlines();c=collections.Counter();hist=collections.Counter();blocks=0
for line in lines:
 a=line.split()
 if a[0]=="tested":
  blocks+=1
  for i in (0,2,4,6):c[a[i]]+=int(a[i+1])
 elif len(a)==2:hist[int(a[0])]+=int(a[1])
assert blocks==13 and c["tested"]+c["skipped_allwidth_mod11"]==30*19**5
assert c["tested"]==sum(hist.values())
result={"tested":c["tested"],"pruned":c["skipped_allwidth_mod11"],"returns":c["returns"],"clock_bad":c["clockbad"],"hist":dict(sorted(hist.items()))}
assert result["tested"]==450214 and result["pruned"]==73832756
print(json.dumps(result,sort_keys=True))
