#!/bin/bash
# r12e3 (replaces chain14b.sh, which was killed while still waiting for CENSUS_DONE; same steps and options, plus claim locks and
# a pipelined deep pass 2).  After census T=55/56 pass 1: summary + count check, kh2 -exact sample checks (one worker per T),
# deep pass 2 on the T=55 deep-1 survivors known by then (2 workers, joins chain16), deep pass 1 on every T=55/56 survivor not
# done or claimed (5 workers; khxt -batch 4096 -exactset -top, nodecap 1.2e8, 900 s), TOP99/TOPUU hit extraction
# (khxt -stophit -dump + py/extract_hit.py -> out/hits/), then deep pass 2 on all remaining deep-1 survivors (mk_surv2.sh rule;
# nodecap 2e8, 2400 s, started only before 09:15Z, cap shortened so that every run ends by 09:55Z; 4 workers).
cd ~/p196_run/r12e; LOG=logs/chain14.log
until grep -q CENSUS_DONE logs/census_55_56.log 2>/dev/null; do sleep 30; done
echo "$(date -u +%FT%TZ) census 55/56 done (chain14c)" >> $LOG
python3 py/census_sum.py 55 56 > logs/census_sum_55_56.txt 2>&1
cat out/census/surv_T55.txt out/census/surv_T56.txt > out/census/surv_55_56.txt
( bash ctrl/kh2_sample.sh 55 > /dev/null 2>&1; echo "$(date -u +%FT%TZ) kh2 55 done" >> $LOG ) &
( bash ctrl/kh2_sample.sh 56 > /dev/null 2>&1; echo "$(date -u +%FT%TZ) kh2 56 done" >> $LOG ) &
SB=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "2026-11-08T09:15:00Z" +%s); EB=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "2026-11-08T09:55:00Z" +%s)
bash mk_surv2.sh 55 > out/census/surv2_T55_a.txt
( bash run_deep3.sh out/census/surv2_T55_a.txt out/deep2 2 200000000 2400 $SB $EB >> logs/deep2_5556.log 2>&1 ) &
bash run_deep3.sh out/census/surv_55_56.txt out/deep5556 5 120000000 900 >> logs/deep5556.log 2>&1
echo "$(date -u +%FT%TZ) deep pass 1 (55/56) chain14c driver done" >> $LOG
until grep -q "early deep pass 1 T=55 done" logs/chain16.log 2>/dev/null; do sleep 30; done
echo "$(date -u +%FT%TZ) deep pass 1 (55/56) complete (both drivers)" >> $LOG
mkdir -p out/hits
for f in out/deep5556/*.out; do
  if grep -Eq "top99_first=[0-9]|topUU_first=[0-9]" $f; then
    w=$(grep -o "word=[01]*" $f | cut -c6-); r=$(grep -o "root=[01]*" $f | cut -c6-); n=${#w}
    if [ "$r" == "$w" ]; then A="-g $w"; else A="-g $r -L $n"; fi
    nice -n 10 ~/p196_run/r12e/bin/khxt 10 $A -batch 4096 -exactset -top -stophit -kmax 2000 -nodecap 120000000 -sec 1800 -dump out/hits/${n}_$w.dump > out/hits/${n}_$w.hit 2>&1
    python3 py/extract_hit.py out/hits/${n}_$w.dump $r $n > out/hits/${n}_$w.extract 2>&1
    echo "$(date -u +%FT%TZ) HIT $n $w root=$r :: $(tail -1 out/hits/${n}_$w.extract | cut -c1-200)" >> $LOG
  fi
done
for f in out/deep5556/*.out; do
  if ! grep -q "^KHXT" $f; then echo "$(date -u +%FT%TZ) NO_VERDICT $f (killed?)" >> $LOG; fi
done
bash mk_surv2.sh 55 > out/census/surv2_T55.txt; bash mk_surv2.sh 56 > out/census/surv2_T56.txt
cat out/census/surv2_T55.txt out/census/surv2_T56.txt > out/census/surv2_55_56.txt
echo "$(date -u +%FT%TZ) deep-2 candidates: T55 $(wc -l < out/census/surv2_T55.txt), T56 $(wc -l < out/census/surv2_T56.txt)" >> $LOG
bash run_deep3.sh out/census/surv2_55_56.txt out/deep2 4 200000000 2400 $SB $EB >> logs/deep2_5556.log 2>&1
echo "$(date -u +%FT%TZ) deep pass 2 (55/56) chain14c driver done" >> $LOG
wait
echo "$(date -u +%FT%TZ) chain14c done" >> $LOG
