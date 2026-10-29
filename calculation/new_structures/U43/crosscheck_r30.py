#!/usr/bin/env python3
"""Three-way regression control: R30 symbolic/concrete checker vs U43 traces.

This compares only a known non-returning control fixture; it does not promote
that fixture or its finite orbit to a Lychrel result.
"""
import argparse
import json
import subprocess
from pathlib import Path


def json_lines(text):
    out=[]
    for line in text.splitlines():
        line=line.strip()
        if line.startswith("{"):
            try: out.append(json.loads(line))
            except json.JSONDecodeError: pass
    return out


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--simulator",required=True,type=Path)
    ap.add_argument("--lattice",required=True,type=Path)
    args=ap.parse_args()
    here=Path(__file__).resolve().parent
    root=here.parents[2]
    widths="20:20,40:40,80:80,160:160"
    r30=subprocess.run(["python3",str(root/"tools/parametric_verify_r30.py"),
                        "--lattice",str(args.lattice),"--J","5","--U","9,14,4","--C","10",
                        "--qmin","256","--kmin","256","--steps","120"],
                       text=True,capture_output=True,check=True)
    u43=subprocess.run(["python3",str(here/"crosscheck.py"),"--simulator",str(args.simulator),
                        "--lattice",str(args.lattice),"--J","5","--U","9,14,4","--C","10",
                        "--widths",widths,"--steps","120","--epoch","120","--gain","5"],
                       text=True,capture_output=True,check=True)
    a=[x for x in json_lines(r30.stdout) if "q" in x and "first_mismatch" in x]
    b=[x for x in json_lines(u43.stdout) if "q" in x and "checkpoints" in x]
    assert len(a)==len(b)==4,(r30.stdout,u43.stdout)
    gamma_clock=[1,0,0,0,1,0,0,0,1,0,0,0]
    expected_clock="".join(str(x) for x in gamma_clock*10)
    for x,y in zip(a,b):
        c=y["checkpoints"][-1]
        assert (x["q"],x["k"])==(y["q"],y["k"])
        assert x["return"]==c["return"]
        assert x["first_mismatch"]==c["first_mismatch"]
        assert x["digits"]==c["actual_pairword_length"]
        assert x["expected_digits"]==c["expected_pairword_length"]
        assert x["gamma"]==expected_clock
        assert x["sum_gamma"]==y["overflow_total"]==30
        assert y["clock_mismatches"]==0
    symbolic=[line for line in r30.stdout.splitlines() if line.startswith("SYMBOLIC ")]
    assert len(symbolic)==1 and '"clock_exact": true' in symbolic[0]
    print(json.dumps({"summary":"R30_CONTROL_CROSSCHECK_PASS","widths":[20,40,80,160],
                      "steps_compared":120,"engines":["R30 parametric verifier","U43 C++ digit-array","U43 Python bigint"],
                      "comparison":"exact return status, first mismatch, length, and overflow clock"},separators=(",",":")))

if __name__=="__main__":main()
