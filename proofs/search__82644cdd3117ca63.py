"""Complete finite-domain functional graph search, with checkable rank witnesses.

Domain: all trimmed canonical quotient states with I=2|B|+2|A|+|C|<=cap.
An EXIT means only that a successor leaves this domain, not global termination.
A CYCLE is a returned interface, not a Lychrel witness unless both gap gains
are nonnegative and the all-gap mathematical bridge has been checked.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import time
from array import array
from collections import Counter
from pathlib import Path
from quotient import State, states, step


def state_json(s: State):
    return [s.c,list(s.B),list(s.A),list(s.C)]


def run(cap: int, directory: Path) -> dict:
    directory.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    vertices=list(states(cap))
    index={s:i for i,s in enumerate(vertices)}
    assert len(index)==len(vertices)
    successor=array('i')
    increments=[]
    hist=Counter()
    digest=hashlib.sha256()
    for s in vertices:
        e=step(s)
        j=index.get(e.target,-1)
        successor.append(j)
        increments.append((e.dg,e.dh,e.overflow))
        hist['edges' if j>=0 else 'exits']+=1
        hist[f'I={s.interface_size}']+=1
        record=[state_json(s),state_json(e.target),e.dg,e.dh,e.overflow]
        if j<0:
            assert e.target.interface_size>cap
        digest.update((json.dumps(record,separators=(',',':'))+'\n').encode())
    # status: -2 unknown, -1 known cycle basin, >=1 transitions until first exit.
    ranks=array('i',[-2])*len(vertices)
    cycles=[]
    for start in range(len(vertices)):
        if ranks[start]!=-2:
            continue
        path=[]
        position={}
        j=start
        while j>=0 and ranks[j]==-2 and j not in position:
            position[j]=len(path)
            path.append(j)
            j=successor[j]
        if j in position:
            cyclic=path[position[j]:]
            gains=[sum(increments[k][a] for k in cyclic) for a in range(3)]
            assert 2*(gains[0]+gains[1])==gains[2]
            cycles.append({'states':[state_json(vertices[k]) for k in cyclic],
                           'gains':gains,'length':len(cyclic)})
            base=-1
        else:
            base=0 if j<0 else ranks[j]
        for k in reversed(path):
            if base>=0:
                base+=1
            ranks[k]=base
    for i,j in enumerate(successor):
        if ranks[i]>=0:
            assert ranks[i]==(1 if j<0 else ranks[j]+1)
        else:
            assert ranks[i]==-1 and j>=0 and ranks[j]==-1
    maxrank=max(ranks,default=0)
    witness=[]
    if maxrank>0:
        j=ranks.index(maxrank)
        while j>=0:
            witness.append({'state':state_json(vertices[j]),'edge':list(increments[j]),'rank':ranks[j]})
            j=successor[j]
        e=step(State(witness[-1]['state'][0],*(tuple(x) for x in witness[-1]['state'][1:])))
        witness.append({'exit_state':state_json(e.target)})
    certificate=directory/f'cap{cap}-ranks.json.gz'
    # JSON permits architecture-independent replay. Stable gzip mtime is zero.
    raw=json.dumps(list(ranks),separators=(',',':')).encode()
    with open(certificate,'wb') as f:
        f.write(gzip.compress(raw,mtime=0))
    result={
        'scope':'Complete induced functional graph on the explicitly capped state domain; exits are unresolved beyond the cap.',
        'cap':cap,'vertices':len(vertices),**dict(sorted(hist.items())),
        'cycles':cycles,'cycle_basin_vertices':sum(r==-1 for r in ranks),
        'max_exit_transitions':maxrank,
        'edge_stream_sha256':digest.hexdigest(),
        'rank_json_sha256':hashlib.sha256(raw).hexdigest(),
        'rank_archive_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'maximal_exit_path':witness,
        'elapsed_seconds':round(time.monotonic()-started,4),
    }
    (directory/f'cap{cap}-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('maximal_exit_path','cycles')},indent=2),flush=True)
    print('cycles:',len(cycles),flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cap',type=int,default=6)
    p.add_argument('--output',type=Path,default=Path('results'))
    args=p.parse_args()
    run(args.cap,args.output)
