#!/bin/bash
# sequential heavy stages (each re-enters the FIFO): 40M residue pass x3 (resumable), p22 B-level count, p=33 first pass
cd /home/claude/research/w5_exterior
for i in 1 2 3; do /home/claude/research/bin/heavy 1800 ./run_pass3c.sh >> logs/pass3c.log 2>&1; done
/home/claude/research/bin/heavy 1800 ./run_count.sh >> logs/count22.log 2>&1
/home/claude/research/bin/heavy 1800 ./run_pass4.sh >> logs/pass4.log 2>&1
