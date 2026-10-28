#!/bin/bash
cd /home/claude/research/w3_formats/code
OUT=$1
echo "start $(date -u)" > $OUT
for b in $(seq 3 40); do
  for p in $(seq 2 12); do
    r=$(timeout 90 ./bwdcensus $b $p $p -bcap 400000 -f1cap 50000 2>/dev/null)
    echo "$r" | grep -E "^SCC|^HITFWD" | cut -c1-200 | sed "s/^/b=$b /" >> $OUT
    echo "$r" | grep SUMMARY | sed -E 's/.*b=([0-9]+) p=([0-9]+) words=([0-9]+).*words_hit=([0-9]+) .*words_undecided=([0-9]+).*/SUM b=\1 p=\2 words=\3 hit=\4 undec=\5/' >> $OUT
  done
done
echo "end $(date -u)" >> $OUT
