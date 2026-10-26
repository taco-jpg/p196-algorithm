#!/usr/bin/env bash
# Mac Studio (M3 Ultra, 32 cores, 150 GB): complete base-10 sweep.  Usage:  bash run_studio.sh [phase0|phase1|phase2|phase3|retry]
# Assumes:  python3 -m venv .venv && .venv/bin/pip install ortools      and a clone of the repo at $REPO
set -u
cd "$(dirname "$0")"
REPO=${REPO:-$HOME/p196-algorithm}
export P196_MIRROR_DIR=$REPO/calculation
PY=${PY:-.venv/bin/python}
JOBS=${JOBS:-30}          # leave 2 cores free
mkdir -p results results/sentinel
case "${1:-phase0}" in
phase0)   # ~3 minutes, 1 core: pipeline sanity.  Every line must say SAT / mirror_cycleOK=True; sentinel sweeps must report exactly sat=1 (b2: sat=2)
  $PY validate_known.py 2,4,8,26 cpsat 100
  $PY validate_known.py 11 cpsat 100
  $PY sweep.py --base 26 --p 4   --G 2 --nmax 9 --mmax 6               --jobs 1 --out results/sentinel/b26.jsonl
  $PY sweep.py --base 11 --p 6   --G 2 --nmin 6 --nmax 7 --mmin 41 --mmax 43 --tl 60 --jobs 1 --out results/sentinel/b11.jsonl
  $PY sweep.py --base 2  --p 2-6 --G 2 --nmax 3 --mmax 7               --jobs 1 --out results/sentinel/b2.jsonl
  $PY sweep.py --base 4  --p 2-6 --G 2 --nmax 2 --mmax 4               --jobs 1 --out results/sentinel/b4.jsonl
  $PY validate_bruteforce.py 4 2 4 6                                    # prints MATCH (about 20 s)
  $PY summarize.py results/sentinel/*.jsonl ;;
phase1)   # base 10, one overflow pair (G=2), cycles up to 12 edges, B up to 30, C up to 45 coefficients.
          # <= 19.6M instances, est. 1-3 h on 30 jobs
  $PY sweep.py --base 10 --p 2-12 --G 2 --nmax 30 --mmax 45 --tl 120 --jobs $JOBS --out results/b10_G2_p2-12.jsonl ;;
phase2)   # G=4 (four overflows per cycle), p<=7, B<=20, C<=30: <= 20M instances, est. 1-3 h
  $PY sweep.py --base 10 --p 4-7  --G 4 --nmax 20 --mmax 30 --tl 120 --jobs $JOBS --out results/b10_G4_p4-7.jsonl ;;
phase3)   # longer cycles, G=2, p=13..16 (extrapolated 58M instances, est. 3-8 h); run in two halves on two machines with --shard 0/2 and 1/2 if available
  $PY sweep.py --base 10 --p 13-16 --G 2 --nmax 30 --mmax 45 --tl 120 --jobs $JOBS --out results/b10_G2_p13-16.jsonl ;;
retry)    # re-run every UNKNOWN (timeout) with 1 h and 4 threads each, 7 at a time
  $PY retry_unknown.py --base 10 --tl 3600 --jobs 7 --threads 4 --out results/retry_unknown.jsonl results/b10_*.jsonl ;;
report)
  $PY summarize.py results/b10_*.jsonl
  [ -f results/FOUND.jsonl ] && $PY recheck.py results/FOUND.jsonl || echo "no SAT instance found" ;;
esac
