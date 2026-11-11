#!/bin/bash
PY=~/p196_run/venv/bin/python
RUN="$PY ~/p196_run/r13a/bandrun.py"
cd ~/p196_run/r13a/ctrl
for solver in kissat404 cadical195; do
 # W0 (T12 exterior, clock 1000): rotation 6 = band start y* = 31 in B0 W0^q
 $RUN L --clock 1000 --V 5,18,4,8,1,15,4,0,5 --T 12 --rot 6 --R 12 --solver $solver
 # p8 lattice bulk rows (clock 10, T=8): all rotations 20-letter SCC rows sampled
 for r in 0 5 10 15; do
  $RUN L --clock 10 --V 17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13 --T 8 --rot $r --R 12 --solver $solver
 done
 # base 9 certificates: both rec0 and rec1 rows at the true band-start rotation
 $RUN L --b 9 --clock 1100011000 --V 1,1,15,15 --T 10 --rot 1 --R 12 --solver $solver
 $RUN L --b 9 --clock 1100011000 --V 11,5,5,11 --T 10 --rot 3 --R 12 --solver $solver
 # base 9 full rotations
 for r in 0 1 2 3; do
  $RUN L --b 9 --clock 1100011000 --V 1,1,15,15 --T 10 --rot $r --R 12 --solver $solver
 done
 # base 9 R test: two periods (delta=4=0 mod s), foreign
 for r in 0 1 2 3; do
  $RUN R --b 9 --clock 1100011000 --V 1,1,15,15 --T 10 --rot $r --epochs 2 --Rfree 12 --solver $solver
  $RUN R --b 9 --clock 1100011000 --V 1,1,15,15 --T 10 --rot $r --epochs 2 --Rfree 12 --nofor --solver $solver
 done
done
