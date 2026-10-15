#!/usr/bin/env python3
"""Diagnose one class with a large cap and no predecessor cache (lower memory).
usage: run_one.py K CAP PREFIX OUT.jsonl"""
import sys, time, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import prefix_cycles as pc
k, cap, prefix, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
t = time.time()
r = pc.analyze(prefix, k, cap, cache=False)
r['seconds'] = round(time.time() - t, 2)
with open(out, 'a') as f:
    f.write(json.dumps(r) + '\n')
print(r['prefix'], r['k'], r['status'], r['states'], r['seconds'])
