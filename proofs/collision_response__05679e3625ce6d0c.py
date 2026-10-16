"""Zero-spacer carry-response and exact independent-update classification.

The all-parameter proof is in COLLISION_RESPONSE.md.  These are independent
ordinary-integer controls, not finite evidence substituted for that proof.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
import random


def canonical(word):
    return (bool(word) and word == word[::-1] and 1 <= word[0] <= 18
            and all(0 <= x <= 18 for x in word)
            and (len(word) % 2 == 0 or word[len(word)//2] % 2 == 0))


@lru_cache(maxsize=None)
def fixed(word, incoming=0):
    value = sum(c*10**i for i, c in enumerate(word))+incoming
    outgoing, remainder = divmod(value, 10**len(word))
    digits = []
    for _ in word:
        remainder, d = divmod(remainder, 10)
        digits.append(d)
    assert outgoing in (0, 1) and remainder == 0
    return tuple(digits), outgoing


def full(word):
    digits, outgoing = fixed(word)
    return digits+((outgoing,) if outgoing else ())


def pair(digits):
    return tuple(a+b for a, b in zip(digits, digits[::-1]))


def leading_nines(word):
    for i, c in enumerate(word):
        if c != 9:
            return i
    return len(word)


def add_shift(target, word, offset, multiplier=1):
    for i, coefficient in enumerate(word):
        target[offset+i] += multiplier*coefficient


def realize(q):
    assert canonical(q)
    d = [0]*len(q)
    for i in range(len(q)//2):
        d[i] = max(0, q[i]-9)
        d[-1-i] = q[i]-d[i]
    if len(q) % 2:
        d[len(q)//2] = q[len(q)//2]//2
    return int(''.join(map(str, d[::-1])))


def kind(word):
    return { (0, 0): 'reset0', (0, 1): 'identity', (1, 1): 'reset1' }[
        (fixed(word, 0)[1], fixed(word, 1)[1])]


def check_response(word):
    zero, f0 = fixed(word, 0)
    one, f1 = fixed(word, 1)
    k = leading_nines(word)
    assert (f1-f0) == (k == len(word))
    expected = tuple(-9 if i < k else 1 if i == k else 0
                     for i in range(len(word)))
    assert tuple(b-a for a, b in zip(zero, one)) == expected


def control(b, h):
    assert canonical(b) and canonical(h)
    check_response(b)
    check_response(h)
    lb, lh = len(b), len(h)
    total, high_start = 2*lb+lh, lb+lh
    kb, kh = leading_nines(b), leading_nines(h)
    e = fixed(b, 0)[1]
    independent_h = fixed(h, 0)[1]
    core_out = fixed(h, e)[1]
    final = fixed(b, core_out)[1]
    q = b+h+b
    seed = realize(q)
    successor = seed+int(str(seed)[::-1])
    digits = tuple(map(int, str(successor)[::-1]))
    width = total+final
    assert len(digits) == width

    p = [0]*width
    add_shift(p, full(b), 0)
    add_shift(p, full(h), lb)
    add_shift(p, full(b), high_start)
    f = [0]*width
    add_shift(f, (1,)*kh, lb, e)
    add_shift(f, (1,)*kb, high_start, core_out)
    defect = [-10*x for x in f]
    for i in range(1, width):
        defect[i] += f[i-1]
    assert f[-1] == 0
    support = set()
    if e and kh:
        support.update(range(lb, lb+kh+1))
    if core_out and kb:
        support.update(range(high_start, high_start+kb+1))
    assert all(not coefficient or i in support for i, coefficient in enumerate(defect))
    assert tuple(x+y for x, y in zip(p, defect)) == digits
    assert sum(digits) == sum(p)-9*(e*kh+core_out*kb)
    g = pair(digits)
    target = pair(tuple(p))
    pair_defect = pair(tuple(defect))
    paired_support = support | {width-1-i for i in support}
    assert all(not coefficient or i in paired_support
               for i, coefficient in enumerate(pair_defect))
    assert tuple(x-y for x, y in zip(g, target)) == pair_defect
    assert (g == target) == (e*kh+core_out*kb == 0)

    independent_target = [0]*width
    add_shift(independent_target, pair(full(b)), 0)
    add_shift(independent_target, pair(full(h)), lb)
    add_shift(independent_target, pair(full(b)), high_start)
    criterion = ((e == 0 and independent_h == 0)
                 or (b[0] >= 10 and h[0] >= 10))
    assert (g == tuple(independent_target)) == criterion
    return {
        'B': b, 'H': h, 'carry_types': [kind(b), kind(h)],
        'prefix9_lengths': [kb, kh],
        'boundary_carries': [0, e, core_out, final],
        'independent_overflow_bits': [e, independent_h],
        'whole_physical_digit_width': width,
        'normalized_digits_low_to_high': digits,
        'formal_independent_digits_P': p,
        'propagation_polynomial_F': f,
        'digit_defect_D_minus_P': defect,
        'paired_defect': pair_defect,
        'paired_mass_loss': 18*(e*kh+core_out*kb),
        'raw_independent_pair_identity_holds': criterion,
    }


def catalog():
    result = []
    for length in (1, 2, 3):
        for left in product(range(19), repeat=length//2):
            for center in (range(0, 19, 2) if length % 2 else (None,)):
                q = tuple(left)+(tuple() if center is None else (center,))+tuple(left[::-1])
                if canonical(q):
                    result.append(q)
    return result


def random_word(rng):
    length = rng.randrange(1, 13)
    left = [rng.randrange(19) for _ in range(length//2)]
    middle = [2*rng.randrange(10)] if length % 2 else []
    if left:
        left[0] = rng.randrange(1, 19)
    else:
        middle[0] = 2*rng.randrange(1, 10)
    return tuple(left+middle+left[::-1])


def main():
    small = catalog()
    rng = random.Random(1960914)
    counts = Counter()
    representatives = {}
    checks = 0
    for b, h in product(small, repeat=2):
        result = control(b, h)
        key = (tuple(result['carry_types']), result['paired_mass_loss'] > 0,
               result['raw_independent_pair_identity_holds'])
        counts[str(key)] += 1
        representatives.setdefault(str(key), result)
        checks += 1
    for _ in range(3000):
        control(random_word(rng), random_word(rng))
        checks += 1
    explicit = [control(b, h) for b, h in (
        ((9, 0, 9), (11, 0, 11)),
        ((9, 9), (11, 0, 11)),
        ((11, 0, 11), (9, 9)),
        ((9, 10, 9), (11, 0, 11)),
        ((11, 0, 11), (11, 0, 11)),
    )]
    output = {
        'status': 'finite controls of proved all-parameter identities',
        'exhaustive_component_widths': [1, 2, 3],
        'canonical_components': len(small),
        'exhaustive_pairs': len(small)**2,
        'deterministic_longer_pairs': 3000,
        'total_independent_integer_controls': checks,
        'exhaustive_case_counts': dict(counts),
        'representatives': list(representatives.values()),
        'explicit_neutral_and_prefix_examples': explicit,
        'all_time_safety_claimed': False,
        'repeatable_reset_claimed': False,
    }
    Path(__file__).with_name('COLLISION_CONTROLS.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k: v for k, v in output.items()
                      if k not in ('representatives', 'explicit_neutral_and_prefix_examples')}, indent=2))


if __name__ == '__main__':
    main()
