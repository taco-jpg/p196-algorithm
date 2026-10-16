# Agent #21 — M99-A01 realizability contract

Status: WIP interface package; not accepted until a clean Lean build and transitive axiom audit are rerun on this branch.

Source pin: `afbb3282be77f63711aca4fb165814104a365806`.

Manager #99 assignment: support the exact Lean realizability contract and missing lemmas; coordinate interfaces with Agent #11; do not claim an unprovided certificate instance.

## Exact conditional contract

For any `Certificate cert`, if `check cert = true`, the repository already proves:

`∃ m, 0 < m ∧ Lychrel196.IsLychrel m`

via `Agent112.Admissibility.checked_positive_decimal_seed`.

This is an existential conditional. It does **not** provide a concrete certificate or concrete seed.

## Exact finite-word realization contract

For any finite natural-coefficient `Word w` with `0 < evalL w`, the repository also proves eventual ordinary-decimal realization:

`∃ t n, 1 ≤ t ∧ 0 < n ∧ ∀ k, pairWord (Lychrel196.orbit n k) = Agent8.orbit w (t + k)`

via `Agent112.Eventual.original_arbitrary_eventual_realization`.

No initial coefficient bound or canonicality premise is required.

## Agent #11 interface boundary

Agent #11 owns `agent11-general-base-first-hit` on `formalize/agent-11/s20261015-coverage`. Its exact first-hit theorem is a symbolic/base-generic result over `ordinaryStep`; it is not an unprovided concrete P196 certificate. Agent #21 does not modify that owned path.

The useful interface question is whether a base-10 specialization of Agent #11's high-region first-hit statements needs an explicit bridge into the accepted `Lychrel196.orbit` semantics. Existing `TemplateStep.pairWord_step` and `pairWord_orbit` provide the general arithmetic bridge, while the existing Agent112 realization theorem supplies the existence-side contract.

## Acceptance boundary

No `sorry`, `admit`, newly introduced mathematical axiom, `native_decide`, or concrete certificate instance is permitted. Any new theorem remains WIP until actual compilation, source inclusion, and transitive axiom audit are available.
