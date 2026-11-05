#!/bin/bash
# stop queue3 before the rec0 leftovers (not requested; rec1 range is the task)
cd ~/p196_run/r11a
until grep -q "start rec0_L13_q8_K2" queue.log; do sleep 5; done
pkill -f queue3.sh; sleep 1; pkill -f "^./cen2_64 rec0.tbl 13 8 2"; sleep 1; rm -f runs/rec0_L13_q8_K2.log.tmp
echo "$(date -u +%FT%TZ) queue3 stopped before rec0 leftovers (rec0 L13 K2, L14 K2, L15, L16 not run: outside requested rec1 range)" >> queue.log
