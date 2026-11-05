#!/bin/bash
# r11d: K-head period filter on residue words, worker I of N.  pattern = g, L = p (khead_len, Kmax 60).
# "family dies at K=k" => no closed walk of length p in G_k => no 9-wire exterior with clock g (three_divides_r/PROOF.md Lemmas A1-A4).
# Watchdog per word: RSS > 3 GB or > 60 s -> SURVIVES_TO (UNDECIDED).
cd ~/p196_run/r11d/kfam
IN=$1; I=$2; N=$3; OUT=res_kfam_w$I.txt; CUR=cur_w$I.out; touch $OUT
n=-1
while read p g rest; do n=$((n+1)); [ $((n % N)) = $I ] || continue
  grep -q " $g " $OUT && continue
  nice -n 10 ./khead_len 60 $g $p > $CUR 2>&1 < /dev/null & pid=$!; t=0; why=""
  while kill -0 $pid 2>/dev/null; do sleep 0.5; t=$((t+1)); rss=$(ps -o rss= -p $pid 2>/dev/null || echo 0)
    if [ "${rss:-0}" -gt 3000000 ]; then kill $pid; why="KILLED_mem"; fi
    if [ $t -gt 120 ]; then kill $pid; why="KILLED_time"; fi; done
  wait $pid 2>/dev/null
  r=$(grep -o "family dies at K=[0-9]*" $CUR); lastK=$(grep -o "^K=[0-9]*" $CUR | tail -1)
  if [ -n "$r" ]; then echo "$p $g DIES ${r##*=}" >> $OUT; else echo "$p $g SURVIVES_TO ${lastK#K=} $why" >> $OUT; fi
done < $IN
echo W_DONE >> $OUT
