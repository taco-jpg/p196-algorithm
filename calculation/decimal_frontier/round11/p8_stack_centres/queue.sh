#!/bin/bash
# r11a job queue: one cen2 job at a time, 6 threads, nice 10; restartable (skips logs that already contain RESULT).
cd ~/p196_run/r11a; mkdir -p runs
job() { # rec L q0 K [lo hi]
  local name="rec$1_L$2_q$3_K$4"; [ -n "$5" ] && name="${name}_$5"
  local log="runs/$name.log"
  grep -q '^RESULT' "$log" 2>/dev/null && return
  echo "$(date -u +%FT%TZ) start $name" >> queue.log
  local s=$(date +%s)
  nice -n 10 ./cen2_64 rec$1.tbl $2 $3 $4 6 $5 $6 > "$log.tmp" && mv "$log.tmp" "$log"
  echo "$(date -u +%FT%TZ) done $name $(( $(date +%s)-s ))s $(grep -o 'returns=[0-9]*' $log) $(grep -o 'maxprefix=[0-9]*' $log)" >> queue.log
}
shards() { # rec L q0 K nshards
  local tot=$(python3 -c "print(19**($2//2)*(10 if $2%2 else 1))"); local k
  for ((k=0;k<$5;k++)); do job $1 $2 $3 $4 $(python3 -c "print($tot*$k//$5)") $(python3 -c "print($tot*($k+1)//$5)"); done
}
for L in 13 14; do job 1 $L 5 1; done
for K in 2 3; do q=$((2+3*K)); for L in 4 5 6 7 8 9 10 11 12; do job 1 $L $q $K; done; done
for L in 4 5 6 7 8 9 10 11 12 13 14; do job 0 $L 5 1; done
for K in 2 3; do q=$((2+3*K)); for L in 4 5 6 7 8 9 10 11 12; do job 0 $L $q $K; done; done
shards 1 15 5 1 9
shards 1 16 5 1 18
job 1 13 8 2; job 1 13 11 3
shards 0 15 5 1 9
shards 0 16 5 1 18
job 1 14 8 2; job 0 13 8 2
echo "$(date -u +%FT%TZ) ALL DONE" >> queue.log
