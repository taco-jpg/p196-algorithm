#!/usr/bin/env python3
"""Complete small-word/all-partition controls for the raw symmetry proof."""

from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json


HERE = Path(__file__).resolve().parent


def words(width):
    count = (width + 1) // 2
    alphabets = [range(1, 19)] + [range(19)] * (count - 1)
    if width % 2:
        alphabets[-1] = range(2, 19, 2) if width == 1 else range(0, 19, 2)
    for half in product(*alphabets):
        yield half + (half[-2::-1] if width % 2 else half[::-1])


def normalize(q):
    carry, digits, outgoing = 0, [], []
    for coefficient in q:
        carry, digit = divmod(coefficient + carry, 10)
        digits.append(digit)
        outgoing.append(carry)
    if carry:
        digits.append(carry)
    return digits, outgoing


def inspect(q, mask):
    length = len(q)
    d, actual = normalize(q)
    e, isolated, seam = [0] * (length + 1), [0] * length, [0] * length
    ends = [i + 1 for i in range(length - 1) if mask & (1 << i)] + [length]
    start = 0
    for end in ends:
        digits, carries = normalize(q[start:end])
        for i, digit in enumerate(digits):
            e[start + i] += digit
        isolated[start:end] = carries
        if start and actual[start - 1]:
            for i in range(start, end):
                if q[i] != 9:
                    break
                seam[i] += 1
        start = end
    assert all(e[i] == 0 for i in range(len(d), len(e)))
    assert seam == [a - c for a, c in zip(actual, isolated)]
    for i in range(length + 1):
        qi = q[i] if i < length else 0
        ci = isolated[i] if i < length else 0
        previous = isolated[i - 1] if i else 0
        assert e[i] == qi - 10 * ci + previous
        ki = seam[i] if i < length else 0
        kp = seam[i - 1] if i else 0
        di = d[i] if i < len(d) else 0
        assert di == e[i] - 10 * ki + kp
    raw = e[:len(d)]
    palindrome = d == d[::-1]
    raw_symmetric = raw == raw[::-1]
    classification = all(a <= 9 for a in q) or (q[0] == 11 and all(a in (0, 11) for a in q))
    assert palindrome == raw_symmetric == classification
    assert not (raw_symmetric and any(seam))
    assert all(-2 <= a - 11 * c <= 9 for a, c in zip(q, isolated))
    flags = (int(palindrome) | (int(raw_symmetric) << 1) | (int(any(seam)) << 2)
             | ((len(d) - length) << 3) | (int(any(a >= 10 for a in e)) << 4))
    return flags, dict(pair_word=q, cut_mask=mask, actual_digits=d,
                       raw_isolated_sum=e, isolated_carries=isolated,
                       actual_carries=actual, seam_mask=seam)


def main():
    catalog, rows, counts = bytearray(), [], Counter()
    for width in range(1, 6):
        word_count, cases = 0, 0
        for q in words(width):
            word_count += 1
            d, _ = normalize(q)
            # Independent ordinary-integer normalization check for each word.
            value = sum(a * 10**i for i, a in enumerate(q))
            assert ''.join(map(str, reversed(d))) == str(value)
            for mask in range(1 << (width - 1)):
                flags, _ = inspect(q, mask)
                catalog.append(flags)
                counts[str(flags)] += 1
                cases += 1
        rows.append(dict(width=width, words=word_count, partitions=cases))
    assert len(catalog) == 58221
    examples = [inspect((9, 9, 18, 9, 9), 6)[1], inspect((12, 12), 1)[1]]
    artifact = HERE / 'raw_symmetry_controls.bin.gz'
    with artifact.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', filename='', mtime=0) as stream:
            stream.write(catalog)
    report = dict(status='PASS', cases=len(catalog), by_width=rows,
                  outcome_counts=dict(sorted(counts.items())), examples=examples,
                  artifact=dict(filename=artifact.name,
                                sha256=sha256(artifact.read_bytes()).hexdigest(),
                                encoding='One outcome byte per case',
                                order='width1..5; admissible half-words lexicographic; cut mask ascending',
                                cut_mask='bit i cuts after column i; all blocks nonempty',
                                bits={'0':'actual palindrome', '1':'raw symmetry at actual output width',
                                      '2':'nonzero seam mask', '3':'whole overflow',
                                      '4':'raw isolated sum has a coefficient at least10'}),
                  scope='Finite all-partition controls for the accompanying all-length algebraic proof; no iterative invariant is claimed.')
    (HERE / 'raw_symmetry_controls.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('outcome_counts', 'examples')}))


if __name__ == '__main__':
    main()
