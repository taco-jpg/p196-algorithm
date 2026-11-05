#!/bin/bash
# r11f watchdog: kill r11f jobs (reachdisk128/backdisk9w/bwin6/wbuild run from r11f) if their summed RSS exceeds 110 GB
while pgrep -f "reachdisk128|backdisk9w|bwin6|wbuild" >/dev/null; do
  tot=0; pids=""
  for p in $(pgrep -f "reachdisk128|backdisk9w|bwin6|wbuild"); do
    cwd=$(lsof -a -p $p -d cwd -Fn 2>/dev/null | grep ^n | cut -c2-)
    [ "$cwd" = "$HOME/p196_run/r11f" ] || continue
    r=$(ps -o rss= -p $p 2>/dev/null); [ -n "$r" ] || continue
    tot=$((tot + r)); pids="$pids $p"
  done
  if [ $tot -gt 115343360 ]; then echo "$(date -u +%FT%TZ) watchdog: r11f RSS ${tot}KB > 110GB, killing$pids" >> logs/watchdog.log; kill $pids; fi
  sleep 20
done
