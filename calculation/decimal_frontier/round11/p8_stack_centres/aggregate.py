#!/usr/bin/env python3
"""r11a: aggregate cen2 RESULT lines in runs/ by (table, K, q0) over all lengths / shards.  usage: aggregate.py"""
import glob, collections
agg = collections.OrderedDict()
for f in sorted(glob.glob("runs/*.log")):
    if "ctrl" in f:
        continue
    l = open(f).readline()
    if not l.startswith("RESULT"):
        print("BAD", f); continue
    d = dict(x.split("=", 1) for x in l.split()[1:] if "=" in x)
    key = (d["tbl"].replace(".tbl", ""), int(d["K"]), int(d["q0"]))
    a = agg.setdefault(key, {"L": collections.Counter(), "n": 0, "ret": 0, "clk": 0, "len": 0, "gf": 0, "mp": 0})
    a["L"][int(d["L"])] += int(d["centres"])
    for k, f2 in (("n", "centres"), ("ret", "returns"), ("clk", "clockdev"), ("len", "lenerr"), ("gf", "guardfail")):
        a[k] += int(d[f2])
    a["mp"] = max(a["mp"], int(d["maxprefix"]))
for k in sorted(agg):
    a = agg[k]; Ls = sorted(a["L"])
    full = all(a["L"][L] == 19 ** (L // 2) * (10 if L % 2 else 1) for L in Ls)
    print(f"{k[0]:5s} K={k[1]} q={k[2]:2d} L={Ls[0]}..{Ls[-1]} complete={full} centres={a['n']} returns={a['ret']} "
          f"clockdev={a['clk']} lenerr={a['len']} guardfail={a['gf']} maxprefix={a['mp']}")
