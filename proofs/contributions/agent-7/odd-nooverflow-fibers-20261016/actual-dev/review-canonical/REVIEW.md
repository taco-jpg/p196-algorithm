# Independent review: canonical odd coefficient-word fibers

Reviewer: Agent #7, `/root/runtime`. Result: **PASS for the stated encoded-target domain**. No author source was changed.

## Source and execution

- `OddCanonical.lean`: SHA256 `46529b9c0bd55a3ae069900789f4747e9de7f58b5c6f82350ee4c657a551e617`.
- `OddWords.lean`: SHA256 `f0827099cffeeab2997c0a572906d8bd370e048aa859beb3bb8189ad5bc217a3`.
- Fresh independent build: `attempt-002/verification.json`. All nine project modules in the import closure and the separate five-theorem review fixture compiled with pinned Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`.
- All 122 explicit public theorem statements in that closure, including the five review fixtures, passed individual `#print axioms` checks. Exhaustive module-origin traversal checked 285 theorem constants. Every mathematical axiom dependency belongs to `propext`, `Classical.choice`, `Quot.sound`.
- The source bytes were pinned before compilation and compared again afterward. No cached project objects were used.

The first reviewer harness invocation failed before Lean started because its repository ancestor path was off by one. The original runner and a startup diagnostic remain in `attempt-001`; the corrected complete execution is `attempt-002`.

## Semantic review

`CanonicalOddFiber` names the full coefficient word directly. It requires length `2*m+1`, reversal symmetry, each coefficient below 19, a positive full-word first coefficient, an even coefficient at the actual middle index, zero final carry from the existing decimal scan, and the existing `Agent8.stepWord` output. It does not assume an encoded source half in the definition.

Completeness goes both ways. `symmetric_odd_decomposition` splits any symmetric word of that length into a half, one center, and the reversed half. The center lookup theorem transfers parity at the actual index, and the head identity transfers positivity. The exact length makes the middle index valid, so `getD 0` cannot conceal a missing center. The resulting encoded fiber is exactly the previously checked actual arithmetic fiber. The forward direction establishes every condition of the full-word predicate from the encoding.

Duplicate freedom is justified by injectivity of the odd mirror encoding in both half and center. Filtering the already duplicate-free path enumerator and then mapping by this injection produces distinct complete words. There is no cardinality argument counting repeated carry witnesses as distinct words.

The width-one boundary is handled correctly by `xs.headD z`: when the half is empty, positivity concerns the center itself. An independent finite check covers all ten center digits and finds exactly `[[v.val]]` for positive even `v`, and an empty fiber otherwise. Further independent checks establish `CanonicalOddFiber [2] 2 [1,2,1]`, reject `CanonicalOddFiber [4] 1 [2,1,2]`, prove `fullOddPreimages [2] 2 = [[1,2,1]]`, and reject the empty source word. These distinguish outer-coefficient parity from actual-center parity.

## Scope

This module completely handles targets of the form `oddMirror (ss.map Fin.val) (2*v.val)`. A theorem for every raw requested output list still needs a checked output-range argument and exact decoder. Parent is adding those as `OddOutputRange` and `OddComplete`; this review does not pre-approve them. The accepted claims concern one actual reverse-add transition on canonical coefficient words, not the entire integer orbit or an all-time nontermination assertion.
