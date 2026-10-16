"""Independent ordinary-integer replay of saved universal-front cycles.

Imports no discovery or carry-transition code. Each edge is realized as a
finite symmetric q word, at two arbitrary-tail lengths; the general local
carry reset argument is written in STATUS.md. A cycle is a counterexample
within the arbitrary-wake abstraction, not a finite reverse-add orbit.
"""
from pathlib import Path
from functools import lru_cache
import json
HERE=Path(__file__).resolve().parent


def integer_image(q):
    assert q==q[::-1] and q[0]>0 and all(0<=x<=18 for x in q)
    d=[0]*len(q)
    for j in range(len(q)//2):
        d[-1-j]=min(9,q[j]);d[j]=q[j]-d[-1-j]
    if len(q)%2:assert q[len(q)//2]%2==0;d[len(q)//2]=q[len(q)//2]//2
    n=int(''.join(map(str,d[::-1])));s=str(n+int(str(n)[::-1]))[::-1]
    return tuple(int(s[j])+int(s[-1-j]) for j in range(len(s))),len(s)-len(q)


@lru_cache(None)
def bulk_image(b,h):
    p=len(b);half=(17 if h else 8,)+tuple(b[i%p] for i in range(1,8*p+3))
    q=half+(0,)+half[::-1];out,hh=integer_image(q);assert hh==h
    base=3*p
    nb=tuple(out[base+i] for i in range(p))
    assert all(out[i]==nb[i%p] for i in range(2*p,6*p))
    return nb


@lru_cache(None)
def bulk_trace(b,clock,period):
    bs=[];a=b
    for t in range(period):
        assert any(x!=9 for x in a)
        bs.append(a);a=bulk_image(a,clock[t%len(clock)])
    assert a==b
    return tuple(bs)


@lru_cache(None)
def replay_edge(b,nb,suffix,target_suffix,cut,ncut,h,delta,incoming,K):
    p=len(b);start=(cut-len(suffix))%p+2*p;start=max(start,2)
    prefix=(17 if h else 8,)+(0,)*(start-2)+(18 if incoming else 0,)
    cutactual=len(prefix)+len(suffix);assert cutactual%p==cut
    for m in (2,7):
        end=cutactual+(m+4)*p+4
        half=prefix+suffix+tuple(b[i%p] for i in range(cutactual,end))
        q=half+(4,)+half[::-1];out,hh=integer_image(q);assert hh==h
        newcut=cutactual+delta;assert newcut%p==ncut
        assert out[newcut-len(target_suffix):newcut]==target_suffix
        assert all(out[i]==nb[i%p] for i in range(newcut,newcut+2*p+2))
        # Reconstruct the discovery's canonical output end from a wholly
        # known numeric window, then crop its suffix to K.
        lower=start+h;last=end-2*p
        while last>lower and out[last-1]==nb[(last-1)%p]:last-=1
        assert last==newcut
        assert out[max(lower,last-K):last]==target_suffix
    return 2


def main():
    data=json.loads((HERE/'front_language_results.json').read_text());cycles=edges=checks=0
    for row in data['records']:
        if row['status']!='COMPLETE_LOCAL_GRAPH':continue
        assert row['bounded'] is False
        b=tuple(row['bulk']);clock=tuple(row['clock']);bs=bulk_trace(b,clock,row['temporal_period'])
        cycle=row['positive_cycle'];keys=row['positive_cycle_states'];assert len(cycle)==len(keys)
        weight=displacement=overflows=0
        for i,edge in enumerate(cycle):
            u,v,h,d,c=edge;assert v==cycle[(i+1)%len(cycle)][0]
            t,cut,suffix=keys[i];nt,ncut,target=keys[(i+1)%len(keys)]
            assert nt==(t+1)%len(bs) and h==clock[t%len(clock)]
            assert all(0<=x<=18 for x in suffix+target)
            checks+=replay_edge(bs[t],bs[nt],tuple(suffix),tuple(target),cut,ncut,h,d,c,row['K'])
            weight+=2*d-h;displacement+=d;overflows+=h;edges+=1
        assert weight==row['weight'] and weight>0
        assert displacement==row['displacement'] and overflows==row['overflows']
        cycles+=1
    out=dict(status='PASS',cycles=cycles,cycle_edges=edges,
             cycle_edge_parameter_checks_covered=checks,
             ordinary_integer_edge_checks=2*replay_edge.cache_info().currsize,
             unique_local_edges=replay_edge.cache_info().currsize,
             independent_bulk_step_checks=bulk_image.cache_info().currsize,
             variable_tail_block_counts=[2,7],
             scope='Each saved positive-weight local cycle replayed; no claim that its arbitrary carry sequence is realizable by one finite exterior.',
             decimal_lychrel_existence_proved=False)
    (HERE/'front_cycle_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
