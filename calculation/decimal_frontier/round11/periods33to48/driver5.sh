#!/bin/bash
# r11d driver5: words still open after c3 (12M) AND the K-head filter, minus the 3 known repetitions (p11^3, p11^4, N12^4): bxb cap 40M / 300 s, 6 shards
cd ~/p196_run/r11d
studio/run_stage_b.sh c4 "33 34 35 36 37 38 39 40 42 44 45 46 48" 40000000 300 lists_res2 6
echo DRIVER5_DONE
