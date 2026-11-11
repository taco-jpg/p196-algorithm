#!/bin/bash
cd ~/p196_run/r13a
export DEADLINE=$(( $(date +%s) + 300 ))
exec ~/p196_run/venv/bin/python pool.py ~/p196_run/r13a/jobs_xchk7.txt 8 xchk7 > logs/pool_xchk7.out 2>&1
