#!/bin/bash
# r11d: K-head period filter (khead_len) on the primitive roots u of short-root residue words; L = the residue lengths p.
# Watchdog: kill if RSS > 8 GB or > 1500 s. One job at a time (1 thread).
cd ~/p196_run/r11d/kfam
run() { pat=$1; Ls=$2; out=kf_${pat}_L${Ls//,/_}.out
  nice -n 10 ./khead_len 45 $pat $Ls > $out 2>&1 & pid=$!; t=0
  while kill -0 $pid 2>/dev/null; do sleep 5; t=$((t+5)); rss=$(ps -o rss= -p $pid 2>/dev/null || echo 0)
    if [ "${rss:-0}" -gt 8000000 ] || [ $t -gt 1500 ]; then kill $pid; echo "KILLED by watchdog t=$t rss=$rss" >> $out; fi; done
  echo "$pat L=$Ls: $(tail -1 $out | cut -c1-150)"; }
run 00011 40,45
run 0000111 35,42
run 0010101 35,42
run 000100011 36,45
run 001010101 36,45
run 0001000111 40
run 00101010101 44
run 00010010111 33,44
run 000100100011 36,48
run 001001010101 36,48
run 000100010111 48
run 000011100011 48
run 0000101010011 39
run 0001000100101 39
run 0001000100011 39
run 0010101010101 39
run 0001 36,48
run 01 40,48
echo KFAM_DONE
