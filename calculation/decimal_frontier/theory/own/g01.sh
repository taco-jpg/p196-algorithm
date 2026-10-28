#!/bin/bash
# for bases B1..B2: which G0=1 streams (10, 100, 1000, 10000, 100000) have exterior B-cycles?  prints base and list
for b in $(seq $1 $2); do
  printf "10\n100\n1000\n10000\n100000\n" > /tmp/g01_$b.txt
  res=$( ( ulimit -v 1500000; timeout 10 ./bauto4 $b /tmp/g01_$b.txt -cap 300000 2>/dev/null ) | awk '{g=$4; sub("g=","",g); a[g]++} END{for(k in a) printf "%s(%d) ", k, a[k]}')
  echo "b=$b: $res"
done
