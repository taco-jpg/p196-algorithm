#!/usr/bin/env python3
"""Full-horizon 6000-step positive two-front propagation law and collision detector."""
import csv,sys
P=sys.argv[1]
rows=[{k:int(v) for k,v in r.items()} for r in csv.DictReader(open(P),delimiter='\t')]
assert len(rows)==6001 and all(r['time']==i for i,r in enumerate(rows))
def periodic(field,shift,first,last):
    bad=[t for t in range(first,last+1) if rows[t+22][field]-rows[t][field] != shift]
    assert not bad,(field,bad[:10])
    return last-first+1
n1=periodic('min',-5,18,5978)
n2=periodic('max',15,10,3405)
n3=periodic('center_front',-5,52,5978)
collision=next(x['time'] for x in rows if x['center_front']>=0 and x['max']>=x['center_front'])
assert collision==3426,collision
anchor=3300
first_deviation=next(t for t in range(anchor,6001) if rows[t]['max']!=
   rows[anchor+(t-anchor)%22]['max']+15*((t-anchor)//22))
assert first_deviation==3428,first_deviation
assert rows[3426]['max']==4434 and rows[3426]['center_front']==4433
for t in range(0,6001):
    assert rows[t]['min']>=0 and rows[t]['max']>=0 and rows[t]['count']>0
key=[0,1,10,18,52,100,200,800,2000,3300,3400,3425,3426,3427,3428,3500,4000,6000]
with open(sys.argv[2],'w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader()
    for t in key:w.writerow(rows[t])
print(f'PULSE_COLLISION_PASS low22={n1} inner22={n2} centre22={n3} '
    f'collision={collision} inner_first_break={first_deviation} '
    f'final_n={rows[-1]["length"]}')
