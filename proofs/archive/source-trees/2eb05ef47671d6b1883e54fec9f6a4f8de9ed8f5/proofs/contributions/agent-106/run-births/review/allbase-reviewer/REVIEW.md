# Independent all-base review: PASS

Reviewer: the author of `OverflowBirths.lean`, not the author of either
file reviewed here. The two reviewed source files were treated as read-only.
No source correction was needed and no new mathematical theorem was added.

Frozen source SHA-256:

| Source | SHA-256 |
| --- | --- |
| `BaseBirths.lean` | `dcca96672161ac382020d476c6bf75d2b3b47456c76193cba55fdfcd6650af33` |
| `ActualBaseBirths.lean` | `e9fd9ed2a8065d7b6327d0400f7d94eea1049ba3f5b24241dcec244600121a6d` |

## 1. Integer-base boundaries

The local formula is exactly `(x+a)%b + (x+c)%b`, for integer base `b`,
`2 <= b`, `0 <= x <= 2*b-2`, and computed or supplied carry bits in `[0,1]`.
Both dividends lie in `[0,2*b)`, so the helper lemma's two intervals cover
every case. Positivity of `b` prevents negative-division or zero-base edge
cases. No primality, decimal-specific convention, or upper base bound is used.

Zero output requires both residues zero; maximal output requires both
residues `b-1`. Solving these two digit conditions gives exactly the three
alternatives in each theorem. Those alternatives remain disjoint at base 2.
The new-birth theorems remove precisely the unchanged old extreme; mixed
carry values cannot satisfy either extreme classification.

The stronger theorem that a birth has a strictly interior old coefficient
correctly requires `b >= 3`. At base 2, old `x=0` with carries `(1,1)` maps
to 2, and old `x=2` with carries `(0,0)` maps to 0. The proved binary control
therefore identifies a genuine sharp failure of the stronger conclusion,
not a failure of the complete classification. The all-base actual bridge
uses only normalization results valid at `b >= 2`; importing seam theorems
with stronger hypotheses does not silently impose those hypotheses here.

## 2. Actual carries and reset/template tags

`incoming b xs k` is the terminal carry of ordinary normalization of the
prefix `xs.take k`, starting at zero. It is not an arbitrary carry witness.
`ordinary_body_at` proves the pointwise link by induction on that same list.
`incoming_bit` obtains its bounds from the bounded prefix; it remains valid
when `k` exceeds the length because `take` then saturates, although the pair
classification itself explicitly requires `k < xs.length`.

Every actual-carry calculation uses `ordinaryTags`, which replaces every
Boolean reset flag by `false`. The actual output uses the same ordinary
tag projection; its second ordinary projection is removed using the proved
idempotence lemma. The no-overflow hypothesis is also the terminal carry of
this ordinary chain, not the terminal carry of a template with resets.
Consequently arbitrary old/template flags cannot change the actual result,
fake a no-overflow branch, or supply nonphysical incoming carries. Neither
flag symmetry nor a special placement of reset markers is needed.

## 3. Physical width, mirror indices, and positive leading digit

The branch test in `actualDigits` uses the computed terminal carry.
Under `hn`, `actual_nooverflow_body` removes the terminal zero slot rather
than retaining a padded output. `actual_nooverflow_length` proves the output
length equals `xs.length`. Thus the reflected index is exactly
`xs.length - 1 - k`; it is not the shifted overflow index. The hypothesis
`k < xs.length` proves that both accesses are within the real list.

For the final canonical theorem, `hqs` also equates source lengths with
`digits.length`. The imported `reverse_add_normalization` proves output
digit bounds, positive last digit, its actual length including any carry,
and its integer value. The no-overflow specialization therefore has the
original canonical width and a nonzero leading digit. `PositiveLast digits`
excludes empty and leading-zero input words, while zero *low* digits remain
allowed. A reversed word may have high zero digits, but `reversedValue`
evaluates those as zero, exactly as ordinary numerical reversal does.

`SignedDigitUniqueness.eval` is ordinary least-significant-first Horner
evaluation. The final value equality is therefore
`n + reverse_b(n)`, with `n = eval b digits > 0`; positivity follows from
the stated input hypotheses and the imported `canonical_input_positive`.
The result's digit bounds and positive last digit establish its canonical
integer representation. No fixed-width zero padding is being substituted
for that representation.

## 4. Symmetry versus actual realizability

There are deliberately three semantic layers:

| Layer | What the hypotheses establish |
| --- | --- |
| `BaseBirths.localPair_*` | Local arithmetic with a bounded coefficient and two bits |
| `ActualBaseBirths.actual_zero_iff` / `actual_max_iff` | The real ordinary normalization of a bounded symmetric coefficient list |
| `canonical_reverse_add_extremes` | A canonical positive integer's genuine reverse-and-add output |

Symmetry and coefficient bounds alone do **not** imply that the source
is a true mirror-sum word. For example the one-entry coefficient word `[1]`
is bounded, symmetric, and non-overflowing in base 2, but no one-digit
input has odd mirror sum 1. The middle-layer theorems do not assert this
missing realization and remain correct for that word.

The final theorem closes this issue with the explicit equality
`xs.map Prod.fst = pairs digits`, together with valid canonical input
digits. This supplies actual realizability, symmetry, the center-even
condition when applicable, coefficient bounds, nonempty width, and positive
outer coefficient. `hqs` constrains the *input* representation; it does not
assume the desired output formula. The actual output formula is separately
proved from ordinary carrying and the true reflected index. No semantic
gap was found in the final integer bridge.

## 5. Independent execution evidence

The reviewer created `fresh-build-001/` only after checking it did not
exist, copied source snapshots into it, and compiled all eight project
modules in dependency order. `LEAN_PATH` contained only this new directory.
The author's compiled oleans, shared build106 oleans, and other reviewers'
oleans were not used. Only the official Lean 4.19.0 runtime was shared.

All eight modules and a generated `AllAxioms.lean` exited with status 0.
The audit prints axioms for all 100 exported theorems across the complete
dependency closure. The only reported axioms are `propext`,
`Classical.choice`, and `Quot.sound`; some controls use none. No `sorryAx`,
custom axiom, `native_decide`, or compiler-trust escape appears. Dependency
source inspection also found no prohibited proof placeholder.

`rebuild.json` records source, snapshot, log, runtime, preload, script and
olean hashes; each exact compiler command, cwd, exit code, and source
stability check; and the complete audited theorem list. Per-module logs,
the combined axiom log, original source snapshots, and the entrypoint log
are retained. Existing unused-variable warnings in `ResetNormalization`
are harmless and retained rather than suppressed.

Supplementary independent Python controls checked 4,092 scalar cases in
bases 2 through 32. They also formed integers from canonical digit words,
reversed and added them numerically, then compared those independently
extracted output digits to coefficient normalization: all positive inputs
through width 7 in bases 2 and 3, and through width 4 in bases 4 through 10.
The physical width, positive leading digit, value, actual incoming carries,
and both same-width extreme classifications agreed in every tested case.
`semantic_controls.json` retains exact counts. These finite checks are
supplementary; the unrestricted conclusion rests on the rebuilt Lean proofs.

Acceptance is limited to the stated one-step arithmetic and canonical
no-overflow bridge. Neither source asserts infinite regeneration, invariant
closure, ancestry survival, or a Lychrel-existence result.
