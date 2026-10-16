# Agent #101: numerical fibers from finite digit lists

## Checked result

`proofs/Agent101NumericFibers.lean` transports the complete digit-split
enumeration to **ordinary natural numbers** under the unchanged
`Lychrel196.step` implementation. Its defining map is
`numericFiber h c = (canonicalWords h c).map natValue`.

The principal checked statements are:

- `mem_numericFiber`: if every coefficient of `coefficientWord h c` is at
  most 18, membership is equivalent to the conjunction of the ordinary
  decimal-width interval and the exact numerical step equation.
- `numericFiber_nodup`: the numerical enumeration has no repetitions.
- `length_numericFiber`: its exact length is `profileCount h c`.
- `length_numericFiber_cons`: for a nonempty half-profile the length is
  `pairCount true s * centerCount c * natProduct (h.map (pairCount false))`.
- `length_numericFiber_cons_le`: the length is at most
  `9 * 10 ^ h.length`.
- `all_preimages_887`: the complete numerical inverse image of 887,
  across **all** input widths, is precisely
  `[790, 691, 592, 493, 394, 295, 196]`.

Here `decimalWidth n L` means
`0 < L ∧ 10 ^ (L - 1) ≤ n ∧ n < 10 ^ L`. The general fiber result is
deliberately a **fixed input width** result. Different input widths can
collide under reverse-and-add; the additional all-width claim is only the
explicit 887 example, where the other widths are independently excluded.

## Mathematical bridge and scope

Finite lists are least-significant-first. `digitFn` extends a list by zero,
and `natValue` applies the original `DecimalDigits.value` at the list length.
`canonical_to_list` restricts an arbitrary `Canonical n d L` witness to a
finite list without constraining or counting the irrelevant infinite tail
of `d`. `canonical_list_exists` supplies such a finite representation for
every positive integer.

The proofs establish numerical injectivity of canonical digit lists,
transport list zip-sums to `DecimalDigits.columnSum`, and reuse the original
fixed-width symmetric-coefficient injectivity theorem. The membership
theorem does not assume a profile has a digit realization: unrealizable
profiles are covered and yield empty numerical fibers. No statement about
infinite avoidance or the full 196 orbit follows from these results.

## Verification

Compiler: Lean 4.19.0, commit `6caaee842e94`, from the independently pinned
Agent #101 runtime. Compilation used an isolated directory and `LEAN_PATH=.`.
The dependency `Lychrel196Research__c696e0ea3db39d92.lean` was copied without
modification as `Lychrel196Research.lean`, then compiled before the four
Agent #101 modules. Its SHA-256 is
`f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`.

Final source SHA-256:
`bba80a597345f7f3bd207698a6e6b338ee20335e647f518604fa43654b13fd97`.

`numeric_v09_pass.log` records a successful compiler exit (0) with the
final module. Every exported definition/theorem has an axiom audit.
The final theorem audits use only the standard axioms `propext`,
`Classical.choice`, and `Quot.sound`; there is no `sorryAx`, new axiom,
`native_decide`, or `Lean.ofReduceBool`. The two small concrete checks use
kernel-checked `decide`.

`base_compile.log`, `full_pairs.log`, `full_bounds.log`, and
`full_enumeration.log` record the independently compiled dependency closure.
`numeric_v08_pass.lean` and `numeric_v08_pass.log` preserve the first complete
numerical-fiber milestone before the final concrete example was appended.

## Retained failed attempts

The `numeric_v01_failed.lean`, `numeric_v03_failed.lean`, and
`numeric_v05_failed.lean` files and their matching logs preserve useful
rejected proof attempts. They are historical evidence, not checked modules
and not dependencies. They document respectively a definitional addition
rewrite/explicit positivity issue, a step-value rewrite issue, and
Std-only decimal-width proof repairs. Any `sorryAx` printed in those failed
logs is Lean's diagnostic placeholder for an unsuccessful proof and is
absent from the successful final module's audit.

No compiled objects or runtime binaries are part of this evidence folder.
