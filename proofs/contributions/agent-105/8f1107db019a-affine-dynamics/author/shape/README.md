# Agent 105 affine shape author record

Session: `8f1107db019a`.

Source: `proofs/Agent105AffineShape.lean`.

Frozen source SHA-256:
`979c493bdb2ff26d8f88e50a440c906948a5dbf66f7ae53c800793447cd13a16`.

## Completed actual-word results

For an arbitrary fixed finite `rs : List Agent102.RunSpec`, define

```lean
widthSlope rs := (rs.map (fun r => r.length.positivePart.slope.toNat)).sum
widthIntercept rs := (Agent102.widthAffine rs).intercept
```

`wordAt_length_affine` proves, at every `k ≥ Agent102.lengthCutoff rs`,

```lean
((Agent102.wordAt rs k).length : Int) =
  (widthSlope rs : Int) * (k : Int) + widthIntercept rs
```

The existing `Agent102.widthAffine_eval` already proves the exact eventual
affine width expression. This module imports it and identifies its slope with
the displayed natural-number sum; it does not reprove the finite-run width
calculation. `widthAffine_slope_nonneg` records nonnegativity, and
`widthIntercept_eq_sum` identifies the intercept with the finite sum of the
positive-part intercepts.

`wordAt_length_shift` derives the natural-number equality

```lean
(wordAt rs (k + s)).length = (wordAt rs k).length + widthSlope rs * s
```

for **every** `s : Nat` at the same cutoff `lengthCutoff rs ≤ k`. It uses two
actual width identities and integer distributivity, then injectivity of the
natural-number cast into the integers. No truncated subtraction is exchanged
with an affine difference.

The coefficient additionally satisfies `widthSlope_eq_slope_toNat_sum`:

```lean
widthSlope rs = (rs.map (fun r => r.length.slope.toNat)).sum
```

This equality does not require nonnegative original slopes. A negative
original slope already has natural-number truncation zero. When all original
slopes are nonnegative, `widthSlope_int_eq_slope_sum` gives the exact original
integer slope sum:

```lean
(widthSlope rs : Int) = (rs.map (fun r => r.length.slope)).sum
```

## Actual first symbol

`wordAt_headOption_eventually` proves

```lean
∃ d : Option Nat, ∃ K : Nat,
  ∀ k, K ≤ k → (wordAt rs k).head? = d
```

The proof inducts on the fixed source run list and reuses the already-proved
`Agent105.AffineNormalize.lengthDichotomy`. If the first run is eventually
empty, the induction hypothesis supplies the first symbol of the suffix. If
its length is eventually positive, the actual first symbol is its fixed
literal digit. `Option Nat` distinguishes an empty word from a word beginning
with digit zero. The derived `wordAt_headD_eventually` supports any default,
and `wordAt_head_eventually` specializes to the existing `headD 0` convention.

The assembly interface `wordAt_head_width_eventually` takes a maximum of the
head and width cutoffs and provides both facts together:

```lean
∃ d K : Nat, ∀ k, K ≤ k →
  (wordAt rs k).headD 0 = d ∧
    ∀ s : Nat, (wordAt rs (k + s)).length =
      (wordAt rs k).length + widthSlope rs * s
```

All statements permit negative slopes, negative intercepts, zero-length runs,
zero-valued symbols, empty specifications, and adjacent equal symbols. No
digit bound is needed for these shape facts. Strict growth is not inferred:
applications needing positive growth must establish `0 < widthSlope rs`.

## Source reuse and validation

`Agent102RunEndpoints.lean` and its scalar input are imported byte-for-byte from
Agent 102's publication `a3329eda74fc419d76c185fa843d9e6e1602a09b`.
The normalization module remains frozen at SHA-256
`c2605568740b442bbe2494181a8a44f963d177ef1465d75a7b056badf9c1e33c`.
`dependency-pins.json` records all eleven non-Std dependency sources, hashes,
Git content identifiers, and canonical imports. `AUTHOR-RESULT.json` records
the final source and author result.

The author compiled the exact dependencies using the previously validated
normalization build artifacts. Newly introduced normalization and endpoint
module artifacts were checked against their source stamps before use. The
shape source itself was compiled on every attempt:

- Attempt 001 retains two failed proof elaborations: a redundant `dsimp`, and
  a mismatch between two presentations of `List.sum`.
- Attempt 002 compiles the complete head/width theorem chain successfully.
- Attempt 003 adds the original-slope adapters and compiles all fifteen public
  theorem declarations successfully.

Every public theorem has a literal `#print axioms` command. The output sets are
subsets of `propext`, `Classical.choice`, and `Quot.sound`; the intercept-sum
identity requires no axioms. All sources and compiler output are retained under
`attempts/`.

The frozen source has been handed to `/root/ownership_audit` for independent
semantic review and incorporation into the coordinated final canonical
closure check. The author cache is not represented as an independent fresh
build. Full dependency rebuilds are coordinated by the parent because a
concurrent earlier rebuild of the inherited carry library exhausted the
shared memory budget; no fresh-build success is predeclared here.
