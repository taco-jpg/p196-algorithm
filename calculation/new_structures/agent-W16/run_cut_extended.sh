#!/bin/sh
# Reproduce the complete W16 deeper-cut 33,456-edge two-counter family.
# From repository root. Requires g++ (C++17), GMP headers and libraries.
set -eu
cd calculation/new_structures/agent-W16
g++ -std=c++17 -O3 cut_extended.cpp -o /tmp/w16_deeper_cut
g++ -std=c++17 -O3 independent_gmp.cpp -lgmpxx -lgmp -o /tmp/w16_deeper_gmp
/tmp/w16_deeper_cut 440 530 33456 40 427 | tee /tmp/w16_deeper_baseline.log
grep -F 'fnv64=f362715e583f869' /tmp/w16_deeper_baseline.log
/tmp/w16_deeper_cut 443 537 33456 40 427 | tee /tmp/w16_deeper_control.log
grep -F 'fnv64=7682f311c8194b8a' /tmp/w16_deeper_control.log
/tmp/w16_deeper_gmp 440 530 33456 | tee /tmp/w16_deeper_gmp.log
grep -F 'fnv64=f362715e583f869' /tmp/w16_deeper_gmp.log
if /tmp/w16_deeper_cut 440 530 33457 40 427 >/tmp/w16_deeper_failure.log 2>&1; then
    echo 'ERROR: expected the next edge to reject' >&2; exit 1
fi
grep -F 'contract failure t=33456 reason=gamma cut phase slip' /tmp/w16_deeper_failure.log
echo 'ALL W16 DEEP-CUT CHECKS PASSED'
