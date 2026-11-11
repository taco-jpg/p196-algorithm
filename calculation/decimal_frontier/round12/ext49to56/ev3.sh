#!/bin/bash
# r12e3 event keys for the local monitor (read-only). One line per event; the monitor prints lines it has not seen before.
cd ~/p196_run/r12e
for f in out/deep5556/*.out; do
  [ -e "$f" ] || continue
  l=$(grep "^KHXT " "$f" | head -1)
  if [ -z "$l" ]; then echo "DEEP1 NOVERDICT $f"; continue; fi
  if echo "$l" | grep -Eq "top99_first=[0-9]|topUU_first=[0-9]"; then echo "DEEP1 TOPHIT $(basename $f) :: $(echo $l | cut -c1-230)"; fi
  if echo "$l" | grep -q SURVIVES; then echo "DEEP1 SURVIVES $(basename $f) :: $(echo $l | sed 's/.* SURVIVES/SURVIVES/' | cut -c1-150)"; fi
done
for f in out/deep2/5[56]_*.out; do
  [ -e "$f" ] || continue
  l=$(grep "^KHXT " "$f" | head -1)
  if [ -z "$l" ]; then echo "DEEP2 NOVERDICT $f"; else echo "DEEP2 $(basename $f) :: $(echo $l | sed -E 's/.* (DIES|SURVIVES)/\1/' | cut -c1-170)"; fi
done
n=$(ls out/census | grep -c '^T56_s.*\.done$'); echo "CENSUS56 done_round=$(( n / 9 ))"
grep -h "CENSUS_DONE" logs/census_55_56.log 2>/dev/null
cat out/confirm/done_r12e2.log out/decisive/done.log 2>/dev/null | sed 's/^/DONE /'
grep -h KILL logs/watchdog.log 2>/dev/null | grep "2026-11-08T0[6-9]" | sed 's/^/WATCHDOG /'
for c in 14 15 16; do [ -f logs/chain$c.log ] && sed "s/^/CHAIN$c /" logs/chain$c.log; done
grep "^  TOP" out/decisive/T52w.err | grep -v "c99=0 k99=0 nUU=[0-9]* cUU=0" | head -2 | sed 's/^/DECISIVE_TOPHIT /'
la=$(sysctl -n vm.loadavg | awk '{print int($3)}'); [ "$la" -gt 30 ] && echo "LOAD5_ABOVE_30"
[ -s out/decisive/T52w.out ] && echo "DECISIVE_RESULT $(cut -c1-200 out/decisive/T52w.out)"
[ -s out/confirm/p21sq_kh2s.out ] && grep -h "^KH2" out/confirm/p21sq_kh2s.out | sed 's/^/P21_KH2S /'

cat out/confirm/done_r12e3.log 2>/dev/null | sed "s/^/DONE /"
[ -s out/confirm/T52w_kh2s.out ] && grep -h "^KH2" out/confirm/T52w_kh2s.out | sed "s/^/T52_KH2S /"
[ -f logs/chain17.log ] && sed "s/^/CHAIN17 /" logs/chain17.log
grep "^  TOP" out/long/T53a.err 2>/dev/null | grep -v "c99=0 k99=0 nUU=[0-9]* cUU=0" | head -2 | sed "s/^/LONG_TOPHIT /"
exit 0
