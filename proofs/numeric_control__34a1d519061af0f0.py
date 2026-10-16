"""Independent integer controls for the arbitrary-clock outer-prefix map.

Every incoming carry is realized using an even central coefficient 0 or18.
These finite controls supplement the symbolic column derivation, not an
unbounded proof or a decimal Lychrel existence claim.
"""
from itertools import product
from pathlib import Path
import hashlib,json


def predicted(prefix, incoming):
    low=[];c=0
    for x in prefix:
        low.append((x+c)%10);c=(x+c)//10
    high=[];c=incoming
    for x in reversed(prefix):
        high.append((x+c)%10);c=(x+c)//10
    high.reverse()
    if c:
        return tuple([low[0]+1]+[low[i]+high[i-1] for i in range(1,len(prefix))])
    return tuple(a+b for a,b in zip(low,high))


def realized(prefix,incoming):
    digits=[max(x-9,0) for x in prefix]+[9*incoming]+[min(x,9) for x in reversed(prefix)]
    n=sum(d*10**i for i,d in enumerate(digits))
    assert n>0 and len(str(n))==len(digits)
    ds=[int(x) for x in str(n)][::-1]
    q=tuple(a+b for a,b in zip(ds,ds[::-1]))
    assert q==prefix+(18*incoming,)+prefix[::-1]
    v=n+int(str(n)[::-1])
    out=[int(x) for x in str(v)][::-1]
    return tuple(out[i]+out[-i-1] for i in range(len(prefix)))


def run():
    count=0
    for width in range(1,4):
        for first in range(1,19):
            for rest in product(range(19),repeat=width-1):
                prefix=(first,)+rest
                for incoming in range(2):
                    assert predicted(prefix,incoming)==realized(prefix,incoming)
                    count+=1
    folder=Path(__file__).parent
    rows=[json.loads(x) for x in (folder/'results.jsonl').read_text().splitlines()]
    assert [r['width'] for r in rows]==[1,2,3,4,5]
    assert all(r['universal_trap_size']==0 and r['all_rank_or_closure_obligations_checked'] for r in rows)
    result={'independent_integer_controls':count,'prefix_widths_checked':[1,2,3],
            'all_control_transitions_match':True,'greatest_trap_results':rows,
            'source_sha256':hashlib.sha256((folder/'search.cpp').read_bytes()).hexdigest(),
            'decimal_lychrel_existence_proved':False}
    (folder/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='greatest_trap_results'}))


if __name__=='__main__':run()
