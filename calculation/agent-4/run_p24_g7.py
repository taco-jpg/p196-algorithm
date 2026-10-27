#!/usr/bin/env python3
"""Agent 4, scoped p24 weight-seven all-width B-cycle computation, not Lean."""
from collections import Counter
from pathlib import Path
import re, subprocess, sys

root=Path(__file__).resolve().parent
words=subprocess.check_output(
    [str(root/"low_digit_automaton"),"--emit","24"],text=True
).splitlines()
words=[w for w in words if w.count("1")==7]
assert len(words)==32,len(words)
results=[]
for w in words:
    try:
        p=subprocess.run([str(root/"fixed_g_B_probe"),w,"2000000","100"],
                         capture_output=True,text=True,timeout=7)
    except subprocess.TimeoutExpired:
        results.append((w,"TIMEOUT-UNDECIDED",0,0));continue
    line=p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "ERROR"
    status=line.split(" ")[0]
    match=re.search(r"depth=(\d+) states=(\d+)",line)
    depth,states=(int(match[1]),int(match[2])) if match else (0,0)
    results.append((w,status,depth,states))
print("candidate_necklaces=",len(words))
print("statuses=",dict(Counter(r[1] for r in results)))
print("max_states_word=",max((r[3],r[0],r[2]) for r in results))
for w,s,d,n in results:
    if s!="EXHAUSTED-NO-B-CYCLE":print("UNRESOLVED",w,s,d,n)
if any(z[1]!="EXHAUSTED-NO-B-CYCLE" for z in results):sys.exit(1)
print("COMPUTED p24 weight7: all 32 exhaustive full-B negatives")
