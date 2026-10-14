"""Exact finite defects in the uniform-six bulk under a prescribed N/O clock."""
from resume_front_collision import local_step
from collections import Counter
import json


def trim(q, background=6):
    q=tuple(q)
    left=0
    while left<len(q) and q[left]==background:left+=1
    if left==len(q):return ()
    right=len(q)
    while right>left and q[right-1]==background:right-=1
    return q[left:right]


def pair(q):
    # Padding absorbs the exact radius. The all-12 incoming carry is one.
    q=(6,)*4+tuple(q)+(6,)*4
    q=local_step(q,0,0)
    q=local_step(q,1,1)
    assert q[:2]==(6,6) and q[-2:]==(6,6)
    return trim(q)


def macro(q):
    for _ in range(3):q=pair(q)
    return q


def runs(q):
    out=[]
    for x in q:
        if out and out[-1][0]==x:out[-1][1]+=1
        else:out.append([x,1])
    return out


def orbit(q,n=200):
    seen={};trace=[]
    for t in range(n+1):
        q=trim(q)
        if q in seen:return {'transient':seen[q],'period':t-seen[q],'trace':trace}
        seen[q]=t
        trace.append({'t':t,'width':len(q),'q':q})
        q=macro(q)
    return {'transient':None,'period':None,'trace':trace}

if __name__=='__main__':
    data={}
    for m in range(31):
        result=orbit((8,)+(6,)*m+(8,),200)
        data[m]=result
        print(m,result['transient'],result['period'],[r['width'] for r in result['trace'][:12]],'last',result['trace'][-1]['width'],flush=True)
    open('persist_wake_dynamics_results.json','w').write(json.dumps(data))
