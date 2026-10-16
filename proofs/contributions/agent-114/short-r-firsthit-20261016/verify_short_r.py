#!/usr/bin/env python3
"""Agent 114: exact finite reverse-and-add controls for the Group-I short spacers.

This does NOT prove any infinite-time statement or constitute Lean verification.
Standard-library only; Python >= 3.8.
"""
import hashlib
import json
import sys

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)

HORIZON = 3000


def initial_coefficients(r):
    """Exactly DelayedOverlapGate.initial r 1 1 6, little-endian."""
    assert r >= 1
    L = 2 * r + 7
    q = []
    for i in range(L):
        if i in (0, 1, 2*r+5, 2*r+6):
            q.append(1)
        elif i in (r+1, r+5):
            q.append(1)
        elif i in (r+2, r+4):
            q.append(7)
        elif i == r+3:
            q.append(12)
        else:
            q.append(0)
    assert q == q[::-1]
    return q


def canonical_representative(q):
    """One positive exact-width decimal split of all mirrored pair sums."""
    L = len(q)
    d = [0] * L
    for i in range((L+1)//2):
        j = L-1-i
        if i == j:
            assert q[i] % 2 == 0
            d[i] = q[i]//2
        else:
            d[i] = q[i]//2
            d[j] = q[i]-d[i]
    assert d[-1] != 0 and all(0 <= x <= 9 for x in d)
    assert all(d[i]+d[L-1-i] == q[i] for i in range(L))
    return int(''.join(map(str, reversed(d))))


def add_reverse_digits(d):
    """Independent grade-school base-10 operation on little-endian digits."""
    out = []
    carry = 0
    for a, b in zip(d, reversed(d)):
        s = a+b+carry
        out.append(s % 10)
        carry = s // 10
    if carry:
        out.append(carry)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def run(r, horizon):
    q = initial_coefficients(r)
    n = canonical_representative(q)
    L = 2*r+7
    assert len(str(n)) == L
    n1_from_columns = sum(v*(10**i) for i, v in enumerate(q))
    assert n1_from_columns == n+int(str(n)[::-1])
    x = n
    rolling = hashlib.sha256()
    first11 = []
    first_hit = None
    for t in range(1, horizon+1):
        before_digits = [int(ch) for ch in reversed(str(x))]
        manual = add_reverse_digits(before_digits)
        x += int(str(x)[::-1])
        current = str(x)
        assert manual == [int(ch) for ch in reversed(current)], (r,t)
        is_pal = current == current[::-1]
        assert is_pal == (manual == manual[::-1]), (r,t)
        rolling.update((str(t)+':'+current+'\n').encode('ascii'))
        if t <= 11:
            first11.append({'t':t, 'value':current, 'palindrome':is_pal})
        if is_pal:
            first_hit = t
            break
    return {
        'r':r,'width':L,'canonical_representative':str(n),
        'pair_coefficients_little_endian':q,
        'first_reverse_add':str(n1_from_columns),
        'horizon_checked':t,'first_positive_palindrome_through_horizon':first_hit,
        'last_value_digit_length':len(current),
        'last_value_sha256':hashlib.sha256(current.encode('ascii')).hexdigest(),
        'trajectory_sha256':rolling.hexdigest(),
        'first_11_steps':first11,
    }


def main():
    records = [run(r, HORIZON) for r in (1,2,3,4)]
    control = run(5,11)
    assert all(rec['first_positive_palindrome_through_horizon'] is None for rec in records)
    assert control['first_positive_palindrome_through_horizon'] == 11
    assert control['first_11_steps'][-1]['value'] == '88088935999953988088'
    data = {
        'description':'Exact finite computational evidence only; not Lean checked or infinite-time proof',
        'operation':'T(n)=n+decimal_reverse(n)',
        'short_spacer_horizon':HORIZON,
        'short_spacer_records':records,
        'r5_boundary_control':control,
    }
    json.dump(data,sys.stdout,indent=2,ensure_ascii=False,sort_keys=True)
    sys.stdout.write('\n')

if __name__ == '__main__':
    main()
