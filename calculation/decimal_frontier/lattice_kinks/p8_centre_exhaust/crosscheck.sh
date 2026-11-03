#!/bin/sh
# per-centre C++ vs Python (klib.pairword_step) comparison: full for L4,L5; every 37th centre for L6,L7
cd "$(dirname "$0")"
for R in 0 1; do for L in 4 5 6 7; do
  S=1; [ $L -ge 6 ] && S=37
  python3 ref.py $R $L 5 $S | sort > ref_$R$L.txt
  ./centre rec$R.tbl $L 5 1 x | grep '^D' | sort > cc_$R$L.txt
  N=$(wc -l < ref_$R$L.txt); M=$(comm -23 ref_$R$L.txt cc_$R$L.txt | wc -l)
  echo "rec$R L$L python_centres=$N mismatches_vs_cpp=$M"
  rm -f ref_$R$L.txt cc_$R$L.txt
done; done
