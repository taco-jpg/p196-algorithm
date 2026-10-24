#!/usr/bin/env bash
# Reproduce every COMPUTED number in REPORT.md (Linux or macOS; C++17 compiler, Python 3.13, numpy).
# Usage: sprint/agent-04/run_all.sh [DATADIR]      (DATADIR needs ~1.3 GB free; default ./agent04-data)
# Measured on the sprint machine (2 cores, 8 GB): measured stages sum to 1,120 s (~19 min) plus compilation;
# peak RSS 4,172 MiB (k=7 peeling).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
D="${1:-$PWD/agent04-data}"
mkdir -p "$D"
cd "$HERE"
CXX="${CXX:-g++}"
for p in kcol scc cyc scan realized repeats repstat entry; do
  "$CXX" -O2 -std=c++17 -o "$D/$p" "$p.cpp"
done

# 0. reference implementation == Lean definitions; the 14 Agent117 witnesses re-checked
python3 check_ref.py 4
python3 witness_anatomy.py

# 1. global infinite-rank set I_k (in-degree peeling over all 19^k words) and prefix status
for k in 4 5 6 7; do python3 measure.py "$D/kcol" global $k "$D"; python3 measure.py "$D/kcol" prefixes $k "$D"; done
# 2. strongly connected components of I_k, shortest cycles, survival under projection
for k in 4 5 6 7; do python3 measure.py "$D/scc" $k "$D"; cat "$D/core_$k.tsv"; done
python3 measure.py "$D/cyc" 4 "$D" 30 40
python3 measure.py "$D/cyc" 5 "$D" 30 40
python3 measure.py "$D/cyc" 6 "$D" 30 40
python3 measure.py "$D/cyc" 7 "$D" 8 40
python3 proj_survival.py "$D"
# 3. real orbits: edge validation, entry into I_k, realized closed walks, prefix delays
python3 measure.py "$D/scan" "$D" 1 1000000 300 "$D/scan1e6"; cat "$D/scan1e6.summary.txt"
python3 measure.py "$D/realized" 1 1000000 300 4 13 "$D/realized_1e6.tsv"
python3 measure.py "$D/repstat" 1 1000000 300 4 9
python3 measure.py "$D/repeats" 196 100000 4 13
python3 measure.py "$D/repeats" 10097 3000 4 13
# 4. entry walks to the length-7 cycle and the Lean data
printf '10 2 3 2 7 5 0 0\n1 3 5 5 9 12 5 1\n2 6 10 11 9 4 12 0\n4 13 1 3 9 10 4 0\n9 6 3 7 9 0 9 0\n18 12 6 14 18 0 18 0\n9 12 9 11 14 9 9 1\n' > "$D/cyc7.txt"
python3 - "$D" <<'EOF'
import csv, sys
D = sys.argv[1]
st = {}
for k in (4, 5, 6, 7):
    for r in csv.DictReader(open(f"{D}/prefix_status_k{k}.tsv"), delimiter="\t"):
        st.setdefault(int(r["prefix"]), {})[k] = r["status"]
sc = {int(r["prefix"]): r for r in csv.DictReader(open(f"{D}/scan1e6.prefix.tsv"), delimiter="\t")}
openp = [p for p in st if p >= 1000 and all(st[p][k] == "cycle" for k in range(4, 8))]
top20 = [p for _, p in sorted((-int(sc[p]["max_time"]), p) for p in openp if p in sc)[:20]]
three = [138, 164, 198, 248, 275, 398, 626, 710, 716, 790, 911, 936, 952]
with open(f"{D}/targets.txt", "w") as f:
    for p in three + top20 + [4456]:
        f.write(f"P{p} " + " ".join(str(p)) + "\n")
open(f"{D}/top20.txt", "w").write("\n".join(map(str, top20)) + "\n")
print("top20 (delay desc, prefix asc):", top20)
EOF
python3 measure.py "$D/entry" 7 "$D" "$D/cyc7.txt" "$D/targets.txt" "$D/entry7.tsv"
python3 gen_lean_realized.py - x > "$D/w5target.txt"
python3 measure.py "$D/entry" 7 "$D" "$D/cyc7.txt" "$D/w5target.txt" "$D/entry_w5.tsv"
LEANDIR="$HERE/../../lean/P196/Sprint/Agent04"
python3 gen_lean_prefixes.py "$D/entry7.tsv" "$D/top20.txt" "$D/PrefixesK7.lean"
python3 gen_lean_realized.py "$D/entry_w5.tsv" "$D/Realized.lean"
cmp "$D/PrefixesK7.lean" "$LEANDIR/PrefixesK7.lean" && echo "PrefixesK7.lean regenerated identically"
cmp "$D/Realized.lean" "$LEANDIR/Realized.lean" && echo "Realized.lean regenerated identically"
# 5. lifting towers of the shortest cycles
printf '[[[10,2,3,2,7,5,0],0],[[1,3,5,5,9,12,5],1],[[2,6,10,11,9,4,12],0],[[4,13,1,3,9,10,4],0],[[9,6,3,7,9,0,9],0],[[18,12,6,14,18,0,18],0],[[9,12,9,11,14,9,9],1]]\n' > "$D/c7.json"
python3 lift.py "$D/c7.json" 12
# 6. Lean (from lean/):  lake build P196.Sprint.Agent04.Trap P196.Sprint.Agent04.PrefixesK7 P196.Sprint.Agent04.Realized
