#!/bin/bash
cd ~/p196_run/mchk13b || exit 1
while [ ! -f logs/rec01.done ]; do sleep 5; done
for o in 0 1 2 3; do
  ./mc13b run lat/rec2.txt $o 46 8 > logs/rec2_o$o.log 2>&1
done
echo done > logs/rec2.done
