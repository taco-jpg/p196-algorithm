#!/bin/bash
# r11d driver4: after driver3, rebuild residue (report_r11d.py), order it p33..40 then 42..48, run 6 kfam workers on it.
cd ~/p196_run/r11d
while pgrep -f driver3.sh >/dev/null; do sleep 30; done
nice -n 10 python3 py/report_r11d.py > out/report_after_c3.txt
sort -n -k1,1 -s out/residue_wire.txt > kfam/res_in.txt
for i in 0 1 2 3 4 5; do kfam/run_res_par.sh kfam/res_in.txt $i 6 & done
wait
echo DRIVER4_DONE
