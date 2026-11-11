#!/bin/bash
# r12a: centre-side comoving defect sets E_R(V) (rigid2.py cdefect)
P=${P:-1}; JOBS=${JOBS:-cdef/jobs_r4.txt}
cd ~/p196_run/r12a
echo "pool start $(date) P=$P $JOBS" >> cdef/pool.log
cat $JOBS | xargs -P $P -L 1 bash -c "f=cdef/cdefect_U\$0_r\$1.log; [ -s \$f ] && grep -q RESULT \$f && exit 0; /usr/bin/time -l nice -n 5 ~/p196_run/venv/bin/python ~/p196_run/r12a/rigid2.py cdefect --U \$0 --r \$1 > \$f 2>&1; echo \"U\$0 R\$1 \$(grep RESULT \$f) rss=\$(grep \"maximum resident\" \$f | awk \"{print \\\$1}\")\" >> cdef/pool.log"
echo "pool done $(date)" >> cdef/pool.log
