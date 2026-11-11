#!/bin/bash
# r12e: second deep pass (khxt -exactset -top, 3600 s, nodecap 2e8) on the words that survived the first deep pass of T=49..52
cd ~/p196_run/r12e
sleep 30
while pgrep -f "run_deep.sh out/census/surv_49_52.txt" > /dev/null || pgrep -f "bash chain8.sh" > /dev/null; do sleep 20; done
for f in out/deep1/*.out; do if grep -q SURVIVES $f; then w=$(grep -o "word=[01]*" $f | cut -c6-); echo "${#w} $w"; fi; done > out/census/surv2_49_52.txt
bash run_deep.sh out/census/surv2_49_52.txt out/deep2 2 200000000 3600 > logs/deep2.log 2>&1
