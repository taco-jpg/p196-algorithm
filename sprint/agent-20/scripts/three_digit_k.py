#!/usr/bin/env python3
"""Rank of selected 3-digit claims at one width k: three_digit_k.py K PREFIX:CLAIM ..."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__file__))
from recompute_ranks import Ranker, initial_words
from inverse_long import LazyPred
k = int(sys.argv[1]); R = Ranker(LazyPred(k))
for arg in sys.argv[2:]:
    p, B = arg.split(":"); t0 = time.time()
    r = max(R.get(w) for w in initial_words([int(x) for x in p], k))
    print(f"{p} k={k} rank={r} t<={r+1} claimed t<={B} {'ok' if r + 1 <= int(B) else 'LARGER'} "
          f"({time.time()-t0:.0f}s, {len(R.rank)} states cached)", flush=True)
