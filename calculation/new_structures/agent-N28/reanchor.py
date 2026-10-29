#!/usr/bin/env python3
"""N28 movable periodic cuts. Exact same-family reanchoring plus independent bigint replay."""
import argparse,json
from paired_pump import init,step_contract,expand,family,seed,digits,pairs

def reanchor(p,slots,words,j,radius=400):
    old=slots[j];m=len(words[j]);good=[]
    lo=max(old-radius,m+2,slots[j-1]+2*m if j else 0)
    hi=min(old+radius,len(p)//2-m-2,slots[j+1]-2*m if j+1<len(slots) else len(p)//2-m-2)
    for i in range(lo,hi):
        if i==old:continue
        a=min(old,i);b=max(old,i)
        # Exact cut-shift identity: all intervening positions have period m.
        if any(p[x]!=p[x+m] for x in range(a,b)):continue
        ss=slots[:];ss[j]=i
        ww=[w[:] for w in words];ww[j]=p[i:i+m]
        result,_=step_contract(p,ss,ww)
        if result is not None:good.append((i,ww,result))
    if not good:return None
    new,ww,result=good[len(good)//2]
    for count in (1,2,3):
        d=[0]*len(slots);d[j]=count
        ss=slots[:];ss[j]=new
        assert expand(p,slots,words,d)==expand(p,ss,ww,d)
    return new,ww,result,[good[0][0],good[-1][0]]

def run(k,limit,check):
    p,slots,words=init(k)
    changes=[(0,0,0),(1,0,0),(0,2,5),(7,11,13),(101,23,59)]
    values=[seed(family(tuple(k+x for x in delta))[0]) for delta in changes] if check else []
    events=[];checked=0;status='LIMIT'
    t=0
    while t<=limit:
        if check:
            for value,delta in zip(values,changes):
                d=digits(value)
                assert d!=d[::-1],('palindrome',t,delta)
                assert pairs(d)==expand(p,slots,words,delta),('pairword',t,delta)
                checked+=1
        if t==limit:break
        res,msg=step_contract(p,slots,words)
        if res is None:
            if ':j' not in msg:status=msg;break
            j=int(msg.split(':j')[1][0])
            repaired=reanchor(p,slots,words,j)
            if repaired is None:status=msg;break
            old=slots[j];new,words,res,span=repaired
            slots[j]=new
            events.append({'t':t,'j':j,'old':old,'new':new,'span':span,'first_failure':msg})
        q,words,g,anchor=res
        p=q;t+=1
        if check:values=[v+int(str(v)[::-1]) for v in values]
    return {'k':k,'certified_edges':t,'stop':status,'repairs':events,'final_slots':slots,'final_pairword_length':len(p),'independent_bigint_equalities':checked}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--k',type=int,default=240)
    ap.add_argument('--steps',type=int,default=1000)
    ap.add_argument('--check',action='store_true')
    a=ap.parse_args()
    print(json.dumps(run(a.k,a.steps,a.check),indent=2))
if __name__=='__main__':main()
