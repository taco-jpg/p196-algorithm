#!/bin/bash
# r12e3: long run on the most promising remaining T=49..54 UNDECIDED word (same type of run as the decisive T=52 run that died at
# K=1744): T=53 00001110000111000110001000101010101010101010100100111 (deep pass 2 reached K=1308 in 2,412 s, the deepest of the
# 7 open words; a 2-hour run reaches K ~ 2000+).  Starts in the slot of the T=52 confirmation (after its kh2s) and only if before
# 09:15Z; time cap = until 09:55Z so that the run ends by itself.  khxt -batch 4096 -exactset -top -inv -v, nodecap 2e8.
cd ~/p196_run/r12e; mkdir -p out/long
until grep -q "T52w kh2s done" out/confirm/done_r12e3.log 2>/dev/null; do sleep 30; done
SB=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "2026-11-08T09:15:00Z" +%s); EB=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "2026-11-08T09:55:00Z" +%s)
now=$(date +%s); [ $now -ge $SB ] && { echo "$(date -u +%FT%TZ) chain17: too late, no long run" >> logs/chain17.log; exit 0; }
S=$(( EB - now ))
W=00001110000111000110001000101010101010101010100100111
echo "$(date -u +%FT%TZ) chain17: long run T53a start, -sec $S" >> logs/chain17.log
nice -n 10 ~/p196_run/r12e/bin/khxt 10 -g $W -batch 4096 -exactset -top -inv -v -kmax 100000 -nodecap 200000000 -sec $S > out/long/T53a.out 2> out/long/T53a.err
echo "$(date -u +%FT%TZ) chain17: long run T53a finished :: $(grep '^KHXT ' out/long/T53a.out | cut -c1-200)" >> logs/chain17.log
