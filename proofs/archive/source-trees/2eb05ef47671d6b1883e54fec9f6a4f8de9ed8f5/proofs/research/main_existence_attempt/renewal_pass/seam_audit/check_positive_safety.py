"""Independent ordinary-integer check of every saved active canonical seam.

The seam masks are reconstructed from actual incoming carries and the
initial 9-runs, without importing the seam generator or audit code.
"""
from collections import Counter
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'constructive/collision_response'


def integer(coefficients):
    value = 0
    for q in reversed(coefficients):
        value = 10*value+q
    return value


def reverse(n):
    result = 0
    while n:
        result = result*10+n % 10
        n //= 10
    return result


def check(blocks, expected, source, index):
    whole = [q for block in blocks for q in block]
    assert whole == whole[::-1] and whole[0] > 0
    assert len(whole) % 2 == 0 or whole[len(whole)//2] % 2 == 0
    length = len(whole)
    K = [0]*length
    start = 0
    for block in blocks:
        incoming = integer(whole[:start])//10**start
        assert incoming in (0, 1)
        for position, q in enumerate(block):
            if q != 9:
                break
            K[start+position] = incoming
        start += len(block)
    assert K == expected and any(K)
    # Direct structural proof: an active seam supplies both an input 9
    # and an earlier coefficient that generated carry from initial zero.
    active = next(i for i, k in enumerate(K) if k)
    assert whole[active] == 9
    assert any(q >= 10 for q in whole[:active])
    p = whole[:length//2]
    digits = [max(0, q-9) for q in p]
    if length % 2:
        digits.append(whole[length//2]//2)
    digits.extend(min(9, q) for q in reversed(p))
    seed = integer(digits)
    output = seed+reverse(seed)
    assert output == integer(whole)
    assert output != reverse(output)
    gamma = len(str(output))-length
    assert gamma in (0, 1)
    return dict(source=source, index=index, whole=whole, K=K, gamma=gamma,
                canonical_seed=str(seed), first_output=str(output), safe=True)


def main():
    with gzip.open(SOURCE/'seam_response_cases.json.gz', 'rt') as stream:
        original = json.load(stream)
    with gzip.open(HERE/'short_controls.json.gz', 'rt') as stream:
        short = json.load(stream)
    controls = []
    counts = Counter()
    for index, row in enumerate(original):
        whole = [q for block in row['words'] for q in block]
        canonical = (whole[0] > 0 and whole == whole[::-1]
                     and (len(whole) % 2 == 0 or whole[len(whole)//2] % 2 == 0))
        assert canonical == row['canonical_whole']
        if canonical and any(row['carry_mask']):
            result = check(row['words'], row['carry_mask'], 'original', index)
            controls.append(result)
            counts['original'] += 1
            counts[f'original_gamma{result["gamma"]}'] += 1
    for index, (word_id, mask, gamma, E, K, D) in enumerate(short['cases']):
        if not any(K):
            continue
        whole = short['words'][word_id]
        cuts = [0]+[i+1 for i in range(len(whole)-1) if mask >> i & 1]+[len(whole)]
        blocks = [whole[a:b] for a, b in zip(cuts, cuts[1:])]
        result = check(blocks, K, 'short', index)
        controls.append(result)
        counts['short'] += 1
        counts[f'short_gamma{result["gamma"]}'] += 1
    assert counts['original'] == 395 and counts['original_gamma0'] == 91 and counts['original_gamma1'] == 304
    assert counts['short'] == 2100
    example = check([[9, 9], [18], [9, 9]], [0, 0, 0, 1, 1], 'explicit_BHB', 0)
    assert example['canonical_seed'] == '99900' and example['first_output'] == '100899'
    nonnecessity = dict(whole=[2, 2, 18, 2, 2], blocks=[[2, 2], [18], [2, 2]],
                       K=[0, 0, 0, 0, 0], canonical_seed='22900', first_output='23822')
    assert 22900+reverse(22900) == 23822 and 23822 != reverse(23822)
    assert all(q != 9 for q in nonnecessity['whole'])
    payload = json.dumps(dict(cases=controls, active_seam_example=example,
                             criterion_not_necessary_example=nonnecessity),
                         separators=(',', ':'), sort_keys=True).encode()
    archive = HERE/'positive_safety_controls.json.gz'
    archive.write_bytes(gzip.compress(payload, mtime=0))
    result = dict(status='ALL_CANONICAL_ACTIVE_SEAMS_SAFE',
                  checked_cases=len(controls), counts=dict(counts),
                  content_sha256=hashlib.sha256(payload).hexdigest(),
                  compressed_bytes=archive.stat().st_size,
                  active_seam_example=example, criterion_not_necessary_example=nonnecessity,
                  mask_recomputed_from_actual_prefix_carries=True,
                  ordinary_integer_outputs_checked=True,
                  recurrent_regeneration_proved=False, positive_invariant_found=False)
    (HERE/'positive_safety_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
