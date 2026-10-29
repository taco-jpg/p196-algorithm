#!/usr/bin/env python3
"""Independent genuine Python integer reverse-and-add checker."""
import json,sys
from pathlib import Path
sys.set_int_max_str_digits(0)
ph=json.loads((Path(__file__).resolve().parent/"phase.json").read_text())
def seed(k):
    half=ph["B0"]+ph["W0"]*k
    lo=[p//2 for p in half]
    hi=[p-p//2 for p in half]
    return int("".join(map(str,hi+lo[::-1])))
def fnv(s):
    h=1469598103934665603
    for c in map(int,reversed(s)):
        h=((h^c)*1099511628211)&((1<<64)-1)
    return f"{h:x}"
def run(k=300,steps=2000):
    n=seed(k)
    for t in range(steps+1):
        s=str(n)
        assert s!=s[::-1],("palindrome",t)
        pairs=[int(s[i])+int(s[-1-i]) for i in range(len(s)//2)]
        target=ph["phase_B"][t%8]+ph["phase_W"][t%8]*((len(s)//2-39+19)//20)
        matched=next((i for i,(x,y) in enumerate(zip(pairs,target)) if x!=y),len(pairs))
        assert matched>=59,("prefix failure",t,matched)
        if t in (0,1,100,1000,2000,steps):
            print(f"bigint step={t} digits={len(s)} matched={matched} fnv64={fnv(s)}")
        if t<steps:n+=int(s[::-1])
    print(f"PASS independent BIGINT k={k} steps={steps}")
if __name__=="__main__":
    run(int(sys.argv[1]) if len(sys.argv)>1 else 300,int(sys.argv[2]) if len(sys.argv)>2 else 2000)
