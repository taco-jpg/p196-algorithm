# Verification of the actual whole-word to long-prefix connection

Evidence type: **formal theorem**. Date: 2026-10-15. Lean 4.19.0.

The main source is `ActualPrefix.lean` in the parent directory, namespace `SevenColumnProjection`.

Exact verified conclusions:

- `actual_forwardPrefix`: for any `Admissible L q` and `k ≤ L`, running the pure-List deterministic `forwardPrefix` with the unique actual inner high carry `DecimalDigits.carry q (L-k)` gives exactly the length-k prefix of `nextColumns q L`.
- `actual_forward_admitted`: that actual carry belongs to `{0,1}`, so enumeration of both high inner carries includes the actual output.
- `actual_longCompatible`: with `0 < k` as well, the actual prefix satisfies the columnwise inverse relation in `PrefixInverse.lean`.
- `actual_mem_prefixPredecessors`: the actual source prefix belongs to the executable inverse enumeration of the target prefix; coverage of actual transitions is not assumed as an extra premise.
- `wordPrefix_eq_range_map`: the recursive List prefix equals `(List.range k).map q`, allowing direct composition with the short-source module.

All conclusions require only `k ≤ L`, including overlapping end prefixes and `k=L`. In the latter case the actual high inner carry is zero. Seven columns is the specialization `k=7`. Both low-end and high-end carries are computed from the same complete actual word `q`, not assumed independent.

`forwardPrefix` corresponds entry by entry to one carry branch of `verify_certificates.py:forward_prefixes`: propagate low-end carries in forward order, then high-end carries in reverse order. Without overflow, add corresponding entries. With overflow, prepend 1 to the high-end digit sequence, then truncate and add to the low-end sequence's length. `highDigits_segment` establishes simultaneous equalities for the actual carries and digits of that reverse-order computation.

## Reproduction

At the repository root, set `P196_LEAN` to the Lean 4.19.0 executable; this execution used the environment-compatible wrapper `/workspace/scratch/7649db1e242c/toolchain/lean`. Run:

```sh
P196_LEAN=/path/to/lean P196_BUILD=/tmp/p196-projection-build \
  bash proofs/contributions/agent-104/seven-column-kernel/projection/verify.sh
```

Source dependencies are `proofs/research/continuation/LychrelDigitSums.lean` and the adjacent `PrefixInverse.lean`. `verification.json` records SHA-256 hashes for the dependencies and main source. `base-build.log`, `inverse-final-build.log`, and `final-build.log` preserve this build and the transitive axiom-audit output.

The seven final printed audits contain only the ordinary logical axioms `propext` and `Quot.sound`, plus `Classical.choice` for the relational bridge. There is no `sorryAx`, `Lean.ofReduceBool`, `native_decide`, or custom axiom.

## Historical attempts and scope

`draft-01` through `draft-03` preserve reserved-word naming errors and simplification-order errors in the overflow tail. `draft-04` is the first successful deterministic forward projection. The inverse bridge in `draft-05` failed because the recursive carry was unfolded too early; `draft-06` passes every bridge. The `sorryAx` entries in failed logs are Lean's error-recovery output for unfinished declarations, **not part of the final verification result**. Every original draft and log is retained, rather than replaced by the successful version.

This module does not prove the short-source branches, verify the five finite rank certificates, or imply the full P196 conjecture. It completes the exact semantic connection between an actual complete word and the long-prefix graph. Reproducible `.olean` files, compilation directories, and the toolchain are execution infrastructure, not research contributions.
