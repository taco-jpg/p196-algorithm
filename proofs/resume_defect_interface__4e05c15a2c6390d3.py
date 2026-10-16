"""Search exact travelling interfaces between known periodic q bulks.
Neither a local interface nor periodic bulk alone is a finite Lychrel seed.
"""
from itertools import product
import json,time
from family_search_bulk_periods import bulk_step
from resume_defect_center import BASE


def strip_step(q,left,right,origin,h):
    carry=int(left[(origin-1)%len(left)]>=10)
    lo=[]
    for x in q:
        v=x+carry;lo.append(v%10);carry=v//10
    carry=int(right[(origin+len(q))%len(right)]>=10)
    hi=[]
    for x in reversed(q):
        v=x+carry;hi.append(v%10);carry=v//10
    hi.reverse()
    out=tuple(lo[i]+hi[i-h] for i in range(1,len(q)-1))
    return out,next(iter(bulk_step(left,h))),next(iter(bulk_step(right,h))),origin+1


def travels(core,left,right,steps=16,shift=4):
    assert len(right)==1
    q=left*10+core+right*40
    initial=q;origin=0
    for t in range(steps):q,left,right,origin=strip_step(q,left,right,origin,t%2)
    return q==initial[steps-shift:len(initial)-steps-shift]


def search(maxlen=2):
    results=[]
    for rot in range(4):
        left=BASE[rot:]+BASE[:rot]
        for c in (6,12):
            for n in range(maxlen+1):
                t=time.monotonic();hits=[];count=0
                for core in product(range(19),repeat=n):
                    count+=1
                    if travels(core,left,(c,)):hits.append(core)
                r=dict(left=left,right=c,width=n,tested=count,hits=hits,
                       seconds=round(time.monotonic()-t,3))
                print(json.dumps(r),flush=True);results.append(r)
                if hits:break
    return results


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=2)
    a=ap.parse_args()
    open('resume_defect_interface_results.json','w').write(json.dumps(search(a.width),indent=2))
