#!/bin/bash
# r12a: second-solver cross-check of rigid2.py MODE (defect|cdefect) on JOBS ("U R" lines)
P=${P:-1}; SOLVER=${SOLVER:-kissat404}; MODE=${MODE:-defect}; JOBS=${JOBS:-xsolver/jobs_defect_r12.txt}
cd ~/p196_run/r12a
echo "pool start $(date) P=$P MODE=$MODE SOLVER=$SOLVER JOBS=$JOBS" >> xsolver/pool.log
export SOLVER MODE
cat $JOBS | xargs -P $P -L 1 bash -c "f=xsolver/\${MODE}_U\$0_r\$1_\${SOLVER}.log; [ -s \$f ] && grep -q RESULT \$f && exit 0; /usr/bin/time -l nice -n 5 ~/p196_run/venv/bin/python ~/p196_run/r12a/rigid2.py \$MODE --U \$0 --r \$1 --solver \$SOLVER > \$f 2>&1; echo \"\$MODE U\$0 R\$1 \$SOLVER \$(grep RESULT \$f) rss=\$(grep \"maximum resident\" \$f | awk \"{print \\\$1}\")\" >> xsolver/pool.log"
echo "pool done $(date)" >> xsolver/pool.log
