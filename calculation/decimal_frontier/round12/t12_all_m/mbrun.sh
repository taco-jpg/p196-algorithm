#!/bin/bash
# r12f2: run one mbres.py job.  Args: V R flag(plain|full|nofor) solver
V=$1; R=$2; fl=$3; solver=$4
f=~/p196_run/r12f/bres/mi_group_U${V}_r${R}_n1_${fl}_${solver}.log
[ -e $f ] && exit 0
case $fl in plain) flags="";; full) flags="--full";; nofor) flags="--nofor";; esac
PY=~/p196_run/venv/bin/python
/usr/bin/time -l nice -n 10 $PY ~/p196_run/r12f/mbres.py group --V $V --R $R --m 1 $flags --solver $solver > $f 2>&1
echo "$(date -u +%T) mi group U$V R$R n1 $fl $solver $(grep RESULT $f) rss=$(grep 'maximum resident' $f | awk '{print $1}')" >> ~/p196_run/r12f/bres/pool.log
