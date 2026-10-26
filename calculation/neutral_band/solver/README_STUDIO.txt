SAT/CP search for a base-10 neutral one-band return certificate  (constraint-solving angle)
================================================================================================
Files (all in this folder):
  p196cp.py            the encoding (IR -> CP-SAT or Z3), decoder, mirror re-check
  sweep.py             parallel sweep over length schedules (the thing to run); summarize.py, retry_unknown.py, recheck.py
  validate_known.py    re-finds the Lean certificates (bases 2,4,8,11,17,26)
  validate_bruteforce.py  solver vs exhaustive enumeration of all cycles of a tiny base/box (independent of the solver)
  count_instances.py   instance counts / run-time estimate for a planned sweep; run_studio.sh = the phases below
  mirror_copy/         copy of calculation/neutral_band_search.py (used if P196_MIRROR_DIR / the repo path is absent)

ENCODING (b = base, schedule S = cyclic list of interface lengths (n_k,m_k), k=0..p-1, n=|B|, m=|C|)
  Unknowns: B_k[i] in 0..2(b-1) (B_k[0]>=1), C_k[j] in 0..2(b-1) for j<ceil(m/2) (C_k is a palindrome in any cycle,
  because nextC is a palindrome and trimming is symmetric), carry bits cb (over B, low end), cc (over C), cr (over reverse B).
  Per step k (all constraints linear, carries are bits since entries<=2(b-1) and carry-in<=1):
    digit  D = x + cin - b*cout in [0,b-1]  for every position of the three carry chains  (== (x+cin) mod b, cout = (x+cin) div b)
    e1 = last carry of B-chain, e2 = last carry of C-chain, e1+e2 = 1 (Hyp.flip), gam = last carry of reverse-B chain = scheduled gam
    xd=(b-1)(1-e1), yd=(b-1)(1-e2)
    nextB[i] = DB[i]+DR[n-1-i]                                  (gam=0)
             = (DB++[xd])[i] + ([1]++rev DR)[i], i=0..n          (gam=1)        [exactly nextB of A120Template]
    nextC[j] = DC[j]+DC[m-1-j]  (gam=0);  a=DC++[yd]: a[j]+a[m-j], j=0..m (gam=1)
    trimming: nextB = B_{k+1} ++ (b-1)^u,  nextC = (b-1)^v ++ C_{k+1} ++ (b-1)^v,  B_{k+1},C_{k+1} = state variables of step k+1 (cyclic)
  The schedule determines everything else: gam_k=(m_{k+1}-m_k) mod 2, u_k=n_k+gam_k-n_{k+1}, v_k=(m_k+gam_k-m_{k+1})/2 (must be >=0, integer).
  KEY FACT: in a closed cycle sum u = sum gam, sum v = sum gam/2, so sum(u+v) = 1.5*sum(gam) >= sum(gam): EVERY closed chain
  of valid edges satisfies the cycleOK gain condition.  So "certificate" == "closed chain"; only sum gam >= 2 (even) is possible
  (sum gam = 0 would need constant lengths and N -> N+rev N > N cannot cycle; the solver agrees: UNSAT).
  maximal mode (default): trimming is maximal (B' does not end in b-1; C' with |C'|>=2 does not start/end in b-1).  This is WLOG:
  a neutral coefficient next to the band acts as a band coefficient and e1,e2 are unchanged by b-1 entries; the Lean certs of
  bases 26/11/17 are non-maximal representations of cycles that also exist in canonical form (checked).  --nonmax allows non-maximal.
  Every SAT is decoded and re-checked by the Python mirror of Lean's cycleOK (hard assertion), and recheck.py prints the Lean Edge list.

SCHEDULE SPACE (sweep.py): shape = (gam_k,u_k,v_k) with sum gam = G, sum u = G, sum v = G/2, plus offsets (n_0,m_0) such that all
  lengths lie in the box.  Shapes are enumerated up to rotation, primitive only (a repetition of a shorter cycle is covered by the
  shorter p).  For base 10 schedules with any state in |B|<=3,|C|<=6 are skipped (every start there breaks within 72 steps,
  RESULTS.md, 99,296,982 starts; use --no-cover to re-include them; the solver is fast enough that this is only a ~5% saving).

VALIDATION DONE (this VM)
  * bases 2,4,8,26 (Lean schedules, non-maximal; and canonical-cycle schedules, maximal) -> SAT, mirror cycleOK True, identical to the Lean cert where non-maximal.
  * base 11 (p=6, n=7, m=42..43): SAT in 2.4 s (canonical) / 35 s (Lean form); base 17 (p=6, n=29, m=21): 19 s / 56 s, one CP-SAT thread.
  * exhaustive comparison with brute force (all states in a box, canonical map from the mirror, every cycle):
      base 2 (|B|<=3,|C|<=7, p<=5: 18,143 schedules) MATCH (the 2 cycles); base 3 (|B|<=2,|C|<=5, p<=5: 6,770) MATCH (no cycles);
      base 4 (|B|<=2,|C|<=4, p<=6: 29,335) MATCH (1 cycle, 29,334 UNSAT); Z3 backend: base 4 p<=5 MATCH, base 2 SAT.
  * sweep sentinels: base 26 p=4 box 9x6: 2,915 schedules, exactly 1 SAT (the known cycle); base 11 p=6 box 6-7 x 41-43: 280, exactly 1 SAT;
      base 2 p<=6 box 3x7: 9,479, exactly the 2 brute-force cycles; base 4 p<=6 box 2x4: 3,179, exactly 1.
  * base 10 on this VM: p<=5, G=2, n<=12, m<=14: 30,227 schedules, all UNSAT, 3.4 ms mean, no timeout.

WHAT TO RUN ON THE STUDIO   (cd into this folder; python3 -m venv .venv && .venv/bin/pip install ortools; export REPO=~/p196-algorithm)
  bash run_studio.sh phase0     # ~3 min sanity (must reproduce SAT for known certs, MATCH, sentinel sat=1/2)
  nohup bash run_studio.sh phase1 > results_phase1.log 2>&1 &      # G=2, p=2..12, B<=30, C<=45: <=19.6M schedules
        # mean 3.4 ms (small) .. 19 ms (p=12, large box) per schedule per core => 20-100 core-hours => ~1-3 h with 30 jobs, ~100 MB RSS per job
  nohup bash run_studio.sh phase2 > results_phase2.log 2>&1 &      # G=4, p=4..7, B<=20, C<=30: <=20M schedules (do not run phases concurrently)
  nohup bash run_studio.sh phase3 > results_phase3.log 2>&1 &      # G=2, p=13..16: ~58M (extrapolated), several hours; or --shard i/N on several machines
  bash run_studio.sh retry      # only if some instance printed UNKNOWN (timeout 120 s): 1 h x 4 threads each
  bash run_studio.sh report     # table per (base,p,G) + Lean-formatted edge list of any SAT
  Progress: tail -f results_phase1.log.  Resume after interruption: rerun the same command (finished work units are skipped).
OUTPUT FORMAT  results/*.jsonl: one JSON line per work unit {key:[b,p,G,gam,u], n, unsat, sat, unknown, t_solver, t_wall, tmax, slow:[[S,sec,status]], found:[{S,cert}], unknown_S}.
  results/FOUND.jsonl: one line per SAT: {base,S,cert:{cycleOK_mirror,start_B,start_C,edges:[[B,C,B2,C2,u,v]...],sum_gam,sum_gain}}.
  UNSAT of every instance in a finished (p,G,box) = no base-10 neutral one-band cycle with that cycle length and those interface lengths
  (modulo: encoding correctness [validated above], maximal-trimming WLOG, covered-box result from RESULTS.md).
