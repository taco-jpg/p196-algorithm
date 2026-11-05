#!/bin/bash
cd ~/p196_run/r11d
studio/run_stage.sh c1 "33 34 35 36" 300000 20 bin/bx3 6
studio/run_stage.sh c2 "33 34 35 36" 3000000 60 bin/bx3 6
studio/run_stage.sh c1 "37 38" 300000 20 bin/bx3 6
studio/run_stage.sh c2 "37 38" 3000000 60 bin/bx3 6
studio/run_stage.sh c1 "39 40" 300000 20 bin/bx3 6
studio/run_stage.sh c2 "39 40" 3000000 60 bin/bx3 6
echo DRIVER_DONE
