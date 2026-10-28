#!/bin/bash
# pass 2: complete the first pass (p=17..20, 26, 30) and re-run capped words with cap 3M (resumable, idempotent)
cd /home/claude/research/w5_exterior
for p in 17 18 19 20; do python3 py/census.py 10 $p --cap 3000000 --sec 40; done
for p in 26 30; do python3 py/census.py 10 $p --cap 300000 --sec 20; done
for p in 22 23 24 25 26 27 28 29 30 31 32; do python3 py/census.py 10 $p --cap 3000000 --sec 40; done
