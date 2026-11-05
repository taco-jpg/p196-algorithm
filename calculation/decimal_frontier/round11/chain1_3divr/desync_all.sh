#!/bin/bash
# desync search from N12 cut u_h^k, k=2,3,4, every height h
cd ~/p196_run/r11e
for k in 2 3 4; do
  W=$(python3 -c "print(\"0001\"*(3*$k))"); B=./src/bxd; [ $k -ge 4 ] && B=./src/bxd3
  for h in $(seq 0 54); do
    read hh L H y1 y2 y3 <<< "$(sed -n "$((h+1))p" py/n12cuts.txt)"; F=""; [ $h = 0 ] && F=-first0
    echo -n "k=$k h=$h "; nice -n 10 $B 10 -g $W -from 12 $L $H $y1,$y2,$y3 $F -desync -cap 150000000 -sec 1200 | cut -c1-260
  done
done
