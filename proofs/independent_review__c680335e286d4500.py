#!/usr/bin/env python3
"""Independent sequential-column replay of the frozen 177 control records."""
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def value(ds, b):
    total = 0
    for d in reversed(ds):
        total = total*b + d
    return total

def normalize(q, b):
    out, carries = [], [0]
    for c in q:
        s = c + carries[-1]
        out.append(s % b)
        carries.append(s // b)
    if carries[-1]:
        out.append(carries[-1])
    assert 0 < out[-1] < b and all(0 <= d < b for d in out)
    return out, carries

def main():
    data = json.loads((HERE/'controls.json').read_text())
    rows = data['records']
    assert len(rows) == 177
    assert len({(r['base'], tuple(r['initial_pair_word'])) for r in rows}) == 177
    checks = Counter()
    transition_count = 0
    for row in rows:
        b = row['base']; q = row['initial_pair_word']; n = row['seed']
        assert b >= 3 and q == q[::-1] and q[0] >= b
        assert all(0 <= x <= 2*b-2 for x in q)
        ds = [(n // b**i) % b for i in range(len(q))]
        assert ds[-1] > 0 and value(ds, b) == n
        assert [x+y for x,y in zip(ds, reversed(ds))] == q
        words, integers, pal, all_carries = [q], [n], [ds == ds[::-1]], []
        for t in range(4):
            ds, carry = normalize(words[-1], b)
            all_carries.append(carry)
            integers.append(value(ds, b))
            pal.append(ds == ds[::-1])
            words.append([x+y for x,y in zip(ds, reversed(ds))])
            transition_count += 1
        assert integers == row['integers'] and pal == row['palindromic']
        assert words == row['pair_words']
        labels = []
        a = q[0]-b+1
        if 2*a >= b+2:
            assert not pal[1] and not pal[3]
            assert words[2][0] >= b and words[2][0] != b+1
            labels.append('universal_exterior_third_safety')
        if len(q) >= 2 and min(q) >= b-1:
            r = [x-b+1 for x in q]
            expected = [a] + [r[i]+r[i+1] for i in range(len(r)-1)] + [a]
            assert words[1] == expected
            labels.append('exact_first_high_carry_map')
            if q[0] == 2*b-2 and q[1] >= b+1:
                assert words[2][:2] == [b, q[1]-b] and not pal[3]
                labels.append('maximum_exterior_regeneration')
            z = expected[1]
            if 2*a >= b-1 and a <= b-2 and b+1 <= z <= b+(b-2)//2:
                v = all_carries[1][len(q)-1]
                assert words[2][:2] == [2*a+1, 2*(z-b)+v]
                assert words[2][0] >= b and 1 <= words[2][1] < b
                assert not pal[3]
                labels.append('nonoverflowing_exterior_regeneration')
            if b == 10 and any(x.endswith('regeneration') for x in labels):
                assert not any(pal[1:4])
                labels.append('three_safe_positive_outputs')
            sums = [q[i]+q[i+1] for i in range(len(q)-1)]
            if b == 10 and len(q) >= 3 and q[0] <= 17 and min(sums) >= 28:
                explicit = [2*q[0]-17]
                for i in range(1,len(q)):
                    explicit.append(2*sums[i-1]-(55 if i in (1,len(q)-1) else 54))
                explicit.append(explicit[0])
                assert words[2] == explicit
                high = words[2][0] >= 10 and min(words[2]) >= 9 and max(words[2]) <= 18
                assert high == (min(sums) >= 32)
                labels.append('restricted_high_region_return_iff')
        assert labels == row['checked']
        checks.update(labels)
    boundary = data['boundary_recurrence_controls']
    expected_starts = {(a,b) for a in range(14,18) for b in range(9,19) if a+b >= 32}
    assert {tuple(p[0]) for p in boundary} == expected_starts and len(boundary) == 10
    for path in boundary:
        assert len(path) == 3
        for (a,b), target in zip(path,path[1:]):
            assert target == [2*a-17,2*a+2*b-55]
        assert min(sum(path[1]),sum(path[2])) < 32
    sharp = next(r for r in rows if r['base']==10 and r['initial_pair_word']==[17,18,18,17])
    assert sharp['pair_words'][2] == [17,15,18,15,17]
    assert sharp['pair_words'][4] == [17,9,12,12,9,17]
    rejected = data['rejected_generalization']
    assert rejected['counterexample_initial_pair_word'] == [15,18,18,15]
    assert rejected['second_pair_word'] == [13,11,18,11,13]
    report = {
        'result':'PASS_INDEPENDENT_SEQUENTIAL_CARRY_REPLAY_AND_MATH_REVIEW',
        'method':'Sequential coefficient normalization with explicit carry list; no producer import or integer-reversal routine.',
        'control_count':len(rows), 'transitions':transition_count,
        'checks':dict(sorted(checks.items())), 'boundary_controls':len(boundary),
        'scope':'All-parameter proof independently read; these finite controls verify formulas and short-width cases, not infinite persistence or a Lean formalization.',
        'source_snapshot':{name:sha(HERE/name) for name in ['HIGH_CARRY_RENEWAL.md','check_renewal.py','controls.json','verification.json','root_review.json','independent_review.py']}
    }
    (HERE/'independent_review.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
