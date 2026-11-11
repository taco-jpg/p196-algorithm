#!/bin/bash
# r12a task 2: centre SAT (round-11 encoding satc.py, unchanged), |C|=13,14,15 x 30 U.  P workers.
P=${P:-2}; JOBS=${JOBS:-sat_centre/jobs.txt}
cd ~/p196_run/r12a
echo "pool start $(date) P=$P" >> sat_centre/pool.log
cat $JOBS | xargs -P $P -L 1 bash -c "f=sat_centre/centre_U\$0_L\$1.log; [ -s \$f ] && grep -q RESULT \$f && exit 0; /usr/bin/time -l nice -n 5 ~/p196_run/venv/bin/python ~/p196_run/r12a/satc.py --U \$0 --L \$1 > \$f 2>&1; echo \"\$0 \$1 \$(grep RESULT \$f) rss=\$(grep \"maximum resident\" \$f | awk \"{print \\\$1}\")\" >> sat_centre/pool.log"
echo "pool done $(date)" >> sat_centre/pool.log
