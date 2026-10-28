#!/bin/bash
cd /home/claude/research/w3_formats/code
OUT=../out/uE32_part2.txt
echo "start $(date -u)" > $OUT
exec /home/claude/research/bin/heavy 1750 bash -c "./bwdcensus_n 10 32 32 -part 2 4 -und ../out/und_p32_part2.txt 2>>$OUT.err | cut -c1-1800 >> $OUT"
