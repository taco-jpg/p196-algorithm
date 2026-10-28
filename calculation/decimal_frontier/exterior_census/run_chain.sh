#!/bin/bash
# starts the 40M residue pass (p25..32) after the two earlier heavy jobs ($1 $2 = their pids) have finished
cd /home/claude/research/w5_exterior
while kill -0 $1 2>/dev/null || kill -0 $2 2>/dev/null; do sleep 15; done
/home/claude/research/bin/heavy 1800 ./run_pass3c.sh > logs/pass3c.log 2>&1
