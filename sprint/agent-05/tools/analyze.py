"""Merge delay tables and cross-check them against the repo's certified bounds.

usage: python3 analyze.py OUTDIR table1.txt [table2.txt ...]

Writes OUTDIR/max_delay_P{3,4,5}.tsv (prefix, max delay, smallest witness seed
at that delay, palindrome width, source table) and prints the consistency checks.
Inputs: tables written by delays.cpp; repo_bounds.json (from extract_entries.py);
three_digit_marks.json (parsed from RESULTS.md).
"""
import sys, json, os
from collections import Counter

outdir = sys.argv[1]; files = sys.argv[2:]
os.makedirs(outdir, exist_ok=True)
best = {3: {}, 4: {}, 5: {}}

def better(a, b):  # is a better than b
    if b is None: return True
    if a[0] != b[0]: return a[0] > b[0]
    if len(a[1]) != len(b[1]): return len(a[1]) < len(b[1])
    return a[1] < b[1]

for f in files:
    for line in open(f):
        if not line.startswith('P'): continue
        tag, pre, t, seed, w = line.split()
        L = int(tag[1:]); cand = (int(t), seed, int(w), os.path.basename(f))
        if better(cand, best[L].get(pre)): best[L][pre] = cand

for L in (3, 4, 5):
    with open(f"{outdir}/max_delay_P{L}.tsv", "w") as fo:
        fo.write("prefix\tmax_delay\twitness_seed\tpalindrome_width\tsource\n")
        for p in sorted(best[L]):
            t, s, w, src = best[L][p]
            fo.write(f"{p}\t{t}\t{s}\t{w}\t{src}\n")

here = os.path.dirname(os.path.abspath(__file__))
def datafile(name):
    for d in (here, os.path.join(here, "..", "data"), "."):
        if os.path.exists(os.path.join(d, name)): return os.path.join(d, name)
    raise FileNotFoundError(name)
bounds = json.load(open(datafile("repo_bounds.json")))
bounds["2641"] = 5  # Agent117P2641: ancestry_2641 gives t <= 6
marks = json.load(open(datafile("three_digit_marks.json")))

print(f"prefixes with a witness: P3 {len(best[3])}/900, P4 {len(best[4])}/9000, P5 {len(best[5])}/90000")

# 1. four-digit certified entries: witness delay must be <= bound + 1
viol, slack, tight = [], Counter(), []
for p, b in bounds.items():
    if p in best[4]:
        t = best[4][p][0]
        if t > b + 1: viol.append((p, b, best[4][p]))
        slack[b + 1 - t] += 1
        if t == b + 1: tight.append((p, b, best[4][p][0], best[4][p][1]))
print(f"[check 1] certified 4-digit entries: {len(bounds)}; violations (delay > bound+1): {len(viol)}")
for v in viol: print("   VIOLATION", v)
print(f"   slack (bound+1 - max witness delay) histogram: {sorted(slack.items())}")
print(f"   entries whose bound is attained (sharp): {len(tight)}")
mxc = max((best[4][p][0], p, b) for p, b in bounds.items() if p in best[4])
print(f"   largest witness delay to a certified prefix: {mxc[0]} (prefix {mxc[1]}, rank bound {mxc[2]})")
print(f"   largest certified bound: {max(bounds.values())}; certified prefixes with witness delay > 11: {sum(best[4][p][0] > 11 for p in bounds if p in best[4])}")
for x in sorted(tight, key=lambda x: -x[1])[:15]: print("     sharp", x)

# 2. three-digit exclusions by ancestry bound (Core C, kernels K, classes S) need delay <= 100
v2 = []
for p, m in marks.items():
    if m in "CKS" and p in best[3] and best[3][p][0] > 100: v2.append((p, m, best[3][p]))
print(f"[check 2] three-digit cells marked C/K/S: {sum(m in 'CKS' for m in marks.values())}; with witness delay > 100: {len(v2)}")
for v in v2: print("   VIOLATION", v)
known = {"620": 12, "739": 39}
for p, B in known.items():
    t = best[3].get(p, (None,))[0]
    print(f"   {p}: max witness delay {t} vs proved ancestry bound {B}" + ("  VIOLATION" if t and t > B else ""))
mx = Counter()
for p, m in marks.items():
    if p in best[3]: mx[m] = max(mx[m], best[3][p][0])
print(f"   max witness delay per mark: {dict(mx)}")

# 3. four-digit prefixes by repo status
def status4(p):
    if p in bounds: return "certified-4"
    m = marks[p[:3]]
    if m in "CKSF": return "parent-excluded(" + m + ")"
    if m == "x": return "parent-cycle"
    return "repo-open"
st = Counter(status4(f"{i}") for i in range(1000, 10000))
print(f"[status] four-digit prefixes by repo status: {dict(st)}")
for thr in (50, 80, 100, 120, 150, 200, 250):
    c = Counter(status4(p) for p, v in best[4].items() if v[0] > thr)
    print(f"   delay > {thr}: {sum(c.values())}  {dict(c)}")
for thr in (1, 2, 4, 8):
    c = Counter(status4(p) for p, v in best[4].items() if v[0] <= thr)
    print(f"   delay <= {thr}: {sum(c.values())}  {dict(c)}")
over = sorted(((v[0], p, v[1], status4(p)) for p, v in best[4].items() if v[0] > 100), reverse=True)
with open(f"{outdir}/P4_delay_over_100.tsv", "w") as fo:
    fo.write("prefix\tmax_delay\twitness_seed\trepo_status\n")
    for t, p, s, stt in over: fo.write(f"{p}\t{t}\t{s}\t{stt}\n")
print(f"   wrote {outdir}/P4_delay_over_100.tsv ({len(over)} prefixes)")
