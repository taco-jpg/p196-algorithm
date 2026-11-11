#!/bin/bash
cd ~/p196_run/r13a
PY=~/p196_run/venv/bin/python
sleep 120
for args in "1000 4 32" "1000 5 40" "10 4 16" "00001110001 3 33"; do
  set -- $args
  echo "== cross_census $args"
  perl -e 'alarm shift; exec @ARGV' 280 nice -n 15 $PY cross_census.py $1 $2 $3 2>&1 | tail -3
done
