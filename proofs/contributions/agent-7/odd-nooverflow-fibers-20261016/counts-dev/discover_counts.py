#!/usr/bin/env python3
"""Exact bounded discovery only. Does not establish any Lean theorem."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

def step(tag, x):
    a,b,c,d=x
    return {
        "E":(a,c,b,d), "O":(c,a,d,b), "M":(c,a+b,c+d,b),
        "Z":(a,0,b,d), "H":(a,c,0,d),
    }[tag]

vectors={(1,0,0,0):""}
rows=[]
f0,f1=0,1
nine=(1,0,0,0)
for m in range(17):
    vals=[(max(x[0]+x[1],x[2]+x[3]),x,w) for x,w in vectors.items()]
    best=max(vals)
    maxdiff=max(abs(x[0]+x[1]-x[2]-x[3]) for x in vectors)
    rec={"m":m,"reachable_vectors":len(vectors),"maximum":best[0],"witness_vector":best[1],"witness_word":best[2],"nines_vector":nine,"nines_endpoint":max(nine[0]+nine[1],nine[2]+nine[3]),"fib_m_plus_one":f1,"max_endpoint_difference":maxdiff}
    rows.append(rec)
    print(rec,flush=True)
    if m==16:
        break
    nxt={}
    for x,w in vectors.items():
        for tag in "EOMZH":
            nxt.setdefault(step(tag,x),w+tag)
    vectors=nxt
    nine=step("M",nine)
    f0,f1=f1,f0+f1

(ROOT/"bounded-discovery.json").write_text(json.dumps({"status":"EXPERIMENTAL_ONLY", "includes_boundary_deletions":True,"rows":rows},indent=2)+"\n")
