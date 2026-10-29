#!/usr/bin/env python3
"""W02 complete finite-horizon 20k frontier and second-site pulse grammar checker."""
import sys,collections,json
assert len(sys.argv)==2
with open(sys.argv[1]) as f:
    header=f.readline().split()
    data=[dict(zip(header,map(int,line.split()))) for line in f]
assert len(data)==20001 and data[0]['step']==0 and data[-1]['step']==20000
assert data[0]['len']==50000 and data[-1]['len']==55000
for tag,threshold in (('A',337),('B',155)):
    edge=tag+'right'
    for t in range(threshold,20001-76):
        assert data[t+76][edge]-data[t][edge]==33,(tag,t)
def blocks(v):
    out=[]
    for x in v:
        if not out or x!=out[-1][-1]+1:out.append([x])
        else:out[-1].append(x)
    return out
def errors(tag):
    return [t for t in range(500,20001-76) if data[t+76][tag+'pen']!=data[t][tag+'pen']]
a=blocks(errors('A')); b=blocks(errors('B'))
a_starts=[4514,4590,5578,5654,5958,6034,7630,7706,8086,8162,10746,10822,11278,11354,12570,12646,12950,13026,14546,14622]
assert [g[0] for g in a]==a_starts
assert len(a)==20 and all(len(g)==3 and g[0]%76==30 for g in a)
assert all(a[i+1][0]-a[i][0]==76 for i in range(0,len(a),2))
assert len(b)==42 and collections.Counter(map(len,b))=={3:38,4:4}
b_starts=[g[0] for g in b]
special=[941,946,994,1017,1022,1070]
assert [v for v in b_starts if v%76 !=6]==[941,946,1017,1022,18573,18578,18649,18654]
for origin in (0,17632):
    ep=[g for g in b if g[0] in [x+origin for x in special]]
    assert [g[0] for g in ep]==[x+origin for x in special]
    assert [len(g) for g in ep]==[3,4,3,3,4,3]
remaining=[g for g in b if g[0] not in [x+origin for origin in (0,17632) for x in special]]
assert len(remaining)==30 and all(len(g)==3 and g[0]%76==6 for g in remaining)
assert all(remaining[i+1][0]-remaining[i][0]==76 for i in range(0,len(remaining),2))
print(json.dumps({'status':'COMPUTED','checked_states':60003,'A_pulses':len(a),'A_three_step_pairs':10,'B_pulses':len(b),'B_regular_pairs':15,'B_special_episodes':[941,18573],'B_special_episode_delay':17632,'front_period':76,'front_shift':33,'last_time':20000},sort_keys=True))
