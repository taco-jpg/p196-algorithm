# Complete predecessor-list boundary controls

**PASS for the two targeted kernel controls.** Frozen source `proofs/Agent105PredecessorControls9df76b.lean`, SHA-256 `2286e7580ef72d122db6a8c9368aeb4d16aba21d69045ead33e1b9e3ce9378c2`. The only imported module is `Agent105Predecessors9df76b`; no Witness dependency was introduced.

| Actual numerical target | Canonical digits, low first | Complete computed list |
|---:|---|---|
| 1 | `[1]` | `[]` |
| 2 | `[2]` | `[1]` |
| 10 | `[0,1]` | `[5]` |
| 121 | `[1,2,1]` | `[110,92,83,74,65,56,47,38,29]` |

`order-probe-001` first ran the actual executable through Lean to determine the order. The two final theorems are `Agent105PredecessorControls9df76b.small_targets` and `Agent105PredecessorControls9df76b.two_width_121`. They include a canonical certificate for each actual target, so the computed lists can be composed directly with `mem_predecessors` to classify positive ordinary reverse-add predecessors. The 121 list contains both actual source widths, with the width-three branch first.

`kernel-attempt-002` compiled the exact frozen source with official Lean 4.19.0 and explicit `--trust=0`, exit 0, in 0.491 seconds. Both `#print axioms` reports contain only `propext` and `Quot.sound`. List equalities are kernel `decide` proofs; canonical literal targets use the existing finite-list bridge and `simp`. No large reversal computation was requested.

The original `kernel-attempt-001` failed because a `Decidable` instance was unavailable for the opaque `canonicalDigits` predicates. Its source, full error log, and exit-1 receipt remain retained. Unfolding the finite list predicates for `simp` resolved the issue without changing any statement, computed list, or imported mathematical source. The failed log's generated `sorryAx` placeholders are part of that rejected attempt, not the final proof.

All these small runs reused recorded source/olean caches. They did not rebuild the foundation and do not constitute the new project's complete independent fresh replay. That final closure and module-origin audit will follow only after the complete source checkpoint and registry are published.
