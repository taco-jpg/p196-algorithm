# Long-buffer embedding into the original Agent13 finite family

Agent #108 runtime, session b31b8818. The owned source is
`proofs/Agent108WindowEmbedding.lean`.

Final source SHA256:
`1acb5964188bcb7828bec58cbd8b5328ff9d68467e5951eb3a4bf87d78eb4e7f`.

## Result and scope

For every natural `p`, insert `p` false bits before, between, and after the
chosen bits:

```lean
expandBits p es = List.replicate p false ++
  es.flatMap (fun e => e :: List.replicate p false)
```

The resulting list has length `p+(p+1)*es.length`. Its bit at
`p+(p+1)*j` recovers `es[j]?`, including the out-of-range case. Thus this
encoding is injective. Because an old false block is exactly four nines,
the original unbuffered half-word at these expanded bits is literally the
new half-word with physical buffer length `4*p`. The target half-words
agree as well.

The finite version uses the original Agent13 API without changing its
arithmetic definitions:

```lean
embeddedState p k r e =
  Agent13ProductWeights.familyState (p+(p+1)*r) k (expandFin p e)

embeddedTarget p k r =
  Agent13ProductWeights.targetState (p+(p+1)*r) k
```

Here `e : Fin r → Bool`. `embeddedState_spec` applies the original
`familyState_spec` directly, and `embeddedState_injective` composes the
original `familyState_injective` with the new bit embedding. No new carry,
reverse-and-add transition, or finite-safety proof is substituted for the
original arithmetic proof.

The original dependencies are the byte-identical modules from source
commit `12a32789056f5eec8247166564ac2ef745c3c9d6`; their source map and
independent build are recorded separately by the dependency reviewer.

## Public integration interface

All names below are in namespace `Agent108.WindowWeights`.

| Declaration | Interface |
|---|---|
| `expandBits_length` | Expanded list length is `p+(p+1)*es.length`. |
| `expandBits_getElem?` | Recover original option-valued bit at `p+(p+1)*j`, for every natural `j`. |
| `expandBits_injective` | The list encoding is injective. |
| `ofFn_expandFin` | `List.ofFn (expandFin p e) = expandBits p (List.ofFn e)`. |
| `inputHalf_expandBits` | `inputHalf 0 k (expandBits p es) = inputHalf (4*p) k es`. |
| `targetHalf_expandBits` | The corresponding target half-words agree. |
| `embeddedState_injective p k r` | Actual finite source states are distinct for distinct finite bit functions. |
| `embeddedState_spec p k r e hk` | Source is `SafeState` and `MapsTo` the target, with only `0<k` required. |
| `embeddedTarget_safe p k r hk` | The target is safe for `0<k`. |
| `embeddedState_width` | Source width is `2*halfWidth (p+(p+1)*r) k`. |
| `embeddedTarget_width` | Target has the same explicit even width. |
| `embedded_width_eq` | Source and target widths agree exactly. |
| `embeddedState_half` | `finiteStateHalf (embeddedState p k r e) = inputHalf (4*p) k (List.ofFn e)`. |
| `embeddedTarget_half` | `finiteStateHalf (embeddedTarget p k r) = targetHalf (4*p) k r`. |

The extraction used by these final equalities is defined for every finite
state:

```lean
finiteStateHalf s = (List.range (s.1/2)).map (Agent13ProductWeights.digits s)
```

For a window width `d=b+1`, take `p=d`. This gives physical buffer
`4*d`, while the weight factorization retains its independently chosen
window width. The window factorization must account for the extra pure-nine
windows; the embedding does not identify physical buffer length with
window width. The family contains the `r=0` case, and its list equalities
also hold at `p=0` and `k=0`. Arithmetic safety and transition assertions
retain the original requirement `0<k`.

This module does not prove a weighted-sum identity, the full incoming
operator bound, or avoidance of palindromes for infinitely many steps.
It provides the actual finite-state and literal-half interfaces needed by
the separately owned weight and incoming modules.

## Verification and retained attempts

The final successful attempt is `attempts/006`. A new empty local build
directory was used for each attempt. The final run compiled the pinned
`Agent108WindowDefs`, the owned source, and an explicit `#print axioms`
audit of all 41 public source declarations. All three commands used
official Lean 4.19.0 with `--trust=0` and exited 0. The final source bytes
were unchanged after the run.

Every one of the 41 declarations has exactly one retained axiom report.
Each transitive dependency set is a subset of
`{propext, Classical.choice, Quot.sound}`. No compiler-generated name is
used to expand that allowlist.

The build reuses pinned Mathlib
`c44e0c8ee63ca166450922a373c7409c5d26b00b` and the independently rebuilt
original Agent13 dependency closure. This is an incremental source build
of the new modules, not a claim to have rebuilt Mathlib from source.
`latest-verification.json` records the exact commands, dependency paths,
source hashes, exit codes, and axiom correspondence. Full stdout and
stderr are retained beside each exact source snapshot.

Actual unsuccessful attempts are retained:

- `001`: a redundant tactic after `simp` had already solved the goal, and
  a `change` step needed explicit removal of an appended empty list.
- `005`: a redundant `Option.map_some` rewrite did not match the native
  `Option.map` expression. Removing that rewrite allowed the already
  definitionally equal expression to close directly.

Successful staged attempts `002`, `003`, and `004` remain available as
earlier verified interfaces. They are superseded by the complete fixed
source in `006`.
