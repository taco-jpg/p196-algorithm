#!/usr/bin/env python3
"""Exact rooted-boundary check for a physical +22-column W9 shift."""
B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
SHIFT = 22

assert len(B) == 34
assert len(W) == 9
assert SHIFT == 2 * len(W) + 4
shifted_left_edge = len(B) - SHIFT
assert shifted_left_edge == 12
assert B[shifted_left_edge] == 10
assert 10 not in set(W)
assert W[SHIFT % len(W)] == 1

print(f"shift={SHIFT}=2*{len(W)}+{SHIFT % len(W)}")
print(f"fixed B length={len(B)}; translated W9 window left edge={shifted_left_edge}")
print(f"B[{shifted_left_edge}]={B[shifted_left_edge]}, W phases={sorted(set(W))}")
print("PASS: no phase of W9 can overlap the fixed B34 at the translated left edge.")
print("If only the inner cut moves, the band span is 9*q-22, not 9*q.")
print("A pure coordinate reindexing moves no physical coefficient and cannot move a mismatch out of the band.")
