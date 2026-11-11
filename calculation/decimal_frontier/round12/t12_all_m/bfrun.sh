#!/bin/bash
# r12f2: run one bfree.py job.  Args: U R T flags(comma list of stdclock,nofor,full or plain) solver
U=$1; R=$2; T=$3; fl=$4; solver=$5
f=~/p196_run/r12f/bres/bf_group_U${U}_r${R}_T${T}_${fl}_${solver}.log
[ -e $f ] && exit 0
flags=$(echo "$fl" | sed 's/plain//; s/,/ /g; s/\([a-z][a-z]*\)/--\1/g')
PY=~/p196_run/venv/bin/python
/usr/bin/time -l nice -n 10 $PY ~/p196_run/r12f/bfree.py group --U $U --r $R --T $T $flags --solver $solver > $f 2>&1
echo "$(date -u +%T) bfree group U$U R$R T$T $fl $solver $(grep RESULT $f) rss=$(grep 'maximum resident' $f | awk '{print $1}')" >> ~/p196_run/r12f/bres/pool.log
