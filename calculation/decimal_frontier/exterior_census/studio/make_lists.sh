#!/bin/bash
# Regenerate the survivor word lists lists/fc_b10_p{p}_G{G}.txt for p in [PMIN,PMAX] (seconds; p=40 has 1,943,815 words).
cd "$(dirname "$0")/.."
bin/fc_enum 10 ${1:-17} ${2:-32} -list lists | tee out/fc_counts_regen.txt | tail -3
