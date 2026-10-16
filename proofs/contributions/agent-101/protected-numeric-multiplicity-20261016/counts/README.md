# Agent #101: protected-family ordinary-integer multiplicity

## Checked result

`proofs/Agent101ProtectedMultiplicity.lean` defines

```lean
Agent101.Protected.protectedSeeds m k =
  (P196.Agent3.OverflowHorizon.allBits m).flatMap fun xs =>
    Agent101.numericFiber (P196.Agent3.OverflowHorizon.inputHalf xs k) none
```

The coefficient half is the unchanged Agent #3 definition
`[14] ++ xs.map choice ++ replicate k 18`, where false selects 5 and true
selects 14. The complete coefficient word is that half followed by its
reverse. Every canonical decimal digit split of every indexed profile is
included in the ordinary-natural-number list.

The module proves:

- `mem_protectedSeeds`: complete membership through all Boolean words of
  length `m` and their complete numerical digit-split fibers.
- `mem_protectedSeeds_numeric`: complete membership using ordinary numeric
  step equations and the exact decimal width `2 * (m + k + 1)`.
- `inputFiber_index_unique` and `inputFibers_disjoint`: distinct Boolean
  words have disjoint numerical fibers. This is proved from canonical
  finite digit-list injectivity and Agent #3's word injectivity.
- `protectedSeeds_nodup`: no ordinary seed is repeated in the flat-map
  enumeration.
- `length_protectedSeeds`: the exact number of distinct ordinary seeds is
  `5 * 11 ^ m`, for every `m` and `k`, including `k = 0`.
- `protectedSeeds_exact`: the exact count, no repetitions, positivity of
  each seed, and the uniform ordinary decimal-width interval together.

The counting proof gives five choices at the outer coefficient 14. Each
inner Boolean position contributes six splits for coefficient 5 or five
splits for coefficient 14. Each protective coefficient 18 contributes one
split. The recursion over the complete Boolean enumeration therefore
multiplies the total by eleven at each position.

## Scope

This is the complete digit-split count **within the specified Agent #3
profile family**. It does not assert that this family contains every
possible two-step numerical predecessor of a common image. It makes no
all-time palindrome-avoidance claim. Counting allows `k = 0`; finite-horizon
results imported in other modules must retain their separate `0 < k`
hypothesis. Initial palindrome exclusion and normalized-value/safety
transport are separate modules.

## Pinned dependencies and provenance

The module imports `Agent101NumericFibers` and `FamilyCardinality`.
Agent #3's six original source files are preserved byte-for-byte under
`../dependencies/agent3/`, with all original module names. Their fixed
source commit is `5084eadce9a7e95e518332c29e8404b00214bd0f` from PR #81.
All six mathematical source files are byte-identical to their versions at
`6576cee93d18145c638f298b0abcb1cd0a0f451e`. The adjacent dependency manifest
records original repository paths, Git blobs, SHA-256 values, and sizes.

The accepted numerical module remains unchanged, SHA-256
`bba80a597345f7f3bd207698a6e6b338ee20335e647f518604fa43654b13fd97`.
The exact original foundational module remains unchanged, SHA-256
`f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`.
This counting module needs no foundational import adapter because the
imported Agent #3 cardinality chain is Std-only.

## Verification

Final source SHA-256:
`503dcb1c7d90f031a54caffb89ce8a632edbdc77c9383d06dbacfdbffaf0c1ac`.

The final module compiled with Lean 4.19.0, commit `6caaee842e94`, both
normally and using `--trust=0`; both commands exited 0. All 18 module
declarations have explicit axiom audits. Only `propext`, `Classical.choice`,
and `Quot.sound` occur. There is no `sorryAx`, new axiom, `native_decide`, or
`Lean.ofReduceBool` in the checked module or its final audit.

`verification.json` records exact paths, compiler hash, command arguments,
declaration names, and the verification scope. These are author-local checks;
independent whole-closure review is recorded separately.

`counts_v01_failed.lean.txt` and `counts_v01.log` retain the first rejected
attempt. Its two failures concerned simplification of the trailing product
of ones and multiplication reassociation; the final proof uses explicit
product lemmas. Any `sorryAx` in that failed log is a rejected-proof
diagnostic, not an accepted dependency. `counts_v02_pass.lean.txt` preserves
the first complete checked mathematical checkpoint.

Compiled objects and copied runtime infrastructure are not retained here.
