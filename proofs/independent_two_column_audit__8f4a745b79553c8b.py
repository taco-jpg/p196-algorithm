#!/usr/bin/env python3
"""Literal-integer audit of all seven-input returns of the prefix (4,4)."""

from hashlib import sha256
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent


def literal_transition(prefix, incoming):
    word = tuple(prefix) + (18 * incoming,) + tuple(reversed(prefix))
    value = sum(a * 10**i for i, a in enumerate(word))
    carry = sum(a * 10**i for i, a in enumerate(word[:3])) // 1000
    assert carry == incoming
    digits = []
    while value:
        value, digit = divmod(value, 10)
        digits.append(digit)
    paired = [a + b for a, b in zip(digits, reversed(digits))]
    return paired[:2], len(digits) - len(word), word, digits


def main():
    input_path = HERE / 'two_column_controls.json'
    source_path = HERE / 'two_column_controls.py'
    data = json.loads(input_path.read_text())
    assert len(data['records']) == 128
    assert {tuple(r['controls']) for r in data['records']} == {
        tuple((i >> (6 - t)) & 1 for t in range(7)) for i in range(128)}
    raw, returns, traces = [], [], {}
    for record in data['records']:
        controls = record['controls']
        prefix, prefixes, overflows = [4, 4], [[4, 4]], []
        for t, incoming in enumerate(controls):
            nxt, overflow, word, digits = literal_transition(prefix, incoming)
            raw.append(dict(controls=controls, time=t, prefix=prefix,
                            incoming=incoming, word=word, digits=digits,
                            next_prefix=nxt, overflow=overflow))
            prefix = nxt
            prefixes.append(prefix)
            overflows.append(overflow)
        returned = prefix == [4, 4]
        boolean_condition = (controls[1] == 0 and (
            (controls[3] == 0 and controls[5] == 1 and controls[6] == 1)
            or (controls[0] == 1 and controls[3] == 1 and controls[5] == 0)))
        assert returned == boolean_condition == record['returned']
        assert prefixes == record['prefixes']
        assert overflows == record['overflows'] == [0, 0, 1, 0, 1, 0, 1]
        if returned:
            returns.append(controls)
            traces.setdefault(tuple(tuple(p) for p in prefixes), []).append(controls)
    assert len(returns) == 16 and len(traces) == 3
    expected = {tuple(tuple(p) for p in b['prefixes']): b['controls'] for b in data['branches']}
    assert traces == expected
    result = dict(status='PASS', binary_control_words=128,
                  local_literal_controls=len(raw), returned_control_words=returns,
                  distinct_return_traces=len(traces),
                  return_condition='c1=0 and ((c3=0 and c5=1 and c6=1) or (c0=1 and c3=1 and c5=0))',
                  free_positions=[2, 4],
                  all_128_overflow_words=[0, 0, 1, 0, 1, 0, 1],
                  producer_source_sha256=sha256(source_path.read_bytes()).hexdigest(),
                  producer_data_sha256=sha256(input_path.read_bytes()).hexdigest(),
                  raw_controls=raw,
                  scope='Every local branch has an ordinary symmetric-word realization. The concatenated freely chosen carry histories are not asserted to arise from one ordinary integer orbit.')
    (HERE / 'independent_two_column_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('raw_controls', 'returned_control_words')}))


if __name__ == '__main__':
    main()
