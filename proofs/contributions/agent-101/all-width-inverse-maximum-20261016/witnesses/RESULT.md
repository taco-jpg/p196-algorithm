# All-width inverse maximum witnesses: author PASS

Frozen source: `proofs/Agent101MaximumWitnesses.lean`, SHA-256 `d915b9df4e9ef3ab92ae9a33c3edd655b8567c40af7b88026e067408303182b7`.

## Exact mathematical result

In namespace `Agent101.MaximumWitnesses`, `all_width_maximum_witness D hD` proves, for every `D >= 2`, the existence of an ordinary natural number `Y` and a finite list `ns` such that:

- `decimalWidth Y D`;
- `ns.Nodup`;
- for **every** natural number `n`, `n ∈ ns ↔ 0 < n ∧ Lychrel196.step n = Y`;
- `ns.length = 9 * 10^(D/2 - 1)`.

The definitions make the witness explicit. The half-profile contains `D/2` nines. Even widths have no center; odd widths have center **zero**, preserving the necessary even center sum. The target is `natValue` of this coefficient word, and the list is the existing `numericFiber`. The target is canonical and has units digit 9.

The exact `profileCount_nines` theorem supplies the list length and hence a known predecessor. If any additional positive predecessor had a different width, the unchanged Agent 105 `cross_width_target_digits` theorem would force the shared canonical target's units digit to equal 1. This contradicts the proved units digit 9. Thus all positive predecessors have the required width, and the original fixed-width `mem_numericFiber` theorem gives the displayed complete all-width equivalence.

`one_digit_maximum_witness` separately chooses `Y = 2`, `ns = [1]`, and proves the same complete inverse characterization with cardinality 1. No general claim about the construction at D=0 or D=1 is used. This source does not reprove the global upper bound.

## Actual verification and preserved failure

The two original Agent 105 sources were checked against their exact published hashes, copied unchanged under their original module names, and compiled incrementally with `--trust=0`. Existing objects from the original `Lychrel196Research` foundation and four previous Agent 101 modules were reused; no heavy foundation build was repeated. `dependency-build/` records every source, command, hash, and raw log.

The first complete source attempt failed because the current Std environment does not provide `by_contra`, and `decimalWidth 2 1` needed its definition unfolded before simplification. `attempt-001/` retains the exact failed source and diagnostic output, including the error-generated `sorryAx` traces. These failed diagnostics are not accepted proof evidence. The corrections use `by_cases` and `simp [decimalWidth]`.

`attempt-002/` compiled the entire corrected witness module with:

```text
lean --trust=0 -j1 -DElab.async=false -o Agent101MaximumWitnesses.olean Agent101MaximumWitnesses.lean
```

Exit code was 0. All 20 public declarations (5 definitions and 15 theorems) print their axioms. The union is exactly `[Classical.choice, Quot.sound, propext]`. No warnings remain in the successful witness log. The eight source modules in the actual witness import closure pass the original verifier's code-token scan.

The ready object and frozen build source are in `/workspace/scratch/2a8a87fd78df/agent101-maximum-witness-build-01/attempt-002`. Put that directory first in `LEAN_PATH`, followed by `/workspace/scratch/2a8a87fd78df/agent101-maximum-witness-build-01` and `/workspace/scratch/2a8a87fd78df/agent101-generic-closure-bbbcc857/agent101-nonpalindromic-fibers/source`.

These records are an exact-hash **local author snapshot**, not a claim that every new path had already been published at a repository HEAD. Root owns publication and later independent exact-commit review. No Git write or change to an older frozen mathematical source was performed.
