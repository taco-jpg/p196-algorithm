"""Independent integer and graph replay, importing no discovery code."""
from collections import Counter,defaultdict,deque
from pathlib import Path
import gzip,hashlib,itertools,json,time

ROOT=Path(__file__).parent
GAPS=((2,2),(3,5),(6,3),(64,65))


def freeze(x):return tuple(map(freeze,x)) if isinstance(x,list) else x


def join(s,g,h):
    b,a,c=s
    return b+(9,)*g+a+(9,)*h+c+(9,)*h+a[::-1]+(9,)*g+b[::-1]


def norm(q,carry):
    value=carry+sum(x*10**i for i,x in enumerate(q))
    return tuple((value//10**i)%10 for i in range(len(q))),value//10**len(q)


def mixed(s):
    b,a,c=s;e=[];carry=0
    for part in (b,a,c,a[::-1]):
        digits,carry=norm(part,carry);e.append(carry)
    return e[0]+e[3]==e[1]+e[2]==1


def numeric(q):
    value=sum(x*10**i for i,x in enumerate(q))
    digits=tuple(int(x) for x in str(value)[::-1])
    output=tuple(x+y for x,y in zip(digits,digits[::-1]))
    assert str(value)!=str(value)[::-1],('mixed source produced palindrome',q)
    return output,int(len(digits)>len(q))


def reconstruct(s):
    b,a,c=s;g=h=2;q=join(s,g,h);out,clock=numeric(q)
    nb,na,nc=len(b)+clock,len(a)+clock,len(c)+clock
    rb=out[:nb];offset=nb+g-clock;ra=out[offset:offset+na]
    offset+=na+h-clock;rc=out[offset:offset+nc];raw=(rb,ra,rc)
    assert out==join(raw,g-clock,h-clock)
    if all(x==9 for x in ra):return dict(kind='outer_inner_bands_merged',gamma=clock,raw_state=raw)
    if all(x==9 for x in rc):return dict(kind='central_bands_merged',gamma=clock,raw_state=raw)
    rb2=list(rb)
    while rb2 and rb2[-1]==9:rb2.pop()
    left=0;right=len(ra)
    while ra[left]==9:left+=1
    while ra[right-1]==9:right-=1
    core=0
    while rc[core]==9:core+=1
    target=(tuple(rb2),ra[left:right],rc[core:len(rc)-core])
    shifts=(len(rb)-len(rb2)+left-clock,len(ra)-right+core-clock)
    return dict(kind='edge' if mixed(target) else 'mixed_condition_lost',gamma=clock,target=target,gap_delta=shifts)


def main():
    started=time.monotonic()
    with gzip.open(ROOT/'four_band_controls.json.gz','rb') as f:payload=f.read()
    data=json.loads(payload);graph={freeze(r['state']):r for r in data['graph']}
    assert len(graph)==len(data['graph'])
    arithmetic=0
    for state,record in graph.items():
        assert mixed(state)
        expect=reconstruct(state)
        assert {k:freeze(v) for k,v in record.items() if k!='state'}==expect,(state,expect,record)
        for g,h in GAPS:
            output,clock=numeric(join(state,g,h));arithmetic+=1
            assert clock==record['gamma']
            if 'target' in record:
                target=freeze(record['target']);dg,dh=record['gap_delta']
                assert output==join(target,g+dg,h+dh)
            else:assert output==join(freeze(record['raw_state']),g-clock,h-clock)
        if record['kind']=='edge':assert freeze(record['target']) in graph
    seeds=[]
    for b,a,c in itertools.product(range(1,19),range(19),range(0,19,2)):
        if b==9 or a==9:continue
        state=((b,),(a,),(c,))
        if mixed(state):seeds.append(state)
    assert len(seeds)==len(set(seeds))==765
    assert {freeze(p['initial']) for p in data['paths']}==set(seeds)
    reachable=set();status=Counter();minimum_gap=[0,0];maxpath=0
    for rec in data['paths']:
        state=freeze(rec['initial']);path=[];seen=set();running=[0,0];low=[0,0]
        while state not in seen:
            seen.add(state);reachable.add(state);path.append(state);r=graph[state]
            if 'gap_delta' in r:
                for j in (0,1):running[j]+=r['gap_delta'][j];low[j]=min(low[j],running[j])
            if r['kind']!='edge':break
            state=freeze(r['target'])
        else:raise AssertionError('cycle')
        assert path==freeze(rec['states']) or tuple(path)==freeze(rec['states'])
        assert r['kind']==rec['status']
        assert rec['sufficient_initial_gaps']==[2-x for x in low]
        status[r['kind']]+=1;maxpath=max(maxpath,len(path))
        for j in (0,1):minimum_gap[j]=max(minimum_gap[j],2-low[j])
    assert reachable==set(graph)
    # Construct a strict rank independently, from terminals backward.
    parents=defaultdict(list);rank={};todo=deque()
    for s,r in graph.items():
        if r['kind']=='edge':parents[freeze(r['target'])].append(s)
        else:rank[s]=1;todo.append(s)
    while todo:
        s=todo.popleft()
        for p in parents[s]:
            assert p not in rank
            rank[p]=rank[s]+1;todo.append(p)
    assert len(rank)==len(graph) and max(rank.values())==maxpath==19
    assert not data['cycles']
    # Preserve one whole ordinary-integer witness for the longest safe path.
    longest=max(data['paths'],key=lambda p:len(p['states']));s=freeze(longest['initial'])
    g,h=minimum_gap;q=join(s,g,h);m=len(q)//2
    high=''.join(str(min(x,9)) for x in q[:m])
    middle=str(q[m]//2) if len(q)%2 else ''
    low=''.join(str(max(x-9,0)) for x in q[:m][::-1])
    value=int(high+middle+low);orbit=[value];recorded=[]
    for state in map(freeze,longest['states']):
        assert q==join(state,g,h)
        value+=int(str(value)[::-1]);orbit.append(value)
        digits=tuple(int(x) for x in str(value)[::-1]);q=tuple(a+b for a,b in zip(digits,digits[::-1]))
        assert str(value)!=str(value)[::-1]
        r=graph[state];recorded.append(dict(state=state,g=g,h=h,clock=r['gamma'],kind=r['kind']))
        if 'gap_delta' in r:g+=r['gap_delta'][0];h+=r['gap_delta'][1]
    witness=dict(initial_state=s,initial_gaps=minimum_gap,ordinary_trajectory=orbit,steps=recorded,
                 terminal_kind=longest['status'],scope='Every displayed positive output is nonpalindromic; no later-time claim.')
    (ROOT/'four_band_longest_witness.json').write_text(json.dumps(witness,indent=2)+'\n')
    out=dict(verified=True,payload_sha256=hashlib.sha256(payload).hexdigest(),initial_states=len(seeds),
             reachable_graph_states=len(graph),integer_transition_controls=arithmetic,
             terminal_status_counts=dict(status),dag_rank=max(rank.values()),sufficient_initial_gaps=minimum_gap,
             cycles=0,cap_reached=False,seconds=time.monotonic()-started,
             positive_lychrel_proof=False,scope='Complete singleton-interface four-band family; arbitrary interfaces remain UNKNOWN')
    (ROOT/'four_band_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
