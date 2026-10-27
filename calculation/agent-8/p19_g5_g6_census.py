#!/usr/bin/env python3
"""Exact all-width B transfer census for p19, g weights 5 and 6.
Requires the C++17 fixed-g solver in sibling p18_fixed_g.cpp, originally PR #321.

c++ -O3 -std=c++17 calculation/agent-8/p18_fixed_g.cpp -o /tmp/a8_fixed_g
python3 calculation/agent-8/p19_g5_g6_census.py /tmp/a8_fixed_g
"""
from collections import Counter
from itertools import combinations
import subprocess
import sys
from time import monotonic

def rotation_min(w):
    return min(w[k:] + w[:k] for k in range(len(w)))

def necklace_words(n, weight):
    for on in combinations(range(n), weight):
        g=''.join('1' if i in on else '0' for i in range(n))
        if g == rotation_min(g):
            yield g

def main():
    exe=sys.argv[1] if len(sys.argv)>1 else '/tmp/a8_fixed_g'
    for w, expected in [(5,612),(6,1428)]:
        counts=Counter();total=0;worst=(0,'');deep=(0,'');start=monotonic()
        for g in necklace_words(19,w):
            r=subprocess.run([exe,g,'2000000'],capture_output=True,text=True,timeout=30)
            a=r.stdout.strip().split()
            if r.returncode not in (0,3) or not a:raise RuntimeError((g,r.returncode,r.stdout,r.stderr))
            label=a[0]
            data=dict(q.split('=',1) for q in a[1:] if '=' in q)
            if data.get('g')!=g:raise RuntimeError('stream mismatch')
            counts[label]+=1;S=int(data['states']);D=int(data['depth']);total+=S
            worst=max(worst,(S,g));deep=max(deep,(D,g))
            if label!='EXHAUSTED':print('NONEXHAUSTED',r.stdout.strip(),flush=True)
        print(f'P19_WEIGHT{w} statuses={dict(counts)} states_total={total} max_states={worst} max_depth={deep} wall_s={monotonic()-start:.2f}',flush=True)
        if counts!=Counter({'EXHAUSTED':expected}):sys.exit(1)
    for g in ['11100010000','100010001000']:
        r=subprocess.run([exe,g,'300000'],capture_output=True,text=True,timeout=30)
        print('POSITIVE',r.stdout.strip(),flush=True)
        if r.returncode!=0 or not r.stdout.startswith('ACCEPT'):sys.exit(1)
if __name__=='__main__':main()