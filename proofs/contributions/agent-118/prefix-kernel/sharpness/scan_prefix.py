#!/usr/bin/env python3
"""Exact max ancestry depth H(P) over palindromes P with a given 3-digit prefix, per width (diagnostic)."""
import json, sys, time
from itertools import product
sys.dont_write_bytecode = True
import exact_depth as ed

def palindromes(prefix, W):
    a = tuple(map(int, prefix))
    h = (W + 1) // 2
    if h < 3:
        # widths 3..5 handled by explicit construction
        pass
    for tail in product(range(10), repeat=max(0, h - 3)):
        half = (a + tail)[:h]
        if len(half) < h:
            continue
        digits = half + (half[::-1][1:] if W % 2 else half[::-1])
        if digits[:3] == a:
            yield digits

if __name__ == '__main__':
    prefix, wmax = sys.argv[1], int(sys.argv[2])
    wmin = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    out = []
    for W in range(wmin, wmax + 1):
        ed.depth.cache_clear()
        t = time.time(); best = (-1, None); cnt = 0
        for d in palindromes(prefix, W):
            cnt += 1
            H = ed.palindrome_H(d)
            if H > best[0]:
                best = (H, ''.join(map(str, d)))
        rec = {'prefix': prefix, 'width': W, 'palindromes': cnt, 'max_H': best[0], 'argmax': best[1],
               'seconds': round(time.time() - t, 1), 'memo_words': ed.depth.cache_info().currsize}
        out.append(rec); print(json.dumps(rec), flush=True)
