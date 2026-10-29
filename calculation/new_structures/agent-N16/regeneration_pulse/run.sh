#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -O3 -std=c++17 search.cpp -o /tmp/p196_n16_pulse_search
g++ -O3 -std=c++17 evolve.cpp -o /tmp/p196_n16_pulse_evolve
g++ -O3 -std=c++17 replay.cpp -lgmp -o /tmp/p196_n16_pulse_replay
/tmp/p196_n16_pulse_search rows.txt 600000 | tee /tmp/p196_n16_screen.log
grep -q 'max264=-20' /tmp/p196_n16_screen.log
grep -q 'best264core=HEBBBCI8D2645G2HFAHE3CG5IG8F2' /tmp/p196_n16_screen.log
/tmp/p196_n16_pulse_evolve rows.txt 30000 HEBBBCI8D2645G2HFAHE3CG5IG8F2 | tee /tmp/p196_n16_evolve.log
grep -q 'RESULT best=-2 length=28 core=HEBBBCI8D2545G2HFAHE39AH9IF2' /tmp/p196_n16_evolve.log
/tmp/p196_n16_pulse_replay rows.txt 5 264 87FEBC813IFI5D46 | tee /tmp/p196_n16_early.log
grep -q 't=22 match=145 D=-6' /tmp/p196_n16_early.log
/tmp/p196_n16_pulse_replay rows.txt 300 20000 HEBBBCI8D2545G2HFAHE39AH9IF2 | tee /tmp/p196_n16_q300.log
grep -q 't=264 match=6037 D=2' /tmp/p196_n16_q300.log
grep -q 't=528 match=5978 D=61' /tmp/p196_n16_q300.log
grep -q 't=20000 match=1552 D=4487' /tmp/p196_n16_q300.log
/tmp/p196_n16_pulse_replay rows.txt 301 20000 HEBBBCI8D2545G2HFAHE39AH9IF2 | tee /tmp/p196_n16_q301.log
grep -q 't=20000 match=1572 D=4487' /tmp/p196_n16_q301.log
echo N16_REGENERATION_PULSE_PASS
