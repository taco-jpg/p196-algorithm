#!/usr/bin/env python3
"""r12b: final tables.  Reads census summaries, the deep passes and the uniqueness list; writes out/final_table.md,
out/final_open.txt (UNDECIDED words with reason) and out/r11_status.txt (status of every round-11 open word)."""
import json, glob, collections, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the route directory (Studio: ~/p196_run/r12b)
def least_period(g):
    p = len(g)
    for d in range(1, p + 1):
        if p % d == 0 and g == g[:d] * (p // d): return d
def parse(files):
    res = {}
    for fn in files:
        for l in open(fn):
            if not l.startswith("KHX"): continue
            t = l.split(); d = dict(x.split("=", 1) for x in t[1:] if "=" in x)
            res.setdefault(d["g"], []).append((t[4], int(d["K"]), d.get("reason", ""), fn))
    return res
deep_old = parse(glob.glob("out/pass2/*_s*.out") + glob.glob("out/deep/R_s*.out") + glob.glob("out/deep/A_s*.out"))
deep_new = parse(glob.glob("out/pass3/*_s*.out") + glob.glob("out/pass4/*.log"))
# pass-4 runs stopped by hand (no KHX line): take the last level line as SURVIVES (stopped)
P47 = "00010001000110001100010010001010100101000100011"
for fnr in sorted(glob.glob("out/pass4/p47*.log")):
    last = [l for l in open(fnr) if l.startswith("  K=")]
    if last and not any(l.startswith("KHX") for l in open(fnr)):
        K = int(last[-1].split()[0][2:])
        deep_new.setdefault(P47, []).append(("SURVIVES", K, "stopped by hand", fnr))
# runs with the primitive root as pattern and -L (out/fam): key them by the full clock word root^(L/|root|)
FAMRUNS = {"out/fam/h11b_L44.log": ("00010010111", 44), "out/fam/p21_L42.log": ("001001010101001010101", 42), "out/fam/h9_L45.log": ("001010101", 45), "out/fam/h01_L40.log": ("01", 40), "out/fam/h01_L48.log": ("01", 48), "out/n12/L48.log": ("0001", 48), "out/n12/L36.log": ("0001", 36)}
for fnr, (root, L) in FAMRUNS.items():
    if not os.path.exists(fnr): continue
    lines = open(fnr).readlines()
    if not any(l.startswith("KHX") for l in lines):
        last = [l for l in lines if l.startswith("  K=")]
        if last: deep_new.setdefault(root * (L // len(root)), []).append(("SURVIVES", int(last[-1].split()[0][2:]), "stopped by hand, root pattern", fnr))
    for l in lines:
        if l.startswith("KHX"):
            t = l.split(); d = dict(x.split("=", 1) for x in t[1:] if "=" in x)
            deep_new.setdefault(root * (L // len(root)), []).append((t[4], int(d["K"]), d.get("reason", ""), fnr))
UNIQUE = {  # Theorem U (stabilization), out/uniq/ : clock -> statement
    "000011100010000111000100001110001": "p11^3: only p11 repeated (Theorem U), no band",
    "00001110001000011100010000111000100001110001": "p11^4: only p11 repeated (Theorem U), no band",
    "000100010001000100010001000100010001": "N12^3=(0001)^9: only N12 repeated (Theorem U, P(9)), no band",
}
FAMILY = {"01": "(01)^{4j}: persistent 8-periodic K-head SCC, kept set grows exponentially (khx cannot decide)",
          "0001": "(0001)^{3j} = N12^j: N12 is a closed walk at every K; kept set not stabilised"}
def verdict(g):
    if g in UNIQUE: return "UNIQUE", UNIQUE[g]
    for src in (deep_new, deep_old):
        for st, K, why, fn in src.get(g, []):
            if st == "DIES": return "DIES", "%s K=%d (%s)" % ("khx3 -batch" if src is deep_new else "khx", K, os.path.basename(fn))
    r = g[:least_period(g)]
    why = FAMILY.get(r, "")
    lst = deep_new.get(g, []) + deep_old.get(g, [])
    best = max(lst, key=lambda x: x[1]) if lst else None
    return "UNDECIDED", (why + "; " if why else "") + ("survives to K=%d (%s)" % (best[1], best[2]) if best else "not run")
rows = []; openl = []; tot = collections.Counter()
for p in range(41, 49):
    s = json.load(open("out/census/summary_p%d.json" % p))
    surv = [l.split() for l in open("out/census/surv_p%d.txt" % p) if l.strip()]
    c = collections.Counter(); cprim = collections.Counter()
    for t in surv:
        g = t[1]; v, why = verdict(g); prim = least_period(g) == p
        c[v] += 1; cprim[v] += prim
        if v != "DIES": openl.append("%d %s %s %s :: %s" % (p, g, "prim" if prim else "imprim(root %d)" % least_period(g), v, why))
    band = ("decided = same words (Thm K, U)" if p % 2 == 0 else "no odd-period band") + (", open: %d" % c["UNDECIDED"] if p % 2 == 0 else "")
    tot["words"] += s["words"]; tot["prim"] += s["primitive"]; tot["d1"] += s["dies"]; tot["surv"] += len(surv)
    tot["dd"] += c["DIES"]; tot["u"] += c["UNIQUE"]; tot["und"] += c["UNDECIDED"]
    rows.append("| %d | %d | %d | %d | %d | %d | %d | %d | %d | %s |" % (p, s["words"], s["primitive"], s["dies"], len(surv), c["DIES"], c["UNIQUE"], c["UNDECIDED"], s["words"] - c["UNDECIDED"], band))
rows.append("| all | %d | %d | %d | %d | %d | %d | %d | %d | |" % (tot["words"], tot["prim"], tot["d1"], tot["surv"], tot["dd"], tot["u"], tot["und"], tot["words"] - tot["und"]))
hdr = ["| p = T | F1 words | primitive | pass-1 DIES | pass-1 survivors | deep DIES | known stream only (Thm U) | UNDECIDED | decided | uniform bands |",
       "|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|"]
open("out/final_table.md", "w").write("\n".join(hdr + rows) + "\n")
open("out/final_open.txt", "w").write("\n".join(openl) + "\n")
# round-11 open words
st = collections.Counter(); lines = []
for kind, fn in (("wire", "r11ref/final_open_wire.txt"), ("band", "r11ref/final_open_band.txt")):
    for l in open(fn):
        t = l.split()
        if not t: continue
        p, g = int(t[0]), t[1]
        v, why = verdict(g)
        if v == "UNDECIDED" and g in ("0001" * 10, "0001" * 11): v, why = "DIES", "Theorem A (3 | r); khx 0001 L=40 dies K=13"
        st[(kind, v)] += 1
        lines.append("%s %d %s %s :: %s" % (kind, p, g, v, why))
open("out/r11_status.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(hdr + rows)); print()
for k in sorted(st): print(k, st[k])
print(); print("\n".join(openl))
