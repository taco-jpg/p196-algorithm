# Zero-period ordinary arithmetic bridge: author evidence

Claim: `d5786f691f77c606f7343b1182cc67643f058a8f`.

The directory name reflects the initial combined numeric/mass assignment.
Parent subsequently assigned the finite mass identity to `symbolic_scope`;
this directory covers only `Agent1PeriodicZeroNumeric.lean`. No mass source
was created or edited by this author, and no Git mutation was performed.

## Checked interface

`actual_step_representation n d W hcan hrep` returns

```lean
∃ d', DecimalDigits.Canonical (Lychrel196.step n) d' (Agent8.stepWord W).length ∧
  ∀ i, i < (Agent8.stepWord W).length →
    DecimalDigits.columnSum d' (Agent8.stepWord W).length i =
      ((Agent8.stepWord W)[i]?).getD 0
```

Its premises are the original `Canonical n d W.length` and finite in-range
column equality to `W`. It needs no additional coefficient bounds, symmetry,
or choice of carry. The proof retains both outputs of the existing original
`FoldedDecimal.representation_next`.

The previously missing compatibility is proved explicitly:

- `stepWord_length_nextWidth W` equates the original list successor length
  with `FoldedDecimal.nextWidth` applied to the finite word's zero-default index.
- `stepWord_getD_nextColumns W i hi` equates each in-range original list
  successor entry with `FoldedDecimal.nextColumns`.
- The supporting digit bridge uses the existing `IncomingCarry.outputIn` and
  `carryIn_add`, then separates the actual zero and nonzero terminal carry.
  The nonzero case includes the extra final carry position. Reflected indices
  are constrained by the actual successor width.

`zero_quotient_actual_step B H k n d hB hH hk hcan hrep` returns the same full
canonical representation and finite column equality for the exact word

```lean
periodicWord (quotientOuter B H [0,0,0,0])
  (quotientCenter B H [0,0,0,0]) [0,0,0,0]
  ((k-2)+outerPeriods B H [0,0,0,0]+centerPeriods B H [0,0,0,0])
```

Here `B,H` are bounded by18 and `3 ≤ k`; initial canonical realization and
full column equality are explicit. This wrapper reuses `quotient_step_bounded`
and the separately authored `rawPeriod_zero`. It neither constructs an initial
realization nor claims a cycle obstruction by itself.

## Frozen source and provenance

`proofs/Agent1PeriodicZeroNumeric.lean`:

- SHA256 `8e561a621f18d783aa52ef0f2d6985b0a6cd0293b80fe4b174250665cee07b89`
- Git blob `043300254bb2f95cae725f9963848a011cc2cd58`
- Ten explicit exported theorems, each with a literal `#print axioms`.
- Axiom union: `propext`, `Classical.choice`, `Quot.sound`.

Dependency hashes are pinned by `Agent1PeriodicValidity.registry.json` and by
the frozen `Agent1PeriodicZeroPeriod.lean` hash in `replay.py`. No second
foundation root, alternate digit normalizer, or assumed list/index equivalence
is introduced. The generic realization and unbounded-mass theorems remain the
existing original results.

## Verification records

`dependency-reuse.json` records the17 byte-checked source/object dependencies
used only for incremental development, copied from the parent's fresh validity
replay. `zero-period-dependency-001/` preserves the exact copied ZeroPeriod
source, successful compiler log, and receipt. `numeric-attempt-001/` preserves
the first and only numeric source attempt and its successful log/receipt.
There were no failed Lean proof attempts for this module.

`clean-001/verification.json` records the final fresh author replay. It compiles
all19 modules from source with no reused project objects, using official
Lean4.19.0 (`6caaee842e94`) and `--trust=0 -j1 -DElab.async=false`, then checks
the complete explicit export inventory, every printed axiom dependency, and
source identity before and after the run. This is author evidence; independent
review is a separate record.

Reproduce into new directories:

```sh
python3 proofs/contributions/agent-1/periodic-zero-cycle-20261016/mass-author/replay.py \
  --source-root . \
  --build-dir /tmp/agent1-zero-numeric-replay \
  --evidence-dir /tmp/agent1-zero-numeric-evidence \
  --lean /workspace/p196-tools/lean-4.19.0-linux/bin/lean
```
