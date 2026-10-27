#!/usr/bin/env python3
"""Agent 4 T2: exact capped p23/weight9 B census, no cap-as-negative."""
from pathlib import Path
from collections import Counter
import re,subprocess,sys,time
home=Path(__file__).resolve().parent
words=subprocess.check_output([str(home/"low_digit_automaton"),"--emit","23"],text=True).splitlines()
words=[w for w in words if w.count("1")==9]
assert len(words)==731,len(words)
results=[]
start=time.monotonic()
for i,w in enumerate(words):
    if time.monotonic()-start>65:
        results.extend((v,"NOT_RUN",0,0) for v in words[i:])
        break
    try:
        p=subprocess.run([str(home/"fixed_g_B_probe"),w,"2000000","100"],
                         capture_output=True,text=True,timeout=5)
    except subprocess.TimeoutExpired:
        results.append((w,"TIMEOUT",0,0))
        continue
    line=p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "ERROR"
    status=line.split()[0]
    if p.returncode not in (0,3): status="ERROR_EXIT_"+str(p.returncode)
    m=re.search(r"depth=(\d+) states=(\d+)",line)
    depth,states=(int(m[1]),int(m[2])) if m else (0,0)
    if status=="ACCEPT":
        print("B_CYCLE_CANDIDATE",w,line,flush=True)
        witness=subprocess.run([str(home/"fixed_g_B_probe"),w,"2000000","100","-w"],
                               capture_output=True,text=True,timeout=12)
        print(witness.stdout,flush=True)
    results.append((w,status,depth,states))
counts=Counter(r[1] for r in results)
print("p23 weight9 candidate_necklaces=",len(words))
print("status_counts=",dict(sorted(counts.items())))
print("max_states_word=",max((r[3],r[0],r[2]) for r in results))
print("elapsed_seconds=",round(time.monotonic()-start,3))
for w,s,d,n in results:
    if s!="EXHAUSTED-NO-B-CYCLE": print("UNRESOLVED_OR_ACCEPT",w,s,d,n)
passed=all(r[1]=="EXHAUSTED-NO-B-CYCLE" for r in results)
print("ALL_EXHAUSTED=",passed)
if not passed: sys.exit(1)
