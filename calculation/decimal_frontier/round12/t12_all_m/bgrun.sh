#!/bin/bash
# r12f2: m=2 gap instance (q = 14..16): epoch 1 with clock standard for s < S0, free root-realizable after, exactly N
# overflows in the free part, tail return.  Args: U R S0 N solver
U=$1; R=$2; S0=$3; N=$4; solver=$5
f=~/p196_run/r12f/bres/gap_U${U}_r${R}_s${S0}_n${N}_${solver}.log
[ -e $f ] && exit 0
PY=~/p196_run/venv/bin/python
/usr/bin/time -l nice -n 10 $PY ~/p196_run/r12f/bfree.py group --U $U --r $R --T 120 --stdupto $S0 --nones $N --tailreturn --rootclock --solver $solver > $f 2>&1
echo "$(date -u +%T) gap U$U R$R s0=$S0 n=$N $solver $(grep RESULT $f) rss=$(grep 'maximum resident' $f | awk '{print $1}')" >> ~/p196_run/r12f/bres/pool.log
