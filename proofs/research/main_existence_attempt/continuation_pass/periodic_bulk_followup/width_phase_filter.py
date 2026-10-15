"""Track exact width modulo8 and reflected period4 phase on necessary graph.

Modulo8 is stronger than modulo4 here: one extra four-column bulk period
on each side adds eight total columns when finite interfaces return.
"""
from collections import Counter,deque
from pathlib import Path
from math import gcd
import gzip,hashlib,json
from bulk_phases import outputs,INITIAL
from outer_filter import outer,scc

ROOT=Path(__file__).parent


def reflected(p,width):return tuple(p[(width-1-i)%4] for i in range(4))


def main():
    initial=[(INITIAL,q,w) for q in range(1,19) for w in range(8)]
    todo=deque(initial);seen=set(initial);graph={};mirror_checks=0
    while todo:
        state=todo.popleft();p,q,w=state;edges=[]
        for e in outputs(p):
            pp=e['target'];h=e['clock'];ww=(w+h)%8
            right=reflected(p,w);right_next=reflected(pp,ww)
            candidates=[x for x in outputs(right) if x['clock']==h]
            if 'left_carry' in e:
                candidates=[x for x in candidates if x['left_carry']==e['right_carry'] and x['right_carry']==e['left_carry']]
            assert any(x['target']==right_next for x in candidates)
            mirror_checks+=1
            for qq in outer(q,h):
                target=(pp,qq,ww)
                edges.append(dict(clock=h,target=target,**{k:v for k,v in e.items() if k not in ('clock','target')}))
                if target not in seen:seen.add(target);todo.append(target)
        graph[state]=edges
    comps,ids=scc(graph)
    old=json.loads((ROOT/'outer_filtered_results.json').read_text())['shortest_recorded_cycle']
    loops=8//gcd(8,old['overflow_count']);w=0;lift=[]
    for repeat in range(loops):
        for e in old['loop']:
            p,q=e['source'];pp,qq=e['target'];ww=(w+e['clock'])%8
            source=(tuple(p),q,w);target=(tuple(pp),qq,ww)
            assert any(x['target']==target and x['clock']==e['clock'] for x in graph[source])
            lift.append(dict(source=source,target=target,clock=e['clock'],right_phase=reflected(tuple(p),w)))
            w=ww
    assert w==0 and lift[0]['source']==lift[-1]['target']
    payload=json.dumps(dict(initial=initial,graph=[dict(source=s,edges=graph[s]) for s in sorted(graph)],
                            components=comps,width_compatible_cycle=lift),separators=(',',':'),sort_keys=True).encode()
    (ROOT/'width_phase_graph.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    out=dict(width_modulus=8,paired_bulk_period=4,reachable_states=len(graph),edges=sum(map(len,graph.values())),
             strong_components=len(comps),component_size_distribution=dict(sorted(Counter(map(len,comps)).items())),
             checked_reflection_phase_relations=mirror_checks,
             representative_cycle_length=len(lift),representative_cycle_overflows=sum(e['clock'] for e in lift),
             representative_cycle_gap_gain_if_interfaces_return=sum(e['clock'] for e in lift)//8,
             representative_initial=lift[0]['source'],representative_cycle=lift,
             payload_sha256=hashlib.sha256(payload).hexdigest(),
             finite_canonical_interface_lift='NOT_INSTANTIATED',infinite_existence_proved=False,
             scope='Necessary bulk/outer/width/reflection compatibility only; no free-control cycle is asserted realizable')
    (ROOT/'width_phase_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
