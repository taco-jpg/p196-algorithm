#!/usr/bin/env python3
"""Print every positive integer below 10^P with at most K nonzero decimal digits.
Usage: python3 sparse_seeds.py P K > seeds.txt"""
import sys, itertools
P, K = int(sys.argv[1]), int(sys.argv[2])
out = sys.stdout
for j in range(1, K + 1):
    for pos in itertools.combinations(range(P), j):
        for digs in itertools.product(range(1, 10), repeat=j):
            out.write("%d\n" % sum(dg * 10 ** p for dg, p in zip(digs, pos)))
