#!/bin/bash
# r12f: run one defect-set job.  Args: enc(md|mi) mode(defect|cdefect) U R m solver outdir
enc=$1; mode=$2; U=$3; R=$4; m=$5; solver=$6; out=$7
f=$out/${enc}_${mode}_U${U}_r${R}_m${m}_${solver}.log
[ -e $f ] && exit 0   # skip if started or done (several pools may share a job list; rename a crashed log to rerun)
PY=~/p196_run/venv/bin/python
if [ $enc = md ]; then
  /usr/bin/time -l nice -n 10 $PY ~/p196_run/r12f/mdefect.py $mode --U $U --r $R --m $m --solver $solver > $f 2>&1
else
  /usr/bin/time -l nice -n 10 $PY ~/p196_run/r12f/mindep.py $mode --V $U --R $R --m $m --solver $solver > $f 2>&1
fi
echo "$(date +%T) $enc $mode U$U R$R m$m $solver $(grep RESULT $f) rss=$(grep 'maximum resident' $f | awk '{print $1}')" >> $out/pool.log
