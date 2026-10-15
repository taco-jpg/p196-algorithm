# Adversarial review: agent-113 two-digit-prefix package

Commit a6229d6617a0b4ec105839c3ccd1ee765c944b36 (branch research/agent-113/s20261015). The repository was not modified (`git status` is clean).

## VERDICT: PASS WITH NOTES

The theorems say what the summary claims, and none of them is vacuous. The chain proof handles every case correctly, and the from-source rebuild passes with only the standard axioms. Independent numerics up to 10^9 agree exactly. The notes below are cosmetic or concern the trust base. None of them affects soundness or what the theorems state.

## 1. Statement fidelity

Exact types, printed by the kernel in ReviewTypes.lean:

- `ancestry_bound_65 : ∀ A P t : Nat, 0 < A → PalindromeStartsTwo 6 5 P → Lychrel196.orbit A t = P → t ≤ 6`. The other 12 have the same form. Their (a, b, h) values are 10:1, 20:2, 32:2, 40:3, 41:3, 60:3, 64:3, 76:3, 80:4, 81:4, 82:4, 83:4 and 65:6. I checked each one by parsing the generated files.
- `no_196_thirteen : ∀ t, ∀ ab ∈ thirteenPrefixes, ¬ PalindromeStartsTwo ab.1 ab.2 (orbit 196 t)`. The list holds exactly the 13 pairs.
- `no_196_thirteen_arith : ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10^k ∉ [10,20,32,40,41,60,64,65,76,80,81,82,83]`.
- `startsTwo_iff : StartsTwo a b P ↔ 1 ≤ a ∧ a ≤ 9 ∧ b ≤ 9 ∧ ∃ k, P / 10^k = 10a+b`.

The definitions:

- `StartsTwo a b P := ∃ e W, Canonical P e W ∧ 2 ≤ W ∧ e(W-1) = a ∧ e(W-2) = b`.
  - `Canonical` requires a width L > 0, all digits ≤ 9, a nonzero leading digit, and `value = P`.
  - So e(W-1), e(W-2) are exactly the two leading decimal digits, and `startsTwo_iff` confirms this arithmetically.
  - P/10^k is a two-digit number only when k = W-2, so the arithmetic form is equivalent to the digit form.
- `PalindromeStartsTwo a b P := Lychrel196.Palindrome P ∧ StartsTwo a b P`.
- `Lychrel196.Palindrome n := reverse10 n = n`.
- `reverse10 n := reverseFuel n n 0`. This is ordinary digit reversal that drops leading zeros (`reverse10 1200 = 21`). It is proved equal to `reverseAux` (`reverseFuel_correct`, since fuel n ≥ number of digits) and to positional reflection (`reverse10_value`).
- `step n := n + reverse10 n`. `orbit n 0 = n`, `orbit n (k+1) = step (orbit n k)`. So `orbit` is the genuine reverse-and-add iteration T^k.
- There is no name shadowing. The only definitions of `step`, `orbit` and `Palindrome` are in `Lychrel196`, and `#print` shows the fully qualified names.

On vacuity:

- The hypothesis family is non-empty: `sharp_65.1` gives `PalindromeStartsTwo 6 5 (orbit 1203290 6)`.
- `0 < A` is harmless. P = 0 is never in the family, because `Canonical` forces P > 0.
- `t = 0` gives the trivial bound 0 ≤ h.
- The hypothesis of `no_196_thirteen_arith` (that some `orbit 196 t` is a palindrome) is the open problem itself. It is a genuine conditional, not something false by construction.

Ancestry depth means `orbit A t = P` with no condition on the intermediate states. So intermediate palindromes are allowed, and the width is unrestricted. This matches H(P) = max{k : ∃ A > 0, T^k(A) = P} in the source.

`SharpAt a b R h k := PalindromeStartsTwo a b (orbit R h) ∧ (∀ j < h, ¬ Palindrome (orbit R j)) ∧ orbit R h / 10^k = 10a+b`. Each R is a positive literal, and each h literally equals the matching bound. "Exactness" is the informal conjunction of `ancestry_bound_ab` and `sharp_ab`. No single theorem states it.

## 2. Soundness: `Cert.ancestry_bound` (TwoDigitCertificate.lean:212-279)

**Setup.** Take t = s+1 and M = orbit A s. `last_step_triple` gives three facts:
- width M ≥ 3;
- every pair sum of M is ≤ 9;
- tri M = (a, b, c) with c ≤ 9.

It covers a = 1 through `no_overflow_of_descending_target`. A width-2 target is excluded because two-digit palindromes are aa, which contradicts b < a. The proof needs `b < a`, discharged by `decide`; all 13 prefixes satisfy it.

**Invariant `key i`, for i ≤ s.** width(orbit A (s-i)) ≥ 3 and `inLayer i (tri (orbit A (s-i)))`.

- **i = 0.** The base check applies to (a, b, c), c ≤ 9.
- **i = 0 → 1 (second-to-last state m, lines 243-259).** Lemma 1 applies: all pair sums of M are ≤ 9 and pairAt M 1 = b < a = pairAt M 0, so width M = width m. That forces width m ≥ 3, and `tri_step` then forces topT = 0. So the non-overflow-only `firstRow` closure is the right one. Lemma 1 is used only at this step, which is correct: it needs the all-pair-sums ≤ 9 hypothesis, and that hypothesis is available only for M.
- **i ≥ 1, width m ≥ 3 (lines 260-267).** `tri_step` gives some e ≤ 1, and `stepRow i` closure (both branches) moves the state into layer i+1. The condition i < h comes from the membership being true, since layers beyond h are empty.
- **i ≥ 1, width m < 3 (lines 268-272).** Then m < 100, and step m ≥ 100 by the induction hypothesis on its width. `shortCheck` (with step m < 1000 also checked) gives a contradiction for every layer r ≥ 1. The i = 0 short case cannot occur, because Lemma 1 gives width m = width M ≥ 3.
- **End.** `key s` gives layer s nonempty at tri(A), so s < h, so t ≤ h. The statement's literal bound (for example 6) is definitionally `cert65.layers.length`, and the kernel accepted it.

No case is missed. Box coverage is complete:
- `tri_box` gives 1 ≤ s0 ≤ 18 and s1, s2 ≤ 18;
- `cover18` and `rowAll` cover every row;
- `rangeAll 2` covers e ∈ {0, 1};
- `tri_step` is proved for every width ≥ 3, including the overlapping widths 3-5 (symmetry lemmas `sym0`/`sym1`/`sym2`) and both overflow branches.

The meaning of the layers is never used, only the kernel-checked closure, so the generator is outside the trust base. (`code` is in fact injective on [0,18]^3, but this is not needed.)

## 3. Python/C cross-check (scripts in this directory)

**Exact ancestry-depth DP.** `dp_depth.py` covers n < 10^7 and `dp_depth.c` covers n < 10^9. Because T(n) > n, every predecessor of P is below P, so depths are exact.
- Below 10^6 there are 22 palindromes per prefix, 286 in total, which matches the source's 286.
- Below 10^7 there are 122 per prefix (1586 total).
- Below 10^9 there are 1222 per prefix (15886 total).
- There are **0 violations**. The maximum depth reached equals the claimed bound for every prefix, in every range:

| Prefix | Max depth | First argmax |
|---|---:|---:|
| 10 | 1 | 101 |
| 20 | 2 | 202 |
| 32 | 2 | 32223 |
| 40 | 3 | 404 |
| 41 | 3 | 41414 |
| 60 | 3 | 606 |
| 64 | 3 | 64446 |
| 76 | 3 | 76667 |
| 80 | 4 | 808 |
| 81 | 4 | 815518 |
| 82 | 4 | 82828 |
| 83 | 4 | 83438 |
| 65 | 6 | 659956 |

- For 65, the depth histogram below 10^9 is 0:556, 1:332, 2:129, 3:172, 4:16, 5:5, 6:12.

**Sharpness (`sharp_check.py`).** All 13 (R, h, k) triples from TwoDigitMain.lean check out:
- T^h(R) is a palindrome;
- no earlier state is a palindrome;
- T^h(R) / 10^k equals the prefix;
- h equals the bound.

For 65 the path is 1203290 → 2126311 → 3262523 → 6515146 → 12930302 → 33234223 → 65477456, and 1203290 is divisible by 11.

An independent search (`find_witnesses.c`) for the smallest first-palindrome witnesses reproduces the given R for 11 prefixes. For 41 and 83 it finds smaller valid witnesses (1005500 and 1005700). The given ones are still valid. If intermediate palindromes are allowed, depth 6 for 65 is already reached from R = 12190 (giving 659956).

**196 orbit.** t = 0..6 gives 196, 887, 1675, 7436, 13783, 52514, 94039 (t = 7 gives 187088). None is a palindrome.

**Semantic lemmas (`semantic_checks.py`).**
- `tri_step` checked on 1,410,900 numbers (all n < 10^6, plus random and adversarial n up to width 60): 0 failures.
- Lemma 1 checked on all m < 10^7 (99,040 meet its hypotheses): 0 failures.
- The exact `key` invariant checked against the decoded Lean layers for all n < 2·10^6 and i ≤ 12 (33,334 instances): 0 failures.

## 4. Generator consistency

`gen_certificates.py` matches the Lean definitions:
- `hi2`, `hi1`, `top` and `next_triple` match `hiCarry2`, `hiCarry1`, `topCarry` and `nextTriple` term for term.
- `code` and `mask` match `code` and `bitAt`.
- `tri3` matches.
- `short_ok` uses the same r range, 1 ≤ r < h.
- The layer-1 rule (non-overflow only) and the layer r+1 rule (all e) are the same.

Re-running the generator into scratch reproduces all 13 `TwoDigitCert*.lean` files and `certificates.json` byte for byte.

A literal Python transcription of `Cert.Checked`, applied to the masks parsed from the .lean files, passes for all 13. Mutation tests confirm the checks are not trivial:
- deleting any single triple from any layer makes the checks fail (257 of 257 deletions caught);
- dropping the last layer also makes them fail.

So each certificate is the least fixpoint. The decoded layers coincide exactly with the source's tables (Section 6, and Section 7 for 65).

## 5. Rebuild

**Command.** The command was run with no other Lean process active:

```
build.sh /home/claude/p196-algorithm …/scratchpad/review-build
```

- Exit code 0, total about 7 minutes.
- Toolchain: Lean 4.19.0 (commit 6caaee842e94).
- The sha256 of every copied source matches the repository files.

**build-summary.txt.** Every module exited 0:

| Module | Time | Module | Time |
|---|---:|---|---:|
| LychrelDigitSums | 70s | TwoDigitCert41 | 24s |
| PalindromeBridge | 0s | TwoDigitCert60 | 23s |
| TwoDigitProjection | 1s | TwoDigitCert64 | 25s |
| TwoDigitGrowth | 2s | TwoDigitCert65 | 50s |
| TwoDigitNumeric | 2s | TwoDigitCert76 | 23s |
| TwoDigitCertificate | 2s | TwoDigitCert80 | 30s |
| TwoDigitCert10 | 7s | TwoDigitCert81 | 30s |
| TwoDigitCert20 | 17s | TwoDigitCert82 | 31s |
| TwoDigitCert32 | 16s | TwoDigitCert83 | 31s |
| TwoDigitCert40 | 25s | TwoDigitMain | 2s |

- `Audit exit=0`.
- `AUDIT-SUMMARY theorems=1840 bad=0 union=[Classical.choice, Quot.sound, propext]`.
- No warnings, errors or `sorry` in any module log.

**ReviewTypes.lean** (in the build dir; output in ReviewTypes.out). It compiled with exit 0 and no errors. The kernel printed the types and definitions quoted in Section 1, and `orbit` and `reverseFuel` as the expected structural recursions. These hand-written examples all type-check:
- the requested restatement (`exact Agent113.TwoDigit.ancestry_bound_65`);
- a fully arithmetic restatement: `reverse10 P = P → P / 10^k = 65 → orbit A t = P → t ≤ 6`, proved through `startsTwo_iff`;
- a non-vacuity example;
- `orbit 196 6 = 94039 ∧ orbit 1203290 6 = 65477456` by `decide`;
- a plain-arithmetic 196 corollary.

`#print axioms` for the three main theorems gives [propext, Classical.choice, Quot.sound].

## 6. Notes and minor defects (none affects soundness)

1. `generator/gen_certificates.py:4` cites `Agent113.TwoDigit.Cert.check`, which does not exist. The Lean name is `Cert.Checked` (with `baseCheck`, `firstRow`, `stepRow` and `shortCheck`). Cosmetic.
2. `TwoDigitCertificate.lean:99` says `Cert.h` is "the number of nonempty-by-construction layers". Lean never checks nonemptiness; `h` is just `layers.length`. This is harmless, since an empty layer could only weaken the bound, and tightness comes from `sharp_ab`. Cosmetic.
3. The forbidden-construct grep in `build.sh:21-22` scans only the package's own files, not the two imported dependencies (LychrelDigitSums.lean, PalindromeBridge.lean). The transitive axiom audit covers this. I also grepped both dependencies by hand and found no sorry, admit, native_decide, axiom, implemented_by, extern or unsafe. Separately, the `extern` pattern would give false positives on prose such as "external".
4. `TwoDigitMain.lean:182-184`: `SharpAt` does not state R > 0, and it does not tie h to the bound constant. Exactness of the maximum is only the informal conjunction described above.
5. There is no independent kernel replay. lean4checker/leanchecker is not shipped with the v4.19.0 toolchain here, so the trust base is the standard Lean 4.19.0 kernel. The `decide +kernel` obligations are kernel-checked when each declaration is added, and they add no `Lean.ofReduceBool`.
6. Scope, which is stated honestly in the docstrings: this is a restricted-family exclusion. It does not prove that 196 is a Lychrel number.
