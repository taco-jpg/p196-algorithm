"""Independent replay and cardinality check of every short-word partition.

This checker obtains decimal digits by ordinary string conversion and
recovers K by exact division of D-E by x-10. It imports no other module
from the project and does not use the generator's prefix-quotient method.
"""
from collections import Counter
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
path = HERE/'short_controls.json.gz'
raw = gzip.decompress(path.read_bytes())
data = json.loads(raw)
words = data['words']
assert len(words) == len({tuple(w) for w in words}) == 3969
word_widths = Counter()
for word in words:
    L = len(word)
    assert 1 <= L <= 5 and word == word[::-1] and 1 <= word[0] <= 18
    assert all(0 <= q <= 18 for q in word)
    assert L % 2 == 0 or word[L//2] % 2 == 0
    word_widths[L] += 1
expected_widths = {1:9, 2:18, 3:18*10, 4:18*19, 5:18*19*10}
assert dict(word_widths) == expected_widths


def numeral(coefficients):
    n = 0
    for coefficient in reversed(coefficients):
        n = 10*n+coefficient
    return n


def digits(n, width):
    result = list(map(int, str(n)[::-1]))
    assert len(result) <= width
    return result+[0]*(width-len(result))


seen = set()
counts = Counter()
for word_id, mask, gamma, E, K, D in data['cases']:
    word = words[word_id]
    L = len(word)
    assert 0 <= mask < 2**(L-1)
    assert (word_id, mask) not in seen
    seen.add((word_id, mask))
    n = numeral(word)
    actual_width = len(str(n))
    assert gamma == actual_width-L and gamma in (0, 1)
    assert D == digits(n, actual_width)
    isolated_sum = [0]*(L+1)
    cuts = [0]+[i+1 for i in range(L-1) if mask >> i & 1]+[L]
    for start, end in zip(cuts, cuts[1:]):
        block = word[start:end]
        isolated_digits = digits(numeral(block), len(block)+1)
        for i, d in enumerate(isolated_digits):
            isolated_sum[start+i] += d
    assert E == isolated_sum[:actual_width]
    assert not any(isolated_sum[actual_width:])
    padded_D = D+[0]*(L+1-len(D))
    recovered = []
    previous = 0
    for index in range(L):
        numerator = previous+isolated_sum[index]-padded_D[index]
        assert numerator % 10 == 0
        current = numerator//10
        assert current in (0, 1)
        recovered.append(current)
        previous = current
    assert isolated_sum[L]+previous == padded_D[L]
    assert recovered == K
    assert 2*sum(D) == 2*sum(E)-18*sum(K)
    symmetric_E = E == E[::-1]
    assert symmetric_E == (D == D[::-1])
    if any(K):
        assert D != D[::-1]
    if symmetric_E:
        assert not any(K)
        assert (all(q <= 9 for q in word) if gamma == 0 else set(word) <= {0, 11})
        counts[f'symmetric_E_gamma{gamma}'] += 1
    counts['nonzero_K'] += bool(any(K))
    counts['total'] += 1
assert len(seen) == sum(expected_widths[L]*2**(L-1) for L in range(1, 6)) == 58221
# Independent closed-form count of the two exact symmetry classes.
assert counts['symmetric_E_gamma0'] == 4+9*2+(9*5)*4+(9*10)*8+(9*10*5)*16 == 8122
assert counts['symmetric_E_gamma1'] == 0+1*2+1*4+2*8+2*16 == 54
assert counts['nonzero_K'] == 2100
result = dict(status='INDEPENDENT_COMPLETE_SHORT_REPLAY_PASS',
              source_content_sha256=hashlib.sha256(raw).hexdigest(),
              canonical_words=len(words), canonical_partition_cases=len(seen),
              counts=dict(counts), independent_decimal_conversion=True,
              K_recovered_by_polynomial_division=True, exhaustive_width_range=[1, 5],
              canonical_nonzero_K_safety_cases=counts['nonzero_K'],
              imports_generator=False)
(HERE/'short_controls_audit.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
