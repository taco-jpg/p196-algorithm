#!/bin/bash
# ONE heavy slot: (1) positive control: base 11 known cert stream (e=011011,g=001001,v=000001) with large caps; (2) Q2e batch of the PR #411 engine, p<=8, bases listed.
cd /home/claude/research/w2_theory/scripts
echo "### control base 11 $(date -u +%H:%M:%S)"
( ulimit -v 2400000; timeout 420 ../own/bin/a113_regular 11 011011 001001 000001 --depth 120 --states 3000000 --edges 60000000 --ops 3000000000 --seconds 400 2>&1 | tail -6 | cut -c1-400 )
for b in 11 17 26 20 16 18 6 14 5 3 24 32 9 12 13 15; do
  echo "### base $b $(date -u +%H:%M:%S)"
  python3 q2e.py $b 8 30
done
echo "### done $(date -u +%H:%M:%S)"
