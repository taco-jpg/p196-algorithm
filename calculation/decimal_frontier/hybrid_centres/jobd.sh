#!/bin/bash
# job daemon: run under  ../bin/heavy 1790 ./jobd.sh  -- executes request files req/NNN (one shell command line each) sequentially.
cd /home/claude/research/w6_hybrid
idle=0
while true; do
  f=$(ls req 2>/dev/null | sort | head -1)
  if [ -z "$f" ]; then
    sleep 5; idle=$((idle+5)); [ $idle -ge 600 ] && { echo "idle exit"; exit 0; }
    continue
  fi
  idle=0
  cmd=$(cat req/$f); mv req/$f done/$f.cmd
  echo "[$(date -u +%H:%M:%S)] START $f: $cmd" >> done/jobd.log
  bash -c "$cmd" > done/$f.log 2>&1
  echo "[$(date -u +%H:%M:%S)] END $f rc=$?" >> done/jobd.log
done
