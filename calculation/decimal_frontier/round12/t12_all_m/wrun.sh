#!/bin/bash
# r12f2: one wclock.py job.  Args: mode q m
mode=$1; q=$2; m=$3
f=~/p196_run/r12f/bres/wclock_${mode}_q${q}_m${m}.log
[ -e $f ] && exit 0
/usr/bin/time -l nice -n 10 ~/p196_run/venv/bin/python ~/p196_run/r12f/wclock.py $mode --q $q --m $m > $f 2>&1
echo "$(date -u +%T) wclock $mode q$q m$m $(grep RESULT $f) rss=$(grep 'maximum resident' $f | awk '{print $1}')" >> ~/p196_run/r12f/bres/pool.log
