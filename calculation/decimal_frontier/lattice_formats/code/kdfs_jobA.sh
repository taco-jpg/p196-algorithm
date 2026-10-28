#!/bin/bash
cd /home/claude/research/w3_formats/code
O=../out/kdfs_jobA.txt; echo "start $(date -u)" > $O
r(){ echo "### $1 W=$2 T=$3 $(date -u)" >> $O; timeout $5 ./kinkdfs ../out/$1 $2 $3 $4 0 200 2>/dev/null >> $O; echo "rc=$? $(date -u)" >> $O; }
r lattice_rec0.txt 6 80 6 300
r lattice_rec1.txt 6 80 6 300
r lattice_p12m9.txt 6 72 6 300
r lattice_rec2.txt 5 192 4 300
r lattice_rec0.txt 7 80 6 600
