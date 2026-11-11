#!/bin/bash
# r12a: independent re-implementation (indep_defect.py) MODE (defect|cdefect) for the V list in JOBS ("V R" lines)
P=${P:-1}; SOLVER=${SOLVER:-cadical195}; MODE=${MODE:-defect}; JOBS=${JOBS:-indep/jobs_defect_r12.txt}
cd ~/p196_run/r12a
echo "pool start $(date) P=$P MODE=$MODE SOLVER=$SOLVER JOBS=$JOBS" >> indep/pool.log
export SOLVER MODE
cat $JOBS | xargs -P $P -L 1 bash -c "f=indep/\${MODE}_V\$0_R\$1_\${SOLVER}.log; [ -s \$f ] && grep -q RESULT \$f && exit 0; /usr/bin/time -l nice -n 5 ~/p196_run/venv/bin/python ~/p196_run/r12a/indep_defect.py \$MODE --V \$0 --R \$1 --solver \$SOLVER > \$f 2>&1; echo \"\$MODE V\$0 R\$1 \$SOLVER \$(grep RESULT \$f) rss=\$(grep \"maximum resident\" \$f | awk \"{print \\\$1}\")\" >> indep/pool.log"
echo "pool done $(date)" >> indep/pool.log
