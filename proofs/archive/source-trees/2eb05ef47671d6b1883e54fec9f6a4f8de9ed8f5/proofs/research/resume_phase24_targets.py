import json
from family_search_bulk_periods import bulk_step
from continuation_theory_multigrowth import transitions, predecessors

def target_states(B):
    bs=[];b=tuple(B)
    for t in range(24):bs.append(b);b=next(iter(bulk_step(b,1-t%2)))
    assert b==tuple(B)
    def incoming(t,i,d):
        b=bs[t%24]
        q=next(b[(i+d*k)%3]for k in range(1,4) if b[(i+d*k)%3]!=9)
        return int(q>=10)
    def out(t,i,d):
        q=bs[t%24][i%3]
        return (q+incoming(t,i,d))//10
    states=[]
    for i in range(3):
        ls=[];lcs=[];rcs=[]
        for j in range(12):
            t=1+2*j
            ls.append((bs[(t-1)%24][(i-1)%3]+incoming(t-1,i-1,1))%10)
            lc=rc=0
            for h in range(2):
                lc|=out(t+h,i,1)<<h
                rc|=incoming(t+h,i,-1)<<h
            lcs.append(lc);rcs.append(rc)
        states.append((tuple(ls),tuple(lcs),tuple(rcs)))
    return states

if __name__=='__main__':
    src=json.load(open('carry_invariant_research_centers_results.json'))
    blocks=sorted({tuple(r['block'])for r in src if r['schedule'][0]==1 and sum(r['block'])%9==0})
    for B in blocks:
        st=target_states(B)
        for i in range(3):
            nxt=list(transitions(10,[2]*12,st[i]))
            assert st[(i+1)%3] in [x[0]for x in nxt],(B,i,st,nxt)
        print(B, [len(list(predecessors(10,[2]*12,s)))for s in st],flush=True)
