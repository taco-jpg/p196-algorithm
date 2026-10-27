#!/usr/bin/env python3
"""Arithmetic controls for the autonomous-B to exact-prefix bridge.

This establishes finite implementation agreement only. The unbounded
padding/trim argument belongs in the paper proof. No search for cycles.
"""
from itertools import product
from pathlib import Path
from random import Random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


def normalize(word, initial):
    output = []
    carry = initial
    for coefficient in word:
        value = coefficient + carry
        output.append(value % 10)
        carry = value // 10
    return tuple(output), carry


def autonomous(word):
    digits, low = normalize(word, 0)
    reflected, overflow = normalize(word[::-1], 1 - low)
    if overflow:
        left = digits + (9 * (1 - low),)
        right = (1,) + reflected[::-1]
    else:
        left, right = digits, reflected[::-1]
    return tuple(a + b for a, b in zip(left, right)), low, overflow


def padded_prefix(word, width):
    return tuple(word[:width]) + (9,) * max(0, width - len(word))


def inward_carry(word, low, width):
    if width >= len(word):
        return 1 - low
    return normalize(word[width:][::-1], 1 - low)[1]


def prefix_successor(prefix, inward):
    low_digits, _ = normalize(prefix, 0)
    high_digits, overflow = normalize(prefix[::-1], inward)
    high_digits = high_digits[::-1]
    if overflow:
        high_digits = (1,) + high_digits[:-1]
    return tuple(a + b for a, b in zip(low_digits, high_digits)), overflow


def carry_fields(word, width):
    """Low/high fields on the neutral-padded half-word, through cut width."""
    assert width >= len(word)
    q = padded_prefix(word, width)
    final_low = normalize(word, 0)[1]
    low = [0]
    for coefficient in q:
        low.append((coefficient + low[-1]) // 10)
    high = [0] * (width + 1)
    high[-1] = 1 - final_low
    for k in reversed(range(width)):
        high[k] = (q[k] + high[k + 1]) // 10
    return q, low, high, final_low


def trim_neutral(word):
    while word and word[-1] == 9:
        word = word[:-1]
    return word


def paired_tile_controls(word):
    """Check existing Tile equations directly against two autonomous steps."""
    odd, _, first_g = autonomous(word)
    if first_g != 0:
        return 0
    odd = trim_neutral(odd)
    next_even, _, second_g = autonomous(odd)
    if second_g != 1:
        return 0
    next_even = trim_neutral(next_even)
    width = max(len(word), len(odd), len(next_even)) + 3
    q, a, c, even_e = carry_fields(word, width)
    r, b, h, odd_e = carry_fields(odd, width)
    q_next = padded_prefix(next_even, width)
    slots = [(a[k], b[k], c[k], 0 if k == 0 else r[k - 1] - 10 * h[k - 1])
             for k in range(width + 1)]
    assert slots[0] == (0, 0, 0, 0)
    for k in range(width):
        x, y, carry = slots[k], slots[k + 1], h[k]
        assert all(0 <= z <= 1 for z in x[:3] + y[:3])
        assert -1 <= x[3] <= 9 and -1 <= y[3] <= 9
        assert r[k] == y[3] + 10 * carry
        assert not (r[k] < 9) or carry == 0
        assert not (r[k] > 9) or carry == 1
        assert y[0] == (q[k] + x[0]) // 10
        assert r[k] == (q[k] + x[0]) % 10 + (q[k] + y[2]) % 10
        assert y[1] == (r[k] + x[1]) // 10
        assert x[2] == (q[k] + y[2]) // 10
        assert q_next[k] == (r[k] + x[1]) % 10 + x[3] + carry
        assert 0 <= x[3] + carry <= 9
    tail = (even_e, odd_e, 1 - even_e, 10 * odd_e - 1)
    for k in range(max(len(word), len(odd)) + 1, width + 1):
        assert slots[k] == tail
    return width


def controls():
    counts = dict(words=0, mirror_steps=0, pad_checks=0,
                  trim_edges=0, prefix_checks=0, paired_tiles=0)

    def check(word):
        counts['words'] += 1
        counts['paired_tiles'] += paired_tile_controls(word)
        raw, low, overflow = autonomous(word)
        center = [18] if low == 0 else [0]
        assert mirror.hyp(10, list(word), center)
        assert tuple(mirror.nextB(10, list(word), center)) == raw
        assert mirror.e1(10, list(word)) == low
        assert mirror.gam(10, list(word), center) == overflow
        counts['mirror_steps'] += 1
        for padding in (0, 1, 2, 5):
            new_raw, new_low, new_overflow = autonomous(word + (9,) * padding)
            assert (new_raw, new_low, new_overflow) == (
                raw + (9,) * padding, low, overflow)
            counts['pad_checks'] += 1
        trim = 0
        while True:
            target = raw[:len(raw) - trim]
            counts['trim_edges'] += 1
            for width in range(1, 10):
                projected, projected_overflow = prefix_successor(
                    padded_prefix(word, width), inward_carry(word, low, width))
                assert projected == padded_prefix(target, width)
                assert projected_overflow == overflow
                counts['prefix_checks'] += 1
            if trim == len(raw) or raw[len(raw) - trim - 1] != 9:
                break
            trim += 1

    check(())
    for length in range(1, 4):
        for head in range(1, 19):
            for rest in product(range(19), repeat=length - 1):
                check((head,) + rest)
    rng = Random(109)
    for _ in range(10000):
        length = rng.randrange(4, 41)
        check((rng.randrange(1, 19),) +
              tuple(rng.randrange(19) for _ in range(length - 1)))
    print('BRIDGE_CONTROLS', ' '.join(f'{k}={v}' for k, v in counts.items()))

    skeleton = ((8, 12, 9), (17, 5, 0), (8, 13, 5), (17, 6, 11),
                (8, 14, 8), (17, 8, 17), (8, 16, 16), (17, 13, 14))
    required = {0: 1, 2: 0, 4: 0, 6: 1}
    accepted_edges = 0
    for phase, prefix in enumerate(skeleton):
        for inward in (0, 1):
            successor, overflow = prefix_successor(prefix, inward)
            matches = (successor == skeleton[(phase + 1) % 8]
                       and overflow == phase % 2)
            assert matches == (phase % 2 == 1 or inward == required[phase])
            accepted_edges += int(matches)
    print(f'EXISTING_SKELETON_CONTROL accepted_edges={accepted_edges} PASS')
    print('ALL BRIDGE CONTROLS PASSED')


if __name__ == '__main__':
    controls()
