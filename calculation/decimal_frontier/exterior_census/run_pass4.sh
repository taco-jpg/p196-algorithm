#!/bin/bash
# pass 4: extension beyond p=32 with the KW=3 build: p=33 first pass (cap 300k) and residue (cap 3M)
cd /home/claude/research/w5_exterior
python3 py/census.py 10 33 --cap 300000 --sec 20 --bx bin/bx3
python3 py/census.py 10 33 --cap 3000000 --sec 40 --bx bin/bx3
