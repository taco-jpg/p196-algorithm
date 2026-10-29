#!/usr/bin/env python3
"""Compare full numeric FNV fingerprints and phase diagnostics, independent engines."""
import re,sys
from pathlib import Path

pattern=re.compile(r'^CHECKPOINT (\d+) digits=(\d+) A=(\d+) B=(\d+) digest=([0-9a-f]+) numeric_fnv=([0-9a-f]+)$')
def parse(filename):
    z={}
    for line in Path(filename).read_text().splitlines():
        m=pattern.fullmatch(line)
        if m:z[int(m.group(1))]=m.groups()[1:]
    assert set(z)=={0,5000,10000,15000,20000},(filename,z.keys())
    return z

def compare(a,b):
    assert a==b,'DIFFERENT ORBITS OR SHAPES'

def main():
    assert len(sys.argv)==3,'USAGE digit20k.log gmp20k.log'
    a,b=parse(sys.argv[1]),parse(sys.argv[2]);compare(a,b)
    altered=dict(a);altered[10000]=(*a[10000][:-1],'0')
    try:compare(altered,b)
    except AssertionError:pass
    else:raise AssertionError('corruption accepted')
    print('INDEPENDENT_FULL_NUMBER_DIGESTS_AND_SHAPES_EQUAL_ALL_FIVE_CHECKPOINTS')
    print('MUTATED_HASH_REJECTED')
if __name__=='__main__':main()