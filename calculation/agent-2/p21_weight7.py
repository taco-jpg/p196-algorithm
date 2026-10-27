#!/usr/bin/env python3
"""Full base-10 P=21 k=7 B overflow-census, using existing exact bauto.

First-head filter is a sound overapproximation. An EXHAUSTED B automaton run
with zero ACCEPT rejects the fixed overflow word for B of arbitrary length.
Never label caps, timeouts, or nonzero subprocess exits as EXHAUSTED.
"""
import argparse
import itertools
import subprocess
from pathlib import Path

def nextx(x,g):
    ans=set()
    for h in (0,1):
        if g and x+h>=10:
            ans.add(x%10+1)
        if not g and x+h<10:
            ans.add(2*x+h)
    return ans

def may_cycle(bits):
    for start in range(1,19):
        states={start}
        for digit in bits:
            states={z for x in states for z in nextx(x,int(digit))}
            if not states:
                break
        if start in states: return True
    return False

def canonical(word):
    return min(word[i:]+word[:i] for i in range(len(word)))

def enumerate_g(p=21,k=7):
    words=set()
    for ones in itertools.combinations(range(p),k):
        group=set(ones)
        word="".join("1" if i in group else "0" for i in range(p))
        words.add(canonical(word))
    return words,sorted(w for w in words if may_cycle(w))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bauto",help="Compiled calculation/neutral_band/structure/bauto.cpp")
    ap.add_argument("--cap",type=int,default=100000)
    ap.add_argument("--timeout",type=int,default=20)
    args=ap.parse_args()
    allg, survivors=enumerate_g()
    print("P=21 weight=7 necklaces",len(allg),"first-head survivors",len(survivors),flush=True)
    assert len(allg)==5538 and len(survivors)==145
    if not args.bauto:
        print("Add --bauto PATH for exact exhaustive stage.")
        return
    binary=Path(args.bauto)
    if not binary.is_file():
        raise SystemExit("compiled bauto not found")
    counts={"EXHAUSTED":0,"ACCEPT":0,"UNDECIDED":0}
    for word in survivors:
        try:
            r=subprocess.run([str(binary.resolve()),"10","21","21","-g",word,
                              "-cap",str(args.cap)],capture_output=True,
                             text=True,timeout=args.timeout)
            if "ACCEPT" in r.stdout:
                status="ACCEPT"
            elif r.returncode!=0 or "state cap reached" in r.stderr or "key too long" in r.stderr:
                status="UNDECIDED"
            elif "b=10 p=21 done" not in r.stderr:
                status="UNDECIDED"
            else:
                status="EXHAUSTED"
        except subprocess.TimeoutExpired:
            status="UNDECIDED"
        counts[status]+=1
        if status!="EXHAUSTED":
            print(word,status,flush=True)
    print("EXACT B RESULT",counts,flush=True)
    if counts["UNDECIDED"] or counts["ACCEPT"]:
        raise SystemExit("NOT A NEGATIVE: unresolved or accepted B stream")

if __name__=="__main__":
    main()
