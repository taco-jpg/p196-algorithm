#!/bin/bash
# after the fixed-period sweep of the closed classes finishes, run tier 4: all-period closure with a larger memory cap for a few selected jobs
cd ~/p196_run/r14a || exit 1
python3 - <<'PY'
s=open('src/rerun_budget.py').read()
if 'R14_FORCE' not in s:
    s=s.replace("jobs = []\nseen = set()","if os.environ.get('R14_FORCE'):\n    done=set()\njobs = []\nseen = set()")
    open('src/rerun_budget.py','w').write(s)
PY
while ! grep -q "sweep done" logs/sweep_run2.out 2>/dev/null; do sleep 15; done
sleep 5
printf "36 0\n23 3\n25 1\n" > logs/rerun_only_t4a.txt
printf "9 3\n9 2\n9 0\n9 1\n" > logs/rerun_only_t4b.txt
R14_FORCE=1 R14_ONLY=logs/rerun_only_t4a.txt python3 src/rerun_budget.py scc 32 5400 5 1 > logs/rerun_t4a.out 2>&1 &
R14_FORCE=1 R14_ONLY=logs/rerun_only_t4b.txt python3 src/rerun_budget.py scc 32 5400 5 1 > logs/rerun_t4b.out 2>&1 &
wait
echo tier4 done > logs/tier4.done
