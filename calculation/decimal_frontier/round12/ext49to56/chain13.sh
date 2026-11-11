#!/bin/bash
# r12e2: when chain12 (deep pass 2, last word (001010101)^6) has finished, start the (p21)^2 confirmation and the decisive attempt
# (one worker each; census T=55/56 runs 9 jobs ~ 9.8 cores -> total <= 12 busy workers).
cd ~/p196_run/r12e
while pgrep -f "bash chain12.sh" > /dev/null; do sleep 10; done
echo "$(date -u +%FT%TZ) chain13: chain12 finished; starting run_p21conf.sh and run_decisive.sh" >> logs/chain13.log
./bg.sh logs/p21conf.log bash run_p21conf.sh
./bg.sh logs/decisive.log bash run_decisive.sh
