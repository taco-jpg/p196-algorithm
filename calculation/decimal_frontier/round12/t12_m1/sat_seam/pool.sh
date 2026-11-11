#!/bin/bash
# r12a task 1: seam SAT (round-11 encoding seamsat.py, unchanged), |J|=10,11,12 x 30 U.  P workers.
P=${P:-4}
cd ~/p196_run/r12a
echo "pool start $(date) P=$P" >> sat_seam/pool.log
cat sat_seam/jobs.txt | xargs -P $P -L 1 bash -c "f=sat_seam/seam_U\$0_L\$1.log; [ -s \$f ] && grep -q RESULT \$f && exit 0; /usr/bin/time -l nice -n 5 ~/p196_run/venv/bin/python ~/p196_run/r12a/seamsat.py seam --U \$0 --Lj \$1 > \$f 2>&1; echo \"\$0 \$1 \$(grep RESULT \$f) rss=\$(grep \"maximum resident\" \$f | awk \"{print \\\$1}\")\" >> sat_seam/pool.log"
echo "pool done $(date)" >> sat_seam/pool.log
