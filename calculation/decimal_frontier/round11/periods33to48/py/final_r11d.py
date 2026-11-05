#!/usr/bin/env python3
"""r11d final table: wire status = bx3 (out/db) or bxb (out/dbB) decisive, else K-head filter (kfam/res_kfam_w*.txt) DIES, else UNDECIDED.
band status = bxb only (out/dbB).  Writes out/final_open_wire.txt and out/final_open_band.txt."""
import json,glob,collections
DEC=("EXHAUSTED","ACCEPT")
def load(files):
    db={}
    for f in files:
        for l in open(f):
            r=json.loads(l); k=(r["p"],r["g"]); o=db.get(k)
            if o and o["status"] in DEC: continue
            if o and r["status"].startswith("CAPPED") and o.get("cap",0)>r.get("cap",0): continue
            db[k]=r
    return db
W=load(sorted(glob.glob("out/db/b10_p*.jsonl"))); B=load(sorted(glob.glob("out/dbB/b10_p*.jsonl")))
KF={}
for f in glob.glob("kfam/res_kfam_w*.txt"):
    for l in open(f):
        a=l.split()
        if len(a)>=3: KF[(int(a[0]),a[1])]=(a[2],a[3] if len(a)>3 else "")
REP={"000011100010000111000100001110001":"p11^3","00001110001000011100010000111000100001110001":"p11^4","000100010001000100010001000100010001000100010001":"N12^4"}
ow=open("out/final_open_wire.txt","w"); ob=open("out/final_open_band.txt","w")
print("| p | words run | wire: bx EXHAUSTED | ACCEPT | K-head DIES | wire UNDECIDED (of which known repetitions) | band-checked | band EXHAUSTED | band hits | band UNDECIDED |")
print("|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
for p in sorted({k[0] for k in set(W)|set(B)}):
    ks=[k for k in set(W)|set(B) if k[0]==p]; c=collections.Counter()
    for k in ks:
        st=[x["status"] for x in (W.get(k),B.get(k)) if x]
        if "ACCEPT" in st: c["acc"]+=1
        elif "EXHAUSTED" in st: c["exh"]+=1
        elif KF.get(k,("",""))[0]=="DIES": c["kf"]+=1
        else:
            c["open"]+=1; c["rep"]+= k[1] in REP; ow.write(f"{p} {k[1]} {REP.get(k[1],'')}\n")
        b=B.get(k)
        if b and p%2==0:
            c["bchk"]+=1; c["bhit"]+= bool(b.get("band"))
            if b["status"] in DEC: c["bexh"]+=1
            else: c["bopen"]+=1; ob.write(f"{p} {k[1]}\n")
    bc = (f"{c['bchk']} | {c['bexh']} | {c['bhit']} | {c['bopen']}") if p%2==0 else "- | - | - | - (odd T: no band period divides T)"
    print(f"| {p} | {len(ks)} | {c['exh']} | {c['acc']} | {c['kf']} | {c['open']} ({c['rep']}) | {bc} |")
