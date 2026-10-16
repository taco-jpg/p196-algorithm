"""Retained discovery calculation; not used to prove the zero theorem.

Exact arbitrary-clock prefix graph at widths 2..4. The analytic theorem is
stronger than this SCC observation and does not rely on SciPy.
"""
from collections import Counter
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import struct
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

HERE=Path(__file__).resolve().parent


def step(prefix,interior):
    low=[];carry=0
    for x in prefix:
        low.append((x+carry)%10);carry=(x+carry)//10
    high=[];carry=interior
    for x in prefix[::-1]:
        high.append((x+carry)%10);carry=(x+carry)//10
    high.reverse()
    if carry:
        return (low[0]+1,)+tuple(low[i]+high[i-1] for i in range(1,len(prefix)))
    return tuple(a+b for a,b in zip(low,high))


def main():
    summary=[]
    for width in (2,3,4):
        prefixes=[(a,)+rest for a in range(1,19) for rest in product(range(19),repeat=width-1)]
        ids={p:i for i,p in enumerate(prefixes)}
        edges=[(ids[step(p,0)],ids[step(p,1)]) for p in prefixes]
        graph=csr_matrix(([1]*(2*len(prefixes)),
            ([i for i in range(len(prefixes)) for _ in (0,1)],[j for pair in edges for j in pair])),
            shape=(len(prefixes),len(prefixes)))
        count,labels=connected_components(graph,directed=True,connection='strong')
        sizes=Counter(map(int,labels))
        probes=[]
        for a in range(1,19):
            targets=[(a,)+(0,)*(width-1)]
            if a<=9:
                targets.append((a,a)+(0,)*(width-2))
            for target in targets:
                i=ids[target]
                probes.append({'prefix':target,'scc_size':sizes[int(labels[i])],'self_loop':i in edges[i]})
        raw=b''.join(struct.pack('<IIII',i,edges[i][0],edges[i][1],int(labels[i]))
                     for i in range(len(prefixes)))
        archive=HERE/f'prefix_scc_width{width}.bin.gz'
        archive.write_bytes(gzip.compress(raw,mtime=0))
        summary.append({'width':width,'vertices':len(prefixes),'sccs':count,
                        'largest_scc':max(sizes.values()),'probes':probes,
                        'archive':archive.name,'payload_sha256':hashlib.sha256(raw).hexdigest()})
    result={'scope':'discovery only; direct column theorem does not depend on this graph',
            'results':summary,'archive_layout':'four little-endian uint32 per row: index,next0,next1,SCC label',
            'vertex_order':'lexicographic positive first coefficient1..18, remaining coefficients0..18',
            'decimal_lychrel_existence_proved':False}
    (HERE/'prefix_scc_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**result,'results':[{k:v for k,v in row.items() if k!='probes'} for row in summary]},indent=2))


if __name__=='__main__':
    main()
