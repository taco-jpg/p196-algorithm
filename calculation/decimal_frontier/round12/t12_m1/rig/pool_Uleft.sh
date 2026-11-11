#!/bin/bash
# r12a: U left-rigidity SAT, depth R=3, all 30 U, 6 at a time
cd ~/p196_run/r12a
echo "pool start $(date)" >> rig/pool.log
seq 0 29 | xargs -P 6 -I{} bash -c "f=rig/Uleft_U{}_r3.log; [ -s \$f ] && grep -q RESULT \$f && exit 0; /usr/bin/time -l nice -n 5 ~/p196_run/venv/bin/python ~/p196_run/r12a/rigid.py Uleft --U {} --r 3 > \$f 2>&1; echo \"U{} \$(grep RESULT \$f)\" >> rig/pool.log"
echo "pool done $(date)" >> rig/pool.log
