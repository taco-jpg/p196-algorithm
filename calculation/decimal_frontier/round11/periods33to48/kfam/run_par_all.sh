#!/bin/bash
cd ~/p196_run/r11d/kfam
for i in 0 1 2 3 4 5; do ./run_res_par.sh $HOME/p196_run/r11d/kfam/res_in.txt $i 6 & done
wait; echo PAR_DONE
