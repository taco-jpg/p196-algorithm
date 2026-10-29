# AUDIT_N16-N30 — agent-V08 red team, 2026-10-28

Verdict: **ISSUE: N19 full-width indexing defect in a PAPER PROOF statement; no new decimal all-time certificate.** “Y” below means only the cited independent V08 subcheck, not that the full 20k/100k reproducer was rerun. N means not rerun by V08. The existing AUDIT_Nseries report separately covers 103 N-series notes, including the earlier N16–N30 finite tests. Local GitHub checkout failed DNS resolution; all V08 checks were implemented independently in Python, without GMP. The repository-wide tools/verify.py --changed could not run.

## Inventory

| Result(s) | Claimed scope | Label | V08 reproduction Y/N | Defects / limits |
|---|---|---|---|---|
| N16: DecimalDefect22Clock, DecimalProtectedExterior20k, DecimalRegenerationPulse | period-22 front and 264-step repair | COMPUTED | N | One-shot gain, then continued erosion; no renewal |
| N17: DecimalWake44, NonstationaryWakePump, WakeAttractor361 | inserted bulk/wake covariance | COMPUTED; PAPER PROOF conditional | N | Agreement eventually breaks; no time-indefinite covariance |
| N18: EightyEightRenormalization, GuardedDecimalOrbit, ThreeRenewals, TwoRenewals | 88-step finite renewal | COMPUTED | N | fourth renewal not established |
| N19: AllCounterPumping20k, CounterSynchronizedSixCycle, GrowingJunction20k, OptimizedDePumping20k, UniversalTwoCounter | two-counter family; central uniform six-cycle | COMPUTED; PAPER PROOF | Y for N19 centre lemma only; N full replay | ISSUE full-width k−1 statement, corrected below |
| N20: AffineSheets | conditional finite-checkable all-time format | PAPER PROOF | N | no decimal closed-cycle instance; no Lean check |
| N21: Decimal20kMixedPhaseTrain, MixedPhaseCarryCollision, OrderedPacketScattering, P12TransducedPacketTrain | finite packet dynamics | COMPUTED; PAPER PROOF local | N | collision finite, no repair cycle |
| N22: Rec2MovingCentre20000, Rec2OutwardDrift128 | finite rec2/m48 drift | COMPUTED | N | finite failure, no persistent centre |
| N23: Decimal100kUniformBand, Decimal20kProtectedBands, DecimalPartialRadixCorridor, ParametricDecimal20kBand, SparsePolynomialDigitBands | 9-band for fixed horizon, uniform in length | COMPUTED | N | required gap scales with horizon; no infinite fixed seed |
| N24: DecimalCarryClockLatch, HybridNeutralLatticeFront, P8HybridShortSeed | conditional 0011 upper carry latch | PAPER PROOF; COMPUTED | Y: 684 true-integer one-step edges; N long replay | no perpetual physical carry-source proof |
| N25: CarryFreeSplicing, FirewallRecharge | symmetric zero-gap splicing | COMPUTED; PAPER PROOF local | Y: 60 true-integer transitions; N long replay | protected gaps still contract |
| N26: CentralSeamRepair, DecimalP8Shield, TwoSectorFront | short-core finite delay | COMPUTED | N | no renewable interface |
| N27: AntiphaseFrontContract, CentralOverflowFront, DecimalNestedRepairTransient | arbitrary-base one-step saturated-centre law | PAPER PROOF; COMPUTED | Y: 130032 local cases; N long replay | temporal antiphase lock only observed finitely |
| N28: CarryGaugeFunnel, FourStepParticleEraser, LongPump20000, MovingJointPump, SlidingCuts | conditional multi-slot pump | PAPER PROOF; COMPUTED | N | 232-step contract, no closed all-time cycle |
| N29: AffinePackets, GeometricMiner, GeometricWords | finite polynomial template checker, five real decimal edges | PAPER PROOF; COMPUTED | Y: 35 genuine integer edges; N long replay | early off-by-one was already corrected; no closing cycle |
| N30: AdversarialCentreCone, PeriodicBuffer20000, TaintEnvelope | arbitrary-centre finite safe mask family | COMPUTED; PAPER PROOF conditional | N | no safe mask lasso |

## ISSUE N19: literal all-width shielding statement is false

The PAPER PROOF section of reports/AgentN19CounterSynchronizedSixCycle.md states that a symmetric central block of **k equal pair coefficients** maps to a central block of **at least k−1** successor coefficients regardless of carries and overflow. Read as the full pairword length, this is incorrect: a genuine integer N=1,984,090 has pairword [1,18,8,8,8,18,1]; its decimal reverse-and-add successor 2,888,981 has pairword [3,16,17,16,17,16,3]. The centered 8-run of length three becomes a 16-run of length one, not two, with gamma=0.

In fact for each k=3,...,20 the realizable symmetric pairword [1,18] ++ 8^k ++ [18,1] maps to a centered 16-run of EXACTLY k−2 with gamma=0. V08 replays the actual integers independently, not just abstract pairword updates. This is an off-by-one **per side** when k is counted in full coefficients. It does not refute the separate N19 script fold_check.py: that script chooses k as the number of *folded halfword* cells and its k−1 check is consistent.

**Corrected all-length PAPER PROOF lemma, sharp:** Let a genuine decimal integer have a symmetric full pairword with a centered x^k run, k>=3, x in {2,4,8,10,14,16}. If its decimal reverse-and-add successor has overflow gamma in {0,1}, the successor has a centered run of at least k−2+gamma coefficients equal to y, where y is the six-cycle successor (2->4->8->16->14->10->2).

Proof: carrying through a constant x block reaches its fixed carry c*=0 for x<10 or c*=1 for x>=10 after at most the first cell. The remaining k−1 normalized digits are therefore all d=(x+c*) mod 10, with 2d=y. With gamma=0, the mirrored overlap of this stable region contains the central k−2 positions. With gamma=1, the reflection axis shifts by a half-cell, giving at least k−1 central matching positions. No assumption on the exterior or initial carry is used. The gamma=0 bound is attained by the explicit family above. The corresponding folded half-width still loses at most one cell per step, which appears to be N19's intended quantity.

V08 independently checked the repaired bound on 10,000 random **actual decimal integers**, with all six x species and variable exterior lengths; zero violations. This correction is a necessary one-step shielding lemma for a mathematically sound central renewal balance, but it offers no nondepleting mechanism and does not establish a decimal Lychrel number.

## Independent reproduction scope

All tests were independent of the repository implementation: Python ordinary integers and explicit base-10 digit reversals. The checks are N19 (18 sharp counterexamples plus 10,000 randomized repaired-bound cases), N24 (684 actual-integer two-column projected edges), N25 (60 spliced integer transitions), N27 (130,032 centre-normalization configurations in bases 2..8, q=3..6 and prefix length 0..3, both carries and overflow choices), N29 (35 real-integer edges and 42 nonpalindrome checks at q=3,4,5,8,12,37,100). The universal parametric proofs, all 20k/100k runs, and full reproduction scripts were NOT independently rerun in this pass.

One-sentence all-time gap addressed: **the corrected k−2+gamma shielding lemma supplies a sound universally quantified centre-front bound required by any proposed all-time renewal invariant, whereas the published full-width k−1 wording would make such an induction invalid.**

No ALERT: no symbolic-length decimal template cycle T(m)→T(m') with m'>m was found.
