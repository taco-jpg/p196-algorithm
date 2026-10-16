"""Exact conditional seven-step 440-prefix return and finite realizations.

No recurring finite orbit is claimed.  This script preserves all finite
control words, the complete bounded catalog outcomes, and selected actual
ordinary trajectories, including failures of renewed eligibility.
"""
from __future__ import annotations

from collections import Counter
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path


PREFIX = (4, 4, 0)
ALPHA = (0, 0, 0, 0, 1, 1, 1)
OVERFLOWS = (0, 0, 1, 0, 1, 0, 1)
REQUIRED = {0: 0, 1: 0, 3: 0, 5: 0, 6: 1}


def normalize(word, incoming=0):
    retained, carries = [], [incoming]
    for x in word:
        carry, digit = divmod(x+carries[-1], 10)
        retained.append(digit)
        carries.append(carry)
    return tuple(retained), tuple(carries)


def pair(word):
    return tuple(x+y for x, y in zip(word, word[::-1]))


def prefix_step(prefix, high_incoming):
    lo, _ = normalize(prefix)
    hi, carries = normalize(prefix[::-1], high_incoming)
    overflow = carries[-1]
    if overflow:
        output = (lo[0]+1, lo[1]+hi[2], lo[2]+hi[1])
    else:
        output = (lo[0]+hi[2], lo[1]+hi[1], lo[2]+hi[0])
    return output, overflow


def full_step(word):
    retained, carries = normalize(word)
    digits = retained+((1,) if carries[-1] else ())
    return pair(digits), digits == digits[::-1], carries[-4], carries[-1]


def realize(q):
    assert q == q[::-1] and 1 <= q[0] <= 18
    assert all(0 <= x <= 18 for x in q)
    d = [0]*len(q)
    for i in range(len(q)//2):
        d[i] = max(0, q[i]-9)
        d[-1-i] = q[i]-d[i]
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        d[len(q)//2] = q[len(q)//2]//2
    return int(''.join(map(str, d[::-1])))


def core_map(h):
    """Evaluate the exact conditional core map; stop at first failed guard."""
    states, controls = [h], []
    for t in range(7):
        d, carries = normalize(h, ALPHA[t])
        c = carries[-1]
        controls.append(c)
        if t in REQUIRED and c != REQUIRED[t]:
            return {'eligible': False, 'first_failed_guard': t,
                    'expected_carry': REQUIRED[t], 'actual_carry': c,
                    'states': states, 'controls': controls}
        if not OVERFLOWS[t]:
            h = pair(d)
        else:
            h = list(pair(d+(0,)))
            edge = c if t == 2 else 5+c if t == 4 else 0
            h[0] += edge
            h[-1] += edge
            h = tuple(h)
        assert h == h[::-1] and all(0 <= x <= 18 for x in h)
        states.append(h)
    return {'eligible': True, 'first_failed_guard': None,
            'states': states, 'controls': controls, 'return_middle': h,
            'safe_seven_steps': max(states[0]) >= 10 and max(states[1]) >= 10}


def cycle(h, literal=False):
    q = PREFIX+h+PREFIX[::-1]
    n = realize(q) if literal else None
    ordinary_values = [str(n)] if literal else None
    states, controls, overflows, pals = [q], [], [], []
    for _ in range(7):
        new_q, pal, c, e = full_step(q)
        assert prefix_step(q[:3], c) == (new_q[:3], e)
        if literal:
            n += int(str(n)[::-1])
            actual_digits = tuple(map(int, str(n)[::-1]))
            assert pair(actual_digits) == new_q
            assert (str(n) == str(n)[::-1]) == pal
            ordinary_values.append(str(n))
        q = new_q
        states.append(q)
        controls.append(c)
        overflows.append(e)
        pals.append(pal)
    returns = q[:3] == PREFIX
    allowed = all(controls[t] == c for t, c in REQUIRED.items())
    assert returns == allowed
    cm = core_map(h)
    assert returns == cm['eligible']
    if returns:
        assert tuple(overflows) == OVERFLOWS
        assert len(q) == len(states[0])+3
        assert all(qt[3:-3] == ht for qt, ht in zip(states, cm['states']))
        assert (not any(pals)) == cm['safe_seven_steps']
    return {'returns': returns, 'safe': not any(pals), 'middle': q[3:-3],
            'controls': controls, 'overflows': overflows,
            'palindrome_steps': [i+1 for i, pal in enumerate(pals) if pal],
            'states': states, 'core_map': cm,
            'ordinary_realizing_seed_and_seven_iterates': ordinary_values}


def prefix_certificate():
    output = []
    for controls in product((0, 1), repeat=7):
        p, states, overflow = PREFIX, [PREFIX], []
        for c in controls:
            p, e = prefix_step(p, c)
            states.append(p)
            overflow.append(e)
        returns = p == PREFIX
        assert returns == all(controls[t] == c for t, c in REQUIRED.items())
        output.append({'controls': controls, 'prefixes': states,
                       'overflows': overflow, 'returns': returns})
    assert sum(r['returns'] for r in output) == 4
    return output


def canonical_cores(width):
    for left in product(range(19), repeat=width//2):
        if left and not left[0]:
            continue
        for middle in (range(0, 19, 2) if width % 2 else (None,)):
            h = left+(() if middle is None else (middle,))+left[::-1]
            if h[0]:
                yield h


def save_gzip(path, data):
    with path.open('wb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as compressed:
            compressed.write(data)
    return {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'uncompressed_bytes': len(data)}


def bounded_catalog(folder):
    summary, return_records, outcomes = [], [], bytearray()
    for width in range(1, 8):
        counts = Counter()
        for h in canonical_cores(width):
            counts['cores'] += 1
            first = cycle(h)
            flag = int(first['returns']) | (int(first['safe']) << 1)
            if first['returns']:
                counts['returns'] += 1
                record = {'middle': h, 'return_middle': first['middle'],
                          'controls': first['controls'], 'safe': first['safe']}
                if first['safe']:
                    counts['safe_returns'] += 1
                    second = cycle(first['middle'])
                    flag |= int(second['returns']) << 2
                    flag |= int(second['safe']) << 3
                    record['second'] = {'returns': second['returns'], 'safe': second['safe'],
                                        'controls': second['controls'],
                                        'middle_after_seven': second['middle']}
                    if second['returns']:
                        counts['second_returns_after_safe_first'] += 1
                        if second['safe']:
                            counts['two_safe_returns'] += 1
                            third = cycle(second['middle'])
                            flag |= int(third['returns']) << 4
                            flag |= int(third['safe']) << 5
                            record['third'] = {'returns': third['returns'], 'safe': third['safe'],
                                              'controls': third['controls'],
                                              'middle_after_seven': third['middle']}
                            if third['returns'] and third['safe']:
                                counts['three_safe_returns'] += 1
                                fourth = cycle(third['middle'])
                                flag |= int(fourth['returns']) << 6
                                flag |= int(fourth['safe']) << 7
                                counts['fourth_attempts_after_three_safe_returns'] += 1
                                record['fourth'] = {'returns': fourth['returns'], 'safe': fourth['safe'],
                                                   'controls': fourth['controls'],
                                                   'middle_after_seven': fourth['middle'],
                                                   'first_failed_guard': fourth['core_map']['first_failed_guard']}
                                if fourth['returns'] and fourth['safe']:
                                    counts['four_safe_returns'] += 1
                return_records.append(record)
            outcomes.append(flag)
        summary.append({'width': width, **dict(counts)})
    catalog_info = save_gzip(folder/'RETURN_CATALOG.json.gz',
                             (json.dumps(return_records, separators=(',', ':'))+'\n').encode())
    outcome_info = save_gzip(folder/'CATALOG_OUTCOMES.bin.gz', bytes(outcomes))
    return summary, catalog_info, outcome_info


def finite_examples():
    output = []
    for name, initial, expected_cycles in (
        ('one_safe_return', (1, 1, 16, 1, 1), 1),
        ('two_safe_returns_then_palindrome', (1, 1, 18, 1, 1), 2),
        ('three_safe_returns', (1, 1, 14, 16, 14, 1, 1), 3),
    ):
        h, records = initial, []
        for i in range(expected_cycles+1):
            record = cycle(h, literal=True)
            records.append(record)
            if i < expected_cycles:
                assert record['returns'] and record['safe']
            h = record['middle']
        output.append({'name': name, 'initial_middle': initial,
                       'certified_safe_returns': expected_cycles,
                       'cycles_including_next_attempt': records})
    assert output[1]['cycles_including_next_attempt'][2]['palindrome_steps'][0] == 1
    assert output[0]['cycles_including_next_attempt'][1]['palindrome_steps'][0] == 2
    return output


def original_gate_reset_probes(folder):
    source = folder.parent/'2026-10-14-collision-review'/'structural_controls.json'
    records = json.loads(source.read_text())['remaining_gate_short_reset_controls']
    output = []
    for r in (4, 5, 6, 31, 32):
        record = next(x for x in records if x['r'] == r)
        start = next(x for x in record['states'] if x['resets'])
        q = tuple(start['pair_word'])
        states, controls, overflows, pals = [q], [], [], []
        for _ in range(9):
            q, pal, c, e = full_step(q)
            states.append(q)
            controls.append(c)
            overflows.append(e)
            pals.append(pal)
        output.append({'r': r,
                       'original_time': record['first_zero_gap_time']+start['offset'],
                       'states': states, 'controls': controls, 'overflows': overflows,
                       'next_palindromic_flags': pals})
    for record in output[:2]:
        assert record['states'][0][:3] == PREFIX
        assert record['controls'][5] == 1
        assert record['states'][7][:3] == (4, 4, 1)
    return output


def main():
    folder = Path(__file__).parent
    prefixes = prefix_certificate()
    (folder/'PREFIX_CONTROL_CERTIFICATE.json').write_text(json.dumps(prefixes, indent=2)+'\n')
    catalog, archive, outcomes = bounded_catalog(folder)
    examples = finite_examples()
    probes = original_gate_reset_probes(folder)
    (folder/'ACTUAL_RETURN_EXAMPLES.json').write_text(json.dumps(examples, indent=2)+'\n')
    (folder/'ORIGINAL_GATE_RESET_PROBES.json').write_text(json.dumps(probes, indent=2)+'\n')
    summary = {
        'status': 'exact conditional seven-step return; finite repeated examples only',
        'all_control_words_checked': 128,
        'returning_control_words': 4,
        'required_control_pattern': '00*0*01',
        'width_increase_per_eligible_return': 3,
        'bounded_canonical_middle_catalog': catalog,
        'return_catalog': archive,
        'all_catalog_outcomes': outcomes,
        'outcome_schema': {
            'enumeration': 'canonical_cores(width), widths1..7, exactly as source',
            'one_byte_per_core_bits': {
                '0': 'first_return', '1': 'first_safe',
                '2': 'second_return_if_first_safe_return',
                '3': 'second_safe_if_first_safe_return',
                '4': 'third_return_if_two_safe_returns',
                '5': 'third_safe_if_two_safe_returns',
                '6': 'fourth_return_if_three_safe_returns',
                '7': 'fourth_safe_if_three_safe_returns',
            }},
        'two_return_example_first_positive_palindrome_time': 15,
        'one_return_example_first_positive_palindrome_time': 9,
        'bounded_fourth_return_result': 'all23 canonical initial cores ofwidth<=7 withthree_safe_returns failtheirfourthcontrolcondition',
        'original_r4_r5_reset_attempt': 'both violate c5=0; prefix440 becomes441 afterseven',
        'all_time_recurrence_claimed': False,
        'new_Lean_verification_claimed_by_this_script': False,
    }
    (folder/'RESET_SUMMARY.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
