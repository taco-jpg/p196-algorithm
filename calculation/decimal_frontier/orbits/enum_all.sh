#!/bin/bash
# enum_all.sh T FRAC MAXSEEDS -- exhaustive small-seed regularization scan, all bases 2..40, D = largest with b^D <= MAXSEEDS (and D>=3)
T=$1; FR=$2; MS=$3
for b in $(seq 2 40); do
  D=3; while [ $(python3 -c "print($b**($D+1)<=$MS)") = "True" ]; do D=$((D+1)); done
  # also run one digit-length shorter for the length dependence
  for d in $(seq 3 $D); do ./cpp/enumscan $b $d $T $FR 3; done
done
