Main-session check of r12d, 2026-11-08 (Studio clock). Script: mchk12d.sh (ran on a copy of r12d; r12d itself only read).
1. indep_enum.py: own parser of p8_scc.txt + plain Python integers N -> N + rev(N), no klib/cen3/tsat.
   22 cen3 cases (rec2 K1 L4-7, K2 L4-5, K3 L4-5; rec0/rec1 K4 L4-6, K5 L4-5, K6 L4-5): returns, maxprefix,
   argmax and the full HIST equal the cen3 logs (INDEP_ENUM_DONE all_agree=True).
2. b9check.py: tsat ret on b9r0/b9r1 L=4,6,8,10; every SAT centre re-checked by an own base-9 simulation (K=1 and
   K=3); full enumeration of L=4,6,8 agrees with tsat SAT/UNSAT in both directions.
3. cen3 rebuilt from cen3.cpp: rec2 K1 L7, rec0 K4 L6, rec1 K6 L5 logs reproduced line for line.
4. shield4.py: the 15 threshold lines equal shield_thresholds.log. lemma_orig.py: output equals lemma_rec*.log except
   that the logs lack the first two lines (header and PASS (1)); the full outputs are lemma_*.out here.
5. Other solvers: rec1 K1 L19 maplechrono UNSAT 620 s; rec0 K1 L20 kissat404 UNSAT 712 s (the first kissat run,
   sat_rec0_K1_L20_kissat.log, crashed after solving because tsat.solve_inst calls accum_stats, which Kissat in PySAT
   does not provide; the copy was patched with try/except NotImplementedError and rerun: kissat2.log).
6. rec2 K1 L4 prefix mode: k=189 SAT (centre [14,18,18,14] = idx 284, one of the argmax centres of item 1), k=190 UNSAT.
7. Log tally (run.log): 29 ret logs UNSAT, none SAT; 87 cen RESULT lines all returns=0; walls/bands 0 SAT;
   CANDIDATE only in the 4 base-9 positive controls.
