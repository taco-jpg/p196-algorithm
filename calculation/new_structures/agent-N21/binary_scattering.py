#!/usr/bin/env python3
"""N21: noncommutative packet scattering on the decimal p12/m9 bulk.
Exact pairword arithmetic. Nine symbol pairs; no infinite-orbit claim.
"""
import json
from packet_train import background,pair_step
ANCHORS=(300,804)
K={
 'A':(6,1,0,1,11,14,10,6,11,16,1),
 'B':(16,0,9,11,1,10,8,5,14,18,0),
 'C':(16,0,9,11,1,10,8,8,9,16,0)
}
EXPECTED={'AA':820,'AB':840,'BA':801,'BB':825,'AC':832,'CA':801,'BC':817,'CB':825,'CC':817}

def insert_symbols(root,items):
    p=root.copy();n=len(p)
    for site,sym in items:
        for j,v in enumerate(K[sym]):p[site+j]=p[n-1-site-j]=v
    return p

def run():
    root=background()
    singles={('L',sym):insert_symbols(root,((ANCHORS[0],sym),)) for sym in K}
    singles.update({('R',sym):insert_symbols(root,((ANCHORS[1],sym),)) for sym in K})
    combined={sy:insert_symbols(root,((ANCHORS[0],sy[0]),(ANCHORS[1],sy[1]))) for sy in EXPECTED}
    found={}
    for t in range(851):
        n=len(root); h=n//2
        for sy,pair in list(combined.items()):
            left=singles['L',sy[0]];right=singles['R',sy[1]]
            assert len(left)==len(right)==len(pair)==n,('length',t,sy)
            bad=[i for i in range(h) if left[i]+right[i]-root[i]!=pair[i]]
            if bad:
                found[sy]={'symbols':sy,'step':t,'first_position':bad[0],'nonlinear_count':len(bad)}
                del combined[sy]
        if not combined:break
        if t==850:raise AssertionError(('no collision',list(combined)))
        root=pair_step(root)
        singles={k:pair_step(p) for k,p in singles.items()}
        combined={k:pair_step(p) for k,p in combined.items()}
    for sy,expect in EXPECTED.items():
        row=found[sy]
        assert row['step']==expect,(row,expect)
        print(json.dumps(row,separators=(',',':')))
    assert found['AB']['step']-found['BA']['step']==39
    print('ORDERED_SCATTER_PASS nine pairs, AB delay over BA = 39 steps')
if __name__=='__main__':run()
