#!/bin/bash
# r12a: defect sets D_R(V) for the a=4 / a=14 rotations (rigid2.py defect)
P=${P:-2}; JOBS=${JOBS:-rig2/defect_jobs.txt}
cd ~/p196_run/r12a
echo "pool start $(date) P=$P $JOBS" >> rig2/defect_pool.log
cat $JOBS | xargs -P $P -L 1 bash -c "f=rig2/defect_U\$0_r\$1.log; [ -s \$f ] && grep -q RESULT \$f && exit 0; /usr/bin/time -l nice -n 5 ~/p196_run/venv/bin/python ~/p196_run/r12a/rigid2.py defect --U \$0 --r \$1 > \$f 2>&1; echo \"U\$0 R\$1 \$(grep RESULT \$f)\" >> rig2/defect_pool.log"
echo "pool done $(date)" >> rig2/defect_pool.log
