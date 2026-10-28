#!/bin/bash
cd /home/claude/research/w2_theory/own
for a in "10 10100110011 11100010000 12" "10 101010010101 100010001000 12"; do
  echo "== cfg $a"; ./cfg $a 2>&1 | grep -vE "^iter"
done
echo "== surv p11"; ./surv 10 10100110011 11100010000 12 0 | tail -3
echo "== surv p12"; ./surv 10 101010010101 100010001000 12 0 | tail -3
