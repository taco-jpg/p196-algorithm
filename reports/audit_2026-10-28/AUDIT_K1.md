# AUDIT K1 -- 12 results on the decimal centre / lattice-kink question (repo HEAD c33d4433, 2026-10-28)

Auditor environment: 2 shared cores, `nice -n 10`, one process at a time, <=4 GB, each run <=10 min. python-sat 1.9 (CaDiCaL153, Glucose4,
MapleChrono) was pip-installed; repo code run unmodified from /home/claude/p196-algorithm (no git writes). Scratch/logs/scripts: this directory
(`/tmp/claude-0/-home-claude/61279d55-9bc5-5e58-836c-ca6225d98f6f/scratchpad/audit/K1/`). Files named below are in it unless a repo path is given.

## 0. Cross-cutting findings

* **The model behind all SAT/DFS "centre window" results is sound as I understand it.** State = top K=w+6 cells of the lower half of the pair word, bottom
  cells forced to equal the lattice (cell(t,pos)=W[t%p][(pos-nB)%m]), incoming ascending carry = lattice carry `cup`. Class coverage: the orbit of
  (phase 0, n) under the dynamics is determined by n mod 4 for p8 lattices (n advances 4 per 8 steps, spatial period 20/48 -> n mod 40/96) and by n mod 3 for p12/m9,
  so `n0=400+o`, o=0..3 resp. 0..2, hits every periodic kink. "Survives every horizon" is implied by periodicity, UNSAT at H implies UNSAT at H'>H, and width is monotone.
* **Independent check of that model (mine, `ind_window.py`)**: no window map, no carry bookkeeping: build the full pair word (exterior B + lattice + free top-w cells, mirrored),
  realise it as an actual decimal integer, do `N + int(str(N)[::-1])` with Python big ints, re-derive the pair word, require every cell below h'-w to equal the lattice.
  Brute force over all 19^w windows for w=2,3,4. Max survived steps equals the SAT "max SAT horizon" (`lifet.py`) in **33/33** cases
  (rec0: `ind_lat0.txt` vs `sat_lat0_small.txt`; rec2 + p12m9: `ind_lat2_p12.txt` vs `sat_lat2_p12_small.txt`). E.g. rec0 w=4 o=0..3 -> 16,15,15,14; rec2 w=4 -> 19,22,12,21; p12m9 w=4 -> 16,19,16.
  Also decoded SAT survivors for rec0 w=8 (o=0,1,3; H=32,34,38) replayed in big-int arithmetic: survive exactly 32/34/38 steps (`replay_sat_out.txt`).
* **Weak point (all SAT results)**: UNSAT is not proof-certified (no DRAT/LRAT). I cross-checked every width-8 UNSAT with two more solvers (Glucose4, MapleChrono; `xsolver_out.txt`, 11 instances, all UNSAT, H-1 controls SAT except rec0 o=2 where H-1=29 is also UNSAT, i.e. 30 is not minimal -- harmless).
  Widths 9-12 were run with CaDiCaL only (single solver) -- the only evidence beyond the small-width equivalence above.
* Hygiene: `results/Agent303P8WidthEight.md` ends with 30 bytes of binary garbage (file corrupted at commit 84c73690). `sat_kink.py`/`lifet.py` insert a nonexistent path
  `/home/claude/research/w7_kink/code` into sys.path (harmless). `python-sat` is not installed by default.
* Redundancy: Agent303 (rec0 w<=8) is implied by Agent1 (rec0 w<=12, width-monotone); Agent306 (p12m9 w=8) is implied by `results/Agent6P12M9Widths10to11.md` (w=11); Agent2K1BoundaryTransfer's open case (j mod 5 = 4) is closed by Agent2K1StationaryWall18; Agent5P12InvisibleDefect's phase-0 table is a row of Agent5P12AllPhaseKernel.

## 1. Agent1P8Rec0Widths9to12 -- **CONFIRMED**
Commands (lat0.txt = `write_lat0` output of agent303_w8_exclusion.py, header `8 39 20 10`; driver `drv.py` = `build(lat,w,o,'hor',H)` + CaDiCaL, exactly what `sat_kink.py ... hor H` does):
`python3 -I drv.py lat0.txt 9 0,37 0,36 1,39 1,38 2,33 2,32 3,43 3,42` -> UNSAT at 37,39,33,43; **SAT at 36,38,32,42** (12.7/11.0/5.4/11.7/14.7/3.4/10.4/11.0 s).
`... 10 0,41 1,43 2,41 3,48` -> all UNSAT (40.1,14.4,12.1,17.5 s). `... 11 0,56 1,48 2,46 3,53` -> all UNSAT (67.5,36.1,36.7,71.9 s).
`... 12 0,64 1,55 2,60 3,60` -> all UNSAT (139.6,141.6,338.0,207.2 s; load from other auditors). Logs `run_agent1_w9..w12.txt`. All numbers equal the note.
Caveats: single solver (CaDiCaL) at w>=9; scope exactly rec0 (not rec1 -- KINK.md argues rec1 is the same lattice shifted, but the shift also moves phase/space alignment; not proved here), not rec2, no w>=13. Label COMPUTED fits.

## 2. Agent303P8WidthEight -- **CONFIRMED** (redundant; corrupted note file)
`python3 -I calculation/.../agent303_w8_exclusion.py` -> UNSAT at (o,H)=(0,33),(1,35),(2,30),(3,39) (4.35,2.58,4.12,3.46 s). Cross-solver (Glucose4, MapleChrono) UNSAT too; SAT survivors at 32/34/(29 is UNSAT)/38 replay in big ints. Subsumed by Agent1. Note file has trailing garbage bytes.

## 3. Agent306P12M9Width8 -- **CONFIRMED**
`cd calculation/decimal_frontier/lattice_kinks/code; for O in 0 1 2: python3 lifet.py ../data/lat_p12m9.txt 8 $O 16` -> max SAT horizon 33,36,32; UNSAT at 34,37,33 (`run_agent306.txt`). Glucose4+MapleChrono UNSAT at 34,37,33. Independent big-int brute force at w=2..4 matches SAT lifetimes (7,10,5 / 8,12,9 / 16,19,16). Implied by Agent6 (w=11).

## 4. Agent369P8Rec2Width8 -- **CONFIRMED**
`for o in 0 1 2 3: python3 lifet.py ../data/lat2.txt 8 $o 16` -> max SAT horizon 28,27,27,37; UNSAT at 29,28,28,38 (`run_agent369.txt`). Glucose4+MapleChrono UNSAT. Big-int brute force w=2..4 on rec2 (exterior B taken from p8_scc.txt record 2, W checked equal to lat2.txt) matches. Not covered by any other note (rec2 only has this). Scope as stated.

## 5. Agent4NeutralK1P11W11P12W9 -- **CONFIRMED**
Inputs `make_neutral_k1_inputs.py k1`; `g++ -O3 -std=c++17 -DNDEBUG kinkdfs_mask.cpp`.
Control `./kinkdfs_mask k1/neutral_b26_control.txt 3 30 0 2` -> survivors 4 (o=0), 2 (o=1): matches. `./kinkdfs_mask k1/neutral_p11.txt 11 90 0 2` -> survivors 0,0 (81 s, 89 s; 24.4M/21.4M prunes);
`./kinkdfs_mask k1/neutral_p12.txt 9 70 0 2` -> survivors 0,0 (34 s, 148 s). (`run_agent4_full.txt`).
Independent cross-check with the *different* SAT window encoding (`drv.py k1/neutral_p11.txt 11 0,90 1,90` -> UNSAT 19.7/25.2 s; `neutral_p12.txt 9 0,70 1,70` -> UNSAT 22.6/26.0 s) and DFS-vs-SAT max lifetime agreement at w=5,6 for both exteriors, o=0,1 (8/8 equal: p11 15,17,17,17; p12 18,19,24,27; `dfs_vs_sat_neutral.txt`). True lifetimes are far below the 90/70 horizons used.
Caveat: depends on the (not re-audited) claim that these are the only decimal neutral exteriors for p<=12 and that other p12 exteriors are rotations; m=1 so only parity of n matters (o=0,1 is complete). Complements OPEN_PROBLEMS' existing "no centre for 1-2 laps" (this one is any period, bounded width).

## 6. Agent2K1BoundaryTransfer -- **CONFIRMED** (partly superseded)
`python3 agent2_boundary_check.py` -> numeric 400-digit control carries (0,1); for all j=0..19: unpeeled 0 with longest path 14,32,26,18 for j mod 5=0..3; 2189 unpeeled for j mod 5=4 (`run_agent2_boundary_check.txt`, 7 s).
`agent2_boundary_transfer.cpp rows.txt 4 10` -> k=10: candidates 169,030,175, edges 292,306,336, survivor core 29,717,052 (138.8 s, <4 GB); k=3: 2189 (`run_transfer_j4_k9.txt`, `run_transfer_j4_k10.txt`). All identical to the note.
**My soundness test of the transition relation** (`agent2_sound.py`): genuine 400-digit integers, lattice below x, random off-lattice columns above, honest big-int step; whenever the true next word still has lattice below x and an off-lattice cell at x, the true next k columns must be in `succ`. 42,044 transitions (k=3..6, both implementations) + 28,099 (k=10,14,18): **0 violations**. Mutant (the earlier wrong rule "descending carry must equal nominal at every overflow") gives 2207+732+763 violations, so the test has power. Hence the over-approximation is sound.
Caveat: j mod 5=4 case was "UNDECIDED beyond width 10" in the note; closed by item 7. Label COMPUTED fine.

## 7. Agent2K1StationaryWall18 -- **CONFIRMED WITH CAVEAT (scope)**
`agent2_stationary_bicore.cpp rows.txt j 18`: j=0 dies k=2; j=1 k=3; j=2 k=3; j=3 k=2; j=4,9,14,19: k=17 bicore 525, k=18 candidates 9,975 -> 0 (`run_bicore_*.txt`, <1 s each). Independent pure-Python Kosaraju SCC version `agent2_stationary_scc.py` for j=0,1,2,3,4,9,14,19: ALL PASSED (22 s), cyclic SCC nodes 525 at k=17, 0 at k=18. Together with item 6 (3-column graph acyclic for all 20 columns with j mod 5<4) this covers all 20 residues x all 8 phases. Logic of the lift (infinite path -> eventually in cyclic SCC -> projection) checked line by line: sound; soundness of `succ` per item 6.
Caveat: it excludes only a **pinned** first-defect column (fixed absolute x for all times). A real kink's first defect moves with the centre at ~1/4 column/step, so this does not touch K1 itself; the note says so. Truly "irrespective of centre width" holds because h-x only grows.

## 8. Agent3BulkLinearCharges -- **CONFIRMED (PAPER PROOF correct; low content)**
Referee: coefficient of a[i] in Q(P') is q[i]-b q[i-1]; of d[i] is q[i]-b q[i+1] (gamma=0) resp. q[i+1]-b q[i+2] (gamma=1): all equivalent to q[i+1]=b q[i], q[i]=b q[i+1] cyclically => q=b^i z, (b^2-1)z=0, (b^m-1)z=0; count = gcd(M, gcd(b^2-1,b^m-1)) = gcd(M,b^{gcd(2,m)}-1); multipliers 2 and 1+b. No gap. 2^4*11^4=22, 22^96=55 mod 99 verified. Label and stated scope (formally independent carries) are exact.
Runs: `agent3_charge_invariants.py` PASS. Mine, `ind_charges.py`: brute-force over all q in (Z/M)^m by literally expanding the update equations, b in {2,3,4,5,10}, M=2..12, m=1..4: 220 cases, count/form/multiplier all as claimed, 0 mismatches; rec2 row charges mod 99 = [0]*8.
Significance: trivial/redundant -- the survivors are exactly digit sum mod 9 and alternating sum mod 11 (KINK.md section 4 already had them). Not a no-go; the note says so.

## 9. Agent3CentreBoundaryFlux -- **CONFIRMED (identity correct; consequence weak)**
`agent3_boundary_flux_check.py` PASS (90,000 steps, bases 2..31, 48 cuts). Mine, `ind_flux.py` (carries via c[i]=floor(sum_{k<i}P[k]b^k / b^i), step via honest integer N+rev N in base b, bases 2..40, with forced 9-chains): 58,500 cases, **0 violations**, all 156 (base,parity,overflow) cells hit (`ind_flux_out.txt`). Proof read: sum the bulk recurrence over [L,R] with q[i+1]=bq[i], bq[i+1]=q[i] mod b^2-1; boundary terms as stated; midpoint cases are correct.
Caveat: the decimal consequence is only a mod-9 relation sum 2^{T-1-t} z[t]=0 on centre digits; since the mod-9 weights are all 1 this is the half-word digit-sum law (N+rev N = 2N mod 9) localised, so it is a necessary condition that I expect to prune little; it is not an exclusion. It also assumes the "returned template" form Q_T=Q_0 mod 99, which follows from zero row charge and q having period 2 (I checked this step). Not Lean-verified, label PAPER PROOF OK.

## 10. Agent5P12InvisibleDefect -- **CONFIRMED (correct, near-trivial)**
`python3 reproduce_wall_jump.py` OK for k=0,1,2,3,10,25,100,1000 (jump 165..9165). Mine (`ind_jump.py`, honest big ints): k=0,1,5,50: defective word (18->9 at j=35) and lattice word have identical next pair words, first mismatch 35 -> 200/209/245/650 -- **but the undefected lattice word already has first mismatch at the centre (h)**. So the "jump" is just instantaneous healing of a local defect; the first-mismatch statistic jumps because the centre mismatch is always there. The proof (all-k, local carry reset since rows have no adjacent 9s, which I confirmed on the printed rows) is correct, the scope statement ("refutes only an unconditional one-step bound on first-mismatch") is accurate, but it says nothing about persistent defects/K2.

## 11. Agent5P12AllPhaseKernel -- **CONFIRMED**
`classify_all_phase.py` -> COMPLETE (4 s). Mine, `ind_kernel.py` (honest big ints, 12 phases, lengths 400,401,418,419,500,501, every interior site, all 18 replacements): 11,316 sites, **0 mismatches** with the published table; phases 0/4/8 give exactly the listed +-9 replacements (residue 7 / 4 / 1 empty), non-overflow phases: no hit (`ind_kernel_out.txt`). Proof read line by line: gamma=0: ΔP'[j+1]=A, ΔP'[j-1]=B (partners untouched) => A=B=0 then 2δ=0 -- correct (also when neighbouring coefficient is 9, because the digit still changes); gamma=1: ΔP'[j]=δ-10A+B, ΔP'[j+1]=A+δ-10B => A=B, δ=9A -- correct; needs no 9 in rows 0,4,8 and upper carry = 1{W[r+1]>=10} -- true. Minor wording gap: "canonical realisation d=min(P,9)" fails to give a nonzero top digit when P[0]<=9 (use d[n-1]=max(1,P[0]-9)); irrelevant to the theorem. Supersedes item 10 partially. Interest: it shows the one-step map is non-injective on the lattice but says nothing about centres.

## 12. Agent14ComplementTwist -- **CONFIRMED WITH CAVEAT (label, scope, relevance)**
`python3 agent14_complement_twist.py` (from repo root) -> COMPLETE (80,320,16),(80,320,16),(192,768,39),(72,432,7), ALL PASSED. Mine (`ind_twist.py`, d up to 2L, all t): min mismatches 16,16,39,7, no exact even-G complement return -- equal.
Caveats: (i) it is an exhaustive finite check on stored rows, so COMPUTED, not PAPER PROOF (the only paper content is the one-line complement conjugacy, which is right: s*=2b-1-s). (ii) **my extra finding**: rec0 and rec1 *do* have exact complement returns when the length parity flips (odd G): 32 (t,d,shift) triples each, e.g. t=0, d=18, shift 5; rec2 and p12m9 have none. The result excludes only the parity-preserving ones, i.e. the class where the lattice symmetry does not exist anyway; the parity-flipping complement-twisted returns for rec0/rec1 (which reduce to ordinary period-2d kinks) are unexcluded and are the only structured candidates. (iii) Relevance to K1 low.

## Lean 4 candidates (finite kernel checks, no native_decide)
1. **Agent2 stationary, j mod 5 in {0..3}** (best): with `lat` = rec0 rows (20x8 + 39 exterior) and `succ_j` the pure function of `agent2_boundary_check.successors`: `theorem : ∀ j<20, j%5≠4 → (Nat.iterate (fun S => S.flatMap (succ_j j)) 33 allStates3) = []` by `decide +kernel`/`rfl` (|allStates3|=8*18*19*19=51,984; paths <=32 transitions; k=2/3 variants even smaller). Soundness of `succ` to the pair-word step would need a separate Lean lemma (the hard part). j mod 5=4 needs the 17 lifted layers (525 states) as data.
2. **Agent5 kernel (local lemma)**: `∀ t∈{0,4,8}, ∀ r<9, ∀ q'<19, q'≠W t r → ((A=B ∧ q'-q=9A) ↔ q'=tab t r)` with A,B = `(q'+c)/10-(q+c)/10` for c=cup t r resp. `if W t ((r+1)%9) ≥ 10 then 1 else 0`; plus `∀ t∉{0,4,8}` no 9 in W t adjacent, 9-free structure; and concrete `pwStep P' = pwStep P` for P of length 400 with `P'[35]=P'[364]=9` (list `rfl`/`decide +kernel`).
3. **Agent14**: `∀ lattice ∈ {rec0,rec1,rec2,p12m9}, ∀ t<p, ∀ d∈[1,L], G t d % 2 = 0 → ∃ j<m, W[(t+d)%p][(j+G/2)%m] + W[t][j] ≠ 18` (decide on data); and the rec0 odd-G witness `∀ j<20, W[18%8][(j+5)%20]+W[0][j]=18`.
4. **Agent3**: `∀ t<8, (∑ j<48, 10^j * W2 t j) % 99 = 0` and `22^96 % 99 = 55`; the general classification (gcd count) as a ZMod lemma.
5. **Small-width window exclusions** (e.g. rec0 w=3: no window of 19^3 survives 13 steps, o=0; or w=4/16 steps) via a verified `pwStep` on length-400 lists: kernel-feasible only for w<=3 (~36M list ops); SAT/DFS results for w>=8 are not realistic without an LRAT checker in the kernel (bv_decide uses axioms ofReduceBool, not allowed).

## Verdict table
Agent1 CONFIRMED | Agent2BoundaryTransfer CONFIRMED (superseded for j=4) | Agent2StationaryWall18 CONFIRMED WITH CAVEAT (pinned defect only) | Agent3Bulk CONFIRMED (trivial) | Agent3Flux CONFIRMED (weak consequence) | Agent4 CONFIRMED (2 methods) | Agent5AllPhaseKernel CONFIRMED | Agent5Invisible CONFIRMED (near-trivial healing) | Agent14 CONFIRMED WITH CAVEAT (COMPUTED not PAPER PROOF; parity-flip twists exist for rec0/1) | Agent303 CONFIRMED (redundant, note corrupted) | Agent306 CONFIRMED (redundant to Agent6) | Agent369 CONFIRMED.
Nothing NOT REPRODUCED, WRONG, or GAP. No result produces a certificate or a decision on K1 beyond width <=12 (rec0), <=11 (p12m9), <=8 (rec2), neutral p11 <=11 / p12 <=9.
