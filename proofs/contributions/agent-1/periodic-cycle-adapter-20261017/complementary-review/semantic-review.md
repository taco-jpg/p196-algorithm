# Complementary source-only review of the cycle numeric adapter

No unresolved semantic defect was found in the observed source. This review is source inspection only: no Lean execution, new proof, orbit search, Git mutation, or independent fresh-build claim. The primary complete fresh review belongs to `/root/symbolic_scope`. This reviewer is `/root/research_status`, a separate specialist in the same session/account, with no authorship of these three modules. CyclePath and CycleGuard were authored by separate child specialists, whose author checks are not this reviewer's executions.

The observations are pinned in `source-inspection-receipt.json` and `observed-sources-001/`. At inspection the checkout HEAD was baseline `3b018f7032b537cd7f6218fb9ad979842bb286d0`; the new mathematical sources were working files, not yet bound here to a final publication commit. The observed registry contains exactly 30 modules, independently reconstructed from literal imports: 27 unchanged dependencies plus the three new modules. The core source pins are:

| Module | SHA256 |
| --- | --- |
| CyclePath | `196f04ef0d9ca89e0eb6151905c0f3abf217eefcf8469c32269e0954423384a9` |
| CycleGuard | `357d626233997cd7b1d9b2606c63f196814854abd29f7e72a1a51254c9aa2041` |
| CycleNumeric | `4cbf4ee50c819e71ee09d108ab62fd703af1287507b969988a09e61b3fe2c527` |

## Premises and finite-cycle repetition

Both numeric endpoints retain a supplied finite exact `QuotientPath B H w N`, all seven original fields of initial `ValidPeriodic`, positive N, and full B/H/w endpoint return. They quantify over arbitrary such data and do not supply a qualifying cycle. The safety endpoint additionally requires the original Boolean `safePeriodic` to be true at every residue i<N. There is no implication from initial safety to successor safety.

`QuotientPath` in WidthPath specifies bounded coefficients, period length four, and all three literal successor equalities at each used source index. CyclePath repeats the actual functions by t%N instead of assuming their arbitrary values beyond N already repeat. The wrap is proved separately using x N=x 0 for each of B,H,w; a phase, width, or projected-node return is not substituted. N>0 supplies each residue bound and is retained whenever division/modulo cycle laws are used. An empty finite horizon is allowed by the repeated-path helper, while a zero-length cycle is excluded by the numeric endpoints.

## One guarded natural schedule

CycleGuard's schedule is the finite schedule at the residue plus floor(t/N) times the existing natural gain G. The first traversal starts at 2*N+3. GuardedPath's finite lower bound protects every residue, and adding a natural gain cannot reduce the guard. The signed accounting theorem is invoked only after the finite source guards are established, so natural subtraction is never silently replaced by an integer difference.

The existing ReturnClock theorem derives the total signed shift equal to positive natural G from the supplied complete return. The resulting finite endpoint identity closes the wrap case of the exact recurrence `(k-2)+outerPeriods+centerPeriods`; the nonwrap case uses the ordinary residue successor. The natural schedule therefore satisfies every source guard k≥3 for all time. The tuple returns but the exponent gains copies; neither the complete coefficient word nor the ordinary integer is claimed to be periodic.

## One seed before every time index

`quotient_cycle_actual_orbit` first obtains one all-time schedule. It then calls the existing `periodicWord_realizable` exactly once at that schedule's initial count, obtaining one positive ordinary integer n and one initial canonical digit function d. Only after n,d have been selected does it introduce arbitrary t.

At each t it invokes `quotient_path_actual_prefix` with that same n,d and the same schedule, on the repeated exact path with finite horizon t. It does not invoke the horizon-dependent existential `quotient_path_finite_realizable` at each t. Thus the quantifiers are genuinely `exists k, exists n, forall t`, not an exchange of `forall horizon, exists seed`. The per-time digit function is existential, as appropriate for a canonical representation of the already fixed `orbit n t`.

The transported representation preserves both original `DecimalDigits.Canonical (orbit n t) d L` and every in-range original column sum at L equal to the complete displayed periodic word. Canonical means positive width, each actual digit at most nine, positive leading digit, and the full numeric value equation. This is ordinary canonical width, not merely stored-list length or a padded numeral. No equation for irrelevant digit-function tails is required. The exact source is `actual_step_representation` in ZeroNumeric, which reuses original `FoldedDecimal.representation_next`; none of those correspondence premises are dropped.

Initial `periodicWord_realizable` uses all original validity fields, including odd-middle parity. Empty stored exterior or center requires no new exclusion; original positivity uses the physical outside `(B++w).headD 0`. The period is nonempty because each used residue has length four. The all-time schedule ensures positive copy count as required by the exact safety equivalence, avoiding the known k=0 boundary.

## The successor is the safe all-time witness

The second endpoint concludes `exists m, 0<m and Lychrel196.IsLychrel m`, and explicitly chooses m=`step n`. Original `IsLychrel` quantifies over every iterate including time zero. Original `safePeriodic_iff_next_not_palindrome` classifies `step (orbit n t)`, not `orbit n t` itself. The proof therefore uses safety at residue t%N together with the canonical full-column representation at t to exclude the next palindrome.

Original `orbit_from_step` states `orbit (step n) t = orbit n (t+1)`, and the original recursive orbit definition identifies the latter with `step (orbit n t)`. This accounts for the index shift exactly, including t=0. Positivity of the chosen successor follows from original `orbit_positive n hn 1`. No initial nonpalindromicity of n is assumed or inferred. If one wanted IsLychrel n instead, that additional initial exclusion would remain necessary; the current endpoint avoids that unsupported claim by choosing the successor.

## Scope and remaining validation

The result is the formal adapter for the already stated conditional full-cycle criterion in original METHOD section4. It reuses existing generic realization, arithmetic transport, safety, and return-gain theorems. It does not discover an affirmative interface cycle, realize an arbitrary graph walk, prove generic safety closure, identify a concrete Lychrel seed, or prove the 196 conjecture. The conditional existence conclusion retains the unresolved supplied-safe-cycle premise.

This complementary review does not replace the primary frozen-source pin, strict full-closure compilation, origin/safe-definition axiom audit, or final published-head check. All such execution claims must be attributed to the actual primary reviewer or parent. If the three source hashes change, this semantic receipt requires rechecking the changed statements/proofs.
