#!/bin/bash
cd /home/claude/research/w3_formats/code
O=../out/kdfs_jobB.txt; echo "start $(date -u)" > $O
r(){ echo "### $1 W=$2 T=$3 $(date -u)" >> $O; timeout $5 ./kinkdfs ../out/$1 $2 $3 $4 0 200 2>/dev/null >> $O; echo "rc=$? $(date -u)" >> $O; }
r lattice_p11n.txt 8 11 40 300
r lattice_p12n1.txt 8 24 20 300
r lattice_p12n2.txt 8 24 20 300
r lattice_p12n3.txt 8 24 20 300
r lattice_p11n.txt 9 11 40 600
