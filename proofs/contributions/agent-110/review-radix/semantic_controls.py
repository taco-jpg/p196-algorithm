#!/usr/bin/env python3
"""Reviewer-written arithmetic controls; does not import author code."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
STATES = [(6, [13]), (12, [4, 10]), (6, [9, 1]),
          (12, [18, 2]), (6, [9, 11, 5]), (12, [10, 1, 7, 11])]


def column_normalize(coefficients, incoming):
    digits, carry = [], incoming
    for coefficient in coefficients:
        carry, digit = divmod(coefficient + carry, 10)
        digits.append(digit)
    return digits, carry


def transition(c, word):
    k = int(c >= 10)
    t = c - 9 * k
    left, e = column_normalize(word, 0)
    right, gamma = column_normalize(list(reversed(word)), k)
    u = c + e - 10 * k
    lhs = left + [u]
    rhs = list(reversed(right)) + [t] if gamma == 0 else [1] + list(reversed(right))
    assert len(lhs) == len(rhs)
    raw = [a + b for a, b in zip(lhs, rhs)]
    result = raw.copy()
    while result and result[-1] == 2 * t:
        result.pop()
    return (2 * t, result), gamma, {'left': left, 'left_carry': e, 'right': right,
                                  'right_carry': gamma, 'u': u, 'raw': raw}


def Z(c, word):
    return 9 * sum(x * 10 ** i for i, x in enumerate(word)) - c * (10 ** len(word) - 1)


def canonical(c, word):
    return 0 < c <= 16 and c % 2 == 0 and all(0 <= x <= 18 for x in word) and (
        not word or (word[0] > 0 and word[-1] != c))


def digits(n):
    return [int(ch) for ch in reversed(str(n))]


def pair_word(n):
    data = digits(n)
    return [a + b for a, b in zip(data, reversed(data))]


def seed_for_core(core):
    q = [13] + [6] * core + [13]
    data = [0] * len(q)
    for i in range(len(q) // 2):
        data[-1 - i] = min(9, q[i])
        data[i] = q[i] - data[-1 - i]
    if len(q) % 2:
        assert q[len(q) // 2] % 2 == 0
        data[len(q) // 2] = q[len(q) // 2] // 2
    n = sum(d * 10 ** i for i, d in enumerate(data))
    assert pair_word(n) == q
    return n


def main():
    arithmetic = []
    for i, (c, word) in enumerate(STATES):
        assert canonical(c, word)
        row = {'index': i, 'phase': c, 'word': word, 'Z': Z(c, word), 'canonical': True}
        # Independently verify both expressions for the exact stated observable.
        assert row['Z'] == 9 * sum((x - c) * 10 ** j for j, x in enumerate(word))
        for copies in [0, 1, 2, 7]:
            assert Z(c, word + [c] * copies) == row['Z']
        if i < len(STATES) - 1:
            successor, gamma, details = transition(c, word)
            assert successor == STATES[i + 1]
            row.update(overflow=gamma, details=details)
        arithmetic.append(row)
    assert [row['overflow'] for row in arithmetic[:-1]] == [1, 0, 0, 1, 1]
    assert (STATES[2][0], Z(*STATES[2])) == (STATES[4][0], Z(*STATES[4])) == (6, -423)
    assert STATES[2] != STATES[4]
    assert Z(*STATES[3]) == -846 and Z(*STATES[5]) == -14508
    literal = []
    for initial_core in [9, 10, 17]:
        n = seed_for_core(initial_core)
        rows = []
        for i, (c, word) in enumerate(STATES):
            q = pair_word(n)
            core_length = len(q) - 2 * len(word)
            assert core_length > 0
            expected = word + [c] * core_length + list(reversed(word))
            assert q == expected
            row = {'time': i, 'integer': str(n), 'digits': len(str(n)),
                   'phase': c, 'outer': word, 'core_length': core_length,
                   'pair_word': q, 'Z': Z(c, word)}
            if i < len(STATES) - 1:
                reverse_n = int(str(n)[::-1])
                successor = n + reverse_n
                actual_overflow = len(str(successor)) - len(str(n))
                assert actual_overflow == arithmetic[i]['overflow']
                row.update(reverse_integer=str(reverse_n), successor=str(successor),
                           actual_decimal_overflow=actual_overflow)
                n = successor
            rows.append(row)
        literal.append({'initial_core': initial_core, 'rows': rows})
    record = {'status': 'PASS', 'reviewer': '/root/runtime_audit',
              'method': 'Independent direct integer addition and string decimal reversal; no author Python imports',
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'exact_exterior_arithmetic': arithmetic, 'literal_integer_controls': literal,
              'ordinary_additions_checked': 15,
              'scope': 'Finite controls and interpretation of the stated map. No universal ordinary-integer bridge, state cycle, infinite safe orbit, or claim about 196.'}
    (HERE / 'semantic-controls.json').write_text(json.dumps(record, indent=2) + '\n')
    print('PASS: 6 canonical states; 5 exact transitions; 15 literal reverse-and-add steps; observable alias but no state return')


if __name__ == '__main__':
    main()
