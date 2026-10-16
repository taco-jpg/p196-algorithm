# Agent 105 affine normalization author record

Session: `8f1107db019a`.

Source: `proofs/Agent105AffineNormalize.lean`.

Final source SHA-256:
`c2605568740b442bbe2494181a8a44f963d177ef1465d75a7b056badf9c1e33c`.

## Current mathematical result

The actual `Agent8.normalize`, `Agent8.fixedDigits`, and `Agent8.terminalCarry`
are used throughout. The shared affine run representation is the unmodified
`Agent102.RunSpec` and `Agent102.wordAt`; a length is expanded as
`(slope * (k : Int) + intercept).toNat`.

The compiled unconditional theorem `normalize_wordAt_eventually` states:

```lean
(rs : List RunSpec) (e : Nat)
(hrs : SpecBound rs 18) (he : e ≤ 1) :
∃ ds : List RunSpec, ∃ c K : Nat,
  SpecBound ds 9 ∧ c ≤ 1 ∧
    ∀ k, K ≤ k →
      normalize (wordAt rs k) e = wordAt ds k ∧
      terminalCarry (wordAt rs k) e = c
```

The companion `fixedDigits_wordAt_eventually` proves the same output
representation before the terminal carry is appended. The closure wrapper is:

```lean
theorem hasAffineRuns_normalize
    (w : Nat → List Nat) (hw : HasAffineRuns w 18) (e : Nat) (he : e ≤ 1) :
    HasAffineRuns (fun k => normalize (w k) e) 9
```

The internal `LengthDichotomy f` says that `(f.eval k).toNat` is eventually
always zero or eventually strictly positive. It is proved for every signed
affine `f` by `lengthDichotomy`, which directly specializes Agent 102's
`Affine.eval_lt_stable` to `Affine.zero` and `f`. The threshold is
`Affine.compareCutoff Affine.zero f`. Only the conversion between integer sign
and `Int.toNat` is added here; Agent 102's scalar comparison is reused exactly.
The three public closure endpoints have no length-dichotomy premise.

## Reused mathematics and construction

The existing `Agent1.RepeatedBlock.terminalCarry_pow_succ` and
`Agent1.RepeatedBlock.fixedDigits_pow_succ` are specialized to singleton blocks.
Their idempotent carry-transfer proof is imported, not reconstructed.

For a positive run of `x` with incoming bit `e`, the output fixed digits are

```text
[(x + e) % 10] ++ replicate (m - 1) ((x + (x + e) / 10) % 10).
```

The outgoing carry is `(x + e) / 10`, independently of the positive run length.
`fixedRunSpec` represents these digits by one constant run and one run whose
affine intercept is reduced by one. `minusOne_toNat` from the shared Basics
module identifies the latter length with `m - 1`, including signed intercepts.

The structural proof then inducts on the fixed source run list. An eventually absent run
passes the incoming carry unchanged. An eventually positive run supplies the
stable outgoing carry to the induction hypothesis for the remaining list.
Taking the maximum of the two finite cutoffs gives one output run list and one
carry valid on the entire tail. The final carry is appended exactly when it is
nonzero, by `Agent8.normalize_decompose`.

## Boundary coverage

- Empty source lists and eventually zero lengths preserve the actual incoming
  carry. In particular, normalizing an empty list with carry one yields `[1]`.
- A run of nines preserves its incoming bit, even when its length is zero.
  `normalize_replicate_nine` gives its exact digit list and final carry for every
  length, without an eventual positivity premise.
- Negative intercepts remain signed affine intercepts. They are not truncated
  in the specification; only the existing `wordAt` expansion uses `Int.toNat`.
- Zero-valued columns are preserved. Removing a zero-length run never removes
  a positive-length run whose symbol is zero.
- Both input carries zero and one, and every literal coefficient from zero
  through eighteen, are covered. The output literal symbols are bounded by
  nine, and the final carry is bounded by one.

No canonical integer-digit trimming, safe return, or infinite orbit is asserted
by this module.

## Source pins and validation

`dependency-pins.json` records every non-Std input module's exact local source
path, SHA-256, and Git blob identifier. Agent 1's proof comes from commit
`0431e0a64da285455421d8a267a92c37dffbfee7`. Agent 102's shared definitions come
from commit `90b3d63e9d4a560c0a22406215497f583cc1ea5a`, and are byte-identical at
the scalar publication commit `a3329eda74fc419d76c185fa843d9e6e1602a09b`.
`Agent102AffineArithmetic.lean` is imported directly from the latter commit.
The five inherited Agent 8
and carry modules are selected from main
`ae8bbdfd2a18e8910eebc25fd2a81661c01abc16` and match Agent 1's own registry.

`develop.py` verifies source hashes, resolves canonical module names in an
isolated temporary directory, compiles with Lean 4.19.0, and retains each proof
source, compiler log, and result record under `attempts/`. Later attempts also
retain the full pin set and exact compiler identity. `--fresh` starts with no
local `.olean` cache; `--reuse PATH` reuses only cached modules whose recorded
source/dependency stamps still match.

Attempts 001 and 004 succeeded on their respective source versions. Attempts
002 and 003 preserve failed simplifier elaborations. Attempt 005 rebuilt all
eight exact-byte dependencies successfully from scratch and records a failed
lambda rewrite in the newly added wrapper. Attempt 006 fixes that wrapper and
successfully compiles all then-current structural endpoints against those
fresh dependencies. Attempt 007 compiles Agent 102's published scalar module
and the complete unconditional normalization endpoints without any error.
All ten printed endpoint axiom sets are exactly
`propext`, `Classical.choice`, and `Quot.sound`.

The frozen complete source and all nine dependency pins were handed to
`/root/ownership_audit` for a separate full canonical fresh rebuild and
source-origin axiom audit, followed by an explicit `--trust=0` recompilation of
the final normalization module. The original canonical verifier's parameters
are retained. That independent result is reported separately by the reviewer;
this author record does not predeclare its outcome.

`SOURCE-RECOVERY.md` documents the correction of an extra terminal newline in
the initial imported snapshots; the failed and earlier successful attempts
remain unchanged.
