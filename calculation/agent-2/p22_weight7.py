#!/usr/bin/env python3
"""Exact p=22, sum(g)=7 B-cycle census in base 10.

Uses the repository's exact structure/bauto.cpp, and a distinct independent
first-head necessary filter. A cap/timeout must be reported UNDECIDED.
"""
import itertools
import argparse
import subprocess
from collections import Counter
from pathlib import Path

P, WEIGHT=22,7

def rotations(word):
    return (word[i:]+word[:i] for i in range(len(word)))

def all_necklaces():
    seen=set()
    for digits in itertools.combinations(range(P),WEIGHT):
        positions=set(digits)
        word="".join("1" if i in positions else "0" for i in range(P))
        seen.add(min(rotations(word)))
    return sorted(seen)

def possible(word):
    for x0 in range(1,19):
        frontier={x0}
        for bit in word:
            is_overflow=(bit=="1")
            nexts=set()
            for x in frontier:
                for h in (0,1):
                    if is_overflow and x+h>=10:
                        nexts.add(x%10+1)
                    elif not is_overflow and x+h<10:
                        nexts.add(2*x+h)
            frontier=nexts
            if not frontier: break
        if x0 in frontier:
            return True
    return False

def classify(bauto,cap,seconds):
    words=all_necklaces()
    survivors=[w for w in words if possible(w)]
    print("necklaces",len(words),"necessary survivors",len(survivors),flush=True)
    assert len(words)==7752 and len(survivors)==107
    if bauto is None:
        return
    executable=Path(bauto).resolve()
    if not executable.is_file():
        raise SystemExit("missing compiled structure/bauto binary")
    result=Counter()
    for w in survivors:
        try:
            r=subprocess.run([str(executable),"10",str(P),str(P),"-g",w,
                              "-cap",str(cap)],capture_output=True,text=True,
                             timeout=seconds)
            if "ACCEPT" in r.stdout:
                state="ACCEPT"
            elif r.returncode !=0 or "state cap reached" in r.stderr or "key too long" in r.stderr:
                state="UNDECIDED"
            elif "b=10 p=22 done" in r.stderr:
                state="EXHAUSTED"
            else:
                state="UNDECIDED"
        except subprocess.TimeoutExpired:
            state="UNDECIDED"
        result[state]+=1
        if state!="EXHAUSTED":
            print(w,state,flush=True)
    print("EXACT B CHECK",dict(result),flush=True)
    if result["ACCEPT"] or result["UNDECIDED"]:
        raise SystemExit("NOT a complete exclusion")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bauto",help="path of compiled calculation/neutral_band/structure/bauto.cpp")
    p.add_argument("--cap",type=int,default=100000)
    p.add_argument("--timeout",type=int,default=20)
    a=p.parse_args()
    classify(a.bauto,a.cap,a.timeout)
