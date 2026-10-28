#!/bin/bash
# usage: symtargets.sh targetsfile(word loop0 ph per line) out per_target_timeout
cd /home/claude/research/w3_formats/code
echo "start $(date -u)" > $2
while read -r w l ph; do
  [ -z "$w" ] && continue
  timeout $3 /tmp/claude-0/bddenv/bin/python symbwd.py 10 $w -quiet -only $l:$ph 2>>$2.err | grep -E "TARGET|STARTDEAD" | cut -c1-200 >> $2
  rc=${PIPESTATUS[0]}
  [ $rc -ne 0 ] && echo "TIMEOUT/ERR rc=$rc p=${#w} g=$w loop0=$l ph=$ph limit=$3" >> $2
done < $1
echo "end $(date -u)" >> $2
