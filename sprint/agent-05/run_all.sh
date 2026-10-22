#!/usr/bin/env bash
# Reproduce sprint agent 05 (delay witnesses). Run from sprint/agent-05/.
# Linux: g++ with OpenMP.  macOS: brew install gcc && use g++-14 (Apple clang has no -fopenmp);
# without OpenMP the program still runs single-threaded.
set -euo pipefail
CXX=${CXX:-g++}
mkdir -p runs data
$CXX -O3 -fopenmp -o delays tools/delays.cpp

# 0. self-tests: class search == brute force (Python), memo == no memo, predecessor solver == brute force
python3 tools/pycheck.py 100000 120 > runs/py5.txt
./delays exhaust 1 5 runs/cpp5.txt --D 120 --memo 2 --table 20
diff runs/py5.txt <(awk '$1=="P4"{print $2, $3, $4}' runs/cpp5.txt) && echo "class search == brute force"
./delays exhaust 1 9 runs/v_nm.txt --D 200
./delays exhaust 1 9 runs/v_m.txt --D 200 --memo 4 --table 24
diff <(grep ^P runs/v_nm.txt) <(grep ^P runs/v_m.txt) && echo "memo == no memo"
python3 tools/extend.py --selftest

# 1. repository data: certified (prefix, rank bound) entries and the three-digit exclusion table
python3 tools/extract_entries.py ../../lean/P196 && mv repo_bounds.json data/
python3 tools/parse_marks.py ../../RESULTS.md data/three_digit_marks.json

# 2. exhaustive search: all seeds with 1..14 digits (column-sum classes), all palindrome hits
./delays exhaust 1 12 runs/ex1_12.txt --D 200 --memo 5 --table 26
./delays exhaust 13 13 runs/ex13.txt --D 200 --memo 5 --table 27
./delays exhaust 14 14 runs/ex14.txt --D 160 --memo 5 --table 27   # 32-core Mac: use --table 30

# 3. known record seeds (OEIS b-files A023109 A065198 A281390 A281506-9 A326414 A340397 A353185
#    A065320-7, A033665, numbers on jasondoucette.com/worldrecords.html) -> data/known_seeds.txt
./delays seeds data/known_seeds.txt runs/known.txt --D 400

# 4. random class sampling (see REPORT.md for the lengths/counts actually run)
for L in 15 16 17 18 19 20 21 22; do ./delays sample $L 4000000 $L runs/s$L.txt --D 200 --memo 5 --table 25; done

# 5. backward extension (predecessor classes) of the best witnesses, then forward re-verification
python3 tools/analyze.py runs/tmp runs/ex*.txt runs/known.txt runs/s*.txt > /dev/null
python3 tools/extend.py runs/tmp/max_delay_P4.tsv 50 1000 runs/ext.tsv --budget 5
cut -f4 runs/ext.tsv | tail -n +2 > runs/ext_seeds.txt
./delays seeds runs/ext_seeds.txt runs/ext_fwd.txt --D 400

# 6. final tables + consistency checks + independent re-verification of every row
python3 tools/analyze.py data runs/ex1_12.txt runs/ex13.txt runs/ex14.txt runs/known.txt runs/s*.txt runs/ext_fwd.txt | tee data/analysis_output.txt
python3 tools/verify_tables.py data
python3 tools/later_hits.py data/max_delay_P4.tsv
gzip -9 -f data/max_delay_P5.tsv

# 7. Lean witness modules (each witness recomputed in Python, then kernel-checked)
python3 tools/gen_lean.py data/max_delay_P4.tsv 100 ../../lean/P196/Sprint/Agent05 Over100 --chunk-size 20 \
  --title "Four-digit prefixes with a realized delay above 100"
python3 tools/sharp_table.py data/max_delay_P4.tsv data/repo_bounds.json data/sharp_P4.tsv
python3 tools/gen_lean.py data/sharp_P4.tsv -1 ../../lean/P196/Sprint/Agent05 Sharp --chunk-size 300 \
  --title "Certified four-digit ancestry bounds attained by real seeds"
(cd ../../lean && lake build P196.Sprint.Agent05.Witness4456 P196.Sprint.Agent05.Over100 P196.Sprint.Agent05.Sharp)
