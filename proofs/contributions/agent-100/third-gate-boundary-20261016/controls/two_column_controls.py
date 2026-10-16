#!/usr/bin/env python3
"""Finite independent controls for the claimed two-column O,N boundary.

Exhausts admissible symmetric coefficient words of widths 2..10 with the
specified first two columns. Ordinary integer additions are primary; a
separate grade-school normalizer checks every output. This is not Lean proof.
"""
import gzip
import hashlib
import itertools
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def admissible(q):
    return (bool(q) and q[0] > 0 and q == q[::-1]
            and all(0 <= a <= 18 for a in q)
            and (len(q) % 2 == 0 or q[len(q) // 2] % 2 == 0))


def profiles(width, outer, second):
    """All independent symmetric coefficients, including small-width collisions."""
    length = (width + 1) // 2
    fixed = {}
    for pos, value in [(0, outer), (1, second)]:
        key = min(pos, width - 1 - pos)
        if key in fixed and fixed[key] != value:
            return
        fixed[key] = value
    domains = []
    for i in range(length):
        allowed = range(0, 19, 2) if width % 2 and i == length - 1 else range(19)
        if i in fixed:
            if fixed[i] not in allowed:
                return
            domains.append([fixed[i]])
        else:
            domains.append(allowed)
    for half in itertools.product(*domains):
        half = list(half)
        q = half + (half[-2::-1] if width % 2 else half[::-1])
        assert admissible(q)
        assert q[0] == outer and q[1] == second
        yield q


def digits(n):
    return [int(a) for a in str(n)[::-1]]


def pairs(d):
    return [x + y for x, y in zip(d, d[::-1])]


def realization(q):
    assert admissible(q)
    d = [0] * len(q)
    for i in range(len(q) // 2):
        high = min(9, q[i]) if i == 0 else max(0, q[i] - 9)
        d[-1 - i] = high
        d[i] = q[i] - high
    if len(q) % 2:
        d[len(q) // 2] = q[len(q) // 2] // 2
    assert d[-1] > 0 and all(0 <= x <= 9 for x in d)
    n = sum(x * 10 ** i for i, x in enumerate(d))
    assert digits(n) == d and pairs(d) == q
    return n


def normalize(q):
    carries, output = [0], []
    for value in q:
        c, digit = divmod(value + carries[-1], 10)
        carries.append(c)
        output.append(digit)
    if carries[-1]:
        output.append(carries[-1])
    return output, carries


def trajectory(q, steps):
    n = realization(q)
    ns, words, carries = [n], [q], []
    for _ in range(steps):
        output, carry = normalize(words[-1])
        nxt = ns[-1] + int(str(ns[-1])[::-1])
        assert digits(nxt) == output
        word = pairs(digits(nxt))
        assert admissible(word)
        ns.append(nxt)
        words.append(word)
        carries.append(carry)
    return ns, words, carries


def main():
    summary = {
        'status': 'FINITE_PASS_NOT_LEAN_PROOF',
        'claim_commit': '2a0d376388cacc83ceab1caf1f2152c195329964',
        'widths': list(range(2, 11)),
        'enumeration': 'Every admissible symmetric coefficient word with the stated fixed first two columns; free inner coefficients range over 0..18 and an odd center over 0,2,..18.',
        'realizations': 'One explicitly constructed canonical integer per coefficient word. Universal digit-split scope is not asserted by these controls.',
        'group_counts': [],
        'empty_groups': [],
        'representatives': [],
        'cases': 0,
        'ordinary_additions': 0,
    }
    decoded_hash = hashlib.sha256()
    decoded_bytes = 0
    payload = OUT / 'two-column-cases.jsonl.gz'
    with payload.open('wb') as raw, gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0, compresslevel=9) as archive:
        for width in range(2, 11):
            specs = [('sixteen_low', 16, z, z, 2) for z in [0, 1]]
            specs += [('sixteen_high', 16, 16 + z, z, 2) for z in [0, 1]]
            specs += [('seven_low', 7, second, None, 1) for second in range(9)]
            specs += [('seven_high', 7, second, None, 1) for second in range(10, 19)]
            for family, outer, second, z, steps in specs:
                count = 0
                first_record = None
                for q in profiles(width, outer, second):
                    ns, words, carries = trajectory(q, steps)
                    if second <= 8:
                        assert carries[0][-2] == 0
                    elif second >= 10:
                        assert carries[0][-2] == 1
                    if family.startswith('sixteen'):
                        expected_second = 7 + z if family == 'sixteen_low' else 14 + z
                        expected_outer = 14 if family == 'sixteen_low' else 15
                        assert carries[0][-1] == 1 and carries[1][-1] == 0
                        assert [len(w) for w in words] == [width, width + 1, width + 1]
                        assert words[1][:2] == [7, expected_second]
                        assert words[2][0] == expected_outer
                    else:
                        expected_outer = 14 if family == 'seven_low' else 15
                        assert carries[0][-1] == 0
                        assert len(words[1]) == width
                        assert words[1][0] == expected_outer
                    record = {'family': family, 'width': width, 'z': z,
                              'second': second, 'integers': ns,
                              'words': words, 'carries': carries}
                    encoded = (json.dumps(record, separators=(',', ':')) + '\n').encode()
                    archive.write(encoded)
                    decoded_hash.update(encoded)
                    decoded_bytes += len(encoded)
                    if first_record is None:
                        first_record = record
                    count += 1
                group = {'family': family, 'width': width, 'z': z, 'second': second, 'count': count}
                summary['group_counts'].append(group)
                summary['cases'] += count
                summary['ordinary_additions'] += count * steps
                if not count:
                    reason = 'Symmetry identifies column 1 with the outer column.' if width == 2 else 'Column 1 is the odd center and must be even.'
                    summary['empty_groups'].append(dict(group, reason=reason))
                elif family.startswith('sixteen') or width <= 3:
                    summary['representatives'].append(first_record)
    summary['trace'] = {'file': payload.name, 'stored_bytes': payload.stat().st_size,
                        'stored_sha256': hashlib.sha256(payload.read_bytes()).hexdigest(),
                        'decoded_bytes': decoded_bytes, 'decoded_sha256': decoded_hash.hexdigest()}
    summary['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT / 'two-column-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({k: summary[k] for k in ['status', 'cases', 'ordinary_additions', 'empty_groups', 'trace', 'source_sha256']}, indent=2))


if __name__ == '__main__':
    main()
