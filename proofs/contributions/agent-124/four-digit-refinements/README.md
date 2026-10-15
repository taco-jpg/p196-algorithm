# Agent 124: four-digit refinements of unresolved three-digit prefix classes

Task `agent124-four-digit-refinements` on `p196/coordination` (claim commit
`033f3f4`). Branch `research/agent-124/s20261015T1600`.

**Decimal Lychrel existence and the claim for 196 remain unproved.** This
task targets restricted palindrome families only.

## Target

The 500 three-digit classes of
`proofs/contributions/2026-10-15-seven-column-prefix/development/remaining_prefixes.txt`
have no uniform ancestry bound from the existing certificates (Agent #117 is
diagnosing them at seven to nine columns). Their four-digit refinements can
nevertheless close: in the same exact prefix abstraction (Agent #104's
complete inverse plus exact short-source edges), 1,841 of the 5,000
refinements are finite and acyclic at some width k <= 6. Excluding the ten
refinements of 739 (implied by Agent #104's 739 theorem) and the two
overflow-compatible classes 1120 and 1121, the target is 1,830 four-digit
classes `abcd` (1,267 at k = 4, 463 at k = 5, 100 at k = 6), listed with
widths and bounds in `exploration/four_digit_targets.json`. For each: every
positive ordinary decimal integer reaching a palindrome that begins `abcd`
does so within the listed bound (at most 48), and the 196 orbit never
contains such a palindrome.

## Status

| Width | Classes | Certificate | Status |
|---|---:|---|---|
| k = 4 | 1,267 | `certificate/f4/`, 7,152 nodes, max rank 20 | **LEAN-CHECKED, dev build** |
| k = 5 | 463 | 72,224 nodes (exploration) | WIP |
| k = 6 | 100 | 324,781 nodes (exploration) | WIP |

"Dev build": compiled with official Lean 4.19.0 (`6caaee842e94`) in a working
directory with the unchanged accepted base modules; a clean empty-directory
rebuild and exhaustive audit are still to come.

### Four-column endpoints (namespace `Agent124.CertF4`, module `A124F4Final`)

The 1,267 classes are split into seven lists `entries00` … `entries06`
(module `A124F4Entries`) of pairs `(digits, r)`. For each list `i`:

- `ancestry_0i : ∀ e ∈ entries0i, ∀ A P t, 0 < A → PalStartsL e.1 P → Lychrel196.orbit A t = P → t ≤ e.2 + 1`
- `no_196_0i : ∀ t, ∀ e ∈ entries0i, ¬ PalStartsL e.1 (Lychrel196.orbit 196 t)`

All 14 endpoints report exactly `propext`, `Classical.choice`, `Quot.sound`
(`logs/f4/A124F4Final.log`). The largest ancestry bound in this batch is 21.

`PalStartsL pre P` (`Agent124PrefixL.lean` in `../prefix-five-six/`) is
`Palindrome P` together with a canonical decimal representation of `P` of
width `W ≥ pre.length` whose leading digits are `pre`; for three digits it is
equivalent to `PalStarts3` (`palStartsL_three_iff`), which is definitionally
Agent #104's accepted family at 7,3,9.

Each entry's Boolean check `entryOK` verifies, by kernel reduction, that the
prefix has length between 1 and k, that a final overflow into the target is
impossible (leading digit at least two or some prefix digit at least three:
an overflow palindrome has every digit at most two,
`Agent124.LeadOne.overflow_palindrome_digits_le_two`), and that every word of
the finite initial family `initialWordsL k pre` has rank at most the listed
bound. `Agent124.PrefixL.ancestry_of_entries` turns this into the actual-orbit
theorem; the row and short-descent checks are those of `Agent124.CodeCert`.

## Exploration (untrusted)

`exploration/screen4.cpp` (C++, validated against the published 739
certificate: 58,501 nodes, bound 39) and its raw outputs `ref4_k*.jsonl`.
At k = 7 only 32 of the remaining 3,159 refinements close
(`exploration/ref4_k7.jsonl`). CYCLE means the abstraction cannot certify
that class at that width, not that its ancestry is unbounded.
