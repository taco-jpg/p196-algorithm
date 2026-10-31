#!/bin/bash
# Round 5 calibration: build the tools and check every known answer. Prints CALIBRATION PASS or stops at the first FAIL.
cd "$(dirname "$0")"
CXX=${CXX:-$(command -v clang++ || command -v g++)}
$CXX -O2 -std=c++17 -o reach reach.cpp || { echo "FAIL: build reach"; exit 1; }
$CXX -O2 -std=c++17 -pthread -o reachmt reachmt.cpp || { echo "FAIL: build reachmt"; exit 1; }
mkdir -p calib
chk() { if grep -qF -- "$2" "$1"; then echo "  ok   $3"; else echo "FAIL: $3 (expected '$2' in $1)"; exit 1; fi; }

# 1. positive controls: known certificates of the same format in base 13 (repo Lean) and base 4 (Seal 1996)
THREADS=4 ./reachmt 13 10 1010010000 ALL > calib/b13.log
chk calib/b13.log "TARGET band[8,16] phase 0 REACHED at height 55" "base 13 band {8,16} phase 0 at height 55"
chk calib/b13.log "TARGET band[8,16] phase 1 REACHED at height 75" "base 13 band {8,16} phase 1 at height 75"
chk calib/b13.log "250301 interfaces reachable" "base 13 complete, 250301 interfaces"
THREADS=4 ./reachmt 4 6 011001 ALL > calib/b4.log
chk calib/b4.log "TARGET band[2,4] phase 1 REACHED at height 13" "base 4 band {2,4} at height 13 (Seal's 13-digit block)"
chk calib/b4.log "956 interfaces reachable" "base 4 complete, 956 interfaces"
# 2. rebuild the left ends and replay them on real big integers (every band length, both parities, 20 periods)
BAND='1:4,0:8' PH=0 ./reach 13 10 1010010000 BAND > calib/fit_b13.log
BAND='1:1,0:2' PH=0 ./reach 4 6 011001 BAND > calib/fit_b4.log
python3 replay_band.py calib/fit_b13.log > calib/fit_b13.replay; chk calib/fit_b13.replay "REPLAY PASS" "base 13 certificate replay"
python3 replay_band.py calib/fit_b4.log > calib/fit_b4.replay; chk calib/fit_b4.replay "REPLAY PASS" "base 4 certificate replay"
# 3. base 10 known answers: neutral-band exteriors (census, EXTERIOR.md) and the p8 clock at period 8
THREADS=4 ./reachmt 10 11 00001110001 ALL > calib/p11.log
chk calib/p11.log "NEW STREAM at height 29: 00111010011" "p11 exterior stream at height 29"
chk calib/p11.log "18060 interfaces reachable" "p11 complete, 18060 interfaces"
THREADS=4 ./reachmt 10 12 0001 ALL > calib/p12.log
chk calib/p12.log "distinct wire streams 3" "p12: exactly 3 streams"
chk calib/p12.log "136652 interfaces reachable" "p12 complete, 136652 interfaces"
THREADS=4 ./reachmt 10 8 01 ALL > calib/c01_8.log
chk calib/c01_8.log "244784 interfaces reachable; band targets reached 0" "clock 01 period 8: complete, no band"
# 4. the single-thread tool (separate storage and hashing) must agree
BAND='1:3,0:6' PH=0 ./reach 10 8 01 BAND > calib/c01_8_reach.log
chk calib/c01_8_reach.log "244784 interfaces reachable" "reach agrees on clock 01 period 8"
./reach 10 12 0001 WIRE > calib/p12_reach.log
chk calib/p12_reach.log "136652 interfaces reachable" "reach agrees on p12"
# 5. batch mode = single mode
printf '8 01\n12 0001\n11 00001110001\n' | THREADS=1 ./reachmt BATCH 10 ALL 5000000 > calib/batch.log
chk calib/batch.log "244784 interfaces reachable" "batch mode"
# 6. clock-shift quotient (ROT=1, used by sweep.py heavy): same targets and heights, counts become orbits
THREADS=2 ./reachmt 4 12 011001 ALL > calib/b4_12.log
ROT=1 THREADS=2 ./reachmt 4 12 011001 ALL > calib/b4_12_rot.log
chk calib/b4_12.log "483598 interfaces reachable" "base 4, T=12: 483598 interfaces"
chk calib/b4_12_rot.log "242303 interfaces reachable (orbits" "base 4, T=12, ROT=1: 242303 orbits"
chk calib/b4_12_rot.log "TARGET band[2,4] phase 1 REACHED at height 13" "ROT=1 keeps the fit at height 13"
chk calib/b4_12_rot.log "TARGET band[2,4] phase 0 REACHED at height 18" "ROT=1 keeps the fit at height 18"
ROT=1 THREADS=2 ./reachmt 10 8 01 ALL > calib/c01_8_rot.log
chk calib/c01_8_rot.log "61248 interfaces reachable (orbits" "clock 01, T=8, ROT=1: 61248 orbits, same depth"
ROT=1 THREADS=2 ./reachmt 10 12 0001 ALL > calib/p12_rot.log
chk calib/p12_rot.log "distinct wire streams 1 (up to the clock shift)" "p12, ROT=1: the 3 streams are one shift orbit"
chk calib/p12_rot.log "45570 interfaces reachable (orbits" "p12, ROT=1: 45570 orbits"
echo "CALIBRATION PASS"
