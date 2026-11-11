#!/bin/bash
cd ~/p196_run/r14a || exit 1
python3 - <<'PY' > class/rep_list.txt
import json
t=json.load(open('class/classes.json'))
for r in t: print(r['rep'])
PY
: > class/selftests.txt
for f in $(cat class/rep_list.txt); do
  out=$(./bin_mc14a selftest $f 7 60000 | tail -1)
  echo "$f : $out" >> class/selftests.txt
done
echo done >> class/selftests.txt
