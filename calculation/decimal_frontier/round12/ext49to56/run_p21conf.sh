#!/bin/bash
# r12e2: independent confirmation of the (p21)^2 death at K=2787 (Task A khxt run, out/taskA/p21sq.*), in the same way as r12e's
# third p47 check: (1) khxt_b (= src/khxt.cpp, -exactset) rerun of pattern p21 with L=42 to level 2750, dumping the exact set of
# level 2750 with full windows (-anc 0); its per-level counts must equal the Task A run (reproducibility, other binary);
# (2) kh2s = r12b's independent kh2 (string windows, full-window trans for every edge, Kosaraju, its own exact closed-walk set),
# seeded with that level, continued with the unchanged kh2 rules: it must keep all seed windows and die at K=2787.
cd ~/p196_run/r12e; mkdir -p out/confirm
W=001001010101001010101
nice -n 10 ~/p196_run/r12e/bin/khxt_b 10 -g $W -L 42 -batch 4096 -exactset -v -kmax 2750 -nodecap 400000000 -anc 0 out/confirm/p21sq_K2750.seed \
  > out/confirm/p21sq_K2750.out 2> out/confirm/p21sq_K2750.err
echo "$(date -u +%FT%TZ) p21sq seed K2750 done" >> out/confirm/done_r12e2.log
nice -n 10 ~/p196_run/r12e/bin/kh2s 10 $W 42 -exact 2800 400000000 out/confirm/p21sq_K2750.seed > out/confirm/p21sq_kh2s.out 2>&1
echo "$(date -u +%FT%TZ) p21sq kh2s done" >> out/confirm/done_r12e2.log
