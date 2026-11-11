#!/bin/bash
# r12e: (replaces the rest of run_anc.sh after p34_K2000)  one worker, in this order:
#  1. p47 seed dump at level 730 (exact set with windows) + independent kh2s continuation (must die at K=763);
#  2. N12^4 = (0001)^12: khxt -top on pattern 0001, L=48, 3600 s (TOP99 closed part must be the 12 padded N12 nodes from K=55 on);
#  3. (p21)^2 ancestry K=1200 D=600.
cd ~/p196_run/r12e; mkdir -p out/confirm out/anc out/fam
# 0. control of the TOP99 extraction path: p11 must hit at K=31 and the extracted walk must replay exactly (mirror + integers)
nice -n 10 ~/p196_run/r12e/bin/khxt 10 -g 00001110001 -batch 4096 -exactset -top -stophit -kmax 100 -dump out/confirm/p11_hit.dump > out/confirm/p11_hit.out 2>&1
python3 py/extract_hit.py out/confirm/p11_hit.dump 00001110001 > out/confirm/p11_extract.out 2>&1
nice -n 10 ~/p196_run/r12e/bin/khxt 10 -g 000100010001 -batch 4096 -exactset -top -stophit -kmax 100 -dump out/confirm/n12_hit.dump > out/confirm/n12_hit.out 2>&1
python3 py/extract_hit.py out/confirm/n12_hit.dump 000100010001 > out/confirm/n12_extract.out 2>&1
nice -n 10 ~/p196_run/r12e/bin/khxt_b 10 -g 00010001000110001100010010001010100101000100011 -batch 4096 -exactset -kmax 730 -nodecap 400000000 -anc 0 out/confirm/p47_K730.seed > out/confirm/p47_K730.out 2>&1
nice -n 10 ~/p196_run/r12e/bin/kh2s 10 00010001000110001100010010001010100101000100011 47 -exact 800 400000000 out/confirm/p47_K730.seed > out/confirm/p47_kh2s.out 2>&1
echo "$(date -u +%FT%TZ) p47 seed + kh2s done" >> out/anc/done.log
nice -n 10 ~/p196_run/r12e/bin/khxt 10 -g 0001 -L 48 -batch 4096 -exactset -top -v -kmax 100000 -nodecap 400000000 -sec 3600 > out/fam/n12x4_L48.out 2> out/fam/n12x4_L48.err
echo "$(date -u +%FT%TZ) n12x4 done" >> out/anc/done.log
nice -n 10 ~/p196_run/r12e/bin/khxt_b 10 -g 001001010101001010101 -L 42 -batch 4096 -exactset -kmax 1200 -nodecap 400000000 -anc 600 out/anc/p21sq_K1200.anc > out/anc/p21sq_K1200.out 2>&1
echo "$(date -u +%FT%TZ) p21sq_K1200 done" >> out/anc/done.log
