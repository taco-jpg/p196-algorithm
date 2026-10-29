# AUDIT_alltime_claims: quantified decimal claims versus actual all-time safety (agent-V09)

**Verdict: PAPER PROOF of a new, physically realizable all-length counterexample to a potential W30 arbitrary-overflow safety upgrade; NO base-10 Lychrel certificate.** This is a red-team *limitation theorem*, not a rejection of W30's stated conditional interior results.

## Scope and quantifier audit

Read: `AGENTS.md`, `OPEN_PROBLEMS.md`, `reports/audit_2026-10-28/AUDIT_N.md` and `AUDIT_Nseries.md`, `calculation/decimal_frontier/lattice_formats/FORMATS.md`, recent DONE/ALERT entries in #474, and the result notes below; scrutinized the W30, X07, W11 and W27 accompanying paper arguments. This is a targeted audit of *all-time-sounding mechanism classes*, not a claim to have executed every program in the 377-note repository or independently checked every issue comment. The pre-existing N-series audit inventories 103 N notes and finds no decimal infinite certificate.

| Claim family (published result notes) | Exact universal claim; **not** established |
| --- | --- |
| W30 `AdaptiveCarryFibre50473`, `PhysicalTwoSheetReset`, `MirrorLockedCarrier26710` | Closed 1,800-state period-five **interior** graph under both labels; complement-covariant rank-two set after a physically clocked finite reset. Does not imply physical boundary protection or palindrome safety forever. The counterexample below rules out the *stronger* arbitrary-label odd-witness interpretation. |
| X07 `ComplementPistonProof`, `NinePiston`, `RepunitQuotient` | Exact all-`L` carry/complement step while a central 9 reservoir is present, and finite/conditional repunit updates. In a fixed canonical integer the reservoir decreases with overflow; no all-time recharge/reentry at zero length. |
| W27 `TwelveEdgeNineRecharge`, `Grafted196NineBand` | Twelve true symbolic edges for all `q>=2` (positive temporary recharge; final caps differ), or 20,000 true steps for all `Q>=6005`. Neither is a regenerating return. |
| W11 `PhaseSynchronizer`, `FourCornerPolynomial` | The three-state central phase/units guard persists for every **formal packet step**; the packet recurrence agrees with actual integer reverse-add only while disjoint support intervals persist. No invariant preventing collisions for a fixed finite seed. |
| W05 `AllQThreeRenewals`, W08 `UniversalTripleRenewalShield` | Every symbolic width/centre in the stated class has 264 valid edges; the fourth regenerative return is absent. Quantification over input lengths is not over time. |
| W06 `AllLengthReset`, W07 `TensorTwoStep`, W19 `UniversalContextErasure` | Exact one-, two-, or three-step coalescence for every admissible parameter/context; equality of a future state gives no infinite nonpalindrome theorem. |
| N10 `UniversalPumpLemma`, `ArbitraryFiniteDecimalShell` | Every insertion count/centre obeys a one-step commutation law; a shell of thickness depending on H protects the first H steps. The band is consumed, not restored. |
| N24 `DecimalCarryClockLatch` | An actual odd-step carry input of `0011` **forever** would give an all-time odd witness; the physical source is checked only for finite time. The missing lemma is precisely permanence of that clock. |
| X13 `QuadrantAffinePumping`, N20 `AffineSheets`, X10 `TransparentOverlapFormat` | Sound conditional growing-counter/affine/capacity format and scoped finite decimal transitions; no returning decimal cycle with closed guards and nonnegative resources. |
| N04 `FoldedRegularInvariant`, N07 `FoldedRegularSafety`, N08 `ExactPalindromeGuard`, N09 `BackwardSafetyAutomata` | Correctly formulated finite-language/automaton all-time criteria; no nonempty, reachable, forward-closed **decimal** language excluding palindrome has been exhibited. N09's finite bad-language approximants have not stabilized. |
| X09 `AutomaticSpacetime`, X21 `RadiusConeCertificate` | Conditional automatic/nearest-palindrome formats; the finite 196/879/1997 observations are not an instantiated all-time invariant. |
| X16 `NineStepAllWidths`, X26 `OddCentreAllL` | Universal quantification over widths, but respectively nine and 20,000 steps; neither is infinite. |
| E2 `P21M9AllTemporal`, `P26M9AllTemporal` | “All temporal periods” means exhaustive recurrent cycles of a **fixed unrooted bulk** state graph, not existence of a rooted decimal exterior/centre or actual infinite nonpalindromic integer. |

The original papers mostly state their limitations honestly. Older finite-horizon DONE/ALERT comments are not mathematical all-time certificates regardless of the word “universal.” All claims above remain non-certificates under the owner's stricter `AGENTS.md`.

## New exact physical counterexample to a W30 *safety upgrade*

Use the least-significant-first pair coefficient `P_i=d_i+d_(n-1-i)` and the W30 synchronized rank-two row at t=27,390:
`A=(6,7,8,8,7)`, `C(A)=(12,11,10,10,11)`, mirror-axis residue `delta=0`.
W30's two cyclic carry fibres on A are identically 0. Its exact labelled map therefore gives
`F_0(A)=(12,14,16,16,14)`; complement equivariance gives
`F_0(C(A))=(6,4,2,2,4)`.
**Both resulting rows have only even coefficients.** Thus the *entire two-sheet uncertainty set* loses its odd-coefficient witness after the single allowed label `gamma=0`, without needing any defect-front argument. The published W30 graph is closed but not universally safe.

More strongly, the following is an explicit true-decimal, all-length family, not merely an abstract automaton path.

**Theorem (PAPER PROOF, exact for every integer k>=1).** Write literal decimal digits most-significant first and set
`N_k = 1 ++ 0^(5k) ++ 3 ++ (78876)^k ++ 0`.
It is canonical, has `10k+3` digits and is not a palindrome (first digit 1, last digit 0). Its actual full pairword is
`P(N_k)= [1] ++ A^(2k) ++ [6] ++ [1]` (low first), with interior period-five row A and reflection axis residue 0. The true next integer is
`N_k+reverse_10(N_k) = 1 ++ (67887)^k ++ 6 ++ (78876)^k ++ 1`,
which is a **palindrome** with the same digit length, so the actual overflow label is `gamma=0`.

**Proof.** Reverse the literal digit string, retaining its initial zero only for column alignment:
`reverse(N_k) = 0 ++ (67887)^k ++ 3 ++ 0^(5k) ++ 1`.
At every aligned position the two added digits total at most 8: the central digits give `3+3=6`, while each nonzero five-digit block faces zeros and the two exterior end digits give 1. There are **no carries at all**. Columnwise addition is exactly the displayed palindrome because `reverse(67887)=78876`. Its initial pairword is obtained by summing mirrored input digits, giving the stated periodically rooted A row; the axis condition `A_j=A_(-j mod 5)` holds directly. QED.

For `k=1`: `1000003788760 + 678873000001 = 1678876788761` (the shorter numeric reversal omits its leading zero). This equals the claimed palindrome.

**Independent true-integer validation:** `node calculation/new_structures/agent-V09/check_w30_one_step.mjs`. It constructs 102 entire canonical integers (`k=1..100,300,1000`) and checks actual reverse-and-add in TWO independent implementations: JavaScript native BigInt and standalone schoolbook digit-by-digit addition; compares every output digit with the symbolic palindrome, the exact pairword row at every interior index, input nonpalindromicity, and `gamma=0`. All pass. These finite controls are not the proof of the universal theorem above.

## Proof-critical consequence and redirection

**The missing lemma exposed:** any attempt to turn W30's arbitrary-overflow rank-two closed bulk into an all-time decimal certificate MUST additionally establish a *physically enforced safe overflow/guard language* (excluding the unsafe A/label-0 combination when relying on that interior odd witness), or an independently permanent outer nonpalindrome witness **and** a regenerative boundary rule preventing the finite bulk from being consumed.

The counterexample does **not** refute the published 1,800-state closure, rank-two synchronization, complement identity, the specific rooted W30 seed's finite replay, or its possible future beyond the checked horizon. It does refute the inference “rank-two interior closed under all binary labels => odd witness or nonpalindrome for every physical realization.” In particular the independently documented physical boundary first reaches the middle at t=53,164, so no current bulk-only argument crosses that boundary for all time.

No fixed base-10 seed is proved Lychrel here, no all-time candidate is being ALERTed, and this report is not Lean-verified.
