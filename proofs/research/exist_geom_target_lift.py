"""Lift centered q-bulk cycles to exact digit/carry targets for the E graph."""
import json
from pathlib import Path
from exist_geom_periodic_bulk_graph import carries


def lift(c,component=None):
    p=c['period'];r=len(c['bulk'][0])
    # Start immediately after an O, so each maximal segment ends in O.
    shift=next((i+1)%p for i,h in enumerate(c['clock']) if h)
    qs=c['bulk'][shift:]+c['bulk'][:shift]
    hs=c['clock'][shift:]+c['clock'][:shift]
    assert hs[-1]==1
    L=[];R=[];AB=[]
    for t in range(p):
        prev=(t-1)%p;a,b=carries(qs[prev]);h=hs[prev]
        lo=[(qs[prev][i]+a[i])%10 for i in range(r)]
        hi=[(qs[prev][(i-h)%r]+b[(i-h+1)%r])%10 for i in range(r)]
        assert [x+y for x,y in zip(lo,hi)]==list(qs[t])
        L.append(hi);R.append(lo);AB.append(carries(qs[t]))
    starts=[];periods=[];start=0
    for t,h in enumerate(hs):
        if h:starts.append(start);periods.append(t-start+1);start=t+1
    states=[]
    for i in range(r):
        ls=tuple(L[t][i] for t in starts)
        lc=tuple(sum(AB[t+j][1][i]<<j for j in range(le)) for t,le in zip(starts,periods))
        rc=tuple(sum(AB[t+j][0][i]<<j for j in range(le)) for t,le in zip(starts,periods))
        states.append((ls,lc,rc))
    for t in range(p):
        for i in range(r):
            total=L[t][i]+R[t][i]
            low=total+AB[t][0][i]
            high=total+AB[t][1][(i+1)%r]
            assert low//10==AB[t][0][(i+1)%r]
            assert high//10==AB[t][1][i]
            assert low%10==R[(t+1)%p][i]
            assert high%10==L[(t+1)%p][(i+hs[t])%r]
    return {'component':component,'period':p,'growth':c['growth'],
            'spatial_period':r,'periods':periods,'clock':hs,'q':qs,
            'L':L,'R':R,'states':states,'arithmetic_edges_checked':p*r,
            'origin_rotation':shift}


if __name__=='__main__':
    data=json.load(open('exist_geom_bulk_two_outer_results.json'))
    targets=[lift(data['positive_components'][i]['cycles'][0],i)
             for i in [0,16,21,24]]
    Path('exist_geom_two_outer_targets.json').write_text(json.dumps(targets,indent=2)+'\n')
    print(json.dumps([{'component':x['component'],'periods':x['periods'],
                       'checked':x['arithmetic_edges_checked']} for x in targets]))
