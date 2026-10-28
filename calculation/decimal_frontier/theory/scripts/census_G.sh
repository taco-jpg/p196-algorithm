#!/bin/bash
# usage: census_G.sh Gmax cap b1 b2 ...   -> out2/extG_b<b>_G<G>.txt ; all sequential, to be run inside ONE heavy call
Gmax=$1; cap=$2; shift 2
cd /home/claude/research/w2_theory/out2
for b in "$@"; do
  L=$(python3 -c "print(int($b).bit_length())")
  for G in $(seq 1 $Gmax); do
    pm=$((L*G)); [ $pm -gt 40 ] && pm=40
    f=extG_b${b}_G${G}
    timeout 900 ../bin/bauto2 $b 1 $pm -G $G -cap $cap > $f.txt 2> $f.err
    echo "b=$b G=$G pmax=$pm accepts=$(grep -c ACCEPT $f.txt) caps=$(grep -c 'state cap' $f.err) keytoolong=$(grep -c 'key too long' $f.err)"
  done
done
