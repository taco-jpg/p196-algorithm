#!/bin/bash
# r12e2: in the slot of the (p21)^2 confirmation, once it is done: V5-style kh2 -exact check of the T=49..54 deep-pass deaths
# (widest level <= 6M nodes, smallest first, 600 s per word), until 09:40Z.
cd ~/p196_run/r12e
until grep -q "p21sq kh2s done" out/confirm/done_r12e2.log 2>/dev/null; do sleep 30; done
END=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "2026-11-08T09:40:00Z" +%s); NOW=$(date -u +%s); B=$(( END - NOW ))
[ $B -gt 600 ] && bash ctrl/kh2_deep.sh T49_54 6000000 600 $B out/deep1 out/deep53 out/deep54 out/deep2 > logs/kh2_deep_T49_54.log 2>&1
echo "$(date -u +%FT%TZ) chain15 done (budget $B s)" >> logs/chain15.log
