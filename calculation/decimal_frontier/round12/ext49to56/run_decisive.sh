#!/bin/bash
# r12e2 decisive attempt (one long run): the census word whose kept set SHRANK between deep pass 1 and deep pass 2
# (T=52 0001000100010001000100011000100011000100011000100011: K=550 kept 3.88M at 900 s -> K=1227 kept 3.06M at 3600 s; all other
# capped words grew).  khxt -batch 4096 -exactset -top -inv -v (exact closed-walk sets, TOP99/TOPUU closed-part test at every level,
# WL hash per level), nodecap 2.5e8, time cap 16,000 s.  DIES => Theorem K;  TOP99/TOPUU hit => candidate exterior (extract_hit.py).
cd ~/p196_run/r12e; mkdir -p out/decisive
W=0001000100010001000100011000100011000100011000100011
nice -n 10 ~/p196_run/r12e/bin/khxt 10 -g $W -batch 4096 -exactset -top -inv -v -kmax 100000 -nodecap 250000000 -sec 16000 \
  > out/decisive/T52w.out 2> out/decisive/T52w.err
echo "$(date -u +%FT%TZ) decisive T52w finished" >> out/decisive/done.log
