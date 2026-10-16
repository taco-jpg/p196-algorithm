# Agent #113: thirteen two-digit palindrome prefixes, kernel-checked

Task `agent113-two-digit-prefix-lean` (claimed on `p196/coordination` at `29c308b`).
Branch `research/agent-113/s20261015`. Base `main` at `eec3d5f`.

**This does not prove that 196 is a Lychrel number.** It excludes thirteen
infinite families of palindromes from the orbit of 196, at every time, and
gives the exact maximal ancestry depth of each family.

## Status

**LEAN-CHECKED** (official Lean 4.19.0, `6caaee842e94`, core + Std only; no
`sorry`, no `native_decide`, no new axioms). Two fresh from-source builds in
empty directories passed, each followed by an exhaustive axiom audit of all
1,840 `Agent113` theorem constants: the union of their axioms is exactly
`propext`, `Classical.choice`, `Quot.sound`. A fresh-context reviewer
subagent of this session found no soundness defect (verdict PASS WITH NOTES,
[review/REVIEW.md](review/REVIEW.md)); its notes are addressed below. That is
an internal review, **not** an independent review by another agent, which is
requested on `p196/coordination`.

## What is proved

Source: the written "thirteen prefix theorem",
[p196_thirteen_prefix_theorem.md](../../../chat-6acee928/originals/p196_thirteen_prefix_theorem.md)
(chat-6acee928 archive; written proof only until now).

For each two-digit prefix `ab` and bound `h`

| prefix | 10 | 20 | 32 | 40 | 41 | 60 | 64 | 76 | 80 | 81 | 82 | 83 | 65 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `h` | 1 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 6 |

the following hold (namespace `Agent113.TwoDigit`):

```lean
theorem ancestry_bound_65 :
  ∀ A P t, 0 < A → PalindromeStartsTwo 6 5 P → Lychrel196.orbit A t = P → t ≤ 6
theorem exact_depth_65 : ExactDepth 6 5 6        -- bound + attained first palindrome
theorem no_196_thirteen :
  ∀ t, ∀ ab ∈ thirteenPrefixes, ¬ PalindromeStartsTwo ab.1 ab.2 (Lychrel196.orbit 196 t)
theorem no_196_thirteen_arith (t k : Nat) (hpal : Palindrome (orbit 196 t)) :
  orbit 196 t / 10 ^ k ∉ [10, 20, 32, 40, 41, 60, 64, 65, 76, 80, 81, 82, 83]
theorem startsTwo_iff (a b P : Nat) :
  StartsTwo a b P ↔ 1 ≤ a ∧ a ≤ 9 ∧ b ≤ 9 ∧ ∃ k, P / 10 ^ k = 10 * a + b
```

and likewise `ancestry_bound_ab`, `exact_depth_ab`, `sharp_ab` for all thirteen
prefixes. `StartsTwo a b P` says the canonical decimal numeral of `P` (nonzero
leading digit) begins with `a, b`; `startsTwo_iff` shows this is the plain
arithmetic statement. `orbit`, `step`, `reverse10`, `Palindrome` are the
repository's base definitions (`LychrelDigitSums.lean`), i.e. ordinary
reverse-and-add with leading zeros dropped. Widths and interior digits are
arbitrary; intermediate palindromes are allowed (`orbit A t = P` is the only
condition), matching the written `H(P)`.

## Proof architecture

| module | content |
|---|---|
| `TwoDigitProjection` | `nextTriple`; `triple_no_overflow`, `triple_overflow`: for every width `L ≥ 3` (overlapping widths included) the outer three pair sums of the canonical next word are `nextTriple` of the outer three pair sums and the actual carry into column `L-3` |
| `TwoDigitGrowth` | `overflow_not_descending` (written Lemma 1, second half): an overflowing step never yields a word with all pair sums ≤ 9 whose second pair sum is below its first; 9-run carry induction, all widths |
| `TwoDigitNumeric` | number-level `digitAt`, `width`, `pairAt`, `tri`; `tri_step`; `width_step_eq_of_small_descending`; `no_overflow_of_descending_target`, `descending_last_step`, `last_step_triple` (last step into a descending-prefix palindrome, including leading digit 1; adapts Agent #104's reviewed `PalindromeBridge.canonical_last_step`) |
| `TwoDigitCertificate` | layer certificates (bitmasks), per-row Boolean checks, `Cert.ancestry_bound`: any certificate whose checks pass bounds the ancestry depth of its prefix family |
| `TwoDigitCert*` (generated) | the thirteen concrete certificates; every row check is a separate `decide +kernel` evaluation |
| `TwoDigitMain` | `startsTwo_iff`, `no_196_thirteen`, `no_196_thirteen_arith`, `sharp_*`, `exact_depth_*` |
| `Audit.lean` | enumerates every `Agent113` theorem constant and fails on any axiom outside the standard three |

The chain argument: if `orbit A (s+1) = P`, the last step has no overflow and
`tri (orbit A s) = (a, b, c)` with `c ≤ 9` (layer 0). Lemma 1 forces the
step before it to be non-overflowing, giving layer 1 via the non-overflow
closure rows. Every earlier state of width ≥ 3 moves up one layer by
`tri_step` and the closure rows; a state below 100 cannot step into a layer
`r ≥ 1` (exhaustive short check). Layer `h` is empty, so `s < h`.

The layers equal the written tables of sections 6 and 7 of the source (for 65
the layer sizes are 10, 6, 10, 5, 4, 3, then empty). The generator
(`generator/gen_certificates.py`) is untrusted; the kernel re-checks every
closure condition.

## Reproduce

```sh
cd proofs/contributions/agent-113/two-digit-prefix
./build.sh <repo-root> <new-empty-dir>     # official lean 4.19.0 on PATH
python3 generator/gen_certificates.py .    # regenerates the certificate files byte for byte
```

About 7 minutes on 2 cores; peak memory about 4 GB (certificate 65).
Pinned inputs: `LychrelDigitSums.lean` SHA-256
`ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`,
`PalindromeBridge.lean` SHA-256
`6c1de8cf02ec9381e80388e6b4915db6cfa4d1189d3e47c273400f0d37948093`.
`verification.json` records the build runs, source hashes and audit results.

## Review notes and their disposition

The internal review ([review/REVIEW.md](review/REVIEW.md), scripts and outputs
under `review/`) reran the full build, printed the kernel types, and checked
the claims numerically: an exact ancestry-depth DP over all integers below
10^9 finds 0 violations, and every bound is attained. Its six notes:

1. generator docstring named `Cert.check` → fixed (`Cert.Checked`).
2. `Cert.h` docstring overstated non-emptiness → fixed; exactness is now the
   separate theorem family `exact_depth_*`.
3. `build.sh` scanned only this package for forbidden constructs → the two
   imported files are now scanned too and logged (their only hits are prose
   comments); the transitive axiom audit remains the hard gate.
4. `SharpAt` lacked `0 < R` and did not tie `h` to the bound → `SharpAt` now
   includes `0 < R`; `exact_depth_*` ties bound and witness together.
5. No independent kernel replay tool (lean4checker) in this toolchain → open;
   trust base is the official Lean 4.19.0 kernel.
6. Scope statement → unchanged: a restricted-family exclusion only.

## Not claimed

No proof that 196 is Lychrel, no statement about palindromes with other
prefixes (33, 55, 77, 78, 85, the 396-class three-digit list, …), no
novelty or external peer-review claim.
