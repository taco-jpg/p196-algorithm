#!/bin/bash
# r12e: second deep pass (2400 s, nodecap 2e8, 2 workers) on the words that survived the first deep pass of T=53 and T=54
cd ~/p196_run/r12e
until grep -q DEEP_DONE logs/deep53.log 2>/dev/null; do sleep 30; done
for f in out/deep53/*.out; do if grep -q SURVIVES $f; then w=$(grep -o "word=[01]*" $f | cut -c6-); echo "${#w} $w"; fi; done > out/census/surv2_53.txt
bash run_deep.sh out/census/surv2_53.txt out/deep2 2 200000000 2400 > logs/deep2_53.log 2>&1
until grep -q DEEP_DONE logs/deep54.log 2>/dev/null; do sleep 30; done
for f in out/deep54/*.out; do if grep -q SURVIVES $f; then w=$(grep -o "word=[01]*" $f | cut -c6-); echo "${#w} $w"; fi; done > out/census/surv2_54.txt
bash run_deep.sh out/census/surv2_54.txt out/deep2 2 200000000 2400 > logs/deep2_54.log 2>&1
