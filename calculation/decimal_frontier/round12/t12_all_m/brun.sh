#!/bin/bash
# r12f2: run one brestore.py job.  Args: mode U R n flag(plain|full|nofor) solver
mode=$1; U=$2; R=$3; n=$4; fl=$5; solver=$6
f=~/p196_run/r12f/bres/b_${mode}_U${U}_r${R}_n${n}_${fl}_${solver}.log
[ -e $f ] && exit 0
case $fl in plain) flags="";; full) flags="--full";; nofor) flags="--nofor";; esac
PY=~/p196_run/venv/bin/python
/usr/bin/time -l nice -n 10 $PY ~/p196_run/r12f/brestore.py $mode --U $U --r $R --n $n $flags --solver $solver > $f 2>&1
echo "$(date -u +%T) $mode U$U R$R n$n $fl $solver $(grep RESULT $f) rss=$(grep 'maximum resident' $f | awk '{print $1}')" >> ~/p196_run/r12f/bres/pool.log
