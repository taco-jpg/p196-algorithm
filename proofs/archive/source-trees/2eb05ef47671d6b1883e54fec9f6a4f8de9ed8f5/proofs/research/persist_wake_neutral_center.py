"""Independent numeric validation of the 11-step neutral exterior candidate."""
from itertools import product
from resume_front_collision import numeric_q_step,representative
import json,time

record=next(r for r in json.load(open('persist_block_neutral_timechange_results.json')) if r['periods']==[1,1,4,5])['accepted'][0]
PATH=record['path']
P=tuple(a+b for a,b in PATH)
CLOCK=(1,1,0,0,0,1,0,0,0,0,1)

def step11(q):
    flags=[]
    for _ in range(11):q,h=numeric_q_step(q);flags.append(h)
    return q,tuple(flags)

def candidate(core,m=8):
    left=P+(9,)*m
    return left+tuple(core)+left[::-1]

def check(core,m=8):
    q=candidate(core,m);out,flags=step11(q)
    if flags!=CLOCK:return False,'clock',None
    target=candidate(core,m+2)
    if out==target:return True,'full',out
    j=0
    while j<min(len(out),len(target)) and out[j]==target[j]:j+=1
    return False,'prefix',j

def search(maxpairs=3):
    stats={};found=[];best=[]
    for pairs in range(maxpairs+1):
        ct=clock=0;preserved=0;maxprefix=0
        for half in product(range(19),repeat=pairs):
            for middle in [()]+[(x,)for x in range(0,19,2)]:
                core=half+middle+half[::-1];ct+=1
                ok,kind,extra=check(core)
                if kind!='clock':clock+=1
                if kind=='prefix':
                    maxprefix=max(maxprefix,extra)
                    if extra>=len(P):preserved+=1
                if ok:
                    found.append(core);print('FOUND',core,flush=True)
                    for m in (0,1,3,20):assert check(core,m)[0]
        stats[pairs]={'cores':ct,'clock_matches':clock,'exterior_preserved':preserved,'max_prefix':maxprefix}
        print(pairs,stats[pairs],flush=True)
    return dict(stats=stats,found=found,clock=CLOCK,exterior_pair_sum=P)

if __name__=='__main__':
    start=time.monotonic();result=search(3);result['seconds']=time.monotonic()-start
    open('persist_wake_neutral_center_results.json','w').write(json.dumps(result,indent=2))
