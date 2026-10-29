#!/usr/bin/env python3
"""Restricted Agent10 canonical e=01 neutral-root diagnostic.
NOT a census of arbitrary overflow schedules or centre formats.
"""
from collections import deque
def edges(b,st,root):
    L,H,y=st
    l0,l1=L&1,L>>1;h0,h1=H&1,H>>1
    for c0 in (0,1):
        x0=b*(1+h0)-(l0+l1+c0+y)
        if not (int(st==root)<=x0<=2*b-2 and (x0+c0)//b==h0):continue
        x1=(x0+l0)%b+(x0+c0)%b
        if not (0<=x1<=2*b-2 and (x1+l1)%b+y==x0):continue
        a,e=(x0+l0)//b,(x1+l1)//b
        if a+e!=1:continue
        for c1 in (0,1):
            if (x1+c1)//b!=h1:continue
            yield (a+2*e,c0+2*c1,(x1+c1)%b)
def reachable(b):
    root=(0,2,1);goal=(2,1,b-1);queue=deque([root]);parents={root:None}
    while queue:
        st=queue.popleft()
        for dst in edges(b,st,root):
            if dst in parents:continue
            parents[dst]=st
            if dst==goal:
                depth=0
                while dst!=root:dst=parents[dst];depth+=1
                return len(parents),depth
            queue.append(dst)
    return len(parents),None
if __name__=='__main__':
    expected={50:(141,36),146:(318,80),1286:(4813,1204),100:(85,None),1000:(293,None)}
    for b,(states,depth) in expected.items():
        s,d=reachable(b)
        assert (s,d)==(states,depth),(b,s,d)
        print('base',b,'reachable states',s,'canonical neutral root depth',d)
    print('PASS restricted positive controls and exact base100/base1000 non-root diagnosis')
