#!/bin/sh
# Reproduce the replication (from this directory).
python3 -I exterior_ref.py 20000
gcc -O2 -o succ_dump succ_dump.c
for cap in 0 1 2 3 4 5 6 7; do gcc -O2 -fopenmp -DCAP=$cap -o enum$cap exterior_enum.c && OMP_NUM_THREADS=2 ./enum$cap > cap$cap.json; done
