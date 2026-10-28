#!/bin/bash
cd /home/claude/research/w3_formats/code
O=../out/ksim_job.txt
echo start > $O
run(){ echo "### $1 Tper=$2 Wmax=$3 seeds=$4" >> $O; ./kinksim ../out/$1 $4 24 $3 $2 8 $5 >> $O 2>&1; }
run lattice_rec0.txt 80 60 400000 11
run lattice_rec1.txt 80 60 400000 12
run lattice_rec2.txt 192 60 150000 13
run lattice_p12m9.txt 72 60 400000 14
run lattice_p11n.txt 11 40 600000 15
run lattice_p12n1.txt 24 40 600000 16
run lattice_p12n2.txt 24 40 600000 17
run lattice_p12n3.txt 24 40 600000 18
echo end >> $O
