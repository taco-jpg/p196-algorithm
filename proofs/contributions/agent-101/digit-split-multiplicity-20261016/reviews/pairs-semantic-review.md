# Independent semantic review: Agent101DigitPairs

## Scope and independence

Reviewer: Agent 101 research/enumeration subagent (`/root/research_inventory`).
I did not author `Agent101DigitPairs.lean`. I did author
`Agent101SplitEnumeration.lean`; this report is **not** an independent review
of the enumeration module. The review covers the digit-pair and optional
center definitions, their membership and no-duplicates specifications, and
the exact count proof's use of kernel-checked `decide`.

Reviewed source: `proofs/Agent101DigitPairs.lean`.

SHA-256:

```text
5c76eae97efd2f30d1775650f7feca477c269419af1c02809800a95ca62821f8
```

**Conclusion: PASS.** I found no semantic mismatch or uncovered parameter
case in this module. The count theorem is universal over `Nat`; its finite
verification covers precisely the bounded branch, and a separate symbolic
proof covers every larger pair sum.

## Digit-pair semantics

`pairChoices outer s` starts from exactly the 100 ordered pairs `(a,b)` with
`0 ≤ a ≤ 9` and `0 ≤ b ≤ 9`, and filters by `a + b = s`. Here `a` is the low
digit and `b` the high digit. The extra condition for `outer = true` is
`0 < b`; zero remains allowed for `a`. Distinct ordered pairs, such as
`(3,7)` and `(7,3)`, represent different original digit assignments and are
correctly retained separately. A diagonal pair appears once.

`mem_pairChoices` is an exact equivalence, including both decimal bounds,
the specified sum, and the conditional nonzero high digit. It does not
merely establish soundness of returned pairs. `pairChoices_nodup` proves
that the original 100-pair list has no duplicates and transports this
property through filtering.

For internal pairs, the count is `s + 1` through `s = 9`, then `19 - s`
through `s = 18`, then zero. In the first branch the unique split with
high digit zero is removed for an outer pair, giving `s`. In the second
branch a high digit zero is impossible already, so the outer and internal
counts agree. The subtraction `19 - s` occurs only where `s ≤ 18`.

The boundary values of the reviewed definitions are:

| Pair sum | Internal count | Outer count | Relevant boundary |
|---:|---:|---:|---|
| 0 | 1 | 0 | `(0,0)` is internal only |
| 1 | 2 | 1 | outer high digit must be positive |
| 9 | 10 | 9 | last increasing-branch value |
| 10 | 9 | 9 | first decreasing-branch value |
| 18 | 1 | 1 | only `(9,9)` |
| 19 or larger | 0 | 0 | no bounded decimal pair |

These are consequences of the source definitions and the accepted universal
count theorem; this table is explanatory, not an additional proof method.

## Exact scope of `decide`

There are two proof uses of `by decide`:

1. `pairChoices_nodup` checks the fixed, unfiltered 100-pair list. The
   subsequent filtering lemma is valid for every `outer` and `s`.
2. In `length_pairChoices`, the local theorem
   `∀ o : Bool, ∀ t : Fin 19, (pairChoices o t.val).length = pairCount o t.val`
   checks all **38** combinations of the two outer flags and the sums
   `0, …, 18`.

The second computation is applied only after establishing `s ≤ 18` and
constructing the corresponding `Fin 19`. For `s > 18`,
`pairChoices_eq_nil_of_large` uses exact membership and the two digit bounds
to prove the enumeration empty. The closed form is independently simplified
to zero in this branch. No unbounded quantifier is discharged by a bounded
sample, and no out-of-range natural number is silently coerced or reduced
modulo 19.

The source uses ordinary `decide`, not `native_decide`, `axiom`, `sorry`, or
an externally trusted result. Its finite decision proofs are checked by the
Lean kernel. The axiom reports below agree with that boundary.

## Optional-center semantics

`centerWords none = [[]]` correctly contributes one empty inner word and
zero digits. For a present coefficient `s`, it contributes exactly the one
digit word `[s / 2]` when `s ≤ 18` and `s % 2 = 0`; otherwise it contributes
no word. Thus the admitted coefficients are precisely `0,2,…,18`, with
digits `0,1,…,9` respectively. Integer division does not admit odd sums
because the parity condition is checked explicitly.

In particular, `centerWords (some 0) = [[0]]` is intentional at this local
layer. A zero center is allowed inside a longer number. Whether a one-digit
zero is canonical is decided by the outer enumeration layer, not by this
module. `centerCount` counts words, so `centerCount none = 1`, not zero.
`mem_centerWords`, its two specialized interfaces, `centerWords_nodup`, and
`length_centerWords` accurately express these cases.

## Independent rebuild and axiom evidence

I copied the exact reviewed source to
`pairs-semantic-review.Agent101DigitPairs.lean` and compiled that snapshot
with `LEAN_PATH` unset. The source imports only `Std`; no project `.olean`
was used by this rebuild.

Compiler:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

Result: **Lean exit code 0**. The snapshot matched the reviewed source at
the time of compilation. All 14 source-level axiom reports were produced:
the four definitions have no axioms; the ten theorems depend only on subsets
of `propext`, `Classical.choice`, and `Quot.sound`. There is no `sorryAx` or
project-specific axiom.

Evidence files in this directory:

- `pairs-semantic-review.Agent101DigitPairs.lean`: exact source snapshot.
- `pairs-semantic-review.lean.log`: raw compile and axiom output.
- `pairs-semantic-review.json`: command, source hash, version, exit code,
  import-path condition, and elapsed time.

No source modification or new mathematical theorem was made for this
review.
