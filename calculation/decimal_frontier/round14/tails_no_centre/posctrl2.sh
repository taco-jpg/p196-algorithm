#!/bin/bash
# positive controls, every wire loop of every certificate base; 40 s per orbit
cd ~/p196_run/mchk14
PY=~/p196_run/venv/bin/python
rm -f lat_ctrl/*
while read b p G cm bm gain; do
  echo "=== base $b p=$p G=$G maxC=$cm maxB=$bm"
  LYB=$b perl -e 'alarm 200; exec @ARGV' $PY mklat14.py $G $p lat_ctrl 1 2>&1 | tail -n 5 | cut -c1-160
  for f in lat_ctrl/b${b}_*_d${p}_*len1_*.txt; do
    [ -e "$f" ] || continue
    echo "  file $(basename $f) hdr $(head -n 1 $f) wire-row $(tail -n 1 $f)"
    for o in 0 1; do
      perl -e 'alarm 40; exec @ARGV' ./mc14w runscc $f $o 12 8 1 > logs_ctrl/tmp2.log 2>&1 || true
      if grep -q "orbit index" logs_ctrl/tmp2.log; then break; fi
      n=$(grep -c PERIODIC logs_ctrl/tmp2.log)
      echo "   orbit $o: exact-orbit lines $n; first: $(grep -m1 PERIODIC logs_ctrl/tmp2.log | cut -c1-120); last K: $(grep -E '^K ' logs_ctrl/tmp2.log | tail -n 1 | cut -c1-70); $(grep -E 'EMPTY' logs_ctrl/tmp2.log | cut -c1-30)"
    done
  done
done < logs_ctrl/certs.txt
