#!/usr/bin/env python3
"""Independent decimal digit-array check of the repaired 20-column centre."""
import argparse
from check_digits import read_rows, one_step

def seed_digits(path, cyc, copies, core):
    half = [r[0] for r in path] + [r[0] for r in cyc] * copies + core
    return [min(z, 9) for z in half] + [z - min(z, 9) for z in half][::-1]

def lifetime(path, cyc, copies, core, horizon):
    d = seed_digits(path, cyc, copies, core)
    for t in range(horizon+1):
        if d == d[::-1]: raise AssertionError(f'palindrome t={t}')
        for i in range(39):
            q = d[i] + d[-1-i]
            if q != path[i][t % 8]:
                return t, i, q, path[i][t % 8]
        if t < horizon: d = one_step(d)
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('data');ap.add_argument('core')
    ap.add_argument('--copies',type=int,default=1)
    ap.add_argument('--steps',type=int,default=400)
    args=ap.parse_args()
    path,cyc=read_rows(args.data)
    core=[int(z) for z in open(args.core).read().split()]
    assert len(core)==20 and all(0<=z<=18 for z in core)
    baseline=[r[0] for r in cyc]
    for name,c in [('plain-bulk',baseline),('repaired',core)]:
        x=lifetime(path,cyc,args.copies,c,args.steps)
        print(f'{name}: seed digits={2*(39+20*args.copies+20)}, first-mismatch={x}')
if __name__=='__main__':main()
