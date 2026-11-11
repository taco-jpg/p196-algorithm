#!/bin/bash
# r12g3: base-9 planted positive control of the K > 25 path (kfwd3 base-D packing, indep packing): K = 26, 27 (k = 4) and
# K = 29 (k = 6, two free middle cells; K = 30 would need 3 free cells, too slow for indep at 1 thread); bottom filter = the lattice window only (planted_filter.py), top = base-9 TopCyc(4)
R=~/p196_run/r12g; L=$R/logs/g3; D=$R/data/g3; mkdir -p $D; cd $D
PY=~/p196_run/venv/bin/python
for lat in b9r0 b9r1; do
  for Kk in "26 4" "27 4" "29 6"; do
    set -- $Kk; K=$1; k=$2; Kf=$((K-k))
    $PY $R/src/planted_filter.py $R/data/lat_$lat.tbl $Kf $D/planted_${lat}_$Kf.bin >> $L/b9_planted.log 2>&1
    for ph in "0 0 0" "0 1 0" "0 0 1" "0 1 1"; do
      set -- $ph
      echo "=== kfwd3 $lat K=$K k=$k phi0=($1,$2,$3)" >> $L/b9_planted.log
      $R/bin/kfwd3 $R/data/lat_$lat.tbl $K $k $D/planted_${lat}_$Kf.bin $1 $2 $3 400 ${THREADS:-2} 0 $R/data/top9/top9_4.bin 4 | grep -E "^(A_0|STABLE|EMPTY|UNDECIDED|  PERIODIC|NESTING|PHASE|bad)" >> $L/b9_planted.log 2>&1
      echo "=== indep $lat K=$K Kb=$Kf phi0=($1,$2,$3)" >> $L/b9_planted.log
      $R/bin/indep_b fwd $R/data/indep/$lat.rows $K $Kf $D/planted_${lat}_$Kf.bin 4 $R/data/indep/top9/top_4.bin $1 $2 $3 ${THREADS:-2} 8 27 3 400 | grep -E "^(ifwd|STABLE|EMPTY|UNDECIDED|  periodic)" >> $L/b9_planted.log 2>&1
    done
  done
done
echo DONE >> $L/b9_planted.log
