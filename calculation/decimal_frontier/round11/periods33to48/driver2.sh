#!/bin/bash
# r11d driver2 (successor agent): waits for driver.sh (PID 33823) to finish, then
#  0. builds bin/bxb (bx + uniform-band acceptance) and runs controls (ctrl/bxb_controls.out); stops if a control fails
#  1. band+wire pass over ALL F1 survivors of p = 34 36 38 40 (q=2 band {6,12}; q=6 6-cycle where 6|p), cap 300k then 3M
#  2. band+wire pass over the IMPRIMITIVE F1 survivors of p = 42 44 45 46 48 (lists_impr), cap 300k then 3M
cd ~/p196_run/r11d
while kill -0 33823 2>/dev/null; do sleep 60; done
echo "== $(date +%T) driver2 start"
c++ -O3 -std=c++17 -DKW=3 -o bin/bxb src/bxb.cpp || { echo BUILD_FAIL; exit 1; }
CO=ctrl/bxb_controls.out; : > $CO
B="6,12;2,4,8,16,14,10;0;18"
nice -n 10 bin/bxb 13 -g 1010010000 -band "8,16" -cap 5000000 >> $CO
nice -n 10 bin/bxb 4 -g 011001 -band "2,4" >> $CO
nice -n 10 bin/bxb 10 -g 01010101 -band "$B" -nosym >> $CO
nice -n 10 bin/bxb 10 -g 00001110001 -band "$B" >> $CO
nice -n 10 bin/bxb 10 -g 000100010001 -band "$B" -nosym >> $CO
nice -n 10 bin/bxb 10 -g 000100010001 -band "$B" >> $CO
nice -n 10 bin/bx3 10 -g 000100010001 -nosym >> $CO
cat $CO
ok=1
grep -q "g=1010010000 EXHAUSTED states=250302 .*band=0/.*@55 band=0/.*@75" $CO || ok=0
grep -q "g=011001 ACCEPT states=957 .*band=0/.*@13" $CO || ok=0
grep "g=01010101 " $CO | grep -q "EXHAUSTED states=244785" || ok=0
grep "g=01010101 " $CO | grep -q "band=" && ok=0
grep -q "g=00001110001 ACCEPT states=18061 .*e=00111010011@29$" $CO || ok=0
[ "$(grep -c 'g=000100010001 ACCEPT states=136653' $CO)" = 2 ] || ok=0
echo "CONTROLS ok=$ok"
[ $ok = 1 ] || exit 1
studio/run_stage_b.sh bc1 "34 36 38 40" 300000 20 lists 6
studio/run_stage_b.sh bc2 "34 36 38 40" 3000000 60 lists 6
studio/run_stage_b.sh ic1 "42 44 45 46 48" 300000 20 lists_impr 6
studio/run_stage_b.sh ic2 "42 44 45 46 48" 3000000 60 lists_impr 6
echo DRIVER2_DONE
