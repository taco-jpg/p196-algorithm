from itertools import product
import json

def prefix_step(q,u):
    c=0;lo=[]
    for x in q:
        lo.append((x+c)%10);c=(x+c)//10
    c=u;hi=[]
    for x in reversed(q):
        hi.append((x+c)%10);c=(x+c)//10
    hi.reverse();h=c
    out=tuple(lo[i]+hi[i]for i in range(len(q))) if not h else (lo[0]+1,)+tuple(lo[i]+hi[i-1]for i in range(1,len(q)))
    return out,h

def analyze(qs,k):
    G={};p=len(qs)
    for t,a in enumerate(qs):
        for tail in product(range(19),repeat=k-1):
            s=(a,)+tail
            G[t,s]=set(((t+1)%p,z) for u in (0,1) for z,h in (prefix_step(s,u),) if z[0]==qs[(t+1)%p])
    alive=set(G);rounds=0
    while True:
        na={s for s in alive if G[s]&alive}
        if na==alive:break
        alive=na;rounds+=1
    out={'outer_cycle':qs,'width':k,'states':len(G),'live':len(alive),'pruning_rounds':rounds}
    if len(alive)<30:out['live_states']=sorted(alive)
    return out

if __name__=='__main__':
    results=[]
    for qs in [(2,5,11),(3,6,12),(1,3,7,14,5,10)]:
        for k in (2,3,4):
            r=analyze(qs,k);results.append(r);print(json.dumps(r),flush=True)
            if not r['live']:break
    open('novel_projective_clock_results.json','w').write(json.dumps(results,indent=2))
