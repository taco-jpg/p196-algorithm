"""Allow the neutral-exterior center to grow, instead of imposing a return period."""
from persist_wake_neutral_center import *

def grow(core,m=8):
    out,flags=step11(candidate(core,m));left=P+(9,)*m;w=len(left)
    if flags!=CLOCK or out[:w]!=left or out[-w:]!=left[::-1]:return None
    assert len(out)==2*w+len(core)+4
    return out[w:-w]

def search(maxpairs=3,iterations=100):
    best=[];hist={};record=0;count=0
    for pairs in range(maxpairs+1):
        for half in product(range(19),repeat=pairs):
            for middle in [()]+[(x,)for x in range(0,19,2)]:
                core=half+middle+half[::-1];q=core;count+=1
                for t in range(iterations):
                    oq=grow(q)
                    if oq is None:break
                    q=oq
                else:t=iterations
                hist[t]=hist.get(t,0)+1
                if t>record:
                    record=t;print('record',record,core,flush=True);best=[dict(seed=core,returns=t,final=q)]
                elif t==record and t>0:best.append(dict(seed=core,returns=t,final=q))
        print('pairs',pairs,'count',count,'best',record,flush=True)
    return dict(count=count,best=best,histogram=hist,iterations=iterations)

if __name__=='__main__':
 result=search(3,100)
 open('persist_wake_neutral_growth_results.json','w').write(json.dumps(result,indent=2))
