#!/usr/bin/env python3
"""Independent finite checks for AA54's scoped U3 transfer observation.

This script does NOT verify an all-time reverse-and-add certificate.
It enumerates the 30 distinct rotations of (9,a,18-a), checks that each
has pairwise-distinct entries and no cyclic reflection axis, and checks
that coefficient-normalization carry-out is constant for incoming carries
0, 1, 2. The reflection-axis impossibility itself is proved in REPORT.md.
"""
from itertools import product

def rotations(w):
    return [w[i:] + w[:i] for i in range(len(w))]

def carry_out(w, carry, base=10):
    for x in w:
        carry = (x + carry) // base
    return carry

def has_reflection_axis(w):
    m = len(w)
    return any(all(w[i] == w[(axis - i) % m] for i in range(m))
               for axis in range(m))

words = set()
for a in range(0, 19, 2):
    words.update(rotations((9, a, 18 - a)))

assert len(words) == 30, len(words)
for w in sorted(words):
    assert len(set(w)) == 3, w
    assert not has_reflection_axis(w), w
    carries = [carry_out(w, c) for c in range(3)]
    assert len(set(carries)) == 1, (w, carries)

print("distinct_U3_rotations=30")
print("pairwise_distinct=30/30")
print("reflection_axes=0/30")
print("constant_carry_out_on_inputs_0_1_2=30/30")
print("scope=local structural check only; no decimal seam or all-time claim")
