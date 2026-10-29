#!/bin/sh
set -eu
cd "$(dirname "$0")"
scan="${TMPDIR:-/tmp}/x07_piston_scan_$$"
probe="${TMPDIR:-/tmp}/x07_piston_probe_$$"
replay="${TMPDIR:-/tmp}/x07_piston_replay_$$"
trap 'rm -f "$scan" "$probe" "$replay"' EXIT
c++ -std=c++17 -O3 piston_scan.cpp -lgmpxx -lgmp -o "$scan"
c++ -std=c++17 -O3 piston_probe.cpp -lgmpxx -lgmp -o "$probe"
c++ -std=c++17 -O3 repdigit_front.cpp -lgmpxx -lgmp -o "$replay"
"$scan" 20000
"$probe" 60000 -2907
"$replay" 9 -2907 8297 20000
