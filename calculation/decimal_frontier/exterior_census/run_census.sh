#!/bin/bash
# usage: run_census.sh p cap sec  -> sequential bx run over lists/all_p$p.txt, output out/census_p$p.txt (appends only missing words)
cd /home/claude/research/w5_exterior
p=$1; cap=$2; sec=$3
out=out/census_p$p.txt
touch $out
# skip words already done (EXHAUSTED/ACCEPT)
grep -E "EXHAUSTED|ACCEPT" $out | sed -E 's/.* g=([01]+) .*/\1/' | sort > /tmp/claude-0/done_p$p.txt
grep -v -x -F -f /tmp/claude-0/done_p$p.txt lists/all_p$p.txt > /tmp/claude-0/todo_p$p.txt || true
grep -v -E "EXHAUSTED|ACCEPT" $out > /tmp/claude-0/notdone_p$p.txt || true
grep -E "EXHAUSTED|ACCEPT|^WIT" $out > /tmp/claude-0/keep_p$p.txt || true
mv /tmp/claude-0/keep_p$p.txt $out
bin/bx 10 -f /tmp/claude-0/todo_p$p.txt -cap $cap -sec $sec >> $out
