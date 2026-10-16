"""Exact universal-prefix test for a disturbance front entering bulk A.
No inferred cycle is accepted without branching over every incoming right carry.
"""
from resume_defect_interface import strip_step
from family_search_bulk_periods import bulk_step
import json,time
A=(3,10,15,8)

def update_prefix(q,bulk,origin,h,incoming):
    padding=tuple(bulk[i%4]for i in range(origin-4,origin))
    data=padding+q;start=origin-4
    c=int(bulk[(start-1)%4]>=10);lo=[]
    for x in data:v=x+c;lo.append(v%10);c=v//10
    c=incoming;hi=[]
    for x in data[::-1]:v=x+c;hi.append(v%10);c=v//10
    hi=hi[::-1]
    out=tuple(lo[i]+hi[i-h]for i in range(h,len(data)))
    nb=next(iter(bulk_step(bulk,h)));neworigin=start+h
    a=0
    while a<len(out) and out[a]==nb[(neworigin+a)%4]:a+=1
    return out[a:],nb,neworigin+a

def sample_candidates(rotation=0,steps=600,width=4):
    left=A[rotation:]+A[:rotation];right=(6,);L=1000
    q=left*(L//4)+right*1800;origin=0;seen={};hits={}
    for t in range(steps+1):
        a=0
        while a<len(q) and q[a]==left[(origin+a)%4]:a+=1
        assert a>=30 and a+width<len(q)-30
        pos=origin+a;profile=q[a:a+width];key=(t%4,pos%4,profile)
        if key in seen:
            tt,oldpos=seen[key];p=t-tt;shift=pos-oldpos
            if shift<0 and p<=96:
                hits[(p,shift,t%4,pos%4,profile)]={'period':p,'shift':shift,'phase':t%4,'origin':pos%4,'profile':profile,'bulk':left,'time':t,'earlier':tt,'width':width,'rotation':rotation}
        seen[key]=(t,pos)
        q,left,right,origin=strip_step(q,left,right,origin,t%2)
    return sorted(hits.values(),key=lambda r:(r['period'],r['time']))

def certify(hit,cap=20000,seconds=20):
    prof=hit['profile'];w=len(prof);bulk=hit['bulk'];origin=hit['origin'];phase=hit['phase'];ts=time.monotonic()
    states={(prof,bulk,origin)};maxstates=1
    for t in range(hit['period']):
        nxt=set()
        for q,b,o in states:
            for c in [0,1]:
                qq,bb,oo=update_prefix(q,b,o,(phase+t)%2,c)
                # Keep a fixed extra causal buffer while allowing net profile growth.
                if len(qq)>w+8:qq=qq[:w+8]
                if not qq:return {'status':'failed','reason':'known window erased','step':t+1}
                nxt.add((qq,bb,oo))
        states=nxt;maxstates=max(maxstates,len(states))
        if maxstates>cap or time.monotonic()-ts>seconds:return {'status':'unknown','step':t+1,'states':len(states),'maxstates':maxstates}
    bad=[(q,b,o)for q,b,o in states if len(q)<w or q[:w]!=prof or b!=bulk or o-origin!=hit['shift']]
    return {'status':'passed' if not bad else 'failed','terminal_states':len(states),'maxstates':maxstates,'counterexamples':bad[:2],'seconds':time.monotonic()-ts}

if __name__=='__main__':
    out=[]
    for width in [3,4,6,8,12]:
        hits=sample_candidates(width=width)
        print(json.dumps({'width':width,'candidates':len(hits),'periods':sorted({r['period']for r in hits})}),flush=True)
        for hit in hits[:3]:
            hit['certificate']=certify(hit);out.append(hit);print(json.dumps(hit),flush=True)
            if hit['certificate']['status']=='passed':break
        if out and out[-1]['certificate']['status']=='passed':break
    open('resume_history_search_backfront_results.json','w').write(json.dumps(out,indent=2))
