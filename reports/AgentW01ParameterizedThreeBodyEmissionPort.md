# W01: base-10 three-body emission port commutes with third-packet spatial delay, while its interior does not

**COMPUTED** (finite only): Four explicit triple-packet geometries, 32 genuinely evolved 24,000-digit decimal integers (8 masks per geometry), every ordinary reverse-and-add step through t=20,000. No base-10 Lychrel certificate, infinite-time implication, Lean verification or 196 claim.

## Construction and observables

This builds on W01's committed three-body shield result (`AgentW01ThreeBodyScatteringShield`). Use the same 39-position p8 root and 20-position periodic coefficient bulk and mirrored digit lifting, with 24,000 decimal digits and three disjoint 50-pair perturbations. Keep X at `j=6000..6049` with replacement `(7j+11)%19`, Y at `j=8000..8049` with `(3(j-8000)+10)%19`, and **move the Z pulse** to `z=10000+80k`, `k∈{-1,0,1,2}`, with the identical position-relative coefficient replacement `(5(j-z)+3)%19`. Thus Z may start at `9920,10000,10080,10160`, while its local coefficient content and the entrance phase stay fixed. For each z, evolve eight integer seeds corresponding to all subsets of X, Y, Z. Each step all eight current lengths agree, and each has an odd folded coefficient among the first 39 mirrored pairs: this is a direct non-palindromicity witness for all 32 finite trajectories, independent of the scattering comparison.

As defined in the companion result, write the third-order inclusion-exclusion digit residual `R3=U_YZ|X-U_YZ` for each individual **physical low and high decimal digit** separately. Let `f_z(t)` be its first nonzero folded coefficient index; define the `61`-cell two-ended emission tile to be its low/high signed digit differences on offsets `r=-20..40` about that front. The signed residual can be negative; its physical digit tracks are compared exactly, not modulo10 or after folding. Let `s_z(t)` be the first position where either low or high digit of the conditioned Y–Z interaction `U_YZ|X` is nonzero, and `g_z=s_z-f_z` its shield gap. The fully algebraic inclusion-exclusion identity itself is a trivial **PAPER PROOF**; every dynamical equality below is strictly **COMPUTED**.

## Spacetime covariance of the nonlinear emission port

For the four tested cases, the *first genuine third-order interaction* is **exactly**

`(t_birth,f_birth)=(4354+88k,9014+60k)`.

For each `k≠0` and every integer reference time `5300≤t≤min(20000,20000-88k)` the following two-ended port relations are exact, with zero mismatches:

- `f_(10000+80k)(t+88k)=f_10000(t)+60k`;
- both physical signed digit residuals at the 61 offsets `-20..40` match *exactly* under this time/position displacement.

This checks **43,839 complete aligned time rows**, including **5,348,358 exact low/high digit equalities** and 43,839 front equalities. Per variant, the row counts are k=-1:14,701; k=+1:14,613; k=+2:14,525. Changing the predicted spatial displacement by one cell or the time delay by one step fails a fixed control at reference t6000.

Independently, for each of the four cases, every `5300≤t≤19956` satisfies the **stronger half-macroperiod** `f_z(t+44)=f_z(t)-10` and the entire 61-cell two-ended signed digit tile repeats: **58,628 exact 44-step rows**, **7,152,616 exact signed digit equalities**. The 22-step translation is not an identical full digit-tile recurrence (verified on the baseline data). Thus the outgoing packet is a phase-44 object within the period-88 ambient lattice.

For **all** four cases and **every integer** `5300≤t≤20000`, the conditioned Y–Z physical-digit interaction remains **zero in the whole outgoing 61-cell tile**, and `g_z(t)≥41`: **58,804 complete shielded time rows**. Moreover the third-order front is at the fixed **same-time** displacement `f_z(t)=f_XY(t)+2000+80k` from the old two-body X–Y daughter front. On both physical decimal-digit tracks, its first 56 cells `r=-20..35` are exact **negative copies** of that X–Y residual, with a nonzero discrepancy in the trailing five-cell seam `r=36..40`, for **every one** of these 58,804 rows (**6,586,048 independent signed-digit comparisons**). This is a genuine finite four-geometry antipodal emitted glider with a local end defect.

For the baseline geometry, the resulting **10 signed seam entries** (five low and five high) have **exactly 44 distinct states**, one per phase, with **period 44** for all tested t5300..20000; they do not have period22. This makes a finite 44-state *observed port alphabet* a plausible input for future exact carry-gate synthesis. Its 44 observed states are **not** an autonomous verified transition system; their generation still depends on the unproven infinite-time environment.

Crucially, the **interior is not covariant** under the same spacetime shift. Every one of the 43,839 aligned comparisons of the shield gap `g_z` to `g_10000` has different values, even while the entire two-ended 61-cell outgoing tile agrees. Final gaps at t20k are `1115, 1011, 1050, 1077` respectively for the four z values. Thus a finite **universal emission port can coexist with four different, growing nonperiodic inner states**. This separation is a constructive candidate for a decoupled carry-gate certificate format, rather than an assertion that all 32 integer trajectories are globally phase-equivalent.

## Reproduction and controls

Everything needed is committed with this result under `calculation/new_structures/agent-W01/`, using `w01_screened_corridor_z.cpp`, `w01_triple_param_gmp.cpp`, `param_verify.py`, `param_run.sh`, and a four-row `param_expected.csv`. Run exactly, from the repository root:

`bash calculation/new_structures/agent-W01/param_run.sh`

This builds a C++17 literal decimal digit-vector implementation and evolves all 32 true orbits for 20,000 steps, with checks for equal lengths and odd-pair nonpalindromicity witnesses at EVERY step; it emits complete source traces in a temporary directory, not a hidden cache. The Python verifier independently checks every stated signed-digit/front relation, all time windows, the local seam phase44, the sharp birth events and mutation controls, and uses the previously published `w01_scatter_phase.cpp` to replay the reference X–Y daughter rather than assuming a stored source signal.

A second, independently implemented GNU GMP integer engine, `w01_triple_param_gmp.cpp`, creates the **new `z=10080` eight decimal integers** as decimal strings and adds literal reversed big integers through step5600. Without using the digit-vector routine, the CSVs or the Python checker, it confirms the expected t4442/j9074 first third-order event, the last defective screened tile t4955, and **301** completely screened 61-cell low/high two-sided tiles t5300..5600 (36,722 signed cancellations) and **301** antipodal translated 56-cell windows (33,712 signed equalities). The original z10000 eight-integer GMP check to t6000 is separately included in the previous companion result. No precomputed multi-megabyte outputs are committed: each is regenerated reproducibly. Requires a C++17 compiler, GMP development headers/libs and Python3.

## What's still missing

This is **not** a periodic centre, a proof about arbitrary Z or arbitrary initial band lengths, a closed finite carry-gate invariant, or a self-regenerating collision. The emission port has an observed phase44 but is supported by a growing, nonperiodic interior, and its observable finite stability to t20k is not an induction to infinity. To close the certificate, one must verify that the five-cell seam and its incoming carry gates form an **autonomous** 44-phase transducer at arbitrary shield depth and that a repeatable source/return mechanism keeps generating the packets. Those assertions are explicitly **UNDECIDED**.
