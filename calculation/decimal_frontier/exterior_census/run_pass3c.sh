#!/bin/bash
# pass 3c: residue of p=25..32 at cap 40M states (1 GB table; the local heavy limit of 2.6 GB address space allows at most ~40M); resumable, chunks of 3 words
cd /home/claude/research/w5_exterior
for p in 25 26 27 28 29 30 31 32; do python3 py/census.py 10 $p --cap 40000000 --sec 300; done
