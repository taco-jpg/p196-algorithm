"""Exact one-column extension of a prescribed periodic outer prefix.

This independent checker imports no candidate generator, SMT encoding, or
spatial-transfer implementation. Macro-edge ranks exclude every infinite
extension, not only an extension with the same temporal period.
"""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def prefix_image(prefix, incoming):
    lo, hi = [], [0]*len(prefix)
    a=0
    for v in prefix:
        lo.append((v+a)%10)
        a=(v+a)//10
    b=incoming
    for j in reversed(range(len(prefix))):
        hi[j]=(prefix[j]+b)%10
        b=(prefix[j]+b)//10
    h=b
    return [v+(1 if h and j==0 else hi[j-h]) for j,v in enumerate(lo)],h,a


def phase_relation(prefix, next_prefix, overflow):
    allowed=[]
    for incoming in (0,1):
        out,h,a=prefix_image(prefix,incoming)
        if out==next_prefix and h==overflow:
            allowed.append(incoming)
    relation=[set() for _ in range(19)]
    for q in range(19):
        for deeper in (0,1):
            incoming=(q+deeper)//10
            if incoming not in allowed:
                continue
            lo=(q+a)%10
            hi=(prefix[-1]+incoming)%10 if overflow else (q+deeper)%10
            relation[q].add(lo+hi)
    return relation,allowed


def analyze(c):
    prefixes=c.get('prefix',[[v] for v in c['outer']])
    p=len(prefixes)
    phase,allowed=[],[]
    for t in range(p):
        rel,ins=phase_relation(prefixes[t],prefixes[(t+1)%p],c['clock'][t])
        phase.append(rel);allowed.append(ins)
    macro=[]
    for q in range(19):
        reachable={q}
        for rel in phase:
            reachable={y for x in reachable for y in rel[x]}
        macro.append(reachable)
    # Repeated deletion of sinks. Assigned heights strictly decrease on edges.
    ranks={}
    while True:
        new={v:1+max((ranks[w] for w in macro[v]),default=-1)
             for v in range(19) if v not in ranks and all(w in ranks for w in macro[v])}
        if not new:
            break
        ranks.update(new)
    for v,rank in ranks.items():
        assert all(w in ranks and ranks[w]<rank for w in macro[v])
    all_excluded=len(ranks)==19
    return dict(period=p,prefix_width=len(prefixes[0]),growth=sum(c['clock']),
                allowed_high_carries=allowed,macro_edges=[sorted(s) for s in macro],
                diagonal_states=[v for v in range(19) if v in macro[v]],
                deletion_ranks={str(k):v for k,v in sorted(ranks.items())},
                remaining_states=[v for v in range(19) if v not in ranks],
                status='NO_INFINITE_ONE_COLUMN_EXTENSION' if all_excluded else 'EXTENSION_NOT_EXCLUDED',
                max_macro_edges=(max(ranks.values()) if all_excluded else None),
                decimal_lychrel_existence_proved=False)


if __name__=='__main__':
    results=[]
    for name in ('cycles_p5.json','cycles_p5_k4.json'):
        data=json.loads((HERE/name).read_text())
        for i,c in enumerate(data['candidates']):
            row=analyze(c)
            row.update(source=name,candidate_index=i)
            results.append(row)
            print(name,i,row['status'],'remaining',len(row['remaining_states']),
                  'bound',row['max_macro_edges'],flush=True)
    (HERE/'prefix_extension_audit.json').write_text(json.dumps(dict(
        status='PASS',scope=__doc__,queries=results),indent=2)+'\n')
