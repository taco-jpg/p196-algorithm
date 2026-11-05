#!/bin/bash
# controls for khead_len: must SURVIVE: p11 word (L=11), 0001 L=12, 01 L=8 (Kmax 14);  must DIE: 01 L=36 (K=3), 0001 L=40 (K=37, Theorem A)
cd ~/p196_run/r11d/kfam
while pgrep -f run_kfam.sh >/dev/null; do sleep 20; done
for a in "14 00001110001 11" "14 0001 12" "14 01 8" "10 01 36" "40 0001 40"; do set -- $a
  echo "ctrl Kmax=$1 pat=$2 L=$3: $(nice -n 10 ./khead_len $1 $2 $3 2>&1 | tail -1 | cut -c1-120)"; done
echo CTRL_DONE
