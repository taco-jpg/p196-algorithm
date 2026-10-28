#!/bin/bash
# usage: run_census_multi.sh cap sec p1 p2 ...
cd /home/claude/research/w5_exterior
cap=$1; sec=$2; shift; shift
for p in "$@"; do ./run_census.sh $p $cap $sec; done
