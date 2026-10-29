# AUDIT F: F1/F2-flavoured results on main of /home/claude/p196-algorithm

Auditor: Claude (Sonnet 5.5), 2026-10-28. Repo untouched (git status clean; nothing committed/pulled/edited).
All my files: `/tmp/claude-0/-home-claude/61279d55-9bc5-5e58-836c-ca6225d98f6f/scratchpad/audit/F/` (logs `run*.log`, `indep/` = my independent programs, `lean/` = Lean files).
Resource rules: one process at a time, `nice -n 10`, every run < 3 min. Final Lean clean build: 174 s, peak RSS 3.08 GB (one file at a time). **Disclosure:** during Lean development two early single-file attempts (an in-kernel BFS version) grew to 5.3 GB / 5.2 GB RSS and were OOM-killed by the container (exceeding the 4 GB guideline); they were discarded and the design was changed (data tables + split files).

## 0. Two things to know before reading the verdicts

1. **Naming clash.** All four `Agent9F1*` results (and Agent12ForbiddenNecklaces32) are about the *filter* "F1" of `exterior_census/EXTERIOR.md` section 2.1 (the 18-state first-coordinate NFA, a necessary condition on an overflow word). They are NOT about OPEN_PROBLEMS task **F1 "New formats"** (templates with two bands / quasi-periodic centre + Lean soundness theorem + a control base). Nothing here is a new format, and nothing here moves toward a base-10 certificate.
2. **What "the model" is.** I audited each result against the NFA exactly as specified in EXTERIOR.md 2.1 (`floor((x+h)/10)=g`, `x' = x%10 + (g ? 1 : (x+h)%10)`, `x in 1..18`, `h in {0,1}`); I did not re-audit that this NFA is the correct first column of the actual exterior B-cycle system (that is shared by all results below and is validated elsewhere in the repo by `bx`/`brute_model.py`).

Summary table

| Result | Verdict | Redundant / irrelevant to a Lychrel certificate? |
|---|---|---|
| Agent9F1AllPeriodRecurrence | CONFIRMED (and now LEAN-VERIFIED by me, see sec. 11) | Irrelevant (descriptive count of a necessary filter) |
| Agent9F1MinimalDFA | CONFIRMED (LEAN-VERIFIED by me) | Irrelevant |
| Agent9F1Periods3360 | CONFIRMED WITH CAVEAT (computation fine; mod-9 premise only informally cited; per-weight data p>44 not independently reproduced) | Irrelevant; mildly useful as proof that censuses beyond p~40 are infeasible |
| Agent9F1PowerClosure | CONFIRMED (LEAN-VERIFIED by me) | Irrelevant; it is what justifies the Burnside formula used by Periods3360 |
| Agent12ForbiddenNecklaces32 | CONFIRMED | Redundant: strictly weaker than the exact F1 NFA that is already in the repo (survivors at p=16: 624 vs 95) |
| Agent12RootRunObstruction | CONFIRMED (proof correct) | Marginal; the fixed-word corollary is true but nothing decimal |
| Agent16F2Base4RootClassification | CONFIRMED (proof correct) | Irrelevant (single word, bases 4,5,6 only) |
| Agent16F2ParametricRootFamily | CONFIRMED WITH CAVEAT (proof correct, one step terse; scope = first column only) | Does NOT give an F2 family: my SCC runs show no exterior SCC for the family except b=4 (r=1) and b=16 (r=3), the known power-of-two bases |
| Agent335F2FixedSchedule4148 | CONFIRMED | Mostly redundant (word 1100011000 is a corollary of Agent12RootRunObstruction); negative result on 2 words only |
| Agent336F2FixedSchedules | CONFIRMED | same |
| E1Skipped127NoGo (commit 89a095d1) | CONFIRMED | Redundant for the repo goal (exterior_census/bx already has no 127-bit limit and F1 density 2G<=p already in EXTERIOR.md 2.2c); it only closes the bookkeeping of the old bauto3 pipeline |

No WRONG, NOT REPRODUCED or GAP verdict. No discrepancy found in any number.

---

## 1. Agent9F1AllPeriodRecurrence  - CONFIRMED

Claim: rooted accepted words a(n): a(0..9)=[1,0,2,3,6,10,11,28,30,75]; a(n)=a(n-2)+a(n-3)+a(n-4)+a(n-5)+a(n-7)+2a(n-9) for n>=10; GF (1+z^2+2z^3+3z^4+4z^5+6z^7+16z^9)/(1-z^2-z^3-z^4-z^5-z^7-2z^9); minimal order 10, Hankel det -17378887139328.

(2) Reproduction: `python3 calculation/decimal_frontier/exterior_census/py/f1_rooted_recurrence.py` printed `relation states 434`, `first 10 rooted counts [1, 0, 2, 3, 6, 10, 11, 28, 30, 75]`, `Hankel determinant -17378887139328`, same recurrence and GF. (log `run1.log`)

(3) Independent check (different language/algorithm): `indep/bf.cpp` (C++ DFS over words, per-start-state subset simulation, transition computed from the rule, not from a table) gives a(n) for n<=28: 0,2,3,6,10,11,28,30,75,82,154,231,364,590,883,1470,2210,3611,5548,8846,13891,21826,34546,54087,85660,134318,212187,333598; the recurrence holds for every n=10..28 (0 violations). Exact rational Hankel determinants from those brute-force values: k=1..10: 1,2,-5,30,2112,-23936,-1384960,201642496,11361585152,**-17378887139328**; k=11: 0; k=12: 0. GF numerator/denominator: series expansion equals a(n) for n<=28 and gcd(num,den)=1 (Euclid over Q).

(4) Referee: the proof is "q(T)F=0 on all 434 reachable relations", i.e. a finite identity V_10(r)=V_8(r)+V_7(r)+V_6(r)+V_5(r)+V_3(r)+2V_1(r) for every reachable state r, plus induction. Correct. **I formalized exactly this in Lean** (sec. 11, `F1.recurrence_n`, `F1.initial_values`). Caveats of wording only: (a) "order 10" means the annihilating polynomial q(T) of degree 10 (it has the factor T); as a recurrence it has 9 terms back and is valid only for n>=10 (n=9 fails: RHS=59, a(9)=75). (b) The Hankel/minimality part is not in Lean (I re-derived it with exact fractions, above).

(5) Irrelevant to a certificate; it counts survivors of a necessary filter.

## 2. Agent9F1MinimalDFA  - CONFIRMED

Claim: the language of cyclic words accepted by the F1 NFA has a minimal complete DFA with 241 states (104 accepting) from the 434 reachable Boolean relations; refinement 2,8,46,124,183,221,234,240,241,241.

(2) `python3 .../f1_minimal_dfa.py /tmp/.../f1_241.json` -> `states original 434 minimal 241 minimal accepting 104`, `refinement [2, 8, 46, 124, 183, 221, 234, 240, 241, 241] random direct checks 12000; rooted n<=60 identical`.

(3) Independent: my own BFS + partition refinement (written for the Lean data, `lean/F1Data.lean`/`F1MinData.lean` generators) gave 434 relation states (176 accepting), refinement [2,8,46,124,183,221,234,240,241,241], 241 classes, 104 accepting representatives, and a separating suffix of length <= 8 for every one of the 241*240/2 = 28,920 pairs of representatives.

(4) Referee: minimality needs (i) a congruence (quotient is a DFA for the same language) and (ii) pairwise distinguishability of the 241 classes. The note's "invariants checked on every original state" is (i); "refinement separates all distinct right languages" is (ii) (Moore's algorithm), correct. Lean version (stronger, kernel-checked, no trust in Python): **`F1.minimal_dfa_241`**: there is a DFA on `Fin 241` accepting the language, and every DFA on `Fin n` accepting it has `n >= 241`; `F1.acc104`: 104 accepting; `F1.reachable_relations_434`: exactly 434 pairwise-distinct reachable relation states. "Minimal" = minimal *complete* DFA (the sink counts as one of the 241).

(5) Irrelevant to finding a certificate. The engine does not use a DFA; the F1 words are not the bottleneck.

## 3. Agent9F1Periods3360  - CONFIRMED WITH CAVEAT

Claim: exact F1 necklace counts p=33..60 (`data/f1_b10_p33_60.csv`), controls p36=351150, p40=1943815; Burnside formula; charge-mod-9 count of carry words e: 2^p (p odd), (2^p+2)/3 (p=2,4 mod 6), (2^p+8)/9 (6|p).

(2) `python3 .../f1_semigroup_count.py 10 60 out.json`: `relation states 434 max shortest depth 17`; its p=33..60 rows equal the committed CSV in all 28 rows (0 mismatches), p36=351150, p40=1943815, p60=11425283484 (primitive 11425255386). `c++ ... f1_necklace_check.cpp` (their FKM program) for p<=44: all 44 lines agree with the Burnside JSON on total, primitive and every weight G (0 mismatches). `f1_charge_mod9_count.py 60` passes its asserts (e.g. p=60, m=9, 128102389400760776).

(3) Independent: (a) my brute-force DFS (`indep/bf.cpp`) necklace/primitive counts for all p<=28 equal the repo's, and equal the older enumerator `fc_counts_b10.txt` for p<=28 (p<=40 in fc_counts agree with the new data). (b) **All 28 CSV rows p=33..60 recomputed from the Lean-proved recurrence a(n) (sec. 1) by Burnside/Moebius** (N(p)=1/p sum phi(p/d)a(d), P(p)=1/p sum mu(p/d)a(d)): 0 mismatches (e.g. a(60)=685516160231, N(60)=11425283484). That is an independent route to every number in the CSV.

(4) Referee for the PAPER PROOF (mod-9 count): the premise is "Existing mod-9 charge closure", uncited in the note. It is Corollary 9a of `calculation/decimal_frontier/theory/THEORY.md`: gcd(2^P-1, b-1) | E, E=sum e_t 2^{P-1-t}. Given that, the count is just #{E in [0,2^P-1] : m | E} with m=gcd(2^P-1,9) in {1,3,9}: = ceil(2^P/m); 2^P = 1 mod m gives (2^P-1)/m+1 = (2^P+m-1)/m. That reproduces the three formulas exactly. Correct. Caveats: premise not cited in the result note; the note's own "not claimed" (filter on e, not on g) is right; the count is trivial and already implicit in THEORY.md consequence (1).

Caveat on computation: per-weight (byG) and primitive-by-weight numbers for p=45..60 are produced by two engines of the same author (f1_semigroup_count / f1_power_closure agree) and the totals are confirmed by my recurrence route, but I did not independently reproduce the per-weight splits beyond p<=44.

(5) Irrelevant to a certificate. Useful only as a sizing fact: F1 survivors are 1.9e6 at p=40 and 1.1e10 at p=60, so a per-word census past p~40 is not realistic.

## 4. Agent9F1PowerClosure  - CONFIRMED

Claim: w passes F1 iff w^k does, for every k>=1; 434 relations, 176 with a diagonal entry, 258 nilpotent with R^5=0, nilpotency histogram 1:1, 2:251, 3:4, 4:1, 5:1; Burnside/Moebius divisor formulas.

(2) `python3 .../f1_power_closure.py 60` -> `states 434 self-loop 176 nilpotent 258 nilpotency-index [(1, 1), (2, 251), (3, 4), (4, 1), (5, 1)]` and `all p<=60 weights and primitive counts equal independent Burnside results`. (Note: it must be run without `python3 -I`, because it imports the sibling `f1_semigroup_count`; the stated command works.) Importantly the "independent" engine `f1_semigroup_count.count` tests closedness of R^k directly (`power_closed`) without assuming power closure, so the p<=60 agreement is a genuine computational check of the claim.

(3)/(4) Referee: proof = finite classification + (diag => all powers have diag; R^5=0 and diag-free => no power has a diagonal, since a diagonal in R^k would give one in R^{5k}=0). Correct, and the Burnside formula needs exactly this closure (the rotation-fixed words of period p/k are u^k, accepted iff u is). **Lean-verified by me**: `F1.power_closure : forall w k, 1 <= k -> (Lang (w^k) <-> Lang w)` and `F1.nilpotency_histogram : [hist 1,...,hist 6] = [1,251,4,1,1,0]`, `F1.diag_free_count = 258`, `F1.acc176`.

(5) Irrelevant to a certificate (structural fact about the filter).

## 5. Agent12ForbiddenNecklaces32  - CONFIRMED (redundant)

Claim: cyclic factors 1101 and 11001 impossible for a closed first-column trajectory; counts of density-admissible (2G<=p) necklaces removed, p<=32.

(2) `python3 .../agent12_forbidden_necklaces.py --pmax 32 --brute-upto 16 --csv ...` -> `PASS`; the produced CSV is identical to the committed `agent12_forbidden_necklaces_32.csv` (modulo CRLF). Spot values reproduced: p=16: 2463/1839/624; p=24: 405986/362755/43231; p=32: 76501983/73118415/3383568, primitive p=32: 76499520/73116576/3382944.

(3) Independent: `indep/forb.cpp` enumerates all binary necklaces of length p<=28 (min-rotation, period), applies 2G<=p, tests cyclic factors by rotation: all six columns equal the CSV for every p<=28 (0 mismatches). `indep/f1_vs_forb.py`: of the 24,154 F1-accepted rooted words with p<=20 (generated by my own NFA simulation), **none** contains a cyclic 1101 or 11001 and none violates 2G<=p, i.e. exact F1 is inside the surviving set (and much smaller).

(4) Referee of the PAPER PROOF: rotation to the factor start is legitimate because the first-column recursion is time-translation invariant and the rotated start has g=1 so x>=b-1>=1 and x<=2b-2; the obstruction is Agent12RootRunObstruction (sec. 6), which I checked. Correct. One more observation: the argument is *exactly* an argument about closed walks of the F1 NFA, so the exact F1 automaton already contains it.

(5) **Redundant**: the exact F1 NFA (EXTERIOR.md; counts to p=40 in `fc_counts_b10.txt`, to p=60 in Periods3360) is strictly stronger: at p=16 there are 95 F1 survivors vs 624 survivors of this prefilter; at p=24 2268 vs 43231. The result itself says "prefilter, not a census".

## 6. Agent12RootRunObstruction  - CONFIRMED

Claim: overflow word beginning 11 0^r 1 (r>=1) has no closed canonical-root first-column trajectory for any base b > 2^(r+1); corollary: fixed word 1100011000 has no reachable exterior SCC for any b>=17; sharpness at b=16; counts b=9:4, b=16:4, b>=17..100: 0, base-13 1010010000: 8.

(2) `python3 .../agent12_root_obstruction.py --max-base 100` -> base 9: 4, 13: 4, 16: 4 (witness (15,16,1,3,7,15,16,1,3,7)), 17/32/49/100: 0, base 13 word 1010010000: 8, PASS.

(3) Independent: my C++ position automaton `indep/pos.cpp` (written from the EXTERIOR.md description, not from bauto3.cpp) gives for 1100011000 exactly 1 state / 0 edges for every b=32..48 and matches bauto3 on three controls (below).

(4) Line-by-line referee: x_0 in [b-1,2b-2] from g_0=1; g_1=1 forces x_1=x_0%b+1>=b-1, so x_0 in {b-1, 2b-2}, giving (b-1,b,1) or (2b-2,b-1,b); g_2=0 requires x_2<=b-1, killing the second; zero steps give x'=2x+h, so x_{r+2}<=2^{r+1}-1 (induction 2(2^{j+1}-1)+1=2^{j+2}-1); the next 1 needs x+h>=b so b<=2^{r+1}. Correct; I re-derived every case. The corollary holds with r=3: b>=17>16. (The note says "fixed, unrotated"; in fact it holds for every rotation, because the cyclic factor 110001 is present in each and the NFA is time-invariant.)

(5) Marginal: a clean small lemma; useful only as the reason why the 1100011000 scans in sec. 9 are trivial.

## 7. Agent16F2Base4RootClassification  - CONFIRMED

Claim: for g=101100 (any rotation) a closed first-column path exists iff b in {4,5,6}, exactly four carry assignments each; trajectories (4,1,3,4,1,2), (6,2,4,5,1,3), (7,2,5,6,1,3).

(2) `python3 .../agent16_base4_f1.py` -> `PASS: all six rotations, every base 2..200, exactly b=4,5,6 have four paths` (2.7 s).

(4) Referee (all steps re-derived): g_2=g_3=1 -> x_3 in {b-1,b}; b-1 would give x_4=b contradicting g_4=0, so x_3=b, x_2%b=b-1, and x_2<=2b-2 gives x_2=b-1, c_2=1, x_4=1; g_0=1,g_1=0 -> x_0>=b, x_1=x_0-b+1; zero steps: x_2=2x_1+c_1, x_5=2+c_4, x_0=4+2c_4+c_5; elimination gives 3b=11+4c_4+2c_5+c_1 in [11,18], so b in {4,5,6} with the stated unique carry triples; free bits c_0, c_3 (coefficients >= b) give 4. All correct. The sufficiency/rotation paragraph is correct (all coefficients positive).

(5) Irrelevant: a single word, first column only, and the answer is *bounded* bases {4,5,6}, the opposite of a family.

## 8. Agent16F2ParametricRootFamily  - CONFIRMED WITH CAVEAT

Claim: g_r = 1 0^r 11 0^(r+1) has a closed first-column path iff 4<=b<=6 (r=1) or 2^(r+1)<=b<=2^(r+2)-3 (r>=2), exactly four carry assignments.

(2) `python3 .../agent16_param_f1.py --output <scratch>`: COMPLETE, r=1..7, all b=2..2^(r+2)+3, all 2r+4 rotations (1030 (r,b) records, all agree), 10.8 s.

(3) Independent: `indep/param_indep.py` brute-forces x_0 and ALL 2^p carry vectors for r=1,2,3 and every b=2..2^(r+2)+3: 62 cases, 0 mismatches with the closed form.

(4) Line-by-line referee: forced middle (x_{r+1}=b-1, c_{r+1}=1, x_{r+2}=b, x_{r+3}=1) correct; first block x_{r+1}=a x_1+U (a=2^r), second block x_p=x_0=2a+V (V has r+1 bits); elimination (a+1)b=2a^2+aV+a+1+U, i.e. b=2a+V-1+(U-V+2)/(a+1), correct; U-V+2 in [3-2a, a+1], multiples of a+1: a+1, 0, -(a+1) (the last only if a>=4), correct; the three cases give b=2a; b=2a+u+1 (u<a); b=3a+u+1 (u<=a-4), union [2a,4a-3] for a>=4 and {4,5,6} for a=2, disjoint, so four assignments (c_0 and c_{r+2} free) per admissible b. Correct. Caveat (minor gap, easily closed): sufficiency says "each block doubles nonnegative coefficients with bits, terminating at b-1 or x_0<=2b-2"; what is really needed is x_t+c_t<=b-1 at every zero step, which in the last step reads ceil(x_0/2)<=b-1, i.e. x_0<=2b-2, true since x_0<=b+2<=2b-2 for b>=4. The statement is right; the sentence is terse.

(5) **Does not give an F2 family.** The note says it gives "arbitrarily large bases with a first-coordinate closure, not an exterior SCC". I checked what happens next with my independent position automaton `indep/pos.cpp` (validated against bauto3, sec. 9): r=1 (101100): b=4 has an exterior graph with 957 states and 4 nontrivial SCCs (the known base-4 certificate base), b=5,6: 5 states, no SCC; r=2 (10011000), b=8..13: at most 79 states, **no** SCC; r=3 (1000110000), b=15..30: b=16 has 111,461 states and 4 SCCs (bauto3 gives the same numbers), every other base no SCC; r=4 (100001100000), all b=31..62: max 11,569 states, no SCC; r=5 sampled b=63,64,65,100,125,126: no SCC. So over r<=4 the only bases with an exterior SCC are the known powers of two 4 and 16. First-column closure is far too weak to indicate a parametric certificate. (Data in `indep/fam_scc.txt`, `fam_r4_all.txt`.)

## 9. Agent335F2FixedSchedule4148 and Agent336F2FixedSchedules  - CONFIRMED

Claims: fixed period-10 overflow words 1100011000 and 1010010000 have no reachable nontrivial exterior SCC in bases 41..48 (335) and 32..40 (336) at cap 3,000,000; state counts: 1100011000: 1 state, 0 edges everywhere; 1010010000: 169,285,133,9,9,9,9,9 (41..48) and 53,9,9,41,9,9,9,9,9 (32..40); controls base 9 (956310 states, 7 SCCs, depth-61 period-4 SCC) and base 13 (250302 states, 5 SCCs, depth-55 uniform SCC).

(2) `bash calculation/decimal_frontier/lattice_formats/code/f2_fixed_schedule_41_48.sh <scratch>/f2_4148`: all numbers above reproduced (7 s), including controls `states=956310 edges=1005301 nontrivial_sccs=7` with the `size=4 cyclen=4 depth=61` SCC and `states=250302 edges=254201 nontrivial_sccs=5` with the `size=1 cyclen=1 depth=55` SCC. 336's command (bauto3, bases 32..40, both words, cap 3M, `-maxscc 0`): reproduced exactly (53,9,9,41,9,9,9,9,9 and 1,...,1), 0 nontrivial SCCs.

(3) Independent: `indep/pos.cpp` re-implements the position automaton from EXTERIOR.md section 1 (cut state (L,H,Y), x_0>=1 only at the first position, closure x_p=x_0, Tarjan SCC) in a different data layout. It reproduces bauto3 on: base 4 / 101100 (957 states, 1012 edges, 4 SCCs), base 9 / 1100011000 (956310, 1005301, 7), base 13 / 1010010000 (250302, 254201, 5), and gives for **both words, every base 32..48**: states 1 (word 1) and 53,9,9,41,9,9,9,9,9,169,285,133,9,9,9,9,9 (word 2), 0 nontrivial SCCs. So the engine is not the only witness.

(4)/(5) Scope is honest ("these two fixed words"). Redundancy: for 1100011000 and every b>=17 the result is the corollary of Agent12RootRunObstruction (cyclic factor 110001, r=3), no computation needed. The word 1010010000 dies equally fast (graphs are trees with <=285 states) but no proof is given. Neither says anything about other schedules, parametric families (cf. sec. 8), or base 10.

## 10. E1Skipped127NoGo (commit 89a095d1, `check_e1_127_skip.py`)  - CONFIRMED

Claim: the 560 overflow necklaces (p=22: 2; p=23: 13; p=24: 545; none for p<=21) skipped by bauto3's `2p+4G>127` key guard all have 2G>p and so no closed F1 walk; hence no reachable exterior.

(2) `python3 .../check_e1_127_skip.py`: `PASS: potential inequalities on every admissible base-10 edge`, `PASS: base-9/base-13/base-10 position-zero positive controls`, `PASS: 560/560 old-skipped canonical necklaces have no position-zero cycle`, `Counts: {22: 2, 23: 13, 24: 545}`.

(3) Independent: Burnside count of necklaces of length p<=24 with 2p+4G>127 (ydig=4 for b=10 as in bauto3.cpp): {22: 2, 23: 13, 24: 545}, total 560. The potential psi (EXTERIOR.md 2.2c: q=1:3, 2:2, 3:2, 4-9:1, 10:2, 11-18:0) checked by my own code on all 36 edges: psi(q')-psi(q)>=2g-1 everywhere, 0 violations.

(4) Referee: summing psi(q')-psi(q)>=2g-1 around a closed walk gives 0>=2G-p; skipped words have G>(127-2p)/4, which exceeds p/2 for all p<=31, so every skipped word violates it; a reachable SCC of the position automaton needs an edge out of the canonical root, i.e. a closed position-0 walk. Correct, at any spatial period and state cap.

(5) Redundant for the repository goal: `exterior_census` (bx, no key truncation) already decides all p<=32 and states the same density filter. The commit only shows that the "E1: remove the 127-bit key and rerun p<=24" step is unnecessary for these 560 words; the rest of E1 (p=25..32 in the lattice pipeline) is untouched.

---

## 11. FORMALIZATION: Lean 4 (v4.19.0, core only), `lean/` directory

Files (all in `/tmp/claude-0/-home-claude/61279d55-9bc5-5e58-836c-ca6225d98f6f/scratchpad/audit/F/lean/`, build script `build.sh`, build log `../lean_build.log`):

| file | content |
|---|---|
| `F1Core.lean` | specification `Step/Reach/Lang` of the F1 NFA; bit-mask relation automaton; theorem `F1.LangB_iff : LangB w = true <-> Lang w` (relation automaton computes exactly the walk language) |
| `F1Data.lean`, `F1MinData.lean` | certificate data (434 states packed, transition tables, BFS parents, 241 class representatives, class map, 28,920 separating words) generated by my own Python; **everything is re-checked in the kernel**, no trust in the data |
| `F1Tables.lean`, `F1Distinct.lean` | `S_is_reachable_set`, `reachable_relations_434` (exactly 434 reachable relation states, pairwise distinct) |
| `F1MinDefs/F1Cls/F1Sep1-4/F1MinDFA.lean` | `minimal_dfa_241`, `minimal_dfa_241_spec`, `acc104`, `acc176` |
| `F1Recurrence.lean` | `recurrence`, `recurrence_n`, `initial_values`, `nodup_allWords`, `a_eq_count` |
| `F1PowerDefs/F1PowerChk1-2/F1Power/F1PowerHist.lean` | `power_closure`, `nilpotency_histogram`, `diag_free_count` |
| `F1Axioms.lean` | `#print axioms`, sanity examples |

Main statements (as printed by Lean):
* `F1.reachable_relations_434 : nS = 434 /\ (forall w, exists i < nS, run initRel w = Sget i) /\ (forall i < nS, exists w, run initRel w = Sget i) /\ (forall i j < nS, Sget i = Sget j -> i = j)`
* `F1.minimal_dfa_241_spec : (exists D : DFA (Fin 241), forall w, D.accepts w = true <-> Lang w) /\ forall n (D : DFA (Fin n)), (forall w, D.accepts w = true <-> Lang w) -> 241 <= n`  (also `acc104`: the 241 representatives contain exactly 104 accepting ones)
* `F1.recurrence_n : forall n, 10 <= n -> a n = a (n-2) + a (n-3) + a (n-4) + a (n-5) + a (n-7) + 2 * a (n-9)`, `F1.initial_values : [a 0,...,a 9] = [1,0,2,3,6,10,11,28,30,75]`, where `a n = ((allWords n).filter LangB).length` and `allWords n` is the nodup list of all 2^n words (`nodup_allWords`, `length_allWords`, `mem_allWords`)
* `F1.power_closure : forall w k, 1 <= k -> (Lang (pow w k) <-> Lang w)`; `F1.nilpotency_histogram : [hist 1,..,hist 6] = [1,251,4,1,1,0]`; `F1.diag_free_count = 258`.

Compile output (clean rebuild of all 18 files, then `cd /home/claude/p196-algorithm/lean && lake env lean .../F1Axioms.lean`), `rc=0 wall=174s user=163s maxrss=3082MB`:
```
'F1.LangB_iff' depends on axioms: [propext, Quot.sound]
'F1.reachable_relations_434' depends on axioms: [propext, Quot.sound]
'F1.minimal_dfa_241' depends on axioms: [propext, Classical.choice, Quot.sound]
'F1.minimal_dfa_241_spec' depends on axioms: [propext, Classical.choice, Quot.sound]
'F1.acc104' depends on axioms: [propext]
'F1.recurrence' / recurrence_n / initial_values / nodup_allWords: [propext, Quot.sound]
'F1.power_closure' depends on axioms: [propext, Classical.choice, Quot.sound]
'F1.nilpotency_histogram' depends on axioms: [propext]
```
No `sorry`, `admit`, `native_decide`, custom axiom, `unsafe`, `implemented_by`, `#eval` (grep clean). Only `decide +kernel` on Bool checkers over compact packed data (pattern of `LatticeBand/Base9.lean`), plus ordinary proofs. Per-file peaks: F1Tables 2.4 GB, F1Distinct 3.1 GB, F1PowerHist 2.9 GB, the rest <= 1.7 GB; 12-28 s each.

What the Lean files do NOT cover (honest list): (i) that the F1 NFA is the right first column of the exterior system (specification taken from EXTERIOR.md 2.1); (ii) the Hankel-determinant minimality of the recurrence order; (iii) the Burnside/Moebius necklace formulas and the CSV numbers for p=33..60 (checked numerically only); (iv) the charge-mod-9 count; (v) nothing about Agent12/16/335/336/E1 (those are not finite-combinatorics of this kind; their proofs I checked by hand and by independent code). Budget note for repo use: the files are split because the kernel keeps all caches per file (single-file version needed 5.2 GB and was OOM-killed); the repo rule allows 8 GB/20 min per file, so merging into `lean/P196/<Name>/` with a registry fragment would need one file per heavy check as done here (all <= 3.1 GB). I did not add anything to the repo.

## 12. What I did not do

* Did not re-run the exterior census or any run longer than 3 minutes; did not replay any certificate with big integers (none of these results claims one).
* Did not independently verify per-weight splits (byG) for p=45..60 (only totals via recurrence+Burnside).
* Did not Lean-check the Agent12/Agent16/E1 paper proofs (verified by hand line by line and by independent brute force; sec. 5-10).
* Did not touch git or any tracked file.

## 13. Bottom line for the project

All eleven items are correct and reproducible; none moves toward a base-10 Lychrel certificate. Eight of the eleven describe the weak *first-coordinate* necessary filter (counts, DFA, recurrence, closure) or small fixed-word F2 negatives; three are redundant with earlier repo content (Agent12ForbiddenNecklaces32, Agent335/336 on word 1100011000, E1Skipped127NoGo). The one potentially misleading item is the Agent16 "parametric family": first-column closure does not extend to an exterior SCC (only b=4 and b=16 for r<=4), so it should not be read as progress on F2. Suggested hygiene: the `F1` label in these result names collides with OPEN_PROBLEMS task F1.
