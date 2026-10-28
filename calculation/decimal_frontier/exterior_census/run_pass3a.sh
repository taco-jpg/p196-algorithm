#!/bin/bash
# pass 3a: fill small p into the DB, then re-run all still-capped words with p<=24 at cap 40M states (~1 GB table)
cd /home/claude/research/w5_exterior
for p in 11 12 13 14 15 16 21; do python3 py/census.py 10 $p --cap 3000000 --sec 40; done
for p in 16 18 21 22 23 24; do python3 py/census.py 10 $p --cap 40000000 --sec 400; done
