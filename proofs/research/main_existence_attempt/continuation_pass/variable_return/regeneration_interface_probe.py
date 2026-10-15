"""Broader positive search at exact old-4/14 neutral-regeneration fronts.

Imports the seam stream's exact gap-independent block transition. Every
retained edge is symbolic in the neutral gap, not inferred from samples.
Caps classify unresolved paths as UNKNOWN. A cycle would require a separate
literal realization and proof audit before any infinite-avoidance claim.
"""
from collections import Counter
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
SEAM=HERE.parent/'seam_persistence'
sys.path.insert(0,str(SEAM))
import neutral_quotient as nq

CONFIG={'outer_widths':[1,2,3],'outer_last':[4,14],
        'middle_widths':[1,2,3,4],
        'middle_first':'18 minus outer_last; symmetric; even odd center',
        'state_cap':200000,'path_step_cap':500,'interface_length_cap':512,
        'wall_time_seconds':60}


def seeds():
    for width in CONFIG['outer_widths']:
        for last in (4,14):
            if width==1:
                exteriors=[(last,)]
            else:
                exteriors=((a,)+inside+(last,) for a in range(1,19)
                           for inside in product(range(19),repeat=width-2))
            for b in exteriors:
                edge=18-last
                centers=[(edge,),(edge,edge)]
                centers.extend((edge,c,edge) for c in range(0,19,2))
                centers.extend((edge,c,c,edge) for c in range(19))
                for h in centers:
                    state=(b,h)
                    assert nq.mixed(state)
                    yield state


def main():
    started=time.monotonic()
    initials=tuple(seeds())
    assert len(initials)==22382 and len(set(initials))==22382
    graph={}
    paths=[]
    cycles=[]
    stopped=False
    for initial_index,initial in enumerate(initials):
        state=initial
        positions={}
        path=[]
        running=minimum=0
        outcome=None
        while outcome is None:
            if state in positions:
                loop=path[positions[state]:]
                gain=sum(graph[s]['gap_delta'] for s in loop)
                overflows=sum(graph[s]['gamma'] for s in loop)
                assert 2*gain==overflows
                outcome='cycle_candidate'
                cycles.append({'initial':initial,'loop':loop,'gap_gain':gain,
                               'overflows':overflows,'needs_independent_audit':True})
                break
            if len(path)>=CONFIG['path_step_cap']:
                outcome='UNKNOWN_path_step_cap'
                break
            if max(len(state[0]),len(state[1]))>CONFIG['interface_length_cap']:
                outcome='UNKNOWN_interface_length_cap'
                break
            if state not in graph and len(graph)>=CONFIG['state_cap']:
                outcome='UNKNOWN_state_cap'
                stopped=True
                break
            if time.monotonic()-started>CONFIG['wall_time_seconds']:
                outcome='UNKNOWN_wall_time_cap'
                stopped=True
                break
            positions[state]=len(path)
            path.append(state)
            if state not in graph:
                graph[state]=nq.transition(state)
            result=graph[state]
            running+=result.get('gap_delta',0)
            minimum=min(minimum,running)
            if result['kind']!='edge':
                outcome=result['kind']
                break
            state=result['target']
        paths.append({'initial':initial,'steps':len(path),'outcome':outcome,
                      'final_state':state,'final_gap_change':running,
                      'minimum_gap_change':minimum,'safe_gap_threshold':2-minimum})
        if stopped:
            break
    records=[{'state':state,**result} for state,result in sorted(graph.items())]
    payload={'configuration':CONFIG,'graph':records,'paths':paths,'cycles':cycles,
             'unstarted_seeds':initials[len(paths):]}
    raw=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
    archive=HERE/'regeneration_interface_outcomes.json.gz'
    archive.write_bytes(gzip.compress(raw,mtime=0))
    counts=Counter(p['outcome'] for p in paths)
    summary={'status':'exact symbolic reachable graph from the specified initial interfaces',
             'configuration':CONFIG,'initial_states':len(initials),
             'started_initial_states':len(paths),'unstarted_initial_states':len(initials)-len(paths),
             'distinct_states':len(graph),'outcomes':dict(counts),
             'transition_kinds':dict(Counter(x['kind'] for x in graph.values())),
             'complete':len(paths)==len(initials) and not any(k.startswith('UNKNOWN') for k in counts),
             'maximum_outer_width':max(len(s[0]) for s in graph),
             'maximum_middle_width':max(len(s[1]) for s in graph),
             'longest_path':max(paths,key=lambda p:p['steps']),
             'sufficient_initial_gap':max(p['safe_gap_threshold'] for p in paths),
             'cycles':cycles,'archive':archive.name,
             'payload_sha256':hashlib.sha256(raw).hexdigest(),
             'quotient_source_sha256':hashlib.sha256(Path(nq.__file__).read_bytes()).hexdigest(),
             'seconds':time.monotonic()-started,
             'all_time_avoidance_proved':False}
    (HERE/'regeneration_interface_results.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
