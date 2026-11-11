#!/bin/bash
# round-robin split: rr_split.sh FILE N PREFIX  -> PREFIX00 .. PREFIX{N-1} (line i goes to shard i mod N)
awk -v N=$2 -v P="$3" '{ f=sprintf("%s%02d", P, (NR-1)%N); print > f }' "$1"
