"""Complete finite exterior graphs, with a literal-integer rank replay.

The search factor and replay use separate normalization implementations.
No result below concerns exteriors after they leave the selected cap.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path

PHASES = (2, 4, 6, 8, 10, 12, 14, 16)
State = tuple[int, tuple[int, ...]]


def normalize(word, carry):
    digits = []
    for x in word:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
    return tuple(digits), carry


def factor(s: State) -> tuple[State, int]:
    c, B = s
    k = int(c >= 10)
    t = c - 9*k
    DB, e = normalize(B, 0)
    DR, gamma = normalize(B[::-1], k)
    lhs = DB + (c + e - 10*k,)
    rhs = (1,) + DR[::-1] if gamma else DR[::-1] + (t,)
    raw = tuple(a+b for a,b in zip(lhs,rhs))
    last = len(raw)
    while last and raw[last-1] == 2*t:
        last -= 1
    return (2*t, raw[:last]), gamma


def literal_factor(s: State) -> tuple[State, int]:
    """Compute the next boundary using one actual finite ordinary integer."""
    c, B = s
    q = B + (c,)*2 + (18-c,)*4 + (c,)*2 + B[::-1]
    total = sum(coefficient * 10**i for i,coefficient in enumerate(q))
    digits = tuple(int(x) for x in str(total)[::-1])
    gamma = len(digits)-len(q)
    raw = [digits[i]+digits[-1-i] for i in range(len(B)+1)]
    cp = 2*c if c < 10 else 2*c-18
    while raw and raw[-1] == cp:
        raw.pop()
    return (cp,tuple(raw)),gamma


def domain(cap: int):
    for c in PHASES:
        yield c, ()
        for length in range(1,cap+1):
            for B in product(range(19),repeat=length):
                if B[0] > 0 and B[-1] != c:
                    yield c,B


def padded_domain(cap: int):
    """Independent fixed-width enumeration, canonicalized at its phase tail."""
    if cap == 0:
        for c in PHASES:
            yield c,()
        return
    for c in PHASES:
        for first in range(1,19):
            for rest in product(range(19),repeat=cap-1):
                B=(first,)+rest
                length=cap
                while length and B[length-1]==c:
                    length-=1
                yield c,B[:length]


def audit(cap: int, replay: bool = True) -> dict:
    edges={s:factor(s)[0] for s in domain(cap)}
    expected=8 if cap==0 else 8*18*19**(cap-1)
    if len(edges)!=expected:
        raise AssertionError('Incomplete canonical enumeration')
    ranks={}
    for start in edges:
        path=[]
        local=set()
        s=start
        while s in edges and s not in ranks:
            if s in local:
                raise AssertionError(('Cycle found; negative certificate rejected',s))
            local.add(s);path.append(s);s=edges[s]
        r=ranks.get(s,0)
        for s in reversed(path):
            r+=1;ranks[s]=r
    digest=hashlib.sha256()
    replay_count=0
    # Different enumeration plus literal arithmetic checks every rank equation.
    for s in padded_domain(cap):
        if s not in edges:
            raise AssertionError(('Padded enumeration outside graph',s))
        v,gamma=literal_factor(s) if replay else factor(s)
        if v!=edges[s] or ranks[s] != 1+ranks.get(v,0):
            raise AssertionError(('Rank replay failed',s,v,ranks[s]))
        digest.update(repr((s,v,gamma,ranks[s])).encode()+b'\n')
        replay_count+=1
    if replay_count!=expected:
        raise AssertionError('Independent enumeration count mismatch')
    # The padded representation is bijective: appending c to length cap
    # inverts its maximal suffix removal, so equal outputs imply equal inputs.
    source=max(ranks,key=ranks.get)
    witness=[]
    s=source
    for time in range(ranks[source]+1):
        witness.append({'time':time,'phase':s[0],'B':list(s[1])})
        s=factor(s)[0]
    return {'cap':cap,'states':len(edges),'immediate_exits':sum(v not in edges for v in edges.values()),
            'cycles':0,'max_first_exit':ranks[source],
            'rank_histogram':dict(sorted(Counter(ranks.values()).items())),
            'independent_literal_rows':replay_count if replay else 0,
            'sha256_row_transcript':digest.hexdigest(),'sharp_path':witness,
            'scope':'All eight periodic phases; all canonical trimmed B within cap; A,C unrestricted. Leaving this cap is not palindrome attainment.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--cap',type=int,default=4,choices=range(5))
    parser.add_argument('--all-caps',action='store_true')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    output=[]
    for cap in range(args.cap+1) if args.all_caps else [args.cap]:
        row=audit(cap)
        output.append(row)
        print(json.dumps({k:v for k,v in row.items() if k not in ('rank_histogram','sharp_path')},indent=2),flush=True)
        if args.output:
            args.output.write_text(json.dumps(output,indent=2)+'\n')
