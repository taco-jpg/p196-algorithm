#!/bin/bash
# usage: j_surv.sh latfile w olo ohi Hin outfile
cd /home/claude/research/w7_kink/code
echo "start $(date -u) $*" > $6
./surv $1 $2 $3 $4 400 $5 0 0 >> $6 2>&1
echo "end $(date -u)" >> $6
