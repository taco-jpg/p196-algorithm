#!/bin/bash
# Mac Studio run order (all scripts single-file, python3 + ortools only; P196_ALGO = path of the repo clone, read-only use)
# pip install ortools     (tested with 9.15)
export P196_ALGO=${P196_ALGO:-$HOME/p196-algorithm}
cd "$(dirname "$0")"
# 0. sanity (2 min total): B automaton vs library, padded C solver on bases 26/16/17
python3 test_bcore.py                      # expect "ALL REPLAYS OK"
python3 test_cpad.py 26 4 20 20            # expect certificate C0 [32,20,20,32] at Z0=7
python3 test_cpad.py 17 6 30 60            # expect certificate at Z0=24 (~10 s)
python3 test_cpad.py 11 6 50 600           # HARD validation (|C|=42..44, Z0~46): not yet finished here, may take minutes-hours; run in background
# 1. exact B-cycle census, base 10, all periods up to 18 (all overflow patterns, no bound on |B|)
#    runtime: p<=15 total ~1 min; p=16..18 heavy patterns (millions of states) minutes each; RAM ~250 B/state/pattern
python3 run_btransfer.py --base 10 --pmin 1 --pmax 18 --procs 24 --maxstates 40000000 --out b10.jsonl
#    deeper, restricted to <=6 overflows per period (the run bound <=4 non-overflow steps forces p <= 5*Sigma): p up to 30
python3 run_btransfer.py --base 10 --pmin 19 --pmax 30 --maxones 6 --procs 24 --maxstates 40000000 --out b10.jsonl
#    same census in the comparison bases (fast): 
for b in 11 17 26 16; do python3 run_btransfer.py --base $b --pmin 1 --pmax 12 --procs 8 --out b$b.jsonl; done
# 2. C-block search for every B-cycle found in base 10 (embarrassingly parallel: one CP-SAT solve per (stream, Z0))
python3 full_search.py --in b10.jsonl --procs 30 --zlo 3 --zhi 100 --tl 600 --out certs10.jsonl     # prints "CERTIFICATE FOUND" lines
# 3. lifetime survey (one process per base; ~5 min each at 200000 samples)
for b in 4 8 10 11 16 17 26; do python3 lifetimes.py 200000 8 8 $b > life$b.txt & done; wait
