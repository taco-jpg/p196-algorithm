#!/bin/sh
set -eu
D="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
sh "$D/run.sh"
c++ -std=c++17 -O3 -Wall -Wextra "$D/uniform_pairword.cpp" -o /tmp/w07_uniform_pairword
/tmp/w07_uniform_pairword
if /tmp/w07_uniform_pairword corrupt > /tmp/w07_uniform_wrong.txt 2>&1; then
 echo 'NEGATIVE CONTROL FAILED' >&2; exit 1
fi
grep -q 'INSERT FAIL t=0' /tmp/w07_uniform_wrong.txt
/tmp/w07_gmp_check 301 20000 > /tmp/w07_uniform_gmp301.txt
grep -q 'final_fnv64=2676930820902518277' /tmp/w07_uniform_gmp301.txt
cat /tmp/w07_uniform_gmp301.txt
echo 'W07_UNIFORM_ALL_CHECKS_PASSED'
