#!/usr/bin/env python3
"""Exact two-run polynomial certificate checker, with explicit rejection.

A phase (U, x, M, y, V) represents the canonical base-b digit word
U + x*n + M + y*n + V for every integer n >= 0.  All edges retain n
except the last edge, which returns to phase zero with n increased by one.

This string encoding supports integer bases 2 through 36.  Acceptance is a
paper-proved sufficient certificate, not a Lean-verified theorem.  No decimal
certificate is supplied.  Optimized Python cannot remove acceptance checks.
"""

ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGIT = {symbol: i for i, symbol in enumerate(ALPHABET)}


def _value(word, base):
    result = 0
    for symbol in word:
        result = result * base + DIGIT[symbol]
    return result


def _ordinary_step(number, base):
    """Reverse the actual canonical integer digits, then add the input."""
    remaining, reversal = number, 0
    while remaining:
        remaining, digit = divmod(remaining, base)
        reversal = reversal * base + digit
    return number + reversal


def _word(phase, n):
    u, x, middle, y, v = phase
    return u + x * n + middle + y * n + v


def _coefficients(phase, base):
    """Coefficients of (base-1)*value(W(n)) in t=base**n."""
    u, x, middle, y, v = phase
    r, s = len(middle), len(v)
    power, tail = base ** (r + s), base ** s
    xd, yd = DIGIT[x], DIGIT[y]
    return (
        power * ((base - 1) * _value(u, base) + xd),
        -xd * power + (base - 1) * _value(middle, base) * tail + yd * tail,
        (base - 1) * _value(v, base) - yd * tail,
    )


def _reversed_phase(phase):
    u, x, middle, y, v = phase
    return v[::-1], y, middle[::-1], x, u[::-1]


def inspect(phases, base):
    """Return (accepted, reason); malformed ordinary inputs are rejected.

    Only lists or tuples of five-string lists or tuples are accepted as the
    input representation.  The shifts are fixed by this API, so no arbitrary
    shift, negative n, or unchecked domain condition is accepted.
    """
    if type(base) is not int or not 2 <= base <= len(ALPHABET):
        return False, 'base must be an integer in 2..36'
    if type(phases) not in (list, tuple) or not phases:
        return False, 'phases must be a nonempty list or tuple'
    allowed = set(ALPHABET[:base])
    for i, phase in enumerate(phases):
        if type(phase) not in (list, tuple) or len(phase) != 5:
            return False, f'phase {i}: expected five fields'
        if any(type(field) is not str for field in phase):
            return False, f'phase {i}: all fields must be strings'
        u, x, middle, y, v = phase
        if not u or not v:
            return False, f'phase {i}: fixed outer words must be nonempty'
        if len(x) != 1 or len(y) != 1:
            return False, f'phase {i}: repeated words must be single digits'
        if any(symbol not in allowed for field in phase for symbol in field):
            return False, f'phase {i}: invalid digit for this base'
        if u[0] == '0':
            return False, f'phase {i}: leading fixed word begins with zero'
        if not any(left != right for left, right in zip(u, reversed(v))):
            return False, f'phase {i}: no permanent fixed outer mismatch'

    # All inputs are now finite, canonical, nonzero digit templates.  The
    # digit-mismatch proof applies for every n>=0, including zero-length runs.
    period = len(phases)
    for i, phase in enumerate(phases):
        target = phases[(i + 1) % period]
        delta = int(i == period - 1)
        for n in (0, 1, 2):
            current = _value(_word(phase, n), base)
            expected = _value(_word(target, n + delta), base)
            if _ordinary_step(current, base) != expected:
                return False, f'phase {i}: ordinary integer transition fails at n={n}'

        # Redundant exact identity check: the three ordinary-integer samples
        # already suffice by interpolation under the validated hypotheses.
        direct = _coefficients(phase, base)
        reverse = _coefficients(_reversed_phase(phase), base)
        following = _coefficients(target, base)
        scale = base ** delta
        lhs = tuple(a + b for a, b in zip(direct, reverse))
        rhs = (following[0] * scale * scale, following[1] * scale, following[2])
        if lhs != rhs:
            return False, f'phase {i}: exact polynomial identity fails'
    return True, 'accepted: canonical two-run cycle, final shift +1'


def check(phases, base):
    """Boolean acceptance predicate; no assertion controls acceptance."""
    return inspect(phases, base)[0]
