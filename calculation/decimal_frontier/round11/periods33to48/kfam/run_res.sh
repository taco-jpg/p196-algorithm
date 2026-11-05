#!/bin/bash
# r11d: K-head period filter on every residue word (out/residue_wire.txt): pattern = the word g itself, L = p.
# "family dies at K=k" => no closed walk of length p in G_k => no 9-wire exterior with clock g (Lemmas A1-A4 of three_divides_r/PROOF.md).
# Watchdog: kill at RSS > 6 GB or > 180 s (-> UNDECIDED). 1 thread.
cd ~/p196_run/r11d/kfam
OUT=res_kfam.txt; touch $OUT
while read p g rest; do
  grep -q " $g " $OUT && continue
  nice -n 10 ./khead_len 60 $g $p > cur.out 2>&1 & pid=$!; t=0; why=""
  while kill -0 $pid 2>/dev/null; do sleep 1; t=$((t+1)); rss=$(ps -o rss= -p $pid 2>/dev/null || echo 0)
    if [ "${rss:-0}" -gt 6000000 ]; then kill $pid; why="KILLED_mem"; fi
    if [ $t -gt 180 ]; then kill $pid; why="KILLED_time"; fi; done
  wait $pid 2>/dev/null
  r=$(grep -o "family dies at K=[0-9]*" cur.out); lastK=$(grep -o "^K=[0-9]*" cur.out | tail -1)
  if [ -n "$r" ]; then echo "$p $g DIES ${r##*=}" >> $OUT; else echo "$p $g SURVIVES_TO ${lastK#K=} $why" >> $OUT; fi
done < ../out/residue_wire.txt
echo RES_DONE >> $OUT
