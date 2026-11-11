#!/usr/bin/env python3
"""r12b: summarise khx census output files (gzip, one KHX line per word).
usage: census_summary.py OUTDIR PLIST  -> prints per-p table, writes OUTDIR/surv_p{p}.txt ("p g reason K kept") and
OUTDIR/summary_p{p}.json.  Primitive/imprimitive split by least period of the necklace word."""
import gzip, glob, json, sys, collections, os

def least_period(g):
    p = len(g)
    for d in range(1, p + 1):
        if p % d == 0 and g == g[:d] * (p // d):
            return d
    return p

outdir = sys.argv[1]
plist = [int(x) for x in sys.argv[2].split(",")]
for p in plist:
    files = sorted(glob.glob(os.path.join(outdir, "p%d_s*.khx.gz" % p)))
    n = 0; dies = 0; surv = 0; kdist = collections.Counter(); reasons = collections.Counter()
    nprim = 0; dies_prim = 0; seen = set(); dup = 0; bad = 0
    survl = []
    for fn in files:
        with gzip.open(fn, "rt") as f:
            for line in f:
                if not line.startswith("KHX"):
                    bad += 1; continue
                tok = line.split()
                d = dict(t.split("=", 1) for t in tok[1:] if "=" in t)
                g = d["g"]
                if len(g) != p or d["p"] != str(p): bad += 1; continue
                if g in seen: dup += 1
                seen.add(g)
                n += 1
                prim = least_period(g) == p
                nprim += prim
                if tok[4] == "DIES":
                    dies += 1; dies_prim += prim; kdist[int(d["K"])] += 1
                else:
                    surv += 1; reasons[d["reason"]] += 1
                    survl.append("%d %s %s %s %s %s" % (p, g, d["reason"], d["K"], d.get("kept", "?"), "prim" if prim else "imprim(root %d)" % least_period(g)))
    with open(os.path.join(outdir, "surv_p%d.txt" % p), "w") as f:
        f.write("\n".join(survl) + ("\n" if survl else ""))
    summ = dict(p=p, words=n, primitive=nprim, dies=dies, dies_primitive=dies_prim, survives=surv, reasons=dict(reasons),
                kdist=dict(sorted(kdist.items())), duplicates=dup, badlines=bad, files=len(files))
    with open(os.path.join(outdir, "summary_p%d.json" % p), "w") as f:
        json.dump(summ, f)
    print("p=%d words=%d primitive=%d DIES=%d SURVIVES=%d %s dup=%d bad=%d maxK=%d" % (p, n, nprim, dies, surv, dict(reasons), dup, bad, max(kdist) if kdist else -1))
