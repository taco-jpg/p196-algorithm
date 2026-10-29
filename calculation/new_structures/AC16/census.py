#!/usr/bin/env python3
"""Reproduce AC16's exhaustive ENDPOINT-ONLY phase-7 W9 necessary-condition cell.
Uses the independently checked shared exact-carry engine V16. No strict-phase pruning.
From repo root: python3 calculation/new_structures/AC16/census.py --full
"""
import argparse, concurrent.futures, pathlib, re, subprocess, tempfile

TOTAL=30*(19**3+19**4)
CHUNK=TOTAL//5
ENGINE="calculation/new_structures/V16/strict_w9_cell_local.cpp"
LAT="calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"

def run(cmd):
    return subprocess.run(cmd,check=True,text=True,capture_output=True).stdout

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--full",action="store_true",help="exhaustive 4,115,400-candidate cell")
    p.add_argument("--sample",type=int,default=1000,help="non-exhaustive quick self-test")
    a=p.parse_args()
    assert pathlib.Path(ENGINE).is_file() and pathlib.Path(LAT).is_file()
    with tempfile.TemporaryDirectory() as d:
        exe=str(pathlib.Path(d)/"ac16w9")
        subprocess.run(["g++","-O3","-std=c++17",ENGINE,"-o",exe],check=True)
        ranges=[(i*CHUNK,CHUNK) for i in range(5)] if a.full else [(0,min(TOTAL,a.sample))]
        def cell(item):
            st,n=item
            cmd=[exe,"--endpoint-only","--phase","7","--q","14","--k","100",
                 "--steps","120","--collar","170","--start",str(st),"--limit",str(n)]
            s=run(cmd)
            m=re.search(r"range=\[(\d+),(\d+)\) tested=(\d+)",s)
            x=re.search(r"survivors=(\d+) clock_failures=(\d+)",s)
            assert m and x,(item,s[-1000:])
            lo,hi,checked=map(int,m.groups())
            restored,clock=map(int,x.groups())
            assert (lo,hi,checked)==(st,st+n,n)
            return checked,restored,clock
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(5,len(ranges))) as pool:
            result=list(pool.map(cell,ranges))
        total=sum(r[0] for r in result)
        restored=sum(r[1] for r in result)
        clockfail=sum(r[2] for r in result)
        assert restored==0 and clockfail==0
        assert total==(TOTAL if a.full else min(TOTAL,a.sample))
        print("label=COMPUTED lane=endpoint-only phase=7 J=3,4 U=30")
        print("tested",total,"domain",TOTAL,"W9_endpoint_restorations",restored,
              "rooted_clock_failures",clockfail)
        print("scope", "EXHAUSTED-reference-width" if a.full else "PARTIAL-sample")
if __name__=="__main__":
    main()
