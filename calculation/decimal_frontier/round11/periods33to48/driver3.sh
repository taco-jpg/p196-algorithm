#!/bin/bash
# r11d driver3: residue pass (words capped at 3M in out/db or out/dbB) with bxb (wire+band), cap 12M / 60 s, 5 shards, DB out/dbB
cd ~/p196_run/r11d
studio/run_stage_b.sh c3 "33 34 35 36 42 44 45 46 48 37 38 39 40" 12000000 60 lists_res 5
echo DRIVER3_DONE
