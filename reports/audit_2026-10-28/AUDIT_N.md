# AUDIT_N -- results/*.md notes not covered by AUDIT_K1 / AUDIT_E / AUDIT_F (repo HEAD 0ffea2fa, 2026-10-28)

Scope: 55 notes (49 present at start + 6 that landed during the audit: Agent19FiniteCorePumping, Agent3Rec2PerturbationRadius,
Agent3ThreeCellBooleanNoGo, E2P21M3ChargeObstruction, E2P21M9ChargeClassification, E2P26M9AllTemporal).
Standard: same as the earlier audits (re-run the stated reproduction when < 10 min; otherwise the control/small version and say so;
write an independent cheap check; read PAPER PROOFs as a hostile referee). Machine: 2 cores, one process at a time, `nice -n 10`, `ulimit -v` <= 4 GB, each run <= 10 min.
Repo untouched (no commit/push/pull/fetch, no tracked file edited; scripts that write files were run from a scratch copy; `git status` clean).
Scratch (all my code and logs): `/tmp/claude-0/-home-claude/61279d55-9bc5-5e58-836c-ca6225d98f6f/scratchpad/audit/N/` (`g01/ rowmap/ a11m4/ agent3/ p12/ cols/ f1/ k14/ a19/ a3/ a15/ a4w/ lean/ logs/`).
Verdict vocabulary: CONFIRMED / CAVEAT / NOT REPRODUCED / WRONG / GAP / SKIPPED. "Shared model" = my check uses the same column/flux equations as the note (these equations were validated against big integers by AUDIT_E/F/K1, not re-validated here).

## Headline
* No WRONG, no NOT REPRODUCED, no GAP found. Every headline number I re-computed matched the note exactly.
* Non-CONFIRMED: **Agent12RootFactorBasis (CAVEAT)**: its necklace counts are exactly +1 above `fc_counts_b10.txt` / EXTERIOR.md for every p (the trivial all-zero necklace 0^p is counted; x=0 start allowed), unexplained in the note; committed CSV also differs from script output in line terminators only.
  **Agent15F2FamilyP1724 (CAVEAT, scope of my check)**: 30,618 decided words not re-run (only the 17 capped words, via the follow-up, and the table arithmetic).
  **Agent4NeutralK1P11W12P12W10 (CAVEAT, partial)**: 74 of 76 prefix runs reproduced (all survivors = 0); two heavy prefixes (p11 w12 o=1 d=9, p12 w10 o=1 d=4) exceeded my 10-minute limit.
  (Agent18P8Rec2Width11 is CONFIRMED but through the K1 CaDiCaL window encoding and a big-integer witness replay, because the note's z3 script cannot run without libz3.)
* Duplication / redundancy: Agent3 ansatz notes are nested (Scalar < Vector < TimeVary < PhaseBeta < Spatial) so three of the 99-results are corollaries; Agent11E2P16M8OneLap is a subset of E2P16M8AllTime; E2P21M9Superperiod8 is the k<=8 slice of E2P21M9AllTemporal; Agent2 T8/T16/T24 are subsumed by Stationary48 except classes j=10,34; six near-identical `full_scc_controls.cpp` copies under Agent12 dirs; Agent14ChargeSaturation is a modular-feasibility negative only.
* No silent contradiction between notes. One stale-status item: OPEN_PROBLEMS E2 still lists (10)^8 as "capped" although Agent11E2P16M4OneLap exhausted the 8-fold quotient forward set (257,093,987 states). Nobody has run a cycle/SCC check on that graph; it would decide E2 for (10)^8 (see suggestions).

---

## 1. Agent10F2OddBaseG01, Agent10F2G01Mod3, Agent10F2G01LinearDecision, Agent10F2G01InfiniteFamily, Agent10F2G01OddExponentCounterexample -- CONFIRMED (5 notes, one model)
Own `g01/bfs.cpp` (neutral-exterior BFS for g=01 straight from the column equations; mode 0 scans all x0, mode 1 uses the closed form x0 = b(a+h0+e) - (l0+l1+c0+y)).
* Repo `a10g01 2 10000`: 1.5 s, 1710 of 5000 even bases accepted. Own BFS (both modes) vs repo CSV, bases 2..3000: states, width, accept identical (0 mismatches); no odd accept, no b = 1 mod 3 accept.
* Family b = 3*2^k - 4 accepts at width k+1: own BFS k<=13, own `g01/fam.py` k<=400, repo script to k=1000.
* Powers of two: 2^13 31,811 states width 1450; 2^15 131,072 states width 4441; 2^17 14,977 states depth 3,744 no accept; 2^19 2,097,152 states width 501,157 -- all as in the notes.
* LinearDecision bound "<= 8b+1 states": observed max 4.6 b states (0.56 of 8b+1) over b = 2..3000. InfiniteFamily (b = 3*2^k - 4): the path is given by closed formulas of bounded degree in b, so exact agreement for k <= 400 (own) and k <= 1000 (repo) is conclusive for the identity part; parity (even/odd k) branches both covered.
* Hostile read: odd-base invariant proof correct. Mod-3 charge proof not re-derived symbolically (numerically consistent on all 3000 bases).
* Caveat: shared column model. The five notes are one statement family; no contradiction between them.

## 2. Agent11E2P16M4AllTime -- CONFIRMED
Own `rowmap/rm.cpp` (row map F_g on cyclic absorbing rows; fixed-point asc/desc carries) `rm 10 0101010101010101 4 all`: 130,321 rows, 2,195 dead (all-9), 110 cycles (60 fixed + 50 three-cycles), 70 mirrored, 64 primitive-spatial-4 (48 fixed + 16 three-cycles). Matches.

## 3. Agent11E2P16M8AllTime -- CONFIRMED (caveat: counting convention)
Own `rm ... 8 sym` 10,425,680 rows, 61,272 dead, closureFail 0; primitive m=8 cycles by block period k=2:128, 6:232, 9:128, 10:16, 18:32, 38:16 (552). My count of cyclic components (728) is before axis de-duplication; the note's 622 is after (its own GRAPH line reports duplicate_axes=14226). Same-m4 control gives the 64 above.

## 4. Agent11E2P16M8OneLap -- CONFIRMED (subset of #3)
No primitive m=8 cycle with block period 1 in my table. Pure corollary of AllTime.

## 5. Agent11E2P16M4OneLap -- CONFIRMED
Repo reproduce script: 5 m 21 s, 48 row cycles, 8 targets; stage 1 CAPPED at 210,365,479 states (depth 366), stage 2 EXHAUSTED at 257,093,987 states (depth 592), accepted = 0.
Independent: `rowmap/targets16.py` derives the 8 canonical accepting target keys from the 48 cycles and they equal the literal keys in the code; positive control `a11m4/ctrl_stage1.cpp` (root key added to the target list) hits (acc=1), so the "0 hits" is not an artefact of a dead search.
Observation (not a defect): the forward set is the *entire* reachable automaton of (01)^8 modulo 8-fold time rotation; the note only tests it against 8 targets. See suggestion S1.

## 6. Agent11E2P48M4Charge -- CONFIRMED
Own `rowmap/q48.py`: 16 primitive three-cycles, 9,216 column-equation checks (= 192 cuts x 48 steps), Q histogram {3:96, 6:96}, Q(root)=0. Proof re-derived: x_{t+1} - 2 x_t = Z_t - Z'_t (mod 9), 2^48 = 1 (mod 9) so sum 2^{-t} Z_t is conserved by every spatial edge; correct for any g with 6 | P.

## 7. Agent11E2P48M8OneLap -- CONFIRMED
Own `rm 10 (01)^24 8 sym` (2 m 34 s): 10,425,680 indexed rows (= 4*19^5 + 4*19^4, as in the note), dead 389,712, closureFail 0, 1,608 cyclic components, primitive m=8 block periods 2:824, 3:384, 6:96, 10:16, 38:16 -- none at block period 1. m=4 control: 96 primitive returns among 14,440 rows.

## 8. Agent3QuadraticParityNoGo, Agent3CubicParityNoGo, Agent3FullBooleanLocalParity, Agent3Rec2PerturbationRadius -- CONFIRMED (4 notes)
Own `agent3/gf2.py` (GF(2) rank of the 2,252 rec2 local tests): ranks 104 / 232 / 388 of 176 / 336 / 512 (quadratic / cubic / full 6-bit Boolean); per-phase zero-function dimension 9 / 13 / 14 (stable on a 40,000-row sample) so kernel = zero space for quadratic (72) and cubic (104), and 124 vs 112 for full Boolean = 12 false-positive dimensions. Repo `verify.py` + `independent_check.py` pass for all three (scratch copy). PerturbationRadius (landed later): same 388 as my own rank; repo scripts: ranks 388 -> 396 (distance 2) -> 398 (triples) -> 400 (distance 3), 34,236 extra two-site rows rank 398; independent check PASS.
Caveat: all four are finite-rank statements about the *rec2-local test set*; none excludes a centre (notes say so).

## 9. Agent3VectorCarryCovariance, Agent3TimeVaryCarryNoGo, Agent3PhaseBetaNoGo, Agent3SpatialWeightsMod198, Agent3ScalarCarryModuli -- CONFIRMED (5 notes; redundant)
Own `agent3/mods.py` (solvability of the covariance linear system over Z/M, 2,252 tests): vector, time-varying and phase-beta ansatz solvable exactly at M in {3, 9, 11} (i.e. M | 99; none at 2, 4, 8, 27, 121, 5, 7, ..., 101); spatial-weights ansatz exactly at {2, 9, 11} (M | 198). Repo `classify.py`/`independent_check.py` pass (scalar gcd 99 etc.).
Redundancy: the ansatz classes are nested (Scalar < Vector < TimeVary < PhaseBeta < Spatial), so Scalar/Vector/TimeVary 99-results are implied by PhaseBeta. 99 vs 198 is not a contradiction (extra freedom in Spatial).

## 10. Agent3FourStepSource -- CONFIRMED (PAPER PROOF read + numerics)
Proof: S4 = 22(2Z0+Z1) + 2Z2 + Z3 with Z0 = d, 2Z0+Z1 = e, Z2 = -2e (mod 9) => S4 = 18e = 0 (mod 9). Correct given the boundary-flux source formulas (Agent3CentreBoundaryFlux, audited in K1).
Independent: `a3/foursrc.py` implements the four Z-cases from the flux report on actual schoolbook carries: (a) flux identity Q' = A_g Q + X_L + Z (mod 99) holds in 84,248/84,248 random steps (L = 3); (b) 3,000 random even-length starts with overflow pattern 1,0,1,0: S4 = 0 (mod 9) in 3,000/3,000; control: odd-start 1010 samples give all nine residues mod 9 (2,665/3,000 nonzero), so the test has power.
Repo C++ `agent3_fourstep_source.cpp` (36 s): o=0,2: 2,476,099 centre words each, 11 distinct S4 mod 99; o=1,3: 1,303,210 words, 90 distinct -- as in the note.

## 11. Agent3PairSourceClosure -- CONFIRMED
Repo script (8 s) PASS: all 48 cuts, 4 length classes, 192/384/576 steps, D0 != 8 for o = 1, 3. Independent: `a3/pairalpha.py` samples 400,000 random numbers and computes V = (2Z_t + Z_{t+1})/q_* mod 99 for overflow-then-no-overflow pairs: even-start alphabet = exactly {0..9} (10), odd-start alphabet = exactly the predicted {-40k - 18e - 9v} (20 residues, all 11 mod 11). Hostile read of Sec. 3 (counting argument 99 / 90) is correct; the pair relaxation is weaker than the four-step identity of #10 for o = 0,2 (no conflict: #10 says the mod-9 part is automatically 0 there).

## 12. Agent5Gamma0FirstDefectGate, Agent5P12BulkCollisionTransfer, Agent5P12OverflowTransfer -- CONFIRMED
Own `p12/transfer.py` + `p12/gate_check.py` (p12/m9 lattice, rebuilt from `lat_p12m9.txt`): bulk-collision closing residues 7,7,4,4,1,1 (span 7) at t=1,2,5,6,9,10 and none at t=3,7,11; overflow phases t=0,4,8 non-closing residues 7,4,1, span 2 for the others; brute force over all colliding palindromic pairs n=7,8,9 gives gates inside the 4-case table; real lattice phases 3,7,11 have no gate. Repo scripts `k2_overflow_transfer.py`, `k2_gate_extension.py`, `gamma0_gate.py` PASS (24 realisable motifs, 3 first-defect exclusions).
Self-correction: my first overflow model had the edge equation wrong (used the current coefficient where the previous one belongs, and a mis-indexed baseline carry); I fixed it and the tables still match the notes (and the brute force).

## 13. Agent5P12CarryExcursionBound -- CONFIRMED (PAPER PROOF)
Own `p12/excursion.py`: for every phase and first-defect residue, DFS over nonbaseline reachable states with baseline as terminal: **acyclic in all 12 phases** (25 / 17 / 12 / 0 nonbaseline states for phase types 0,4,8 / 1,5,9 / 2,6,10 / 3,7,11), longest matching path = (9, 11, 7, 0) x 3, global 11 -- exactly the note. Repo `k2_component_dag.py` also prints global max 11, phases [9,11,7,0]x3. Proof logic (finite DAG => bounded connected excursion; scope limited to ONE connected component, one step) is sound and honestly scoped; it does not conflict with #14/#16 (multi-component, multi-step).

## 14. Agent5P12Connected72Stationary -- CONFIRMED
Own bigint replay (`p12/bigint_checks.py` part C: schoolbook seeds from the pairword, 72 ordinary reverse-and-add steps): both seeds 818 digits, first successor-pairword difference at index 180 (82 differing cells), unperturbed baseline reproduces the lattice. Repo `k2_connected72_counterexample.py` PASS. Scope (counterexample to "strictly outward first-defect motion"; no width/period claims) honest.

## 15. Agent5P12ExponentialFiber, Agent5P12NonErasingFrontJump -- CONFIRMED
Own `bigint_checks.py`: ExponentialFiber k<=8, both length parities: 2^k distinct seeds with identical successor pairword; NonErasingFrontJump k=2,3,4,5,7: the two seeds' successors differ exactly at J and n-1-J (+2 each). Repo `k2_multi_fiber.py` (k<=12, 4,096 seeds) and `k2_delayed_front.py` (k=100, jump 900) PASS. The all-k step is "concatenate k disjoint invisible motifs separated by 2 unchanged sites" -- read, sound.

## 16. Agent12ThreeColumnAllK, Agent12FourthColumnAllK, Agent12FifthColumnAllK, Agent12SixthColumnNoGoAllK, Agent12AdjacentOnesFamilyNoGo, Agent12TripleOnesRoot -- CONFIRMED
Own `cols/cols.py` (N-column time histories straight from the column equations) for g = (11000)^k, k=1..6: columns 3: 4^k; 4: 12, 128, 1152, 11648, 118272, 1215488; 5: 0, 12, 0, 72, 0, 432; 6: 0 for all k. Adjacent ones (11 0^r)^k: zero for r != 3 (r <= 12, k <= 4), 2^k for r = 3. Triple ones (111 0^r)^k: only r=4, 4^k.
Repo scripts (all 14 commands run from scratch copy): threecol/fourcol/fivecol/sixcol/triple/adjacent transfer scripts + independent C++ checkers PASS (k up to 8-12; fifth column k=12: 93,312; sixth column: no two consecutive edges => no time-closed 6th column for any k); sixcol `full_scc_controls` base-9/13 SCC controls run.
All-k logic (closed walks of length k in a fixed block graph; disjoint source/target sets for the 6th column; adjacent-ones depends on SixthColumn at r=3) read: sound.
Clutter: six near-identical copies of `full_scc_controls.cpp` in the `*_allk` dirs.

## 17. Agent12RootFactorBasis -- CAVEAT
Reproduced: own `f1/rootbasis.py` finds the 13 substring-minimal dead words (up to length 16, linear words 1..16 all 131,070 classified) = the note's list; the repo script passes both assertions (2.3 s); necklace table equals the CSV for p<=20.
**Caveat A (count off by one vs EXTERIOR.md):** the note's counts are exactly one larger than `exterior_census/fc_counts_b10.txt` / EXTERIOR.md 2.1-2.3 for every p (p=16: 96 vs 95; p=18: 208 vs 207; p=20: 450 vs 449; p=24: 2,269 vs 2,268 quoted in EXTERIOR.md). Cause (checked with `f1/f1.py` + a factor-basis necklace scan for p = 12, 14, 16, 18, 20): the dead-word automaton allows start coefficient x = 0 (note: "any starting coefficient in 0..18") while the F1 filter uses x in 1..18; x = 0 has a self-loop under g=0, so the all-zero necklace 0^p (G = 0, no overflow, not a legal exterior) is counted. Apart from 0^p the sets are identical (p >= 12). Harmless for use as a *necessary* filter, but the note should say it, or exclude 0^p, since it reports "survivors" beside EXTERIOR numbers.
Caveat B (cosmetic): `cmp` of script CSV vs committed `agent12_factor_basis_32.csv` fails only on line terminators (script writes CRLF, committed is LF); contents identical after `tr -d '\r'`.

## 18. Agent14ChargeSaturation -- CONFIRMED (low value)
Own `k14/pf.py`: 2^80 = 4, 2^18 = 1 (mod 9); row sums of W_t in {171,180,189}; (u,v,2r) -> residues mod (3,9,11) reaches 297/297 triples. Repo python (3 coefficient charge checks, 1,280 real-lattice pairword cases) and C++ independent (3,610 assignments, 297/297) PASS. It is a modular-feasibility negative result ("these charges cannot exclude a centre"); it proves nothing about existence.

## 19. Agent14ParityFlip -- CONFIRMED
Own scan (`k14/pf.py`, same glide/phase model): complement glides exist only for p8 rec0/rec1, even-start d = 18 mod 80, odd-start d = 62 mod 80; none for rec2/m48 and p12/m9. Repo python (alignment table, least mismatches 39 for rec2, 7 for p12) and C++ independent checker PASS. Caveat: the "physically aligned" shift delta = (G+1)/2 or (G-1)/2 is shared between my scan and the note (read: plausible, not re-derived from integers).

## 20. Agent15F2CappedFollowup -- CONFIRMED
Repo `agent15_verify.py` under `ulimit -v 4 GB` (so the "8 GB" requirement in the README is not needed): controls base 9 `1100011000` (956,310 states, 1,005,301 edges, 48,992 repeated), base 13 `1010010000` (250,302 / 254,201 / 3,900), base 7 (10)^12 (32,771 / 40,962 / 8,192) PASS; rows 1-12 PASS in 9 m 50 s (cut by my timeout), rows 13-17 re-run separately (166 s, 96 s, 97 s, 36 s, 78 s) PASS: 9 DECIDED_ACYCLIC with edges = states-1 and 0 repeated edges (a tree, hence acyclic), 8 CAPPED, one base-25 p19 stream exhausted at 18,296,615 states. Independent mirror/predecessor checkers PASS.
Own `rm 7 101001010110001011000 M sym`: M=3 primitive cycles only at block period 2 (6), M=9 at 2:27, 4:18, 8:36 -- no one-lap (period-1) m=3,9 mirror row, as the note says; m=1 targets uniform 0 and 12 (both have singleton predecessor cones, unreachable from root).
Caveat: "DECIDED_ACYCLIC" rests on the engine's repeated-edge counter being exact; it is validated by the three SCC controls with nonzero counts.

## 21. Agent15F2FamilyP1724 -- CAVEAT (scope of my check)
Table arithmetic consistent (30,635 = 30,618 decided + 17 capped); the 17 capped words are exactly the follow-up's 17 words (re-run in #20 with identical state/edge counts). I did NOT re-run the 30,618 decided words (needs the full census, >= 8 GB per the notes). Verdict on what was checked: CONFIRMED; on the whole note: partially reproduced.

## 22. Agent16F2TwoColumnFamily -- CONFIRMED (weak, misleadingly named)
Own count: exactly 4 two-edge paths for r = 1..5 (b = 2^(r+1)). The note is a statement about two-column *prefixes* only; it says so. The "F2" in the name suggests a family certificate, but AUDIT_F found no exterior SCC for these bases except b=4, b=16 -- the note proves nothing beyond two columns.

## 23. Agent18P8Rec2Width11 -- CONFIRMED (via a different SAT encoding; the note's own z3 script NOT run)
The note's reproducer needs a system libz3 (absent here; `import z3` fails), so `agent18_width11_reproduce.py` was not run. Instead:
* Big-integer replay of the published width-11 witnesses (`agent18_width11_check.py`, 40 ordinary reverse-and-add steps, all four phases o=0..3, no palindromes, exterior rows checked): BIGINT_REPLAY_PASS x4 (seed lengths 400..403 -> 420..423).
* Independent encoding: the K1 window encoding `sat_kink.build(lat2, w, o, 'hor', H)` (margin M=6 = the note's "margin-6 model") + CaDiCaL (pysat), `drv.py data/lat2.txt 11 ...`: **UNSAT at (o,H) = (0,50), (1,55), (2,58), (3,64)** (48 s, 59 s, 90 s, 119 s; 27-35k vars, 0.30-0.39M clauses); **SAT at H=40 for all four phases** (13-21 s). Width-8 control `drv.py lat2.txt 8 0,28 0,29`: SAT at 28, UNSAT at 29 (as the note and AUDIT_K1 #4).
* Scope in the note ("sufficient exclusion bounds, not maximal lifetimes", "no claim for width >= 12", no periodic centre of width <= 11 under the margin-6 window model) is honest. The model-vs-integers gap is closed only by the 40-step replay of SAT witnesses (model soundness is a K1-audited fact: AUDIT_K1 #4, w=2..4 big-integer brute force).

## 24. Agent2K1Rec2StationaryT8, ...T16, ...T24 -- CONFIRMED (3 notes)
Repo scripts: T8 3 s: 2,852 reachable states, 1,624 edges, 48/48 exhausted, C++ vs Python agree. T16 3 m 9 s: 1,317,912 states, 1,269,072 edges, no cycles. T24 49 s: 10,393,040 states, 8,273,248 edges raw; Kahn quotient 3,466,248 states / 2,758,832 edges, empty cyclic core 48/48. All equal the notes. Subsumed by #25 except j = 10, 34 (where #25 is UNDECIDED; T8/T16/T24 give the exclusions for those periods only).

## 25. Agent2K1Rec2Stationary48 -- CONFIRMED
Repo `agent2_rec2_data.py` + `agent2_rec2_stationary.cpp`: first vanishing k for j = 0..23 = 2,2,24,4,6,2,4,3,3,4,CAPPED,4,2,2,8,4,2,5,7,2,2,3,4,3 reproduced for every j = 0..47 (j+24 identical; all 46 resolved classes checked, `bin/a2rec2 rec2_rows.txt j 29 3000000`, seconds each); j=10 and j=34 (identical outputs): k=14 has 25,140,401 candidates and 4,884,451 bicore survivors, k=15: 92,804,569 candidates (> the 60M cap) -- identical to the note (43 s each). For j=10 the bicore grows ~3.7x per added column (357,093 -> 1,323,179 -> 4,884,451): the over-approximation does not appear to be closing, so this method is unlikely to decide j=10,34.

## 26. Agent4NeutralK1P11W12P12W10 -- CAVEAT (partial reproduction: 74 of 76 prefix runs done, 2 exceeded my 10-minute limit)
The note's reproducer is `run_neutral_wide.py` (full run = 76 prefix runs of `kinkdfs_mask`, no runtime stated; it is checkpointed). I ran its `--controls-only` mode and then the prefix runs individually (`kinkdfs_mask neutral_pXX.txt W H o o+1 d`, `ulimit -v 3 GB`, `nice`, `timeout 590`):
* Controls (6 s): independent 36-case direct-digit checker PASS; base-26 positive control (4, 2) survivors PASS; 6 partition checks PASS; previous-result controls (p11/p12, w=6, H=30, both parities) PASS.
* Structure found: for the neutral exteriors almost every first digit is pruned immediately (`prunes=1`, survivors 0): p11, both parities: 18 of 19 prefixes; p12 o=0: 18 of 19; p12 o=1: 15 of 19. All of those trivial prefixes were run and give survivors = 0. The whole exclusion therefore rests on a few heavy prefixes (d = 9 = b-1, plus d = 2,3,4 for p12 o=1).
* Heavy prefixes completed with survivors = 0 (last level count 0): p11 w=12 H=100 o=0 d=9 (544 s, 135,344,431 prunes); p12 w=10 H=80 o=0 d=9 (456 s, 98,578,909 prunes); p12 o=1 d=9 (261 s), d=2 (236 s), d=3 (397 s).
* **Not completed (hit my 590 s limit, no result): p11 w=12 o=1 d=9 and p12 w=10 o=1 d=4.** I therefore did not confirm 2 of the 76 prefix runs; no counter-evidence either. The older w=11 / w=9 versions of the same computation were confirmed by two methods in AUDIT_K1 #5 (DFS and a different SAT encoding).
* Scope of the note ("all possible temporal periods": a periodic centre would survive every horizon, so surviving 0 at H = 100 / 80 excludes all periods) is correct as written; only widths <= 12 (p11) and <= 10 (p12) and only the stated exteriors. K1's caveat about the list of neutral exteriors still applies.
* Suggestion: the note should state the per-prefix run times (up to > 10 min each) so a reproducer knows the full run is hours, and should say that 18/19 prefixes per parity are trivial.

## 27-29. E2P21M9AllTemporal, E2P21M9Superperiod8, E2P26M9AllTemporal -- CONFIRMED
Own `rm 10 001001010101001010101 9 sym` (2 m 43 s): 22,284,891 rows, 9 dead, 315 cyclic components (= 35 x 9 axes), primitive by block period 2:45, 4:54, 8:9, 16:36, 24:18, 30:9, 32:18, 34:9, 54:9 (207 = 23 x 9) -- equal to AllTemporal; times starts-per-cycle (2,4,8) give 90/216/72 and 378 primitive for Superperiod8 (which is just the k<=8 slice of AllTemporal).
Own `rm 10 10010100010101001010001000 9 sym` (3 m 17 s): 22,284,891 rows, 225 components (25 x 9), primitive 1:18, 2:36, 4:18, 5:18, 6:9, 19:18, 24:18, 57:18 (153 = 17 x 9) -- equal to P26 note.

## 30. E2P21M3ChargeObstruction -- CONFIRMED (PAPER PROOF + COMPUTED)
Own `rm 10 G21 3 all`: 6,859 rows, 52 cycles, 15 reflective primitive 42-step (k=2) cycles + 3 of k=8 (168 steps). Own `rowmap/qcharge.py G21 3 enumerate`: 18 cycles, 15,876 column-equation checks, Q at block start: (k=2) Q=3 for 9, Q=6 for 6, i.e. all 15 in {3,6}; the 3 k=8 cycles have Q=0 (note: undecided -- stated). Q(root)=0 (L=0, H=g, Y=1 gives Z=0 each step). Proof re-derived (valid for any g with 6 | P; Q -> nQ under n-fold repetition so 3 not dividing n keeps the obstruction). Scope honest (only root repeated n times, 3 not dividing n; 168-step family not covered).

## 31. E2P21M9ChargeClassification -- CONFIRMED (PAPER PROOF + COMPUTED)
Own `DUMP=axis rm2 ... 9 sym` + `qcharge.py G21 9 dump`: 23 primitive cycles, 1,772,064 column-equation checks (all pass), Q at block 0: Q=0: 5, gcd(Q,9)=1: 12, Q in {3,6}: 6 (k:Q breakdown in `logs/`); equals the note's 5/12/6. Rotating by one block multiplies Q by an invertible power of 2 (seen as 4,5,4,5... alternation). Scope (root ring equal to the family's period or restricted repetitions; 5 charge-zero families undecided) is honest.

## 32. Agent19FiniteCorePumping -- CONFIRMED (PAPER PROOF)
Hostile read of the algebra: the monotone carry map is idempotent so c' = c; D_k = A Y^k M R^k F via Z^k u = u R^k; |A| = |F|; pairs(D_k) = H Q^k K rev(Q)^k rev(H); edge conditions follow from commutation; leading digit nonzero when gamma = 0 -- all correct. Independent: `a19/pump.py` 6,000 random templates (bases 2,3,4,5,7,9,10,13,26, random exterior/body/core, k=0..3): 24,000 integer cases, predicted digit string and pairword equal the actual N+rev(N) digits in 24,000/24,000, leading digit nonzero in all. Repo `finite_core_check.py /home/claude/p196-algorithm`: BASE13 controls PASS (75 / 55), b9 2x2000 steps, b26 600, random checks PASS (the base-13 line is skipped if the script is not given a repo root that contains `lean/`).

## 33-34. Agent3ThreeCellBooleanNoGo -- CONFIRMED (repo checks only)
Repo `verify.py` + `independent_check.py` PASS (rank 814/4096 on the 2,252 rec2 tests; 229 seeded cyclic words give 1,792; 288 coboundaries per phase; 4,096 - 1,792 = 2,304 consistent; degree-5 false positive has a physical cyclic counterexample). I did not write a separate 9-bit Boolean rank code (my own GF(2) check covers the 6-bit case of #8, with the same 388).

## 35. F1Semigroup -- CONFIRMED (LEAN-VERIFIED)
Lean 4.19.0, all 18 modules compiled from a scratch copy (`lean -o`, core only; 3 s - 33 s each, no error/warning). `#print axioms` on the endpoints: LangB_iff, reachable_relations_434, recurrence_n, initial_values: {propext, Quot.sound}; minimal_dfa_241_spec, power_closure: + Classical.choice; acc104, nilpotency_histogram: {propext}; no sorryAx, no ofReduceBool/native_decide.
Spec fidelity: Lean `Step` = EXTERIOR.md 2.1 edge relation (q_{t+1} = q mod b + (g ? 1 : (q+r) mod b)). Independent Python (`f1/f1.py`, same spec): 434 reachable relations (with identity), 176 accepting, minimal DFA 241 states / 104 accepting, a(0..9) = 1,0,2,3,6,10,11,28,30,75, recurrence a(n)=a(n-2)+a(n-3)+a(n-4)+a(n-5)+a(n-7)+2a(n-9) holds for 10 <= n <= 30 and fails at n=9 (so "n >= 10" is sharp), power closure Lang(w^k) iff Lang(w): 0 violations in 163,830 (word, k) pairs (words <= 14, k <= 6); necklace counts per p: 95 / 207 / 449 at p = 16 / 18 / 20 (= fc_counts; cf. #17).


(Section numbers above are only labels; the table below is the authoritative one-line-per-note list.)

---

## Suggestions / things to act on
* **S1 (E2 for (10)^8).** Agent11E2P16M4OneLap exhausts the full forward automaton of g=(01)^8 (rotation of (10)^8) modulo 8-fold time rotation: 257,093,987 states, depth 592, 0 hits among the 8 targets. Nobody has run a cycle/SCC test on that graph. An SCC test (or "edges = states-1 style" tree test as in Agent15) would decide E2 for (10)^8 outright: no non-trivial SCC => no exterior for that stream; an SCC => a candidate exterior. OPEN_PROBLEMS.md E2 still lists (10)^8 as capped. (Memory for 257M x 16 B keys is ~4 GB+, so it needs the compact engine of Agent15, not my scratch tools; I did not attempt it.)
* **S2 (fix Agent12RootFactorBasis counts).** Either exclude the all-zero necklace or say it is included; counts then match EXTERIOR.md / fc_counts (95, 207, 449, ..., 2,268 at p=24).
* **S3 (Agent4 note).** State per-prefix run times and that 18/19 prefixes per parity are trivial; the full reproducer needs hours.
* **S4 (Agent15 README).** "8 GB" is not needed: the full 17-stream verify passed under `ulimit -v 4 GB` (about 17 minutes in total).
* **S5 (hygiene).** Delete or share the six copies of `full_scc_controls.cpp`; rename Agent16F2TwoColumnFamily (it is a two-column prefix lemma, not an F2 family); mark Agent3 Scalar/Vector/TimeVary as corollaries of PhaseBeta; mark Agent2 T8/T16/T24 as subsumed by Stationary48 except j=10,34; mark E2P21M9Superperiod8 and Agent11E2P16M8OneLap as slices of AllTemporal/AllTime.
* **S6 (low value).** Agent14ChargeSaturation is a modular-feasibility negative (297/297 residues reachable), useful only to stop people from trying this invariant again.

## Things I did NOT do (so nothing above should be read as covering them)
* Agent15F2FamilyP1724: the 30,618 decided words (full census) not re-run.
* Agent4 prefixes p11 w12 o=1 d=9 and p12 w10 o=1 d=4 (timeouts), and the repo's own driver `run_neutral_wide.py` full mode.
* Agent18's own z3 script (no libz3); replaced by the K1 CaDiCaL window encoding.
* Agent3ThreeCellBooleanNoGo and the Agent3 nested-ansatz repo scripts: repo scripts only for the 9-bit case; my own independent code covers the 6-bit Boolean ranks and the modulus solvability.
* All-k statements of Agent12 (columns, adjacent/triple ones), Agent5 (fiber, front jump), Agent10 G01 family, Agent19: checked at finitely many parameters plus a read of the all-k argument, not formalised.
* E2P21M3/M9 charge notes: Q conservation was checked numerically on 15,876 + 1,772,064 column equations and re-derived by hand; the "unreachable from the root" step uses Q(root)=0 and conservation only (nothing else about the automaton).
* The model equations (column / flux / row-map) were taken from the repo as validated by AUDIT_E/F/K1; I did not re-validate them against big integers here, except in #10 (flux identity on 84k random steps), #14/#15 (real big-integer replays), #23 (witness replay), #32 (24,000 integer cases).

## Table (one line per note)
| Note | Verdict | What I ran / key number |
|---|---|---|
| Agent10F2G01InfiniteFamily | CONFIRMED | own BFS k<=13, table k<=400, repo to 1000 |
| Agent10F2G01LinearDecision | CONFIRMED | states <= 4.6b (bound 8b+1), 1710/5000 accepts |
| Agent10F2G01Mod3 | CONFIRMED | no b = 1 mod 3 accept, b<=3000 |
| Agent10F2G01OddExponentCounterexample | CONFIRMED | 2^17: 14,977 states, depth 3,744, no accept; 2^13/15/19 accept |
| Agent10F2OddBaseG01 | CONFIRMED | no odd accept b<=3000; invariant proof read |
| Agent11E2P16M4AllTime | CONFIRMED | 130,321 rows; 110 cycles; 64 primitive |
| Agent11E2P16M4OneLap | CONFIRMED | repo 5m21s: 257,093,987 states exhausted, 0 hits; root control hits; own 8 targets |
| Agent11E2P16M8AllTime | CONFIRMED | 10,425,680 rows; 552 primitive (728 before axis dedup) |
| Agent11E2P16M8OneLap | CONFIRMED | no block-period-1 primitive m=8 (slice of AllTime) |
| Agent11E2P48M4Charge | CONFIRMED | 16 cycles, 9,216 eqs, Q in {3,6}, Q(root)=0 |
| Agent11E2P48M8OneLap | CONFIRMED | 10,425,680 rows, no block-period-1 primitive |
| Agent12AdjacentOnesFamilyNoGo | CONFIRMED | own r<=12,k<=4; repo r<=50,k<=12 |
| Agent12FifthColumnAllK | CONFIRMED | 0,12,0,72,0,432 (k<=6 own), 93,312 at k=12 (repo) |
| Agent12FourthColumnAllK | CONFIRMED | 12,128,1152,11648,118272,1215488 |
| Agent12RootFactorBasis | **CAVEAT** | 13 words reproduced; counts = EXTERIOR counts + 1 (all-zero necklace); CSV CR/LF only |
| Agent12SixthColumnNoGoAllK | CONFIRMED | 0 for k<=8 (repo), no two consecutive 6th-column edges |
| Agent12ThreeColumnAllK | CONFIRMED | 4^k, k<=8 |
| Agent12TripleOnesRoot | CONFIRMED | only r=4, 4^k |
| Agent14ChargeSaturation | CONFIRMED (low value) | 297/297 residues; repo py + C++ pass |
| Agent14ParityFlip | CONFIRMED | d = 18 / 62 mod 80 for rec0/rec1; none rec2, p12 |
| Agent15F2CappedFollowup | CONFIRMED | 17 streams + 3 controls + mirror/predecessor checks, <= 4 GB |
| Agent15F2FamilyP1724 | **CAVEAT** | 17 capped words re-run; 30,618 decided words not re-run |
| Agent16F2TwoColumnFamily | CONFIRMED (weak, misnamed) | 4 two-edge paths, r=1..5 |
| Agent18P8Rec2Width11 | CONFIRMED (alt. encoding) | CaDiCaL UNSAT at (0,50),(1,55),(2,58),(3,64); SAT H=40 x4; bigint replay x4 |
| Agent2K1Rec2Stationary48 | CONFIRMED | all 48 j; j=10,34: 25,140,401 cand., 4,884,451 survivors |
| Agent2K1Rec2StationaryT8 | CONFIRMED | 2,852 states / 1,624 edges |
| Agent2K1Rec2StationaryT16 | CONFIRMED | 1,317,912 / 1,269,072 |
| Agent2K1Rec2StationaryT24 | CONFIRMED | 10,393,040 / 8,273,248; quotient 3,466,248 / 2,758,832 |
| Agent3CubicParityNoGo | CONFIRMED | rank 232/336, kernel 104 = zero space |
| Agent3FourStepSource | CONFIRMED | S4 = 0 mod 9 in 3,000/3,000; repo 11/90 residues |
| Agent3FullBooleanLocalParity | CONFIRMED | rank 388/512, 12 false positives |
| Agent3PairSourceClosure | CONFIRMED | alphabets 10/20 exactly; repo PASS |
| Agent3PhaseBetaNoGo | CONFIRMED | solvable exactly M in {3,9,11} |
| Agent3QuadraticParityNoGo | CONFIRMED | rank 104/176, kernel 72 = zero space |
| Agent3ScalarCarryModuli | CONFIRMED (corollary) | gcd 99 |
| Agent3SpatialWeightsMod198 | CONFIRMED | exactly {2,9,11} |
| Agent3TimeVaryCarryNoGo | CONFIRMED (corollary) | {3,9,11} |
| Agent3VectorCarryCovariance | CONFIRMED (corollary) | {3,9,11} |
| Agent4NeutralK1P11W12P12W10 | **CAVEAT** | 74/76 prefix runs, all survivors 0; 2 timed out (>10 min) |
| Agent5Gamma0FirstDefectGate | CONFIRMED | phases 3,7,11 no gate; brute force n=7,8,9 |
| Agent5P12BulkCollisionTransfer | CONFIRMED | residues 7,7,4,4,1,1; span 7 |
| Agent5P12CarryExcursionBound | CONFIRMED | own DAG: (9,11,7,0) x3, acyclic, global 11 |
| Agent5P12Connected72Stationary | CONFIRMED | bigint: 818 digits, first diff 180 after 72 steps |
| Agent5P12ExponentialFiber | CONFIRMED | 2^k seeds, k<=8 (own), k<=12 (repo) |
| Agent5P12NonErasingFrontJump | CONFIRMED | diffs exactly at J, n-1-J; k=100 jump 900 (repo) |
| Agent5P12OverflowTransfer | CONFIRMED | non-closing 7,4,1; 24 motifs |
| E2P21M9AllTemporal | CONFIRMED | 22,284,891 rows; 207 primitive; k=2..54 |
| E2P21M9Superperiod8 | CONFIRMED (slice) | 378 primitive for k<=8; 5/6/1 families |
| F1Semigroup | CONFIRMED (Lean) | 18 modules compile; axioms clean; 434 / 241 / 104 / recurrence / power closure re-computed |
| Agent19FiniteCorePumping | CONFIRMED | 24,000 random integer cases; repo controls incl. base 13 |
| Agent3Rec2PerturbationRadius | CONFIRMED | ranks 388/396/398/400 (repo) + own 388 |
| Agent3ThreeCellBooleanNoGo | CONFIRMED (repo only) | rank 814/4096, 1792, 2304 |
| E2P21M3ChargeObstruction | CONFIRMED | 15 cycles Q in {3,6}; 3 k=8 cycles Q=0 |
| E2P21M9ChargeClassification | CONFIRMED | 23 cycles: Q=0 5, unit 12, {3,6} 6; 1,772,064 eqs |
| E2P26M9AllTemporal | CONFIRMED | 22,284,891 rows; 153 primitive; k up to 57 |
