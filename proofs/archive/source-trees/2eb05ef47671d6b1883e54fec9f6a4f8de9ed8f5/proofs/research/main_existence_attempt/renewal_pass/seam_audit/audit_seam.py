"""Independent whole-word seam replay and exhaustive short vacuity controls.

No generator, prior transducer, or prior normalization helper is imported.
Carries are obtained from integer prefix quotients. The unrestricted proof
is in METHOD_AND_PROOF.md; finite controls audit it, not replace it.
"""
from collections import Counter
from pathlib import Path
import gzip
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'constructive/collision_response'


def value(word):
    return sum(q*10**i for i, q in enumerate(word))


def normal_by_integer(word):
    n = value(word)
    length = len(word)
    digits = [n//10**i % 10 for i in range(length)]
    final = n//10**length
    assert final in (0, 1)
    prefix = 0
    carries = []
    for index, q in enumerate(word):
        prefix += q*10**index
        carries.append(prefix//10**(index+1))
    assert all(c in (0, 1) for c in carries)
    return digits, final, carries


def canonical(word):
    return (bool(word) and word[0] > 0 and word == word[::-1]
            and all(0 <= q <= 18 for q in word)
            and (len(word) % 2 == 0 or word[len(word)//2] % 2 == 0))


def realize(word):
    p = word[:len(word)//2]
    digits = [max(0, q-9) for q in p]
    if len(word) % 2:
        digits.append(word[len(word)//2]//2)
    digits.extend(min(9, q) for q in reversed(p))
    return value(digits)


def reverse(n):
    result = 0
    while n:
        result = result*10+n % 10
        n //= 10
    return result


def inspect(blocks):
    whole = [q for block in blocks for q in block]
    assert blocks and all(block for block in blocks)
    assert all(0 <= q <= 18 for q in whole)
    L = len(whole)
    E = [0]*(L+1)
    isolated = []
    incoming = []
    expected_mask = [0]*L
    block_records = []
    start = actual_incoming = 0
    isolated_mass = 0
    for block in blocks:
        digits, final, carries = normal_by_integer(block)
        ell = next((i for i, q in enumerate(block) if q != 9), len(block))
        transmit = int(ell == len(block))
        actual_final = (value(block)+actual_incoming)//10**len(block)
        assert actual_final == final+transmit*actual_incoming and not final*transmit
        for index, digit in enumerate(digits+[final]):
            E[start+index] += digit
        for index in range(ell):
            expected_mask[start+index] = actual_incoming
        isolated.extend(carries)
        incoming.extend([0]+carries[:-1])
        isolated_mass += 2*(sum(digits)+final)
        block_records.append(dict(start=start, incoming=actual_incoming,
                                  isolated_final=final, run9=ell, all9=transmit))
        start += len(block)
        actual_incoming = actual_final
    digits, gamma, whole_carries = normal_by_integer(whole)
    assert gamma == actual_incoming
    K = [c-s for c, s in zip(whole_carries, isolated)]
    assert K == expected_mask and all(k in (0, 1) for k in K)
    correction = [-10*k for k in K]+[0]
    for index, k in enumerate(K):
        correction[index+1] += k
    assert [e+h for e, h in zip(E, correction)] == digits+[gamma]
    if not gamma:
        assert E.pop() == correction.pop() == 0
    actual = digits+([1] if gamma else [])
    pair = [a+b for a, b in zip(actual, actual[::-1])]
    raw_pair = [a+b for a, b in zip(E, E[::-1])]
    assert pair == [a+b+c+d for a, b, c, d in zip(E, E[::-1], correction, correction[::-1])]
    assert sum(pair) == isolated_mass-18*sum(K)
    assert (pair == raw_pair) == (not any(K))
    is_canonical = canonical(whole)
    symmetric_E = E == E[::-1]
    symmetric_D = actual == actual[::-1]
    if symmetric_E and any(K):
        assert not symmetric_D
    if is_canonical:
        n = realize(whole)
        assert n+reverse(n) == value(whole)
        assert len(str(n+reverse(n))) == L+gamma
        assert symmetric_D == (n+reverse(n) == reverse(n+reverse(n)))
        assert symmetric_E == symmetric_D
        if any(K):
            assert not symmetric_D
        if symmetric_E:
            assert not any(K)
            if gamma:
                assert whole[0] == 11 and set(whole) <= {0, 11}
                R = isolated[::-1]
                S = 0
                for q, c, r, tau in zip(whole, isolated, R, incoming):
                    assert q == 10*c+r+9*S
                    assert 0 <= r+9*S+tau <= 9
                    assert S == 0 and c == r and q == 11*c
                    S += c-r
                assert S == 0
            else:
                assert not any(isolated) and all(q <= 9 for q in whole)
    return dict(whole=whole, blocks=block_records, gamma=gamma, E=E, K=K,
                D=actual, isolated_carries=isolated, isolated_incoming=incoming,
                canonical=is_canonical, symmetric_E=symmetric_E, symmetric_D=symmetric_D,
                mass_loss=18*sum(K))


def partitions(word):
    for mask in range(1 << (len(word)-1)):
        blocks = []
        start = 0
        for index in range(len(word)-1):
            if mask >> index & 1:
                blocks.append(word[start:index+1])
                start = index+1
        blocks.append(word[start:])
        yield mask, blocks


def canonical_words(width):
    pairs = width//2
    if pairs == 0:
        for c in range(2, 19, 2):
            yield [c]
        return
    for first in range(1, 19):
        for tail in itertools.product(range(19), repeat=pairs-1):
            p = [first]+list(tail)
            if width % 2:
                for c in range(0, 19, 2):
                    yield p+[c]+p[::-1]
            else:
                yield p+p[::-1]


def main():
    source = SOURCE/'seam_response_cases.json.gz'
    raw = gzip.decompress(source.read_bytes())
    records = json.loads(raw)
    old_summary = json.loads((SOURCE/'seam_response.json').read_text())
    assert hashlib.sha256(raw).hexdigest() == old_summary['full_record_sha256']
    old_counts = Counter()
    for row in records:
        result = inspect(row['words'])
        assert result['blocks'] == row['blocks']
        assert result['gamma'] == row['gamma']
        assert result['K'] == row['carry_mask']
        assert result['D'] == row['actual_digits']
        assert result['mass_loss'] == row['mass_loss']
        assert result['canonical'] == row['canonical_whole']
        assert result['symmetric_E'] == row['raw_symmetric']
        old_counts['total'] += 1
        old_counts['canonical'] += result['canonical']
        old_counts['nonzero_K'] += bool(any(result['K']))
        if result['canonical'] and any(result['K']):
            old_counts['canonical_nonzero_K_safe'] += 1
            old_counts[f'canonical_nonzero_K_safe_gamma{result["gamma"]}'] += 1
        old_counts['symmetric_E_nonzero_K'] += result['symmetric_E'] and any(result['K'])
        if result['canonical'] and result['symmetric_E']:
            old_counts[f'canonical_symmetric_E_gamma{result["gamma"]}'] += 1
    assert old_counts['total'] == old_summary['total_cases'] == 2737
    assert old_counts['canonical'] == old_summary['canonical_ordinary_integer_controls'] == 1767
    assert old_counts['nonzero_K'] == old_summary['nonzero_correction_cases'] == 645

    words = []
    controls = []
    counts = Counter()
    by_width = {}
    for width in range(1, 6):
        word_count = partition_count = 0
        for word in canonical_words(width):
            word_index = len(words)
            words.append(word)
            word_count += 1
            for mask, blocks in partitions(word):
                result = inspect(blocks)
                controls.append([word_index, mask, result['gamma'], result['E'], result['K'], result['D']])
                counts['total'] += 1
                counts['nonzero_K'] += bool(any(result['K']))
                if result['symmetric_E']:
                    counts[f'symmetric_E_gamma{result["gamma"]}'] += 1
                counts['symmetric_E_nonzero_K'] += result['symmetric_E'] and any(result['K'])
                partition_count += 1
        expected_words = 9 if width == 1 else 18*19**(width//2-1)*(10 if width % 2 else 1)
        assert word_count == expected_words
        assert partition_count == word_count*2**(width-1)
        by_width[width] = dict(words=word_count, partitions=partition_count)

    examples = []
    for label, word in [('nonsymmetric_gamma0', [11, 9, 1]),
                        ('nonsymmetric_gamma1', [11, 11, 9, 0, 10, 9, 12])]:
        result = inspect([[q] for q in word])
        assert result['symmetric_E'] and any(result['K']) and not result['canonical']
        examples.append(dict(label=label, partition=[[q] for q in word], **result))
    archive = dict(status='EXHAUSTIVE_CANONICAL_WIDTHS_1_THROUGH_5',
                   case_schema=['word_index', 'cut_mask', 'gamma', 'E', 'K', 'D'],
                   cut_mask_semantics='bit i cuts between columns i and i+1',
                   words=words, cases=controls, noncanonical_boundary_examples=examples)
    payload = json.dumps(archive, separators=(',', ':'), sort_keys=True).encode()
    (HERE/'short_controls.json.gz').write_bytes(gzip.compress(payload, mtime=0))
    (HERE/'noncanonical_examples.json').write_text(json.dumps(examples, indent=2)+'\n')
    result = dict(status='INDEPENDENT_SEAM_AND_VACUITY_AUDIT_PASS',
                  source_archive_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  source_content_sha256=hashlib.sha256(raw).hexdigest(),
                  original_case_counts=dict(old_counts), exhaustive_counts=dict(counts),
                  canonical_words=len(words), canonical_partitions=len(controls), by_width=by_width,
                  short_archive_content_sha256=hashlib.sha256(payload).hexdigest(),
                  short_archive_bytes=(HERE/'short_controls.json.gz').stat().st_size,
                  noncanonical_examples=len(examples),
                  universal_seam_identity_valid=True, mass_iff_valid=True,
                  canonical_symmetric_E_nonzero_K_antecedent='IMPOSSIBLE_BY_UNRESTRICTED_PROOF',
                  canonical_nonzero_K_alone='SUFFICIENT_FOR_ONE_STEP_SAFETY',
                  positive_invariant_found=False)
    (HERE/'seam_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
