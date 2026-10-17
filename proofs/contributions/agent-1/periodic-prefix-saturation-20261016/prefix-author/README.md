# Actual physical-prefix bridge: author evidence

Claim: `8a8e6b9d748cbd25892e4836ff1a25fc55a78ca2`.
Canonical source: `proofs/Agent1PeriodicPrefix.lean`.
Final source SHA-256: `591c10a3f34c75d0dc058fc64db5b3934c1345b6f4fa9015eb64a3586dec8377`.
Direct imports: `Agent1PeriodicOuter`, `SaturationTheorem`, using the exact latter module identity in `Agent2SaturatedProfile.registry.json`.

## Actual checked API

All public declarations are in `Agent1.Periodic`:

- `physicalPrefix (B w : Agent8.Word) : P196.Agent4.Saturation.Prefix` converts the existing `Agent8.firstThree (B ++ w)` tuple to the unchanged prefix structure.
- `firstThree_periodicWord B H w k hlen hk` proves `firstThree (periodicWord B H w k) = firstThree (B ++ w)` whenever `w.length = 4` and `1 ≤ k`.
- `physicalPrefix_a B w hlen` identifies its first coordinate with the existing physical `outside B w`.
- `physicalPrefix_valid B H w hv` derives the existing saturation-prefix `Valid` predicate from original `ValidPeriodic`.
- `physicalPrefix_step B H w hv` returns the conjunction of prefix validity, `Agent8.inputThree (periodicWord B H w 3) ≤ 1`, and the exact equation:

```lean
P196.Agent4.Saturation.advance (physicalPrefix B w)
    (Agent8.inputThree (periodicWord B H w 3)) =
  (physicalPrefix (quotientOuter B H w) (rawPeriod B H w), rawGamma B H w)
```

The control is the actual `inputThree` carry entering the final three columns, not the `lastInput` carry entering only the final column. The proof reuses `prefix_step_of_canonical`, `firstThree_valid`, `terminalCarry_eq_actual_overflow`, and `valid_quotient_transition` at exponent three. That transition supplies a positive target exponent, sufficient for the prefix lemma. Empty B and empty H are covered, with no extra nonemptiness premise. This module proves no saturation classification, abstract-path realization, safe orbit, or guarded multi-step numeric lift.

## Validation and complete preserved attempts

Official Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`, explicit `LEAN_PATH`, 4-GiB virtual-address limit. The 22 existing dependency sources were checked against this worktree and exact registry hashes. Dependencies came from the existing clock parent-clean build and exact saturated-profile build. The new module plus those 22 dependencies are loaded by its full declaration audit. This is incremental author verification; the parent's later fresh build and independent review remain separate.

Each run retains the exact source, command script and JSON, output, exit code, resource usage, dependency/compiler/source/object hashes.

- `attempt-001`: compiler exit 1. The private tuple/structure formula adapter needed let/projection reduction before splitting its conditional. All other declarations elaborated; the failed attempt's `sorryAx` output is rejected evidence only.
- `attempt-002`: compiler exit 0, 0.482 seconds, maximum RSS 751,984 KiB. This is the final unchanged canonical source and checked object.
- `audit-001`: exit 1, because the strict first audit rejected a Lean-generated `_cstage2` implementation declaration.
- `audit-002`: exit 1, retaining a complete inventory of the four generated `_cstage1`/`_cstage2` implementation declarations before the same rejection.
- `audit-003`: exit 0, 1.717 seconds, maximum RSS 770,952 KiB. All 17 new-module declarations were inspected: 11 theorems (four public, two private helpers, five generated proof auxiliaries), two safe source definitions, and four explicitly named compiler implementation definitions. No custom axioms or unrecognized non-safe declarations occur. All six definitions, including compiler variants, are axiom-free; every theorem uses only permitted `propext`, `Classical.choice`, and `Quot.sound`. All five required public names were explicitly found.

Only the owned canonical source and this evidence directory were written. No dependency, existing model/classification, registry, Git state, or external service was modified by this specialist.
