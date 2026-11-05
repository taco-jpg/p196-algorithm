#!/bin/bash
# r11b: level families on small bases vs bwin, then exhaustive path checks with the level family (pathcheck_h)
cd ~/p196_run/r11b; mkdir -p vs
run() { # B CLOCK w0 wmax
  B=$1; C=$2; w0=$3; wm=$4
  ./lvl2 $B $C $w0 vs 2 26
  for ((w=w0+1; w<=wm; w++)); do ./lvl2 $B $C $w vs 2 28 $((w-1)); done
  for w in $w0 $((w0+2)); do echo "bwin reference w=$w:"; ./wbuild $B $C $w vs 2 >/dev/null && ./bwin $B $C $w vs 2 | grep "k="; done
  rm -f vs/*.bits
}
run 6 01 6 10
run 8 01 6 10
run 4 011001 6 10
run 13 1010010000 8 10
run 10 0001 8 10
for T in 12 14 16; do for w in 8 10; do HDIR=vs ./pathcheck_h 6 $T 01 $w | grep PATHCHECK; done; done
for T in 12 14; do for w in 8 10; do HDIR=vs ./pathcheck_h 8 $T 01 $w | grep PATHCHECK; done; done
HDIR=vs ./pathcheck_h 4 6 011001 6 | grep PATHCHECK
for w in 8 10; do HDIR=vs ./pathcheck_h 4 12 011001 $w | grep PATHCHECK; done
for w in 8 10; do HDIR=vs ./pathcheck_h 13 10 1010010000 $w | grep PATHCHECK; done
for w in 8 10; do HDIR=vs ./pathcheck_h 10 12 0001 $w | grep PATHCHECK; done
echo VAL_SMALL_DONE
