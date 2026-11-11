#!/bin/bash
# foreground status waiter: returns after at most $1 seconds or as soon as a new result line appears (prints new lines)
max=${1:-540}
cd ~/p196_run/r14c
mark=/tmp/r14c_mark.txt; [ -f $mark ] || touch $mark
start=$(date +%s)
while true; do
  grep -h -E "^TOWER|^RDIES|^RSURV|^IFB_WORD|^REG|CYCLE|KHR_RUN" logs/ifd_*.out logs/pass4_*.out ctrl/reg_all.log 2>/dev/null | sort -u > /tmp/r14c_now.txt
  new=$(comm -13 <(sort -u $mark) /tmp/r14c_now.txt)
  if [ -n "$new" ]; then echo "$new" | cut -c1-260; cp /tmp/r14c_now.txt $mark; break; fi
  now=$(date +%s); if [ $((now-start)) -ge $max ]; then break; fi
  perl -e 'select(undef,undef,undef,20)'
done
date -u
for f in CAP54a CAP56b N60_1 N60_2 N48_if1961 L32_A3 L40_word; do printf "%s: " $f; tail -1 logs/ifd_$f.err 2>/dev/null | cut -c1-110; done
pgrep -f "bin/(ifb|ifc|ifd|khr|ifw)" | wc -l
