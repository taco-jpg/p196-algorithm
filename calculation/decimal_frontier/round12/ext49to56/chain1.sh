#!/bin/bash
# wait until the T49 kh2 sample check has finished, then run the ancestry queue (keeps the worker count at 12)
cd ~/p196_run/r12e
while pgrep -f "kh2_sample.sh 49" > /dev/null; do sleep 10; done
bash run_anc.sh
