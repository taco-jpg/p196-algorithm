#!/bin/bash
# usage: stage2.sh wordsfile out f1cap bcap
cd /home/claude/research/w3_formats/code
echo "start $(date -u)" > $2
./bwdwords 10 -f1cap $3 -bcap $4 < $1 2>>$2.err | cut -c1-1800 >> $2
echo "end $(date -u)" >> $2
