# Exact period-four return clock: author evidence

Claim: `7f1b9680b99484e550322945ae7be029fb5a200e`.
Canonical source: `proofs/Agent1PeriodicReturnClock.lean`.
Final source SHA-256: `ef4b8ae6380db3b2286ed166e26fe432626eb36a812c8de5c72d54d0c6bb309e`.

## Checked result and interfaces

All public endpoints are in `Agent1.Periodic`:

- `quotient_path_valid`: original `ValidPeriodic` propagates along the existing exact `QuotientPath` through every `i ≤ N`, with no catalog premise.
- `quotient_path_closed_outside_clock_bounds`: return of the physical outside coefficient gives `2 * quotientClockSum B H w N ≤ N ∧ N ≤ 4 * quotientClockSum B H w N`. This includes N=0 and uses the actual carry entering the last column of the original exponent-three word.
- `quotient_return_clock_gain`: original initial validity, exact quotient path, `0 < N`, and complete endpoint equality of B, H, and w give `∃ G : Nat, 0 < G ∧ quotientClockSum B H w N = 8 * G ∧ quotientDeltaSum B H w N = (G : Int) ∧ 16 * G ≤ N ∧ N ≤ 32 * G`.
- `quotient_return_length_ge_sixteen`: the same full-return premises imply `16 ≤ N`.

The one private adapter proves that Agent8's integer sum of actual outside overflows is the cast of the existing natural `quotientClockSum`. The rate proof reuses `Agent8.closed_path_bounds` (and thus its existing potential telescope), without redoing the potentials or finite certificate. The gain proof reuses `quotient_path_equal_width_clock`, selecting `G = quotientClockSum / 8`.

This formalizes the prior positive-overflow/gain argument in original `periodic_bulk_followup/METHOD_AND_PROOF.md` §4, blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c`, and combines it with the already checked quantitative outside bounds. It does not claim discovery of positive gain, construct a return, prove `16 ∣ N`, or establish a safe orbit. The signed shift is formal quotient accounting; a natural exponent-trajectory interpretation still needs the original `k ≥ 3` guard at every used transition.

## Exact validation

Official Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`, explicit `LEAN_PATH`, 4-GiB virtual-address limit. All 20 existing dependency sources were checked against the worktree and the pinned WidthLift registry hashes before each build. The final audit imports those 20 plus the new module. The execution scripts and receipts record source/object/compiler hashes, exact arguments, current directories, dependency identities, output, elapsed time, resident-memory peak and exit status.

- `attempt-001`: source compile exit 0, 0.600 seconds, maximum RSS 454,480 KiB.
- `audit-001`: complete module audit exit 0, 1.519 seconds, maximum RSS 760,444 KiB.
- `attempt-002`: final source compile exit 0, 0.555 seconds, maximum RSS 454,176 KiB. The only change was clarification of one module-comment sentence: no return existence claim is made. Mathematical statements and proof text are unchanged.
- `audit-002`: final complete module audit exit 0, 1.364 seconds, maximum RSS 760,628 KiB. It inspected every new-module declaration: 17 theorems (four public endpoints, one private adapter, twelve generated proofs), zero definitions, zero custom axioms. All axioms are among `propext`, `Classical.choice`, `Quot.sound`; every required public endpoint was explicitly found.

There were no failed compile or audit attempts. All successful versions and their actual evidence are retained. These are incremental author checks; parent fresh build and independent review are separate.

Only the owned canonical module and this contribution directory were written. No dependency, existing mathematical definition, registry, Git state, or external service was changed by this specialist.
