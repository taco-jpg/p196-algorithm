#!/usr/bin/env python3
"""Finite author controls using literal integer reverse-and-add, not Lean code.

These checks do not prove an unbounded theorem and are not independent review.
The authoritative universal arguments are the kernel-checked Lean modules.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def step(n: int) -> int:
    return n + int(str(n)[::-1])


def word(n: int) -> tuple[list[int], list[int], list[int]]:
    digits = list(map(int, str(n)[::-1]))
    q = [a + b for a, b in zip(digits, reversed(digits))]
    carries = [0]
    out = []
    for x in q:
        out.append((x + carries[-1]) % 10)
        carries.append((x + carries[-1]) // 10)
    return q, carries, out


def slot(e, o, i: int) -> tuple[int, int, int, int]:
    eq, ec, _ = e
    oq, oc, od = o
    delay = od[len(oq) - i] if i else oc[-1]
    return ec[i], oc[i], ec[len(eq) - i], delay - oc[len(oq) - i]


def valid(s: tuple[int, int, int, int]) -> bool:
    a, b, c, z = s
    return all(v in (0, 1) for v in (a, b, c)) and -1 <= z <= 9


def tile(outer, inner, q: int, r: int, e: int, q_next: int) -> bool:
    a, b, c, z = outer
    aa, bb, cc, zz = inner
    return (valid(outer) and valid(inner) and 0 <= q <= 18 and 0 <= r <= 18
            and e in (0, 1) and r == zz + 10*e and (r >= 9 or e == 0)
            and (r <= 9 or e == 1) and (q+a)//10 == aa
            and (q+a)%10 + (q+cc)%10 == r and (r+b)//10 == bb
            and c == (q+cc)//10 and q_next == (r+b)%10 + z + e
            and 0 <= z+e <= 9)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--max-seed', type=int, default=5000)
    p.add_argument('--pairs', type=int, default=8)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.max_seed < 1 or args.pairs < 1:
        p.error('Both finite bounds must be positive')
    count_pairs = count_tiles = 0
    for seed in range(1, args.max_seed + 1):
        n = seed
        for _ in range(args.pairs):
            m, k = step(n), step(step(n))
            en, on, kn = word(n), word(m), word(k)
            if en[1][-1] == 0 and on[1][-1] == 1:
                count_pairs += 1
                assert slot(en, on, 0) == (0,0,0,0)
                for i in range(min(len(en[0]),len(on[0]))):
                    assert tile(slot(en,on,i), slot(en,on,i+1),
                                en[0][i],on[0][i],on[1][len(on[0])-i],kn[0][i]), (seed,n,i)
                    count_tiles += 1
            n = k
    assert step(15) == 66 and step(66) == 132
    assert word(15)[0] == [6,6] and word(66)[0] == [12,12]
    assert (word(15)[1][-1], word(66)[1][-1]) == (0,1)
    assert word(132)[0][0] == 3
    assert step(1330) == 1661 and step(1661) == 3322
    assert word(1330)[0] == [1,6,6,1] and word(1661)[0] == [2,12,12,2]
    assert (word(1330)[1][-1], word(1661)[1][-1]) == (0,0)
    result = {
        'status':'PASS', 'classification':'FINITE_AUTHOR_CONTROL_NOT_PROOF_OR_INDEPENDENT_REVIEW',
        'max_seed':args.max_seed,'temporal_pairs_per_seed':args.pairs,
        'matching_actual_nonoverflow_overflow_pairs':count_pairs,'exact_tiles_checked':count_tiles,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'finished_utc':datetime.now(timezone.utc).isoformat(),
        'controls':{'finite_prefix_example':[15,66,132],
                    'phase_does_not_force_overflow_alternation':[1330,1661,3322]},
        'limitations':['Finite range only; not an infinite trajectory proof.',
                       'Written and executed by Agent112, not an independent reviewer.',
                       'Iteration deliberately continues after a palindrome.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
