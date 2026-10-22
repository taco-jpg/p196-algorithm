"""Certified four-digit entries whose ancestry bound b+1 is attained by a witness.
usage: python3 sharp_table.py max_delay_P4.tsv repo_bounds.json OUT.tsv
(2641, rank bound 5, from Agent117P2641 is added to the Agent124FourDigit entries.)"""
import sys, json
best = {}
for line in open(sys.argv[1]):
    if line.startswith("prefix"): continue
    p, t, s = line.split("\t")[:3]; best[p] = (int(t), s)
bounds = json.load(open(sys.argv[2])); bounds["2641"] = 5
rows = sorted((p, best[p][0], best[p][1]) for p, b in bounds.items() if p in best and best[p][0] == b + 1)
with open(sys.argv[3], "w") as f:
    f.write("prefix\tmax_delay\twitness_seed\n")
    for p, t, s in rows: f.write(f"{p}\t{t}\t{s}\n")
print(f"{len(rows)} of {len(bounds)} certified four-digit bounds are attained", file=sys.stderr)
