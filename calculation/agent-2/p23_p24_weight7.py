#!/usr/bin/env python3
"""All-width B exterior exact census at p=23,24 and sum(g)=7 (base 10).

Runs the repository's unchanged C++ structure/bauto.cpp.
A time limit, cap, or nonzero exit is UNDECIDED, never 'no cycle'.
"""
import argparse
import itertools
import subprocess
from pathlib import Path
from collections import Counter

def words(p,k=7):
    seen=set()
    for indices in itertools.combinations(range(p),k):
        mask=set(indices)
        w="".join("1" if i in mask else "0" for i in range(p))
        seen.add(min(w[j:]+w[:j] for j in range(p)))
    return sorted(seen)

def first_head_pass(w):
    for start in range(1,19):
        cur={start}
        for bit in w:
            nxt=set()
            for x in cur:
                for h in (0,1):
                    if bit=="1" and x+h>=10:
                        nxt.add(x%10+1)
                    if bit=="0" and x+h<10:
                        nxt.add(2*x+h)
            cur=nxt
            if not cur:break
        if start in cur:return True
    return False

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bauto")
    parser.add_argument("--cap",type=int,default=100000)
    parser.add_argument("--seconds",type=int,default=20)
    args=parser.parse_args()
    for p,want_total,want_head in ((23,10659,64),(24,14421,32)):
        allw=words(p)
        survivors=[w for w in allw if first_head_pass(w)]
        print("period",p,"necklaces",len(allw),"first-head",len(survivors),flush=True)
        assert len(allw)==want_total and len(survivors)==want_head
        if not args.bauto:
            continue
        binary=Path(args.bauto).resolve()
        if not binary.is_file():raise SystemExit("missing compiled bauto executable")
        count=Counter()
        for word in survivors:
            try:
                r=subprocess.run([str(binary),"10",str(p),str(p),"-g",word,
                                  "-cap",str(args.cap)],
                                 text=True,capture_output=True,timeout=args.seconds)
                if "ACCEPT" in r.stdout:
                    kind="ACCEPT"
                elif r.returncode or "state cap reached" in r.stderr or "key too long" in r.stderr:
                    kind="UNDECIDED"
                elif ("b=10 p="+str(p)+" done") in r.stderr:
                    kind="EXHAUSTED"
                else:
                    kind="UNDECIDED"
            except subprocess.TimeoutExpired:
                kind="UNDECIDED"
            count[kind]+=1
            if kind!="EXHAUSTED":print("NONEXHAUSTIVE",word,kind,flush=True)
        print("RESULT",p,dict(count),flush=True)
        if count["ACCEPT"] or count["UNDECIDED"]:
            raise SystemExit("NOT a valid negative for this scope")

if __name__=="__main__":
    main()
