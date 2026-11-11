#!/bin/bash
# r12e2: compact data proposed for the repository -> out/compact/ (all small text files)
cd ~/p196_run/r12e; C=out/compact; mkdir -p $C
for T in 49 50 51 52 53 54 55 56; do [ -f out/census/summary_T$T.json ] && cp out/census/summary_T$T.json $C/census_summary_T$T.json; done
cat out/census/surv_T*.txt > $C/census_survivors.txt
python3 py/deep_tsv.py > $C/deep_verdicts.tsv
( for f in ctrl/kh2_T*.out ctrl/kh2_deep_*.out; do [ -f $f ] || continue; echo "== $f"; grep -v "^SAME" $f; echo "SAME lines: $(grep -c '^SAME' $f)"; done ) > $C/kh2_checks.txt
( echo "# final verdict lines of the open-word runs (khxt unless stated)"
  for f in out/taskA/*.out out/confirm/p47_khx3.out out/confirm/p47_kh2s.out out/confirm/p21sq_K2750.out out/confirm/p21sq_kh2s.out out/fam/*.out out/decisive/*.out out/anc/*.out out/confirm/*_extract.out; do
    [ -f $f ] || continue; echo "== $f"; grep -E "^(KHXT|KHX |KH2|TOP99|widths)" $f | tail -2; done ) > $C/open_words.txt
grep "^ANC" out/anc/p34_K2000.anc > $C/p34_K2000_ancestors.txt
grep "^ANC" out/anc/p21sq_K800.anc > $C/p21sq_K800_ancestors.txt
for f in out/taskA/p34.err out/taskA/p47.err out/taskA/p21sq.err out/decisive/T52w.err; do
  [ -f $f ] && grep "^  K=" $f | sed 's/^  //' | awk '{print $1, $2, $5}' > $C/levels_$(basename $(dirname $f))_$(basename $f .err).txt; done
ls -la $C; du -sh $C
