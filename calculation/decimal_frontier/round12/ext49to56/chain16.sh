#!/bin/bash
# r12e3: (1) once all 18 T=55 pass-1 shards are done: census_sum.py 55 and deep pass 1 on the T=55 survivors with ONE worker (the
# 12th slot while T=56 pass 1 runs on 9), same options as every deep pass 1 (khxt -batch 4096 -exactset -top, nodecap 1.2e8,
# 900 s), via run_deep3.sh (claim locks: chain14c's driver can join the same list later without duplicates);
# (2) then deep pass 2 on the T=55 deep-1 survivors (mk_surv2.sh rule; nodecap 2e8, 2400 s, started only before 09:15Z, cap
# shortened so that every run ends by 09:55Z) with one worker; chain14c adds workers on the same list after the census.
cd ~/p196_run/r12e; LOG=logs/chain16.log
until [ "$(ls out/census/ | grep -c '^T55_s.*\.done$')" -ge 18 ]; do sleep 30; done
echo "$(date -u +%FT%TZ) T=55 pass 1: 18 shards done" >> $LOG
python3 py/census_sum.py 55 > logs/census_sum_55.txt 2>&1
echo "$(date -u +%FT%TZ) $(head -c 600 logs/census_sum_55.txt)" >> $LOG
bash run_deep3.sh out/census/surv_T55.txt out/deep5556 1 120000000 900 >> logs/deep55_early.log 2>&1
echo "$(date -u +%FT%TZ) early deep pass 1 T=55 done" >> $LOG
SB=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "2026-11-08T09:15:00Z" +%s); EB=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "2026-11-08T09:55:00Z" +%s)
bash mk_surv2.sh 55 > out/census/surv2_T55_early.txt
echo "$(date -u +%FT%TZ) T=55 deep-2 candidates (early): $(wc -l < out/census/surv2_T55_early.txt)" >> $LOG
bash run_deep3.sh out/census/surv2_T55_early.txt out/deep2 1 200000000 2400 $SB $EB >> logs/deep2_5556.log 2>&1
echo "$(date -u +%FT%TZ) chain16 done" >> $LOG
