#!/bin/bash
# Main-session check of r12d. Own scratch dir ~/p196_run/mchk12d; r12d itself is only read.
set -u
D=~/p196_run/mchk12d
PY=~/p196_run/venv/bin/python
R=~/p196_run/r12d
cd $D || exit 1
TO(){ perl -e 'alarm shift; exec @ARGV' "$@"; }
echo "start $(date)"
rm -rf r12d_copy && cp -R $R r12d_copy && rm -rf r12d_copy/logs r12d_copy/__pycache__ r12d_copy/cen2 r12d_copy/cen3

echo "== SAT cross-solver / prefix runs (background)"
( cd r12d_copy
  TO 5400 nice -n 10 $PY tsrun.py ret --lat rec0 --q0 5 --K 1 --L 20 --solver kissat404 > $D/sat_rec0_K1_L20_kissat.log 2>&1 &
  TO 5400 nice -n 10 $PY tsrun.py ret --lat rec1 --q0 5 --K 1 --L 19 --solver maplechrono > $D/sat_rec1_K1_L19_maple.log 2>&1 &
  TO 5400 nice -n 10 $PY tsrun.py prefix --lat rec2 --q0 4 --K 1 --L 4 --k 189 > $D/pre_rec2_K1_L4_k189.log 2>&1 &
  TO 5400 nice -n 10 $PY tsrun.py prefix --lat rec2 --q0 4 --K 1 --L 4 --k 190 > $D/pre_rec2_K1_L4_k190.log 2>&1 &
  wait ) &
SATPID=$!

echo "== independent big-integer enumeration vs cen3 logs"
nice -n 10 $PY -I $D/indep_enum.py r12d_copy/repo/calculation/decimal_frontier/lattice_formats/p8_scc.txt $R/logs/cen 8

echo "== base-9 positive controls"
nice -n 10 $PY -I $D/b9check.py $D/r12d_copy 8

echo "== cen3 rebuilt from source, three logs reproduced"
( cd r12d_copy && clang++ -O3 -std=c++17 -o cen3 cen3.cpp -lpthread 2>&1 | tail -3 )
for a in "rec2 1 7 4" "rec0 4 6 15" "rec1 6 5 21"; do
  set -- $a
  out=$(cd r12d_copy && nice -n 10 ./cen3 $1.tbl $3 $4 $2 4 | grep -E '^(RESULT|HIST)')
  ref=$(grep -E '^(RESULT|HIST)' $R/logs/cen/cen_$1_K$2_L$3.log | tail -2)
  if [ "$(echo "$out" | sed 's/ [0-9.]*s$//')" = "$(echo "$ref" | sed 's/ [0-9.]*s$//')" ]; then v=SAME; else v=DIFFER; fi
  echo "cen3 $1 K=$2 L=$3: $v"; [ $v = DIFFER ] && { echo " new: $out"; echo " log: $ref"; }
done

echo "== shield thresholds and insertion kernel re-run"
( cd r12d_copy && nice -n 10 $PY shield4.py 01 > $D/shield01.out 2>&1; nice -n 10 $PY shield4.py 2 > $D/shield2.out 2>&1 )
grep -h '^rec' shield01.out shield2.out | sort > shield_new.txt
grep '^rec' $R/shield_thresholds.log | sort > shield_old.txt
if cmp -s shield_new.txt shield_old.txt; then echo "shield: SAME ($(wc -l < shield_new.txt) lines)"; else echo "shield: DIFFER"; diff shield_old.txt shield_new.txt | head; fi
for r in 0 1 2; do
  ( cd r12d_copy && nice -n 10 $PY lemma_orig.py $r > $D/lemma_$r.out 2>&1 )
  if cmp -s lemma_$r.out $R/lemma_rec$r.log; then echo "lemma rec$r: SAME"; else echo "lemma rec$r: DIFFER"; diff $R/lemma_rec$r.log lemma_$r.out | head -5; fi
done

echo "== log tally (read-only)"
cd $R/logs
echo "ret logs (prod): RESULT kinds"; grep -h '^RESULT' prod/ret_*.log | awk '{print $2}' | sort | uniq -c
echo "ret logs without RESULT:"; for f in prod/ret_*.log; do grep -q '^RESULT' $f || echo "  $f: $(tail -1 $f | cut -c1-90)"; done
echo "final_prefix_ok values:"; grep -h '^INST' prod/ret_*.log | grep -o 'final_prefix_ok=[A-Za-z]*' | sort | uniq -c
echo "claimed SAT table rows (lat K L -> result):"
for f in prod/ret_*.log; do r=$(grep -h '^RESULT' $f | tail -1 | awk '{print $2}'); s=$(grep -h '^RESULT' $f | tail -1 | grep -o 'solver=[a-z0-9]*'); echo "  $(basename $f .log) ${r:-NONE} $s"; done | sort -V
echo "cubes2 RESULT lines:"; grep -h '^RESULT' prod/cubes2_*.log | cut -c1-170
echo "cen logs: returns / clockdev / lenerr / guardfail"; grep -h '^RESULT' cen/*.log | grep -o 'returns=[0-9]* clockdev=[0-9]* lenerr=[0-9]* guardfail=[0-9]*' | sort | uniq -c
echo "cen logs without RESULT:"; for f in cen/*.log; do grep -q '^RESULT' $f || echo "  $f: $(tail -1 $f | cut -c1-80)"; done
echo "wall DONE/PARTIAL:"; for f in wall/*.log; do echo "  $(basename $f): $(grep -h '^DONE' $f | tail -1 | cut -c1-90) | RES SAT lines=$(grep -c '^RES SAT' $f) RES UNSAT=$(grep -c '^RES UNSAT' $f)"; done
echo "band:"; for f in band/*.log; do echo "  $(basename $f): $(grep -h '^RES ' $f | awk '{print $2}' | sort | uniq -c | tr '\n' ' ')"; done
echo "surv:"; for f in surv/*.log; do echo "  $(basename $f): $(grep -h '^LIFETIME' $f | awk '{print $4, $5}' | tr '\n' ' ') $(grep -h '^DONE' $f | cut -c1-40)"; done
echo "CANDIDATE lines anywhere:"; grep -rl CANDIDATE . | sort
cd $D

echo "== waiting for SAT runs"
wait $SATPID
for f in sat_*.log pre_*.log; do echo "$f: $(grep -h '^RESULT\|^CHECK' $f | cut -c1-200)"; grep -q '^RESULT' $f || tail -3 $f; done
echo "end $(date)"
echo MCHK12D_DONE
