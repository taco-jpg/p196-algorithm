#!/usr/bin/env python3
"""Exact numerical criterion and coefficient lift for neutral-center cycles.

Acceptance uses only integer states (m, Z), their interval bounds, and the
prescribed carry/overflow/trim data. It never calls the symmetric-word
decoder. A successful cycle can be lifted because each state's predecessor
constructs a symmetric coefficient word with exactly that width and value.

This checks the CENTER subsystem only. Matching an actual exterior B cycle
is a separate obligation; success here alone is not a Lychrel certificate.
"""

from center_integer import Center, fixed_reverse


def _valid_base(base):
    return type(base) is int and base >= 2


def _valid_state(base, state):
    """Check the whole nonzero interval, not symmetric representability."""
    return (type(state) is Center
            and type(state.width) is int and state.width >= 1
            and type(state.signed) is int
            and 0 < abs(state.signed) <= base ** state.width - 1)


def _bit(value):
    return type(value) is int and value in (0, 1)


def raw_numeric(base, source, g):
    """Return the untrimmed image on the whole nonzero interval domain.

Malformed inputs raise ValueError. The returned raw state may have Z=0,
which is terminal and therefore cannot occur as a state of an accepted
cycle. Symmetric representability of the source is deliberately unchecked.
"""
    if not _valid_base(base) or not _valid_state(base, source):
        raise ValueError("source must lie in the nonzero center interval")
    if not _bit(g):
        raise ValueError("overflow must be a bit")
    m, z = source.width, source.signed
    x = abs(z)
    sign = 1 if z > 0 else -1
    raw_z = sign * (x + base ** g * fixed_reverse(base, x - 1, m)
                    - base ** (m + g))
    return Center(m + g, raw_z)


def check_edge(base, source, target, e, g, v):
    """Fail-closed numerical edge test with arbitrary nonnegative trim v."""
    if not _valid_base(base):
        return False
    if not _valid_state(base, source) or not _valid_state(base, target):
        return False
    if not _bit(e) or not _bit(g) or type(v) is not int or v < 0:
        return False
    if e != int(source.signed < 0):
        return False
    if target.width != source.width + g - 2 * v:
        return False
    raw = raw_numeric(base, source, g)
    return raw.signed == base ** v * target.signed


def check_cycle(base, states, carries, overflows, trims):
    """Check a nonempty cyclic list; the last edge returns to states[0].

Each argument sequence must be a list or tuple of the same length. Every
acceptance guard is an explicit Boolean branch, including under python -O.
No coefficient words are decoded or reconstructed by this predicate.
"""
    if not _valid_base(base):
        return False
    arrays = (states, carries, overflows, trims)
    if any(type(values) not in (list, tuple) for values in arrays):
        return False
    count = len(states)
    if count == 0 or any(len(values) != count for values in arrays):
        return False
    return all(check_edge(base, states[i], states[(i + 1) % count],
                          carries[i], overflows[i], trims[i])
               for i in range(count))


def _digits(base, number, width):
    """Fixed-width ordinary digits, least significant first."""
    digits = []
    for _ in range(width):
        number, digit = divmod(number, base)
        digits.append(digit)
    if number:
        raise RuntimeError("numerical source digit value exceeds its width")
    return digits


def _paired(digits):
    return tuple(a + b for a, b in zip(digits, reversed(digits)))


def _signed_value(base, word):
    number = 0
    for coefficient in reversed(word):
        number = base * number + coefficient
    return number - (base ** len(word) - 1)


def lift_cycle(base, states, carries, overflows, trims):
    """Construct every coefficient center and independently replay all edges.

Invalid numerical input raises ValueError. RuntimeError signals an internal
arithmetic inconsistency after acceptance, never a successful certificate.
The returned tuple is indexed in the same order as the supplied states.
"""
    if not check_cycle(base, states, carries, overflows, trims):
        raise ValueError("numerical center cycle was rejected")
    count, h = len(states), base - 1
    centers = [None] * count
    for i, source in enumerate(states):
        m, z, e, g, v = (source.width, source.signed, carries[i],
                         overflows[i], trims[i])
        digit_value = z - 1 if z > 0 else base ** m + z
        digits = _digits(base, digit_value, m)
        if g:
            digits.append(h * e)
        raw_word = _paired(digits)
        if v and (raw_word[:v] != (h,) * v
                  or raw_word[len(raw_word) - v:] != (h,) * v):
            raise RuntimeError("numerical trim did not give neutral endpoints")
        word = raw_word[v:len(raw_word) - v] if v else raw_word
        j = (i + 1) % count
        if (len(word) != states[j].width
                or _signed_value(base, word) != states[j].signed
                or word != word[::-1]
                or any(not 0 <= c <= 2 * h for c in word)):
            raise RuntimeError("constructed center does not realize target")
        centers[j] = word

    if any(word is None for word in centers):
        raise RuntimeError("coefficient lift left a state unconstructed")

    # Independent coefficient arithmetic now verifies the actual cycle.
    # This stage does not use raw_numeric, fixed_reverse, or a decoder.
    for i, word in enumerate(centers):
        e, g, v = carries[i], overflows[i], trims[i]
        carry, digits = e, []
        for coefficient in word:
            carry, digit = divmod(coefficient + carry, base)
            digits.append(digit)
        if carry != 1 - e:
            raise RuntimeError("reconstructed source does not flip the carry")
        if g:
            digits.append(h * e)
        actual_raw = _paired(digits)
        expected_raw = (h,) * v + centers[(i + 1) % count] + (h,) * v
        if actual_raw != expected_raw:
            raise RuntimeError("reconstructed coefficient edge failed replay")
    return tuple(centers)
