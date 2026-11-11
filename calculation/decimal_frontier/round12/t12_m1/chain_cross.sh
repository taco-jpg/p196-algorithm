#!/bin/bash
# r12a: after the seam cross-check pools finish, run the centre cross-checks (independent enc2; kissat404)
cd ~/p196_run/r12a
( while pgrep -f "indep/pool.sh" > /dev/null; do sleep 30; done
  MODE=cdefect JOBS=indep/jobs_cdefect.txt P=1 ./indep/pool.sh ) &
( while pgrep -f "xsolver/pool.sh" > /dev/null; do sleep 30; done
  MODE=cdefect JOBS=xsolver/jobs_cdefect.txt P=1 ./xsolver/pool.sh ) &
wait
