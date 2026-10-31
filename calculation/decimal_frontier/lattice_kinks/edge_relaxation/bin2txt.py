#!/usr/bin/env python3
"""Convert a kink6 binary cyclic-set file (unsigned 128-bit keys) to the text format used by incr.py / exact_small.py:
'scc t j par w0 .. w{K-1}' (scc column = 0).  usage: bin2txt.py lat K in.bin out.txt"""
import sys
from klib import load
name, K, fi, fo = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
M = load(name).m
data = open(fi, 'rb').read()
with open(fo, 'w') as f:
    for i in range(0, len(data), 16):
        k = int.from_bytes(data[i:i + 16], 'little')
        ph = k >> 100; par = ph % 2; ph //= 2; j = ph % M; t = ph // M
        w = [(k >> (5 * q)) & 31 for q in range(K)]
        f.write(f'0 {t} {j} {par} ' + ' '.join(map(str, w)) + '\n')
