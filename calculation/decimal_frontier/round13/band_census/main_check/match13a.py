import json,os
H=os.path.expanduser("~/p196_run/mchk13a/logs")
want={(11,8,5):"(13,2,13)",(13,10,7):"(5,16,5)"}
def rots(v):
    return {tuple(v[i:]+v[:i]) for i in range(len(v))}
for l in open(f"{H}/scan_1000.jsonl"):
    r=json.loads(l)
    V=r["V"]
    hit=[w for w in want if tuple(w) in rots(list(V))]
    # V may be longer (repeated); test whether V is a rotation of a target or of a repeat
    if hit:
        print("BAND",V,"T",r["T"],"want",[want[w] for w in hit])
        for o in r["orbits"]:
            print("  orbit",o["o"],"empty",o["empty"],"nper",o["nper"])
            for p in o["periodic"][:12]:
                print("    K",p[0],"per",p[2],"word",p[6].strip()[:90])
