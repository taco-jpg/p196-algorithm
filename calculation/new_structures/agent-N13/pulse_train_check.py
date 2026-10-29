#!/usr/bin/env python3
"""Full-horizon pulse-pulse interaction milestones, no exhaustive no-go conclusion."""
import csv,sys
r=[{k:int(v) for k,v in row.items()} for row in csv.DictReader(open(sys.argv[1]),delimiter='\t')]
assert len(r)==4001 and all(x['time']==i for i,x in enumerate(r))
first=lambda key: next(x['time'] for x in r if x[key]>0)
assert first('overlap')==836
assert first('nonlinear')==841
assert first('unexpected')==858
assert r[858]['umin']==r[858]['umax']==2415
assert all(x['overlap']==0 and x['nonlinear']==0 and x['unexpected']==0 for x in r[:836])
assert all(x['nonlinear']==0 and x['unexpected']==0 for x in r[:841])
assert all(x['unexpected']==0 for x in r[:858])
assert all(x['alllen']==10400+(x['time']+1)//2 for x in r)
for t in [858,900,1100,2000,3000,4000]:assert r[t]['lo1']<r[t]['hi1']<r[t]['hi2']
KEYS=[0,1,10,100,500,800,825,835,836,837,840,841,842,850,857,858,859,880,900,1000,1100,1500,2000,3000,4000]
with open(sys.argv[2],'w',newline='') as fh:
 w=csv.DictWriter(fh,fieldnames=r[0].keys(),lineterminator='\n');w.writeheader()
 for t in KEYS:w.writerow(r[t])
print('BIPOLAR_TWO_PULSE_SCATTERING_PASS first_overlap=836 first_exclusive_nonlin=841 first_outside_support=858 at_j2415')
