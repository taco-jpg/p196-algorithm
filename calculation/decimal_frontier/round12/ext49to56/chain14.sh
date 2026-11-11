#!/bin/bash
# r12e2: after census T=55/56 pass 1 (run_census3.sh): summary + count check, kh2 -exact sample checks (one worker per T),
# deep pass 1 on all pass-1 survivors (run_deep.sh: khxt -batch 4096 -exactset -top, root pattern for imprimitive words,
# nodecap 1.2e8, 900 s = the T=49..54 deep pass), TOP99/TOPUU hit extraction, deep pass 2 (nodecap 2e8, 2400 s = chain12) on the
# deep-1 survivors except words that carry a known stream (TOP99 hit) and (01)^28 (G_K(01) keeps 8-periodic walks at every K).
cd ~/p196_run/r12e; LOG=logs/chain14.log
until grep -q CENSUS_DONE logs/census_55_56.log 2>/dev/null; do sleep 30; done
echo "$(date -u +%FT%TZ) census 55/56 done" >> $LOG
python3 py/census_sum.py 55 56 > logs/census_sum_55_56.txt 2>&1
cat out/census/surv_T55.txt out/census/surv_T56.txt > out/census/surv_55_56.txt
( bash ctrl/kh2_sample.sh 55 > /dev/null 2>&1; echo "$(date -u +%FT%TZ) kh2 55 done" >> $LOG ) &
( bash ctrl/kh2_sample.sh 56 > /dev/null 2>&1; echo "$(date -u +%FT%TZ) kh2 56 done" >> $LOG ) &
bash run_deep.sh out/census/surv_55_56.txt out/deep5556 8 120000000 900 > logs/deep5556.log 2>&1
echo "$(date -u +%FT%TZ) deep pass 1 (55/56) done" >> $LOG
mkdir -p out/hits
for f in out/deep5556/*.out; do
  if grep -Eq "top99_first=[0-9]|topUU_first=[0-9]" $f; then
    w=$(grep -o "word=[01]*" $f | cut -c6-); r=$(grep -o "root=[01]*" $f | cut -c6-); n=${#w}
    if [ "$r" == "$w" ]; then A="-g $w"; else A="-g $r -L $n"; fi
    nice -n 10 ~/p196_run/r12e/bin/khxt 10 $A -batch 4096 -exactset -top -stophit -kmax 2000 -nodecap 200000000 -sec 1800 -dump out/hits/${n}_$w.dump > out/hits/${n}_$w.hit 2>&1
    python3 py/extract_hit.py out/hits/${n}_$w.dump $r $n > out/hits/${n}_$w.extract 2>&1
    echo "$(date -u +%FT%TZ) HIT $n $w root=$r :: $(tail -1 out/hits/${n}_$w.extract | cut -c1-200)" >> $LOG
  fi
done
for f in out/deep5556/*.out; do
  if grep -q SURVIVES $f && ! grep -Eq "top99_first=[0-9]|topUU_first=[0-9]" $f; then
    w=$(grep -o "word=[01]*" $f | cut -c6-); r=$(grep -o "root=[01]*" $f | cut -c6-)
    [ "$r" == "01" ] && continue
    echo "${#w} $w"
  fi
done > out/census/surv2_55_56.txt
bash run_deep.sh out/census/surv2_55_56.txt out/deep2 8 200000000 2400 > logs/deep2_55_56.log 2>&1
echo "$(date -u +%FT%TZ) deep pass 2 (55/56) done" >> $LOG
wait
echo "$(date -u +%FT%TZ) chain14 done" >> $LOG
