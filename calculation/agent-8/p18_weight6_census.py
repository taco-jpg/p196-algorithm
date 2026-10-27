#!/usr/bin/env python3
"""Independent exhaustive p18 g-weight6 exterior-cycle audit. C++ executable required.

Build: c++ -O3 -std=c++17 calculation/agent-8/p18_fixed_g.cpp -o /tmp/a8_p18
Run: python3 calculation/agent-8/p18_weight6_census.py /tmp/a8_p18
"""
import itertools
import subprocess
import sys
from collections import Counter
from time import monotonic

P = 18
WEIGHT = 6
CAP = "5000000"

def necklaces():
    for on in itertools.combinations(range(P), WEIGHT):
        a = ['0'] * P
        for k in on:
            a[k] = '1'
        w = ''.join(a)
        if w == min(w[t:] + w[:t] for t in range(P)):
            yield w

def run(exe, bits):
    p = subprocess.run([exe, bits, CAP], capture_output=True, text=True, timeout=60)
    stdout = p.stdout.strip()
    if p.returncode not in (0, 3) or not stdout:
        raise RuntimeError(f'Unexpected exit on {bits}: rc={p.returncode} {p.stdout} {p.stderr}')
    words = stdout.split()
    status = words[0]
    args = dict(z.split('=', 1) for z in words[1:] if '=' in z)
    if args.get('g') != bits:
        raise RuntimeError(f'Wrong stream in solver output: {bits} => {stdout}')
    if status not in ('EXHAUSTED', 'CAPPED', 'DEPTH_CAPPED', 'ACCEPT'):
        raise RuntimeError(f'Unexpected status: {stdout}')
    return status, int(args['states']), int(args['depth']), stdout

def main():
    exe = sys.argv[1] if len(sys.argv)>1 else '/tmp/a8_p18'
    starts = monotonic()
    tally = Counter()
    total = 0
    maximal = (0, '')
    deep = (0, '')
    for g in necklaces():
        status,states,depth,msg=run(exe,g)
        tally[status] += 1
        total += states
        maximal=max(maximal,(states,g))
        deep=max(deep,(depth,g))
        if status != 'EXHAUSTED':
            print('NONEXHAUSTED',msg,flush=True)
    print('P18_WEIGHT6',dict(tally),'total_word_states',total,
          'max_states',maximal,'max_depth',deep,
          'wall_s',round(monotonic()-starts,2),flush=True)
    if sum(tally.values()) != 1038 or tally != Counter({'EXHAUSTED': 1038}):
        sys.exit(1)
    for good in ('11100010000','100010001000'):
        status,states,depth,msg=run(exe,good)
        print('POSITIVE_CONTROL',msg)
        if status!='ACCEPT':sys.exit(1)

if __name__=='__main__':
    main()