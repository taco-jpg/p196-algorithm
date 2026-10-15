import sys, json, os
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'review-agent101-cap56'))
from outer_ref import outer
def path(c,B,cap):
    P=[(c,tuple(B))]
    while True:
        c2,Bp,g=outer(c,list(B))
        if len(Bp)>cap: P.append(("EXIT",len(Bp),g)); return P
        c,B=c2,Bp; P.append((c,tuple(B)))
        assert len(P)<1000
out={}
for c,B in [(4,(3,16,8,15,0)),(4,(3,18,13,17,0)),(4,(3,18,13,14,15,1)),(8,(7,17,8,10,15,13,3))]:
    P=path(c,B,7); out[f"{c}:{B}"]=dict(steps=len(P)-1,path=[str(x) for x in P])
    print(c,B,"exit time",len(P)-1)
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'sharp_paths_cap7.json'),'w'),indent=1)
