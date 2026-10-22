"""Join an external prefix list against the max-delay table.

usage: python3 check_list.py max_delay_P4.tsv LIST.txt

LIST lines: "PREFIX" (an open prefix) or "PREFIX BOUND" (a certified prefix with
rank bound BOUND, i.e. claimed ancestry bound t <= BOUND + 1). Digits may be
written 4456 or [4,4,5,6]; '#' starts a comment.

For certified lines, any witness delay > BOUND + 1 is a contradiction: either the
certificate pipeline or this table is wrong (the witness can be re-checked with
`python3 -c` in two lines, or in Lean with Sprint.Agent05.witnessOK).
For open lines, prints how many need N >= delay in the base check.
"""
import sys, re
best = {}
for line in open(sys.argv[1]):
    if line.startswith("prefix"): continue
    p, t, s = line.split("\t")[:3]
    best[p] = (int(t), s)
cert, opn = [], []
for line in open(sys.argv[2]):
    line = line.split("#")[0].strip()
    if not line: continue
    m = re.match(r"\[?([\d,\s]+)\]?\s*[,;\s]\s*(\d+)?\s*\)?$", line) or re.match(r"\[?([\d,\s]+)\]?$", line)
    digits = re.sub(r"[^\d]", "", m.group(1))
    b = m.group(2) if m.lastindex and m.lastindex >= 2 else None
    (cert if b is not None else opn).append((digits, None if b is None else int(b)))
bad = [(p, b, best[p]) for p, b in cert if p in best and best[p][0] > b + 1]
print(f"certified lines: {len(cert)}; contradictions (witness delay > bound+1): {len(bad)}")
for x in bad: print("  CONTRADICTION", x)
if opn:
    ds = sorted((best.get(p, (-1, ""))[0], p) for p, _ in opn)
    print(f"open lines: {len(opn)}; with a witness: {sum(d >= 0 for d, _ in ds)}")
    for thr in (48, 100, 150, 200, 250):
        print(f"  witness delay > {thr}: {sum(d > thr for d, _ in ds)}")
    print("  top 10:", ds[::-1][:10])
