#!/bin/bash
# first pass: cap 300k states per word, p=26..32 (b=10); resumable via db
cd /home/claude/research/w5_exterior
for p in "$@"; do python3 py/census.py 10 $p --cap 300000 --sec 20; done
