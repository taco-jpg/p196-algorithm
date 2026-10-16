"""Independent block-algebra, integer and descending-rank graph audit.

Does not import the seam quotient, graph generator, or affine normalizer.
The arbitrary-gap justification is the stated 9-run carry-transmission
law, whose exact finite interfaces are all recomputed here.
"""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def norm(q,carry=0):
    ds=[]
    for x in q:
        ds.append((x+carry)%10)
        carry=(x+carry)//10
    return tuple(ds),carry


def mixed(b,h):
    _,e=norm(b)
    _,z=norm(h,e)
    return z!=e


def predicted(state):
    b,h=state
    db,e=norm(b)
    dh,z=norm(h,e)
    assert z==1-e
    dr,gamma=norm(b[::-1],z)
    if gamma:
        left=db+(9*(1-e),)
        right=(1,)+dr[::-1]
        middle=dh+(9*e,)
    else:
        left,right,middle=db,dr[::-1],dh
    rawb=tuple(x+y for x,y in zip(left,right))
    rawh=tuple(x+y for x,y in zip(middle,middle[::-1]))
    if all(x==9 for x in rawh):
        return {'kind':'bands_merged','gamma':gamma,'raw_outer':rawb,'raw_middle':rawh}
    b_end=len(rawb)
    while b_end and rawb[b_end-1]==9:
        b_end-=1
    h_start=0
    while rawh[h_start]==9:
        h_start+=1
    target=(rawb[:b_end],rawh[h_start:len(rawh)-h_start])
    gain=len(rawb)-b_end+h_start-gamma
    kind='edge' if mixed(*target) else 'mixed_carry_lost'
    return {'kind':kind,'gamma':gamma,'target':target,'gap_delta':gain}


def freeze(x):
    if isinstance(x,list):
        return tuple(freeze(v) for v in x)
    if isinstance(x,dict):
        return {k:freeze(v) for k,v in x.items()}
    return x


def assembled(state,gap):
    b,h=state
    return b+(9,)*gap+h+(9,)*gap+b[::-1]


def ordinary(q):
    ds=[0]*len(q)
    for i in range(len(q)//2):
        ds[i]=max(0,q[i]-9)
        ds[-i-1]=min(q[i],9)
    if len(q)%2:
        assert q[len(q)//2]%2==0
        ds[len(q)//2]=q[len(q)//2]//2
    n=int(''.join(map(str,ds[::-1])))
    z=n+int(str(n)[::-1])
    s=str(z)
    return tuple(int(a)+int(b) for a,b in zip(s,s[::-1])),len(s)-len(ds),s!=s[::-1]


def main():
    summary=json.loads((HERE/'regeneration_interface_results.json').read_text())
    raw=gzip.decompress((HERE/summary['archive']).read_bytes())
    assert hashlib.sha256(raw).hexdigest()==summary['payload_sha256']
    data=freeze(json.loads(raw))
    graph={r['state']:{k:v for k,v in r.items() if k!='state'} for r in data['graph']}
    assert len(graph)==83679
    controls=0
    for state,result in graph.items():
        assert predicted(state)==result
        b,h=state
        assert h==h[::-1] and (len(h)%2==0 or h[len(h)//2]%2==0)
        assert h[0]!=9 and (not b or b[-1]!=9)
        assert mixed(b,h)
        for gap in (2,64):
            out,gamma,safe=ordinary(assembled(state,gap))
            assert safe and gamma==result['gamma']
            if result['kind']=='bands_merged':
                rawb=result['raw_outer'];rawh=result['raw_middle']
                expected=rawb+(9,)*(gap-gamma)+rawh+(9,)*(gap-gamma)+rawb[::-1]
            else:
                expected=assembled(result['target'],gap+result['gap_delta'])
            assert out==expected
            controls+=1
        if result['kind']=='edge':
            assert result['target'] in graph
    rank={}
    for start in graph:
        path=[];positions=set();state=start
        while state not in rank:
            assert state not in positions, ('cycle',state)
            positions.add(state);path.append(state)
            edge=graph[state]
            if edge['kind']!='edge':
                rank[state]=1
                break
            state=edge['target']
        for s in reversed(path):
            edge=graph[s]
            rank[s]=1 if edge['kind']!='edge' else 1+rank[edge['target']]
    for s,edge in graph.items():
        if edge['kind']=='edge':
            assert rank[s]==rank[edge['target']]+1
        else:
            assert rank[s]==1
    assert max(rank.values())==50
    for p in data['paths']:
        state=p['initial'];offset=minimum=0;t=0
        while True:
            edge=graph[state];t+=1
            offset+=edge.get('gap_delta',0);minimum=min(minimum,offset)
            if edge['kind']!='edge':
                break
            state=edge['target']
        assert t==p['steps'] and state==p['final_state']
        assert edge['kind']==p['outcome']
        assert (offset,minimum,2-minimum)==(p['final_gap_change'],p['minimum_gap_change'],p['safe_gap_threshold'])
    positive=[{'state':s,**r} for s,r in graph.items() if r['kind']=='edge' and r['gap_delta']>0]
    ranks_raw=json.dumps([{'state':s,'rank':rank[s]} for s in sorted(rank)],
                        sort_keys=True,separators=(',',':')).encode()
    (HERE/'regeneration_interface_ranks.json.gz').write_bytes(gzip.compress(ranks_raw,mtime=0))
    result={'status':'PASS','block_transitions_checked':len(graph),
            'ordinary_integer_transitions_checked':controls,'rank_certificates':len(rank),
            'maximum_rank':max(rank.values()),'all_seed_paths_replayed':len(data['paths']),
            'positive_gap_edges_retaining_mixed_carries':len(positive),
            'largest_retained_gap_gain':max(r['gap_delta'] for r in positive),
            'gap_gain_distribution_all_transitions':dict(Counter(str(r.get('gap_delta')) for r in graph.values())),
            'rank_payload_sha256':hashlib.sha256(ranks_raw).hexdigest(),
            'graph_payload_sha256':hashlib.sha256(raw).hexdigest(),
            'imports_quotient_or_generator':False,'all_parameter_justification':'exact block algebra and 9 carry transmission',
            'formalized_in_Lean':False,'decimal_lychrel_existence_proved':False}
    (HERE/'regeneration_interface_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
