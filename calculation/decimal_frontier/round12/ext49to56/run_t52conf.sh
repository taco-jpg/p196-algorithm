#!/bin/bash
# r12e3: independent confirmation of the decisive-run death (T=52 word W: khxt DIES K=1744, out/decisive/T52w.*), done exactly as
# r12e's third p47 check and r12e2's (p21)^2 check: (1) khxt_b (src/khxt.cpp, separate binary) reruns W to level 1710 with -anc 0
# (exact set of level 1710 with full windows; 9,822 windows in the decisive run); its per-level lines must equal
# out/decisive/T52w.err at every level 1..1710; (2) kh2s = r12b's independent kh2 (string windows, full-window trans for every edge,
# Kosaraju, its own exact closed-walk set) seeded with that level must keep all seed windows, reproduce the candidate/kept counts
# at 1711..1743 and die at K=1744.
cd ~/p196_run/r12e; mkdir -p out/confirm
W=0001000100010001000100011000100011000100011000100011
nice -n 10 ~/p196_run/r12e/bin/khxt_b 10 -g $W -batch 4096 -exactset -v -kmax 1710 -nodecap 400000000 -anc 0 out/confirm/T52w_K1710.seed \
  > out/confirm/T52w_K1710.out 2> out/confirm/T52w_K1710.err
echo "$(date -u +%FT%TZ) T52w seed K1710 done" >> out/confirm/done_r12e3.log
nice -n 10 ~/p196_run/r12e/bin/kh2s 10 $W 52 -exact 1800 400000000 out/confirm/T52w_K1710.seed > out/confirm/T52w_kh2s.out 2>&1
echo "$(date -u +%FT%TZ) T52w kh2s done" >> out/confirm/done_r12e3.log
