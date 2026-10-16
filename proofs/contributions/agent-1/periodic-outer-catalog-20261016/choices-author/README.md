# Literal outer-choice enumeration: author checkpoint

Authored under the published outer-product claim `db88a5c78fd5f67ac134031d8486c26df9201799`. Only `proofs/Agent1PeriodicOuterChoices.lean` and this evidence directory were written. No Git state or external coordination message was changed.

Frozen source SHA-256: `9bd84fb0c22b2252fb71f0310fe763e6a07192ef0fb80299763459ab48fb76ad`.

The module imports only `Agent1PeriodicPhaseCatalog`. In `Agent1.Periodic` it defines:

- `OuterNode := Word × Nat`.
- `OuterEdge` with fields `source`, `clock`, `carries`, `target`, deriving `DecidableEq` and `Repr`.
- `outerImages q g`, exactly the `List.range 2` carry enumeration filtered by original `Agent8.overflow`, mapped by original `Agent8.nextExterior`, then `eraseDups`.
- `outerOutputs s`, exactly the original `phaseEdges` filtered by `source = s.1`, followed by the requested `flatMap` and `map`. Every original phase carry label is copied unchanged; only duplicate exterior images within each phase edge are removed.

The two public theorems have the agreed APIs:

```lean
mem_outerImages_of_actual (q e : Nat) (he : e ≤ 1) :
  Agent8.nextExterior q e ∈ outerImages q (Agent8.overflow q e)

outerOutputs_mem_of_phaseEdge (s : OuterNode) (e : PhaseEdge)
  (he : e ∈ phaseEdges) (hsource : e.source = s.1) (q' : Nat)
  (hq : q' ∈ outerImages s.2 e.clock) :
  (⟨s, e.clock, e.carries, (e.target, q')⟩ : OuterEdge) ∈ outerOutputs s
```

These are enumeration/membership facts. They do not assert that the carry bit can be independently chosen, that an arbitrary product edge/path is realizable, or that any whole-interface cycle exists. The outside/head arithmetic is owned by the separate `Agent1PeriodicOuter` author and parent composition.

## Actual attempts and audit

All commands use official Lean 4.19.0, commit `6caaee842e94`, with `--trust=0 -j1 -DElab.async=false` and a 600-second timeout. Dependency sources and objects were reused from the provided fresh 20-module parent build at `/workspace/p196-agent1-session-20261016/periodic-phase-parent-clean-001/agent1-periodic-phase-catalog/source`. Every imported source was checked against `Agent1PeriodicPhaseCatalog.registry.json`, its local repository copy, and its Git blob identity; all source/object hashes are retained and rechecked. This is an **author increment**, not a new fresh dependency build.

- `attempt-001`: FAIL, exit 1. Two membership cases remained because simplification did not turn a known inequality into the Boolean equality test used by `eraseDups`. The failed source and complete recovery `sorryAx` output are retained.
- `attempt-002`: PASS, exit zero in 0.479 seconds. The only repair adds `beq_false_of_ne` to the membership proof's simplification set. Definitions and theorem statements did not change.
- `audit-001`: PASS, exit zero in 1.417 seconds. All six top-level public declaration types/axiom sets are printed. The complete actual new-module origin audit covers **18 theorem constants** and **20 safe definitions**, including generated structure/instance helpers; there are zero safe opaque declarations. Their logical axiom union is exactly **`propext` and `Quot.sound`**.

Separate compiler metadata contains seven unsafe implementation specialization axioms and 58 unsafe definitions, with zero partial definitions or unsafe opaque entries. These do not occur in any audited logical axiom set. No custom source axiom, active proof placeholder, or external proof-oracle token occurs in the accepted source.

## Finite order and literal-table verification

`audit-001/ChoicesControls.lean` uses ordinary kernel `by decide` to check both strict ascending order and an explicit complete output table for all **36** pairs `q=1,...,18` and `g=0,1`. The check passed in 0.315 seconds; both finite theorems are axiom-free. The table has:

| Exterior range | Clock zero output | Clock one output |
|---|---|---|
| `q=1,...,8` | `[2*q, 2*q+1]` | `[]` |
| `q=9` | `[18]` | `[10]` |
| `q=10,...,18` | `[]` | `[q%10+1]` |

Thus deduplication retains the ascending image order on the entire requested finite exterior domain. These finite specifications do not add a path-realizability statement. They are kept outside the production module and separately identified from the two general membership theorems.

The importable accepted object is `attempt-002/Agent1PeriodicOuterChoices.olean`. The source is frozen; `frozen-receipt.json` records final source/object hashes and dependency stability. Parent owns publication and subsequent independent full-closure verification.
