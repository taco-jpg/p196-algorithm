# Agent #119: four-column three-digit palindrome-prefix kernel

Task `agent119-four-column-prefix-kernel` (claimed on `p196/coordination` at `b2c4da7`).
Contribution branch `research/agent-119/s20261015T1555`, base `main` `eec3d5f`.

**Evidence label: Formal theorem** (Lean 4.19.0 kernel; standard axioms only).
**Status: LEAN-CHECKED (clean rebuilds PASS at `3bb721d` and `ca95951`), independently reviewed (PASS) at `3bb721d`**;
the only later Lean source change is a comment-only docstring correction (see *Verification*).

**Scope.** These are restricted palindrome-family exclusions. They do not prove that 196
is a Lychrel number, do not settle decimal Lychrel existence, and claim no optimality of the
listed bounds (except that the bound 5 of the class 33 is attained).

## Results

`T(n) = n + reverse(n)`, iterated without stopping at intermediate palindromes
(`Lychrel196.orbit`, `Lychrel196.step`, `Lychrel196.Palindrome` from the pinned base module).
`Starts3 a b c P` means: the canonical decimal numeral of `P` has at least three digits and its
three most significant digits are `a, b, c`.

| Lean theorem | Statement |
|---|---|
| `FourColumnKernel.Certificate.ancestry_bound` | `(a,b,c,B) ∈ table4 → ∀ A P t, 0 < A → PalindromeStarts3 a b c P → orbit A t = P → t ≤ B` |
| `FourColumnKernel.Certificate.no_196` | `(a,b,c,B) ∈ table4 → ∀ t, ¬ PalindromeStarts3 a b c (orbit 196 t)` |
| `FourColumnKernel.Certificate.no_196_listed_prefix` | every palindrome in the 196 orbit avoids every prefix listed in `table4` |
| `FourColumnKernel.Certificate.ancestry_bound_33` | every palindrome beginning `33` (any width ≥ 2, including `33`) has ancestry depth ≤ 5 |
| `FourColumnKernel.Certificate.no_196_33` | the 196 orbit never reaches a palindrome beginning `33` |
| `FourColumnKernel.Certificate.sharp_33` | `orbit 1109090 5 = 33266233`, a palindrome, with no earlier palindrome (bound 5 attained) |

`table4` (`certificate/Table4.lean`) has the 229 classes of the 360-class table in
`proofs/chat-6acee928/originals/p196_four_column_obstruction.md` §6 that no other task owns:
the written table minus all extensions of Agent #113's thirteen two-digit prefixes
`{10,20,32,40,41,60,64,65,76,80,81,82,83}` (130 classes) and minus `620` (Agent #104).
Every bound equals the written bound. Bound distribution:
1:43, 2:30, 3:65, 4:29, 5:15, 6:7, 7:7, 8:13, 9:5, 10:4, 11:2, 12:7, 13:1, 14:1 (max `561:14`).
Thirty classes have leading digit 1 (`120`, `130`, …, `196`, `197`).

Previously these classes had a written proof and a Python finite certificate only.

## Proof structure

| File | Content |
|---|---|
| `FourColumnAncestry.lean` | `project4` (first `min L 4` pair sums); the 207 admissible short words of widths 1–3; decidable short-transition descent check; `actual_iterPairs_rank4`: an actual time-`t` pair state whose projection has checked rank `r` satisfies `t ≤ r` |
| `ThreeDigitBridge.lean` | `overflow_palindrome_prefix`: an overflowing step onto a palindrome of width ≥ 3 has prefix 110, 111, 121 or 122 (from the exact overflow criterion of the base and two carry equations), so leading digit 1 is covered; `canonical_last_step3`; finite root family `rootWords`; `time_bound_of_root`; conditional endpoints `ancestry_bound_of_checks`, `no_196_of_checks` |
| `certificate/Rank4Data.lean` | generated rank tree, 7,776 words (33 short), max rank 13 |
| `certificate/Rows4_*.lean`, `AllRows4.lean` | every row checked against the complete proved inverse by `decide +kernel` (`allRows`) |
| `certificate/Short4.lean` | exact short descent for all 207 short words by `decide +kernel` (`shortDescent4`) |
| `FourColumnConclusion.lean` | `table4_checked` (`decide +kernel`), all endpoints above, class 33 |

Reused **unchanged** (Agent #104, integrated and reviewed): `PrefixInverse`, `FastInverse`,
`ActualPrefix` (its projection theorem is generic in the prefix width), `ShortBoundary`,
`PrefixCertificate`, `PalindromeBridge`, `certificate/LongRowsBase`, `certificate/FastRowsBase`;
base `proofs/research/continuation/LychrelDigitSums.lean` (SHA256 `ca5f4652…0b57`).
`check.py` pins all nine to Agent #104's accepted source hashes.

The descending-prefix lemma that the written source uses for the first inverse step is
**not** used: the kernel accepts the same 229 bounds with the unrestricted (overflow and
no-overflow) inverse and with exact short-source predecessors included.

`generate_certificate.py` is untrusted. It mirrors the Lean definitions, transcribes the
written table, recomputes every bound (aborting on any mismatch) and emits the certificate
modules and `certificate/summary.json`.

## Verification

| Run | Commit | Result |
|---|---|---|
| Author clean rebuild, `check.py` (`verification/clean01-3bb721d/`) | `3bb721d` | PASS: 33 modules compiled from an empty snapshot with official Lean 4.19.0 (`6caaee842e94`); all 1,127 Agent #119 theorem constants (including generated ones) audited with `#print axioms`; union `{propext, Classical.choice, Quot.sound}`; no forbidden token |
| Independent review by a fresh-context reviewer subagent (`review/subagent-3bb721d/REVIEW.md`) | `3bb721d` | PASS: own toolchain download (archive SHA256 `6fe3ce97…13fe`), own build scheduler, 33 modules exit 0; all 2,541 closure theorems audited (1,124 in `FourColumnKernel`), union within the three standard axioms; semantic review of statements, table fidelity (229/229), growth-prefix exactness, short/long coverage, width-2 case of class 33; supplementary controls |
| Author clean rebuild after the docstring patch (`verification/clean02-ca95951/`) | `ca95951` | PASS: same 33 modules from an empty snapshot; all 1,127 Agent #119 theorem constants audited; union `{propext, Classical.choice, Quot.sound}`; package worktree clean at that commit |

The reviewer reported four non-blocking documentation issues: a stale README (fixed here),
two docstrings of `ThreeDigitBridge.lean` that omitted the `¬ GrowthPrefix` premise (fixed by a
comment-only patch; no statement or proof changed), a redundant `maxRecDepth` option in the
generated `AllRows4.lean` (harmless, left unchanged so the certificate bytes stay as reviewed),
and WIP commit labels.

The reviewer is a subagent spawned by Agent #119 with fresh context; it is not a different
coordination agent and not an external peer review. Its supplementary controls (not proofs):
the original chat program reproduces the table; literal orbits for `A ≤ 2,000,000`, `t ≤ 20`
(111,548 listed-prefix palindrome hits, 0 violations); exact ancestry depth of every
palindrome below `10^8` (5,078 listed, 0 violations; 183 of 229 bounds attained there).
`review/subagent-3bb721d/COMPRESSED.json` records the one losslessly compressed log.

## Reproduce

```sh
python3 proofs/contributions/agent-119/four-column-prefix/check.py /path/to/lean-4.19.0/bin/lean \
  --evidence /new/empty/dir --jobs 2
python3 proofs/contributions/agent-119/four-column-prefix/generate_certificate.py --check-only
```

`check.py` copies the 33-module import closure into a fresh flat snapshot, verifies the nine
pins, compiles with `lean -j1 -DElab.async=false`, audits every Agent #119 theorem constant and
writes `verification.json`. A full run takes about 8–15 minutes on two cores (peak memory
about 2.5 GiB, in the base module).

## Relation to concurrent work

This task's 229 classes, Agent #113's 130 extensions of its thirteen two-digit classes
(integrated via PR47), Agent #104's 739 (integrated) and 620 (claimed), Agent #118's
217/218/777 and Agent #124's 33 five/six-column classes are pairwise disjoint, and their union
is exactly the 397-class written three-digit baseline (`baseline_396.json` plus 739). The
completion state of each other task is recorded in its own task record.
The roughly 500 remaining three-digit classes are outside the baseline (Agent #117 owns their
cycle diagnosis; Agent #124 refines some to four digits). None of this resolves 196.
