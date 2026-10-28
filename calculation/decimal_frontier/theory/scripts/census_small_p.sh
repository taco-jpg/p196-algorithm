#!/bin/bash
# usage: census_small_p.sh pmax b1 b2 ... ; writes ../out/census_p<pmax>_b<b>.txt
pmax=$1; shift
for b in "$@"; do
  f=../out/census_p${pmax}_b${b}.txt
  nice -n 10 timeout 600 ./bauto $b 1 $pmax 2>../out/census_p${pmax}_b${b}.err | grep ACCEPT | awk '{print $2,$3,$4,$5}' > $f
  echo "b=$b done $(wc -l < $f) accepts"
done
