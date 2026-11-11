#!/bin/bash
# r12b census pass 1: khx (exact K-head closed-walk filter) over ALL F1 necklaces (primitive + imprimitive) of length p = 41..48.
# lists/p{p}/fc_b10_p{p}_G*.txt from fc_enum (counts = data/f1_b10_p33_60.csv).  One output line per word (gzip).
cd ~/p196_run/r12b
N=${N:-16}
ARGS="-kmax 400 -nodecap 20000000 -sec 4"
mkdir -p out/census
for p in ${PLIST:-41 42 43 44 45 46 47 48}; do
  [ -f out/census/p$p.done ] && continue
  for ((i=0;i<N;i++)); do
    s=$(printf %02d $i)
    ( cat lists/p$p/fc_b10_p${p}_G*.txt | awk -v N=$N -v i=$i "(NR-1)%N==i" | nice -n 10 ~/p196_run/r12b/bin/khx 10 -f /dev/stdin $ARGS | gzip -1 > out/census/p${p}_s$s.khx.gz ) &
  done
  wait
  touch out/census/p$p.done
  echo "$(date -u +%FT%TZ) p=$p done"
done
echo CENSUS1_DONE
