#!/usr/bin/env python3
"""W02: exact finite 40k diagonal-front and nested pulse-timing fixture checker."""
import json,collections,sys
assert len(sys.argv)==2
with open(sys.argv[1]) as f:
    names=f.readline().split()
    data=[dict(zip(names,map(int,line.split()))) for line in f]
assert len(data)==40001 and data[0]['len']==100000 and data[-1]['len']==110000
for symbol,first in (('A',337),('B',155)):
    assert all(data[t+76][symbol+'right']-data[t][symbol+'right']==33 for t in range(first,39925))
def clusters(indices):
    ans=[]
    for t in indices:
        if ans and ans[-1][-1]+1==t:ans[-1].append(t)
        else:ans.append([t])
    return ans
def get(sym):return clusters(t for t in range(500,39925) if data[t+76][sym+'pen']!=data[t][sym+'pen'])
a,b=get('A'),get('B')
assert len(a)==38 and all(len(q)==3 and q[0]%76==30 for q in a)
assert all(a[i+1][0]-a[i][0]==76 for i in range(0,len(a),2))
assert len(b)==70 and collections.Counter(map(len,b))=={3:64,4:6}
starts=[941,18573,39093];offs=[0,5,53,76,81,129];lens=[3,4,3,3,4,3]
for s in starts:
    matching=[q for q in b if q[0] in [s+x for x in offs]]
    assert [q[0] for q in matching]==[s+x for x in offs]
    assert [len(q) for q in matching]==lens
assert [starts[1]-starts[0],starts[2]-starts[1]]==[17632,20520]
exclude={s+x for s in starts for x in offs}
regular=[q for q in b if q[0] not in exclude]
assert len(regular)==52 and all(len(q)==3 and q[0]%76==6 for q in regular)
assert all(regular[i+1][0]-regular[i][0]==76 for i in range(0,len(regular),2))
print(json.dumps({'label':'COMPUTED','time_horizon':40000,'ordinary_seed_digits':100000,'A_three_step_pairs':19,'B_regular_three_step_pairs':26,'B_special_six_cluster_starts':starts,'intervals':[17632,20520],'interval_increment':2888,'B_four_step_pulses':6,'trace_states':len(data)},sort_keys=True))
