#!/bin/bash
# usage: btable.sh bmin bmax pmin pmax
for b in $(seq $1 $2); do
  for p in $(seq $3 $4); do
    timeout 20 ./bauto $b $p $p 2>/dev/null | awk -v b=$b '{print}' 
  done
done
