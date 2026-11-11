#!/bin/bash
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
for args in "1000 5 120" "10 5 30" "00001110001 4 22"; do
  set -- $args
  echo "== cross_census $args"
  perl -e 'alarm shift; exec @ARGV' 280 nice -n 15 $PY cross_census.py $1 $2 $3 2>&1 | tail -4
done
