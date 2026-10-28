#!/bin/bash
cd /home/claude/research/w2_theory/out2
for b in 16 11 17 18 20 24 26 6 14 3 5 32 9 12 13 10; do
  python3 ../scripts/q2d.py $b 8 15 2 2>&1
done
