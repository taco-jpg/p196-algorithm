#!/usr/bin/env python3
"""Exact constructive generator of the base-1286 period-four neutral certificate.
No SAT library or external file required. Run from repo root:
  python3 calculation/neutral_band/agent10_base1286/generate.py --output /tmp/cert_b1286.json
The generated certificate must match the tracked cert_b1286.json byte-for-byte.
"""
import json, argparse, collections
BASE=1286
C0=[1607,1044,742,548,548,742,1044,1607]

def column_edges(st,first=False):
    L,H,y=st;l0,l1=L&1,L>>1;h0,h1=H&1,H>>1
    for c0 in (0,1):
        # Valid on all root-reachable states: a+e=1 (proved in reports/Agent10F2G01LinearDecision.md).
        x0=BASE*(1+h0)-(l0+l1+c0+y)
        if not (int(first)<=x0<=2*BASE-2 and (x0+c0)//BASE==h0):continue
        x1=(x0+l0)%BASE+(x0+c0)%BASE
        if not (0<=x1<=2*BASE-2 and (x1+l1)%BASE+y==x0):continue
        a,e=(x0+l0)//BASE,(x1+l1)//BASE
        if a+e!=1:continue
        for c1 in (0,1):
            if (x1+c1)//BASE!=h1:continue
            yield (a+2*e,c0+2*c1,(x1+c1)%BASE),(x0,x1,c0,c1)

def reach_exterior():
    root=(0,2,1); parents={root:None};queue=collections.deque([root]);target=None
    while queue:
        st=queue.popleft()
        for dst,col in column_edges(st,st==root):
            if dst in parents:continue
            parents[dst]=(st,col)
            if dst==(2,1,BASE-1):target=dst;break
            queue.append(dst)
        if target:break
    assert target is not None
    cols=[];x=target
    while x!=root:
        parent,col=parents[x]; cols.append(col);x=parent
    cols.reverse();return [c[0] for c in cols],[c[1] for c in cols]

def norm(word,carry):
    out=[]
    for p in word:
        v=p+carry;out.append(v%BASE);carry=v//BASE
    return out,carry

def advance(B,C):
    db,e=norm(B,0);dc,e2=norm(C,e);dr,g=norm(B[::-1],e2)
    assert e != e2
    if g:
        xb=[p+q for p,q in zip(db+[(BASE-1)*(1-e)],[1]+dr[::-1])]
        xc=[p+q for p,q in zip(dc+[(BASE-1)*(1-e2)],[(BASE-1)*(1-e2)]+dc[::-1])]
    else:
        xb=[p+q for p,q in zip(db,dr[::-1])]
        xc=[p+q for p,q in zip(dc,dc[::-1])]
    u=v=0
    while xb and xb[-1]==BASE-1:xb.pop();u+=1
    while len(xc)>=2 and xc[0]==BASE-1 and xc[-1]==BASE-1:xc=xc[1:-1];v+=1
    return xb,xc,e,e2,g,u,v

def make():
    B0,B1=reach_exterior()
    assert len(B0)==1204 and len(B1)==1204
    B,C=B0,C0
    edges=[]
    for t in range(4):
        bn,cn,e,e2,g,u,v=advance(B,C)
        edges.append(dict(B=B,C=C,B_next=bn,C_next=cn,e=e,e2=e2,gamma=g,u=u,v=v))
        B,C=bn,cn
    assert B==B0 and C==C0 and sum(x['u']+x['v']-x['gamma'] for x in edges)==1
    assert [(z['e'],z['e2'],z['gamma'],z['u'],z['v']) for z in edges]==[(0,1,0,1,0),(1,0,1,0,0),(0,1,0,1,1),(1,0,1,0,0)]
    return {'base':BASE,'label':'COMPUTED','width':len(B0),'centre_length':len(C0),'time_period':4,'initial_band':12,'cycle_band_gain':1,'edges':edges}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='cert_b1286.json');a=p.parse_args()
    data=make()
    with open(a.output,'w',encoding='utf8') as f:json.dump(data,f,indent=2);f.write('\n')
    print('PASS: generated four-edge base1286 cycle; width',data['width'],'band gain',data['cycle_band_gain'])
if __name__=='__main__':main()
