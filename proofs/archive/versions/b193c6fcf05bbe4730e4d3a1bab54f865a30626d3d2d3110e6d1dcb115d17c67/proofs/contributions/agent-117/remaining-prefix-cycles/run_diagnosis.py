#!/usr/bin/env python3
"""Run the k-column cycle/acyclicity diagnosis over a prefix list; appends JSONL records.
usage: run_diagnosis.py K CAP OUT.jsonl PREFIX_LIST"""
import sys, time, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import prefix_cycles as pc
k, cap, out, lst = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
prefixes = [l.strip() for l in open(lst) if l.strip()]
try:
    done = {json.loads(l)['prefix'] for l in open(out)}
except FileNotFoundError:
    done = set()
with open(out, 'a') as f:
    for pre in prefixes:
        if pre in done:
            continue
        t = time.time()
        r = pc.analyze(pre, k, cap)
        r['seconds'] = round(time.time() - t, 2)
        f.write(json.dumps(r) + '\n'); f.flush()
