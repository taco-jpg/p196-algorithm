# All-base local extreme births and the actual nooverflow bridge

Author role: Agent #106 / base_generalization. The two submitted sources are `../../BaseBirths.lean` and `../../ActualBaseBirths.lean`. This directory preserves development evidence; `.olean` build outputs live in external scratch space and should not be committed.

## Exact scope

Let `b ≥ 2`, `0 ≤ x ≤ 2*b-2`, and let `a,c` be the incoming carry bits on the two sides, either actual or to be instantiated. Define

`localPair b x a c = (x+a)%b + (x+c)%b`。

The complete classification is:

| Output | Input pair coefficient x | a | c | Local mechanism |
|---|---:|---:|---:|---|
| 0 | 0 | 0 | 0 | Existing zero retained |
| 0 | b | 0 | 0 | New zero |
| 0 | b−1 | 1 | 1 | New zero |
| 2b−2 | b−1 | 0 | 0 | New maximum |
| 2b−2 | b−2 | 1 | 1 | New maximum |
| 2b−2 | 2b−2 | 1 | 1 | Existing maximum retained |

The three branches for each output are mutually exclusive and exhaustive. Unequal incoming carries cannot produce either extreme. For `b≥3`, the source `x` of any newborn extreme lies strictly between the two extremes. For `b=2`, the complete classification remains unchanged, but `x=b` is the maximum and `x=b−2` is zero. Binary therefore allows direct interchange of the two extremes: `localPair 2 0 1 1 = 2` and `localPair 2 2 0 0 = 0`. This is distinct from the binary boundary where the existing intrinsic-output safety result fails.

## Relation between the new content and existing results

The existing `base-reflection-formal` classification concerns original coefficients/carries and reflection symmetry of the full output. The existing `base-intrinsic-formal` classification concerns adjacent high-neutral patterns, reset/ordinary carry defects, and nonpalindromic output safety. The new proposition here is a pointwise necessary-and-sufficient classification for a mirrored output pair to equal the minimum or maximum; it does not reprove those whole-output results.

`BaseBirths.lean` imports only `Std` and has 7 public theorems. Its birth predicate is a one-step local predicate, not an ancestry, lifetime, or whole-orbit theorem. Agent 102's maximal extreme-run ancestry/lifetime work was not duplicated.

`ActualBaseBirths.lean` reuses the semantics of the existing `PhysicalWidth` and `ReverseAdd` and has 11 public theorems. Actual incoming carry is defined as the terminal carry of ordinary sequential normalization through the first k columns; arbitrary independent carry inputs are not passed off as actual carries. When the computed final carry is zero, main bridge `actual_nooverflow_pair_at` proves that `pairs (actualDigits b xs)[k]` equals the local expression above, with mirrored index `xs.length−1−k`.

The main theorem `canonical_reverse_add_extremes` requires:

- `b ≥ 2`；
- Input digits satisfy the existing `DigitBounds` and `PositiveLast` conditions;
- The source coefficient projection really equals `ReverseAdd.pairs digits`;
- The computed ordinary final carry is zero;
- The index is within the source length.

Its conclusions simultaneously give actual output digit bounds, a positive leading digit, value `n + reverse_b(n)`, and complete iff classifications of both extremes for actual output pairs. Every conclusion is explicitly restricted to one nooverflow step; the changed mirrored pairing under overflow is not covered.

## Compilation and axioms

Lean 4.19.0 was used. `compile-02.log` contains complete compilation of the frozen Std module and 7 `#print axioms` outputs; `actual-04.log` contains complete compilation of the frozen actual module and 11 `#print axioms` outputs. Dependencies are only subsets of Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; the concrete binary examples are axiom-free. There is no `sorry`, `admit`, `native_decide`, or new axiom.

Independent reviewer nooverflow_births rebuilt the frozen `BaseBirths.lean` from an empty directory and passed its semantic and kernel review; that reviewer stores the detailed logs separately.

Frozen source SHA256:

- BaseBirths.lean: `dcca96672161ac382020d476c6bf75d2b3b47456c76193cba55fdfcd6650af33`
- ActualBaseBirths.lean: `e9fd9ed2a8065d7b6327d0400f7d94eea1049ba3f5b24241dcec244600121a6d`

## Preserved development history

- `BaseBirths.compile-01.lean` / `compile-01.log`: successful on the first attempt, with only an unused-helper-argument warning; the frozen version renames it `_hb`.
- `actual-01.log`: the first actual-digit indexing bridge passed.
- `ActualBaseBirths.actual-02.lean` / `actual-02.log`: the only failed source; attempting `rw [hs]` on a dependent index produced an invalid motive type.
- `actual-03.log`: the core actual-pair bridge passed after switching to `simp only [hs]`.
- `actual-04.log`: passed after adding the complete classification and canonical wrapper.
- `dependency-logs/`: source-compilation logs for six existing all-base modules, all passing.

After generation, these logs were moved here from development/base at the repository root, so paths in early logs retain their original execution locations.

## Reproduction

`build_dependencies.py` builds the six existing modules using an exact source map, without copying or modifying them. Specify an external scratch directory, export the runtime's required `LD_PRELOAD`, and set `LEAN_BIN`. Then use that directory as `LEAN_PATH` and compile `BaseBirths.lean` followed by `ActualBaseBirths.lean`. Example:

```sh
export LEAN_BIN=/workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean
export LD_PRELOAD=/workspace/scratch/50e90e07524e/runtime/readlink_self.so
python proofs/contributions/agent-106/run-births/development/base/build_dependencies.py /workspace/scratch/50e90e07524e/base106-rebuild
export LEAN_PATH=/workspace/scratch/50e90e07524e/base106-rebuild
"$LEAN_BIN" -o "$LEAN_PATH/BaseBirths.olean" proofs/contributions/agent-106/run-births/BaseBirths.lean
"$LEAN_BIN" -o "$LEAN_PATH/ActualBaseBirths.olean" proofs/contributions/agent-106/run-births/ActualBaseBirths.lean
```
