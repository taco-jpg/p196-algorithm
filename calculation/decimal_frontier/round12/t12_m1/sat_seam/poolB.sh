#!/bin/bash
# r12a task 1, second worker group on a disjoint tail of the job list (same command as pool.sh)
P=${P:-2}
cd ~/p196_run/r12a
echo "poolB start $(date) P=$P" >> sat_seam/pool.log
cat sat_seam/jobs_tailB.txt | xargs -P $P -L 1 bash -c "f=sat_seam/seam_U\$0_L\$1.log; [ -s \$f ] && grep -q RESULT \$f && exit 0; /usr/bin/time -l nice -n 5 ~/p196_run/venv/bin/python ~/p196_run/r12a/seamsat.py seam --U \$0 --Lj \$1 > \$f 2>&1; echo \"\$0 \$1 \$(grep RESULT \$f) rss=\$(grep \"maximum resident\" \$f | awk \"{print \\\$1}\")\" >> sat_seam/pool.log"
echo "poolB done $(date)" >> sat_seam/pool.log
