#!/bin/bash
# positive controls: every Lean-verified neutral-band certificate must reappear as an exact orbit of the wire closure
cd ~/p196_run/mchk14
PY=~/p196_run/venv/bin/python
mkdir -p lat_ctrl logs_ctrl
$PY - <<'P' > logs_ctrl/certs.txt
import sys, os
sys.path.insert(0, os.path.expanduser('~/p196_repo/calculation'))
import neutral_band_search as nb
for b, es in nb._lean_certs():
    G = ''.join(str(nb.gam(b, E[0], E[1])) for E in es)
    print(b, len(es), G, max(len(E[1]) for E in es), max(len(E[0]) for E in es), sum(E[4]+E[5] for E in es))
P
cat logs_ctrl/certs.txt
while read b p G cm bm gain; do
  echo "=== base $b p=$p G=$G maxC=$cm maxB=$bm gain=$gain"
  LYB=$b perl -e 'alarm 120; exec @ARGV' $PY mklat14.py $G $p lat_ctrl 3 2>&1 | tail -n 4 | cut -c1-200
  for f in lat_ctrl/b${b}_*_d${p}_*len1_*.txt; do
    [ -e "$f" ] || continue
    r=$(head -n 1 $f); wl=$(tail -n 1 $f)
    echo "  file $f hdr $r wire-row $wl"
    for o in 0 1 2 3; do
      perl -e 'alarm 100; exec @ARGV' ./mc14w runscc $f $o 40 8 1 > logs_ctrl/tmp.log 2>&1 || true
      if grep -q "orbit index" logs_ctrl/tmp.log; then break; fi
      echo "   orbit $o: $(head -n 1 logs_ctrl/tmp.log | cut -c1-90)"; grep -E "PERIODIC" logs_ctrl/tmp.log | head -n 6 | cut -c1-200; grep -E "^K " logs_ctrl/tmp.log | tail -n 1 | cut -c1-110; grep -E "EMPTY" logs_ctrl/tmp.log | cut -c1-60
    done
    break
  done
done < logs_ctrl/certs.txt
