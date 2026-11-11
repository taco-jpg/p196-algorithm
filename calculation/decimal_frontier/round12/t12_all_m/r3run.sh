#!/bin/bash
# r12f3: run one job.  Args: logpath cmd args...   (log skipped if it exists = started or done)
f=$1; shift
[ -e "$f" ] && exit 0
/usr/bin/time -l nice -n 10 "$@" > "$f" 2>&1
echo "$(date -u +%FT%TZ) $(basename $f) $(grep RESULT $f | tail -1) rss=$(grep "maximum resident" $f | awk "{print \$1}")" >> ~/p196_run/r12f/r3/pool.log
