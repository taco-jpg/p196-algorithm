#!/bin/bash
# r11a queue3 (successor agent; = queue2 + missing rec1 L16 shard + final controls): finishes queue.sh, reordered; one cen2 job at a time, 6 threads, nice 10; restartable.
cd ~/p196_run/r11a; mkdir -p runs
PY=~/p196_run/venv/bin/python3
log() { echo "$(date -u +%FT%TZ) $*" >> queue.log; }
while pgrep -f "^./cen2_64" >/dev/null; do sleep 10; done
for T in runs/*.log.tmp; do [ -e "$T" ] || continue; grep -q "^RESULT" $T && mv $T ${T%.tmp} && log "done (orphan) ${T%.tmp} $(grep -o "returns=[0-9]*" ${T%.tmp})"; done
job() { # tbl L q0 K [lo hi]
  local name="$1_L$2_q$3_K$4"; [ -n "$5" ] && name="${name}_$5"
  local log="runs/$name.log"
  grep -q "^RESULT" "$log" 2>/dev/null && return
  log "start $name"; local s=$(date +%s)
  nice -n 10 ./cen2_64 $1.tbl $2 $3 $4 6 $5 $6 > "$log.tmp" && mv "$log.tmp" "$log"
  log "done $name $(( $(date +%s)-s ))s $(grep -o "returns=[0-9]*" $log) $(grep -o "maxprefix=[0-9]*" $log)"
}
shards() { local tot=$($PY -c "print(19**($2//2)*(10 if $2%2 else 1))"); local k
  for ((k=0;k<$5;k++)); do job $1 $2 $3 $4 $($PY -c "print($tot*$k//$5)") $($PY -c "print($tot*($k+1)//$5)"); done; }
# 0. controls: FORCEDEV build (every 7th lane via scalar path) and Python reference for K=2,3
if [ ! -f ctrl.done ]; then
  log "start controls"
  clang++ -O3 -std=c++17 -DFORCEDEV=1 -DVW=64 -o cen2_fd cen2.cpp -lpthread 2>>queue.log
  for a in "rec1 8 8 2" "rec1 7 11 3" "rec0 8 8 2" "stk2 8 5 1" "stk1 6 2 1"; do set -- $a
    nice -n 10 ./cen2_fd $1.tbl $2 $3 $4 6 > runs/ctrl_fd_$1_L$2_q$3_K$4.log; done
  for a in "rec1 6 8 2" "rec0 5 11 3" "stk1 6 2 1" "stk3 5 0 1"; do set -- $a
    nice -n 10 $PY ref2gen.py $1.tbl $2 $3 $4 > runs/ctrl_ref_$1_L$2_q$3_K$4.log; done
  touch ctrl.done; log "done controls"
fi
job rec1 16 5 1 16040031760 16983563041
# 1. rec1 longer periods at L=13,14
job rec1 13 8 2; job rec1 13 11 3; job rec1 14 8 2
# 2. stacked exterior at small W20 count r (direct, s = 1,2,3), and rec0/rec1 below the shield threshold
for s in 1 2 3; do for r in 0 1 2 3 4 5; do for L in 4 5 6 7 8 9 10 11 12; do job stk$s $L $r 1; done; done; done
for R in rec1 rec0; do for r in 0 1 2 3 4; do for L in 4 5 6 7 8 9 10 11 12; do job $R $L $r 1; done; done; done
for R in rec1 rec0; do for r in 0 1 2 3 4 5 6 7; do for L in 4 5 6 7 8 9 10; do job $R $L $r 2; done; done; done
for R in rec1 rec0; do for r in 0 1 2 3 4 5 6 7 8 9 10; do for L in 4 5 6 7 8 9 10; do job $R $L $r 3; done; done; done
for s in 1 2 3; do for r in 0 1 2 3 4 5 6 7 8; do for L in 4 5 6 7 8 9 10; do job stk$s $L $r 2; done; done; done
# 3. rec0 leftovers (beyond the requested rec1 range)
job rec0 13 8 2
shards rec0 15 5 1 9
shards rec0 16 5 1 18
job rec0 14 8 2
# 4. Python reference controls (single thread)
for a in "rec1 6 8 2" "rec0 5 11 3" "stk1 6 2 1" "stk3 5 0 1"; do set -- $a
  f=runs/ctrl_ref_$1_L$2_q$3_K$4.log; [ -s $f ] || nice -n 10 $PY ref2gen.py $1.tbl $2 $3 $4 > $f; done
log "ALL DONE (queue3)"
