#!/usr/bin/env python3
"""Bounded constructed-family inspection; computational evidence, not a proof."""
from collections import Counter
from pathlib import Path
import datetime
import hashlib
import itertools
import json
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE_COMMIT = 'fa8cf9024c8aaa8c97a6426b004a7869c12ed887'
ALGORITHM = 'proofs/periodic_word_quotient__8404d0a63dd1fa13.py'
W = (9, 9, 9, 9)
MAX_CASES = 30000
MAX_SECONDS = 30

def pin(path):
    data = subprocess.check_output(['git', 'show', SOURCE_COMMIT + ':' + path], cwd=ROOT)
    assert data == (ROOT / path).read_bytes()
    return data, {'path': path, 'commit': SOURCE_COMMIT, 'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}

source, algorithm_pin = pin(ALGORITHM)
# Load the pinned existing pure full/image/valid functions without importing a
# module or creating __pycache__; its main/search routine is never called.
original = {'__name__': 'pinned_source_inspection', '__file__': str(ROOT / ALGORITHM)}
exec(compile(source, ALGORITHM, 'exec'), original)

def fixed(word, carry):
    digits = []
    for x in word:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
    return tuple(digits), carry

def strip_center(word, period=W):
    count = 0
    while len(word) >= 2 * len(period) and word[:len(period)] == period and word[-len(period):] == period[::-1]:
        word = word[len(period):-len(period)]
        count += 1
    return word, count

def raw(state):
    b, h, w = state
    out, clock = original['image'](original['full'](state, 3))
    nb, nh = len(b) + 4, len(h) + 8 + clock
    rb, rw, rh = out[:nb], out[nb:nb+4], out[nb+4:nb+4+nh]
    assert out == original['full']((rb, rh, rw), 1)
    return rb, rh, rw, clock

def inspect(b, h):
    state = b, h, W
    assert original['valid'](state)
    rb, rh, rw, clock = raw(state)
    e = fixed(b, 0)[1]
    f = fixed(h, e)[1]
    assert clock == fixed(b[::-1], f)[1]
    assert rw == (18 - 9 * (e + f),) * 4
    qh, count = strip_center(rh, rw)
    qb = rb
    while len(qb) >= 4 and qb[-4:] == rw:
        qb = qb[:-4]
    assert original['valid']((qb, qh, rw))
    next_period = raw((qb, qh, rw))[2]
    normalized = strip_center(h) == (h, 0)
    if e + f == 1:
        digits = fixed(h, e)[0] + (9 * e,) * clock
        paired = tuple(x+y for x, y in zip(digits, digits[::-1]))
        assert rh == W + paired + W
        assert strip_center(paired) == (qh, count-1)
    predicates = {
        'initial_normalized': normalized,
        'actual_entries_mixed': e+f == 1,
        'actual_clock_one': clock == 1,
        'extra_strip_at_least_one': count >= 2,
        'quotient_center_nonempty': bool(qh),
        'drop_exactly_seven': len(qh)+7 == len(h),
        'next_actual_period_nine': next_period == W,
    }
    return {'B': b, 'H': h, 'left_entry': e, 'right_entry': f,
            'clock': clock, 'raw_period': rw, 'center_periods': count,
            'quotient_B': qb, 'quotient_H': qh, 'next_raw_period': next_period,
            'predicates': predicates}

started = time.monotonic()
started_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
centers = set()
for p in range(5):
    wrap = (9,) * p
    for a in range(19):
        centers.add(wrap + (a, a) + wrap)
        for b in range(19):
            centers.add(wrap + (a, b, b, a) + wrap)
        for c in range(0, 19, 2):
            centers.add(wrap + (a, c, a) + wrap)
outers = [(1,), (9,), (10,), (18,), (10, 0), (18, 0), (10, 8), (18, 8), (9, 0)]
counts = Counter()
failure_counts = Counter()
candidate_witnesses = []
unnormalized_drop_seven_controls = []
normalized_extra_strip_controls = []
for h in sorted(centers, key=lambda h: (len(h), h)):
    for b in outers:
        assert counts['cases'] < MAX_CASES, 'CASE_BUDGET_EXHAUSTED'
        assert time.monotonic() - started < MAX_SECONDS, 'TIME_BUDGET_EXHAUSTED'
        result = inspect(b, h)
        counts['cases'] += 1
        predicates = result['predicates']
        for key, yes in predicates.items():
            counts[key] += int(yes)
            if not yes:
                failure_counts[key] += 1
        if all(predicates.values()):
            candidate_witnesses.append(result)
        if predicates['actual_entries_mixed'] and predicates['actual_clock_one']:
            counts['mixed_clock_one'] += 1
            if predicates['initial_normalized']:
                counts['normalized_mixed_clock_one'] += 1
                counts['normalized_mixed_clock_one_extra_strip'] += int(predicates['extra_strip_at_least_one'])
        if all(yes for key, yes in predicates.items() if key != 'initial_normalized'):
            counts['drop_seven_without_initial_normalization'] += 1
            if len(unnormalized_drop_seven_controls) < 5:
                unnormalized_drop_seven_controls.append(result)
        if predicates['initial_normalized'] and predicates['actual_entries_mixed'] and predicates['extra_strip_at_least_one']:
            counts['normalized_mixed_extra_strip'] += 1
            if len(normalized_extra_strip_controls) < 5:
                normalized_extra_strip_controls.append(result)

pins = [algorithm_pin]
for path in ['proofs/Agent1PeriodicDigits.lean', 'proofs/Agent1PeriodicGuard.lean',
             'proofs/Agent1PeriodicQuotient.lean', 'proofs/Agent1PeriodicCenterStrip.lean',
             'proofs/Agent1PeriodicNines.lean', 'proofs/Agent1PeriodicNinesCenter.lean']:
    pins.append(pin(path)[1])
report = {
    'status': 'CANDIDATE_FOUND_UNPROVED' if candidate_witnesses else 'NO_CANDIDATE_IN_BOUNDED_CONSTRUCTED_FAMILY',
    'mathematical_impossibility_proved': False,
    'lean_run_performed': False,
    'source_pins': pins,
    'discovery_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'started_at_utc': started_utc,
    'finished_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'elapsed_seconds': time.monotonic()-started,
    'budget': {'maximum_cases': MAX_CASES, 'maximum_seconds': MAX_SECONDS, 'complete_planned_family': True},
    'family': {'center': '9^p ++ core ++ 9^p; p=0..4; core=[a,a], [a,b,b,a], or [a,c,a]; a,b=0..18; c=0,2,..18',
        'distinct_centers': len(centers), 'outers': outers,
        'maximum_center_length': max(map(len, centers)),
        'maximum_outer_length': max(map(len, outers))},
    'counts': dict(counts), 'failed_predicate_counts': dict(failure_counts),
    'candidate_witnesses': candidate_witnesses,
    'drop_seven_controls_without_initial_normalization': unnormalized_drop_seven_controls,
    'normalized_extra_strip_controls': normalized_extra_strip_controls,
    'scope': 'Local one-step plus one next-period computation only. No full-cycle search and no universal impossibility conclusion.',
}
with (HERE / 'discovery-001.json').open('x') as out:
    out.write(json.dumps(report, indent=2) + '\n')
print(json.dumps({'status': report['status'], 'counts': report['counts'],
                  'elapsed_seconds': report['elapsed_seconds'],
                  'unnormalized_drop_seven_controls': unnormalized_drop_seven_controls}, indent=2))
