#!/bin/bash
# pass 3b: residue of p=25..32 at cap 12M states (0.5 GB table), smallest p/G first; resumable
cd /home/claude/research/w5_exterior
for p in 25 26 27 28 29 30 31 32; do python3 py/census.py 10 $p --cap 12000000 --sec 120; done
