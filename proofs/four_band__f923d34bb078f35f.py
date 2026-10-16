"""Two independent neutral gaps and three finite interfaces, actual clocks.

The state (B,A,C) represents B 9^g A 9^h C 9^h rev(A) 9^g rev(B).
Both mirrored pairs of nine-bands must remain mixed. All arithmetic is
whole-word; the clock is the actual final carry. This is a new architecture,
not a larger SAT instance. A positive cycle still requires a written proof.
"""
from pathlib import Path
from collections import Counter
import gzip, hashlib, itertools, json

ROOT=Path(__file__).parent
GAP_CONTROLS=((2,2),(3,5),(6,3),(64,65))
CAPS=dict(states=100000,path_steps=1000,total_interface_width=256)


def norm(q,carry=0):
    digits=[]
    for x in q:
        carry,d=divmod(x+carry,10);digits.append(d)
    return tuple(digits),carry


def pair(q):return tuple(a+b for a,b in zip(q,q[::-1]))


def step(q):
    d,carry=norm(q)
    return pair(d+((carry,) if carry else ()))


def assemble(state,g,h):
    b,a,c=state
    return b+(9,)*g+a+(9,)*h+c+(9,)*h+a[::-1]+(9,)*g+b[::-1]


def blocks(state):
    b,a,c=state
    db,e0=norm(b);da,e1=norm(a,e0);dc,e2=norm(c,e1)
    dr_a,e3=norm(a[::-1],e2);dr_b,gamma=norm(b[::-1],e3)
    return (db,da,dc,dr_a,dr_b),(e0,e1,e2,e3),gamma


def mixed(state):
    ds,e,gamma=blocks(state)
    return e[0]+e[3]==1 and e[1]+e[2]==1


def valid(state):
    b,a,c=state
    return ((not b or (b[0]>0 and b[-1]!=9)) and bool(a) and a[0]!=9 and a[-1]!=9
            and bool(c) and c==c[::-1] and c[0]!=9
            and (len(c)%2==0 or c[len(c)//2]%2==0)
            and all(0<=x<=18 for x in b+a+c))


def transition(state):
    assert valid(state) and mixed(state)
    (db,da,dc,dra,drb),e,gamma=blocks(state)
    if gamma:
        rb=tuple(x+y for x,y in zip(db+(9*(1-e[0]),),(1,)+drb[::-1]))
        ra=tuple(x+y for x,y in zip(da+(9*(1-e[1]),),(9*(1-e[3]),)+dra[::-1]))
        rc=pair(dc+(9*(1-e[2]),))
    else:
        rb=tuple(x+y for x,y in zip(db,drb[::-1]))
        ra=tuple(x+y for x,y in zip(da,dra[::-1]))
        rc=pair(dc)
    raw=(rb,ra,rc)
    for g,h in GAP_CONTROLS:
        assert step(assemble(state,g,h))==assemble(raw,g-gamma,h-gamma)
    if all(x==9 for x in ra):
        return dict(kind='outer_inner_bands_merged',gamma=gamma,raw_state=raw)
    if all(x==9 for x in rc):
        return dict(kind='central_bands_merged',gamma=gamma,raw_state=raw)
    ub=0
    while ub<len(rb) and rb[-1-ub]==9:ub+=1
    va=0
    while ra[va]==9:va+=1
    ua=0
    while ra[-1-ua]==9:ua+=1
    vc=0
    while rc[vc]==9:vc+=1
    target=(rb[:len(rb)-ub],ra[va:len(ra)-ua],rc[vc:len(rc)-vc])
    dg,dh=ub+va-gamma,ua+vc-gamma
    assert valid(target)
    for g,h in GAP_CONTROLS:
        assert step(assemble(state,g,h))==assemble(target,g+dg,h+dh)
    b,a,c=state;bb,aa,cc=target
    assert 2*len(bb)+2*len(aa)+len(cc)+2*dg+2*dh==2*len(b)+2*len(a)+len(c)+gamma
    return dict(kind='edge' if mixed(target) else 'mixed_condition_lost',
                gamma=gamma,target=target,gap_delta=(dg,dh))


def seeds():
    for b,a,c in itertools.product(range(1,19),range(19),range(0,19,2)):
        state=((b,),(a,),(c,))
        if valid(state) and mixed(state):yield state


def main():
    graph={};paths=[];cycles=[];initials=list(seeds())
    for initial in initials:
        state=initial;seen={};path=[];running=[0,0];minimum=[0,0]
        while True:
            if state in seen:
                loop=path[seen[state]:]
                gain=[sum(graph[s]['gap_delta'][j] for s in loop) for j in (0,1)]
                overflow=sum(graph[s]['gamma'] for s in loop)
                assert 2*sum(gain)==overflow
                cycles.append(dict(initial=initial,loop=loop,gap_gain=gain,overflow_count=overflow,
                                   nonnegative_each_gap=all(x>=0 for x in gain)))
                status='cycle';break
            if len(path)>=CAPS['path_steps'] or sum(map(len,state))>CAPS['total_interface_width']:
                status='UNKNOWN_INTERFACE_OR_PATH_CAP';break
            if state not in graph:
                if len(graph)>=CAPS['states']:
                    status='UNKNOWN_GRAPH_CAP';break
                graph[state]=transition(state)
            seen[state]=len(path);path.append(state);result=graph[state]
            if 'gap_delta' in result:
                for j in (0,1):
                    running[j]+=result['gap_delta'][j];minimum[j]=min(minimum[j],running[j])
            if result['kind']!='edge':status=result['kind'];break
            state=result['target']
        paths.append(dict(initial=initial,states=path,status=status,
                          sufficient_initial_gaps=[2-x for x in minimum],final_state=state))
    records=[dict(state=s,**r) for s,r in sorted(graph.items())]
    payload=json.dumps(dict(graph=records,paths=paths,cycles=cycles),separators=(',',':'),sort_keys=True).encode()
    (ROOT/'four_band_controls.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    summary=dict(initial_family='B,A,C each one coefficient, outer B positive, C even, all endpoints non9, both band pairs mixed',
                 initial_states=len(initials),graph_states=len(graph),transition_counts=dict(Counter(x['kind'] for x in graph.values())),
                 path_status_counts=dict(Counter(x['status'] for x in paths)),cycles=cycles,
                 caps=CAPS,cap_reached=any(x['status'].startswith('UNKNOWN') for x in paths),
                 longest_path_states=max(len(x['states']) for x in paths),
                 largest_interface_widths=[max(len(s[j]) for s in graph) for j in range(3)],
                 sufficient_initial_gaps=[max(x['sufficient_initial_gaps'][j] for x in paths) for j in (0,1)],
                 arithmetic_gap_controls=GAP_CONTROLS,payload_sha256=hashlib.sha256(payload).hexdigest(),
                 infinite_existence_proved=False)
    (ROOT/'four_band_results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
