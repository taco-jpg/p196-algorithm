#!/usr/bin/env python3
"""Exact numerical neutral-center dynamics; PAPER model, not a Lean checker.

Coefficients are least significant first, symmetric, and in [0, 2*b-2].
Center(width, signed) stores Z = val_b(C) - (b**width - 1).
The source report proves that width and Z determine C uniquely.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import gcd


@dataclass(frozen=True)
class Center:
    width: int
    signed: int


@dataclass(frozen=True)
class Transition:
    source: Center
    overflow: int
    incoming: int
    raw: Center
    target: Center
    trim: int

    @property
    def next_incoming(self):
        return None if self.target.signed == 0 else int(self.target.signed < 0)


def _base(base):
    if type(base) is not int or base < 2:
        raise ValueError("base must be an integer >= 2")


def encode(base, coefficients):
    """Encode a bounded symmetric word; zero/empty words remain representable."""
    _base(base)
    word = tuple(coefficients)
    if any(type(c) is not int or not 0 <= c <= 2 * base - 2 for c in word):
        raise ValueError("coefficient outside the natural-number bounds")
    if word != word[::-1]:
        raise ValueError("center must be symmetric")
    number = 0
    for c in reversed(word):
        number = base * number + c
    return Center(len(word), number - (base ** len(word) - 1))


def decode(base, center):
    """Recover the unique symmetric word, rejecting nonrepresentable states.

For an outer coefficient c at remaining width m>=2, the high quotient
is c or c+1, while c is congruent to the low residue modulo b. The two
consecutive high candidates contain at most one candidate of that residue.
"""
    _base(base)
    if not isinstance(center, Center):
        raise ValueError("state must be a Center")
    if type(center.width) is not int or center.width < 0:
        raise ValueError("width must be a natural number")
    if type(center.signed) is not int:
        raise ValueError("signed value must be an integer")
    width = center.width
    power = base ** width
    number = center.signed + power - 1
    if not 0 <= number <= 2 * (power - 1):
        raise ValueError("signed value exceeds coefficient bounds")
    left = []
    while width >= 2:
        high_power = power // base
        quotient, residue = number // high_power, number % base
        candidates = [c for c in (quotient - 1, quotient)
                      if 0 <= c <= 2 * base - 2 and c % base == residue]
        if len(candidates) != 1:
            raise ValueError("no symmetric bounded realization")
        c = candidates[0]
        rest = number - c * (1 + high_power)
        if rest < 0 or rest % base:
            raise ValueError("no symmetric bounded realization")
        left.append(c)
        number = rest // base
        width -= 2
        power //= base * base
    if width == 1:
        if not 0 <= number <= 2 * base - 2:
            raise ValueError("invalid middle coefficient")
        middle = (number,)
    else:
        if number:
            raise ValueError("nonzero empty interior")
        middle = ()
    return tuple(left) + middle + tuple(reversed(left))


def fixed_reverse(base, number, width):
    """Reverse exactly width base-b digits, including their zero padding."""
    _base(base)
    if type(width) is not int or width < 0 or type(number) is not int:
        raise ValueError("invalid fixed-width numeral")
    if not 0 <= number < base ** width:
        raise ValueError("number does not fit the fixed width")
    result = 0
    for _ in range(width):
        number, digit = divmod(number, base)
        result = base * result + digit
    return result


def base_order(base, number):
    """Largest r with b**r dividing nonzero number; b need not be prime."""
    _base(base)
    if type(number) is not int or number == 0:
        raise ValueError("base divisibility order needs a nonzero integer")
    order = 0
    while number % base == 0:
        number //= base
        order += 1
    return order


def normalize(base, center):
    """Remove every paired neutral endpoint; zero remains a terminal state."""
    decode(base, center)
    if center.signed == 0:
        return Center(center.width % 2, 0), center.width // 2
    trim = base_order(base, center.signed)
    target = Center(center.width - 2 * trim, center.signed // base ** trim)
    if target.width < 1:
        raise ValueError("invalid neutral trimming order")
    return target, trim


def step(base, center, overflow):
    """Compute one prescribed-overflow step and maximal symmetric trim.

No exterior is assumed. A zero target cannot satisfy a later carry flip.
The public entry point validates representability; it is not a full B/C
cycleOK predicate and cannot certify a Lychrel number on its own.
"""
    decode(base, center)
    if type(overflow) is not int or overflow not in (0, 1):
        raise ValueError("overflow must be a bit")
    z, width = center.signed, center.width
    if z == 0:
        raise ValueError("all-neutral center cannot flip the carry")
    magnitude = abs(z)
    sign = 1 if z > 0 else -1
    reversed_digits = fixed_reverse(base, magnitude - 1, width)
    raw_z = sign * (magnitude + base ** overflow * reversed_digits
                    - base ** (width + overflow))
    raw = Center(width + overflow, raw_z)
    if raw_z == 0:
        trim = raw.width // 2
        target = Center(raw.width % 2, 0)
    else:
        trim = base_order(base, raw_z)
        target = Center(raw.width - 2 * trim, raw_z // base ** trim)
    return Transition(center, overflow, int(z < 0), raw, target, trim)


def padding_key(base, center):
    """Faithful rational key for equivalence under neutral-pair padding."""
    decode(base, center)
    return center.width % 2, Fraction(center.signed, base ** (center.width // 2))


def from_padding_key(base, parity, value):
    """Recover the canonical representative, or reject an unrealizable key."""
    _base(base)
    if type(parity) is not int or parity not in (0, 1):
        raise ValueError("parity must be a bit")
    if not isinstance(value, (int, Fraction)) or isinstance(value, bool):
        raise ValueError("rational value must be exact")
    value = Fraction(value)
    denominator, half_width = value.denominator, 0
    while denominator != 1:
        divisor = gcd(denominator, base)
        if divisor == 1:
            raise ValueError("denominator contains a prime outside the base")
        denominator //= divisor
        half_width += 1
    signed = value * base ** half_width
    if signed.denominator != 1:
        raise ValueError("rational denominator was not eliminated")
    center = Center(2 * half_width + parity, signed.numerator)
    decode(base, center)
    return center


def main():
    for word in ((10, 10), (10, 0, 0, 10)):
        state = encode(10, word)
        result = step(10, state, 0)
        print(f"C={word} state={state} key={padding_key(10, state)} "
              f"next={result.target} next_C={decode(10, result.target)}")


if __name__ == "__main__":
    main()
