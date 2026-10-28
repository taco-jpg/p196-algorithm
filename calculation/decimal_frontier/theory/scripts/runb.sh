#!/bin/bash
# usage: runb.sh outfile b p g   (single bauto -w run through heavy)
out=$1; shift
/home/claude/research/bin/heavy 300 /home/claude/research/w2_theory/bin/bauto $1 $2 $2 -w -g $3 >> $out 2>/dev/null
