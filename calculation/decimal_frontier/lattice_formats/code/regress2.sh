#!/bin/bash
# usage: regress2.sh out bmin bmax pmin pmax per_run_timeout
cd /home/claude/research/w3_formats/code
OUT=$1; BMIN=$2; BMAX=$3; PMIN=$4; PMAX=$5; TO=$6
echo "start $(date -u)" > $OUT
for b in $(seq $BMIN $BMAX); do
  for p in $(seq $PMIN $PMAX); do
    r=$(timeout $TO ./bwdcensus $b $p $p -bcap 200000 -f1cap 50000 2>/dev/null); rc=$?
    echo "$r" | grep -E "SCC|HITFWD|HITBWD" | cut -c1-200 | sed "s/^/b=$b /" >> $OUT
    echo "$r" | grep SUMMARY | sed -E 's/.*b=([0-9]+) p=([0-9]+) words=([0-9]+).*words_hit=([0-9]+) .*words_undecided=([0-9]+).*/SUM b=\1 p=\2 words=\3 hit=\4 undec=\5/' >> $OUT
    [ $rc -ne 0 ] && echo "TIMEOUT/ERR b=$b p=$p rc=$rc" >> $OUT
  done
done
echo "end $(date -u)" >> $OUT
