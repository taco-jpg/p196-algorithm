#!/usr/bin/env python3
"""Base-10 p=16 B overflow necklaces: necessary first-head filter, exact B check."""
import itertools
import subprocess
import sys
from pathlib import Path

def next_head(x, overflow):
    out = set()
    for carry in (0, 1):
        if overflow and x + carry >= 10:
            out.add(x % 10 + 1)
        if not overflow and x + carry < 10:
            out.add(2*x + carry)
    return out

def eligible(bits):
    for first in range(1,19):
        cur={first}
        for bit in bits:
            cur={z for x in cur for z in next_head(x,int(bit))}
            if not cur:
                break
        if first in cur:
            return True
    return False

def canonical(word):
    return min(word[i:]+word[:i] for i in range(len(word)))

def classify(k, check=False):
    words=set()
    for ones in itertools.combinations(range(16), k):
        idx=set(ones)
        words.add(canonical("".join("1" if j in idx else "0" for j in range(16))))
    survivors=sorted(word for word in words if eligible(word))
    print(f"weight={k} necklaces={len(words)} first_head_survivors={len(survivors)}",flush=True)
    if check:
        script=Path(__file__).with_name("bauto_py.py")
        for word in survivors:
            out=subprocess.run([sys.executable,str(script),word],capture_output=True,text=True,check=True,timeout=300).stdout.strip()
            print(word,out,flush=True)
            if "EXHAUSTED" not in out or "accepted 0" not in out:
                print("UNDECIDED or ACCEPT: do not claim exclusion",file=sys.stderr)
                raise SystemExit(1)
    return survivors

if __name__=="__main__":
    weights=[int(v) for v in sys.argv[1:] if v!="--check"] or list(range(17))
    check="--check" in sys.argv[1:]
    for k in weights:
        if not 0<=k<=16: raise SystemExit("weight must be 0..16")
        classify(k,check=check and 4<=k<=7)
