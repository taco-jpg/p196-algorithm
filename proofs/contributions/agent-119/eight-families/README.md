# Agent #119: eight `dd 0^(2r) dd` palindrome families never occur in the orbit of 196

Task `agent119-eight-families-lean` (claimed on `p196/coordination` at `7891ad3`).
Contribution branch `research/agent-119/s20261015T2005-eight-families`, base `main` `6d56f54`.

**Evidence label: Formal theorem** (Lean 4.19.0 kernel; standard axioms only).
**Status: LEAN-CHECKED.** Clean-rebuild evidence and review status are recorded below and in
the task record. The family `d = 5` is **not** treated and remains open. Nothing here proves
that 196 is a Lychrel number.

## Statement

`fam d r = 11 * d * (10^(2r+2) + 1)` is the palindrome with decimal digits `d d 0^(2r) d d`
(for example `4444`, `440044`, `44000044`).

| Lean theorem | Statement |
|---|---|
| `Agent119.EightFamilies.orbit196_ne_fam` | `d ∈ {1,2,3,4,6,7,8,9} → Lychrel196.orbit 196 t ≠ fam d r`, for every `r` and every `t` |
| `Agent119.EightFamilies.orbit196_digits_ne_fam` | the same in digit form: no canonical numeral of `orbit 196 t` of width `2r+4` has digits `famDigit d r` |
| `Agent119.EightFamilies.fam_canonical` | the canonical decimal digits of `fam d r` (`1 ≤ d ≤ 9`) are `famDigit d r`, width `2r+4` |
| `Agent119.EightFamilies.orbit196_not_dvd3` | no member of the 196 orbit is divisible by 3 |
| `Agent119.EightFamilies.orbit196_dvd11` | every member from time 3 on is divisible by 11 |

Written source: section 3 of `proofs/chat-6acee928/originals/p196_all_palindromes_and_eight_families.md`
(written proof and Python checks only). The statement covers every time `t`, including times
after an earlier palindrome, exactly as in the written source.

## Proof

All reasoning is about the actual decimal map of the pinned base module. `V t` is the exact
(width, pair-sum word) state of `orbit 196 t` (`iterPairs` started from the canonical digits of
196), linked to the canonical digits of the orbit by `iterPairs_representation`.

* `d = 3, 6, 9`: `fam d r` is divisible by 3, while `orbit 196 t ≡ 196·2^t ≢ 0 (mod 3)`.
* Times `t ≤ 4` and the width-four members `dddd` are excluded by direct computation and
  size (`early_or_short`). Below, `t = s + 1 ≥ 5` and `r ≥ 1`.
* Final step overflowing (`last_step_overflow`): the target must begin with 1, so `d = 1`;
  the exact overflow palindrome criterion then gives the source pair-sum prefix `[11,0,0]`,
  which has no predecessor in Agent #104's complete prefix inverse (`no_pred_11_0_0`).
* Final step not overflowing (`last_step_no_overflow`): no carries, so the pair-sum word of
  `M = orbit 196 s` is exactly the digit word of `fam d r`.
  * Overflow onto `M` (`middle_overflow`): `M` has leading digit 1 and interior zeros; with
    `11 ∣ M` its digits are `1 1 0^(2r) (d-1)(d-1)`, and the two outer column equations of
    the source leave only `d ∈ {1,2}`. For `d = 2`, `M = fam 1 r`. For `d = 1`, every inner
    column carries, so the odd-width source has the odd centre pair sum 9, contradicting
    admissibility.
  * No overflow onto `M`: for `d = 1` the outer pair sum of `M` would be at least 2
    (`middle_no_overflow_one`). For even `d`, Agent #104's `NoOverflow` relation read from
    carry state `(0,0)` forces the source to be half the target, so `M = fam (d/2) r`
    (`noOverflow_half`, `middle_no_overflow_even`). For `d = 7`, the source prefix is
    `[3,13,9,9]`, its predecessors begin `[1,16]`, and `[1,16]` has no predecessor
    (`seven_chain`).
* `reduce` combines these cases; the chain `1 → 2 → 4 → 8` and the case `7` give the theorem.

The descent `M = fam (d/2) r` steps back along the actual orbit by one addition; no division
by 11 along the orbit is used.

Reused **unchanged**: base `proofs/research/continuation/LychrelDigitSums.lean`
(SHA256 `ca5f4652…0b57`) and Agent #104's integrated `PrefixInverse`, `ActualPrefix`,
`PalindromeBridge`. `check.py` pins all four.

## Reproduce

```sh
python3 proofs/contributions/agent-119/eight-families/check.py /path/to/lean-4.19.0/bin/lean \
  --evidence /new/empty/dir --jobs 2
```

It copies the five-module import closure into a fresh snapshot, verifies the pins, compiles
with `lean -j1 -DElab.async=false`, audits every Agent #119 theorem constant with
`#print axioms` and writes `verification.json`.

## Scope and limits

Only these eight one-parameter families are excluded. Apart from `d = 3` (class `33`, already
closed by the four-column certificates) and `7777` (class `777`), their members lie in
three-digit classes outside the 397-class written baseline: `110`/`111` (growth classes),
`220`/`222`, `440`/`444`, `660`/`666`, `770`, `880`/`888`, `990`/`999`. The exclusion uses the
196-specific residues modulo 3 and 11, which the ancestry certificates do not use. `d = 5`
(`55 0^(2r) 55`) is not excluded: the written source shows an orbit with the same residues
modulo 99 that reaches a member of that family.
