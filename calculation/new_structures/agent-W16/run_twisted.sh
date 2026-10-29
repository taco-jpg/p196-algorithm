#!/bin/sh
# Run from repository root. Requires C++17 and GMP.
set -eu
cd calculation/new_structures/agent-W16
g++ -std=c++17 -O3 twisted_macro.cpp -o /tmp/w16_twisted
g++ -std=c++17 -O3 twisted_macro_gmp.cpp -lgmpxx -lgmp -o /tmp/w16_twisted_gmp
g++ -std=c++17 -O3 phase_scan.cpp -o /tmp/w16_phase_scan
/tmp/w16_twisted > /tmp/w16_twisted_observations.txt
diff -u phase_observations.txt /tmp/w16_twisted_observations.txt
/tmp/w16_twisted_gmp
/tmp/w16_phase_scan
