#!/usr/bin/env python3
"""Agent 4, T2 p23 eight overflows, exact B-position census (not Lean)."""
from collections import Counter
from pathlib import Path
import re
import subprocess
import sys

home=Path(__file__).resolve().parent
words=subprocess.check_output(
    [str(home/"low_digit_automaton"),"--emit","23"],text=True
).splitlines()
words=[w for w in words if w.count("1")==8]
assert len(words)==463,len(words)
results=[]
for w in words:
    try:
        proc=subprocess.run(
            [str(home/"fixed_g_B_probe"),w,"2000000","100"],
            capture_output=True,text=True,timeout=7
        )
    except subprocess.TimeoutExpired:
        results.append((w,"TIMEOUT-UNDECIDED",0,0));continue
    line=proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else "ERROR"
    status=line.split()[0]
    m=re.search(r"depth=(\d+) states=(\d+)",line)
    depth,states=(int(m[1]),int(m[2])) if m else (0,0)
    results.append((w,status,depth,states))
print("candidate_necklaces=",len(words))
print("status_counts=",dict(Counter(z[1] for z in results)))
print("max_states_word=",max((z[3],z[0],z[2]) for z in results))
for w,status,depth,states in results:
    if status!="EXHAUSTED-NO-B-CYCLE":
        print("UNRESOLVED",w,status,depth,states)
if any(z[1]!="EXHAUSTED-NO-B-CYCLE" for z in results):sys.exit(1)
print("COMPUTED p23 weight8: all 463 B-position searches exhausted")
