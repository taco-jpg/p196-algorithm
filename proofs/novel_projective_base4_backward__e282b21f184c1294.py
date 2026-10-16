"""Exact bounded exploration of spatial predecessors of non-neutral 3/6 bulk.
Graph closure and target reachability are separate from a complete family proof.
"""
import json
from continuation_theory_multigrowth import backwards,transitions

def target_for(periods,d0):
    d=d0;ls=[];cs=[]
    for p in periods:
        ls.append(d);bits=0
        for i in range(p):
            c=int(d>=5);bits|=c<<i;d=2*d-9*c
        cs.append(bits)
    assert d==d0
    return (tuple(ls),tuple(cs),tuple(cs))

def periods_of(clock):
    out=[];n=0
    for i,a in enumerate(clock):
        n+=1
        if a>=10 or (a==9 and clock[(i+1)%len(clock)]==10):out.append(n);n=0
    assert n==0
    return out

if __name__=='__main__':
    src=json.load(open('novel_projective_period18_clocks.json'))
    clocks=[r['clock'] for r in src['results'] if r['checks'][-1]['live']]
    results=[]
    for ci,clock in enumerate(clocks):
        ps=periods_of(clock)
        for d in (3,6):
            target=target_for(ps,d)
            assert any(s==target for s,dp in transitions(10,ps,target))
            r=backwards(10,ps,target,maxstates=50000,seconds=20)
            r['clock_index']=ci;r['bulk_digit']=d;r['target']=target
            print(json.dumps(r),flush=True);results.append(r)
            open('novel_projective_base4_backward_results.json','w').write(json.dumps(results,indent=2))
