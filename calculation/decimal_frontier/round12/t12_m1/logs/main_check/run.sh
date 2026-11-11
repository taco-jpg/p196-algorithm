#!/bin/bash
# Main-session spot check of r12a: does the INDEPENDENT encoding reproduce rigid2's NON-empty defect sets,
# and does a fresh copy reproduce one main lemma?  Own scratch dir ~/p196_run/mchk12a.
D=~/p196_run/mchk12a; mkdir -p $D && cd $D
cp ../r12a/*.py . 2>/dev/null; cp ../r12a/*.txt . 2>/dev/null
PY=~/p196_run/venv/bin/python
run(){ name=$1; shift; ( /usr/bin/time -l nice -n 10 $PY "$@" > $name.log 2>&1; echo "$name :: $(grep -h -o -E '(D|E)=\[[0-9, ]*\] [A-Z]+' $name.log | tail -1) :: $(grep 'maximum resident' $name.log | awk '{printf "%.1fGB", $1/1e9}')" >> summary.txt ) & }
: > summary.txt
run indep_D1_V5   indep_defect.py defect  --V 5  --R 1 --solver cadical195
run indep_D1_V26  indep_defect.py defect  --V 26 --R 1 --solver cadical195
run indep_D1_V0   indep_defect.py defect  --V 0  --R 1 --solver cadical195
run indep_E4_V5   indep_defect.py cdefect --V 5  --R 4 --solver cadical195
run indep_E4_V23  indep_defect.py cdefect --V 23 --R 4 --solver cadical195
run rigid2_D12_U26 rigid2.py defect --U 26 --r 12 --solver cadical195
wait
echo "== expected (rigid2/cadical, r12a FINAL §5): D_1(U5)={6,7,15,16} D_1(U26)={2,3,11,12} D_1(U0)=empty E_4(U5)={3,12} E_4(U23)={7,16} D_12(U26)=empty"
sort summary.txt
grep -h -i -E "word|U=|V=" indep_D1_V5.log rigid2_D12_U26.log | head -4
echo MCHK12A_DONE
