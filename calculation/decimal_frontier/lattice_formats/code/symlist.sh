#!/bin/bash
# usage: symlist.sh wordsfile out per_word_timeout   (base 10; symbolic backward cones, all uniform targets)
cd /home/claude/research/w3_formats/code
echo "start $(date -u)" > $2
while read -r w; do
  [ -z "$w" ] && continue
  timeout $3 /tmp/claude-0/bddenv/bin/python symbwd.py 10 $w -quiet 2>>$2.err | grep -E "TARGET|RESULT|STARTDEAD|built" | cut -c1-200 >> $2
  rc=${PIPESTATUS[0]}
  [ $rc -ne 0 ] && echo "TIMEOUT/ERR rc=$rc p=${#w} g=$w" >> $2
done < $1
echo "end $(date -u)" >> $2
