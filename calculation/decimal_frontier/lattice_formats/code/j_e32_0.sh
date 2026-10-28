#!/bin/bash
cd /home/claude/research/w3_formats/code
OUT=../out/uE32_part0.txt
echo "start $(date -u)" > $OUT
exec /home/claude/research/bin/heavy 1750 bash -c "./bwdcensus_n 10 32 32 -part 0 4 -und ../out/und_p32_part0.txt 2>>$OUT.err | cut -c1-1800 >> $OUT"
