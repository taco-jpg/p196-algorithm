# Independent adversarial review: Agent #119 four-column three-digit prefix package

**Verdict: PASS** for the formal content: statements, proofs, dependency fidelity, clean rebuild, axiom audit and table fidelity. Nothing blocks acceptance. Four documentation issues should be fixed before integration (section 9). None of them affects a theorem.

**Scope.** This review covers only the restricted palindrome families named below. It is not evidence about the full 196 (Lychrel) conjecture, and the package claims nothing about it. Palindromes whose prefix is outside the 229-entry table remain open. So do the four growth prefixes 110/111/121/122 and the classes owned by other agents.

| Item | Value |
|---|---|
| Repository | taco-jpg/p196-algorithm (local clone `/home/claude/p196-algorithm`) |
| Branch / commit reviewed | `research/agent-119/s20261015T1555` @ `3bb721d1a1b193551ba73cff1d859d6834c559ce` |
| Base | `main` @ `eec3d5f3646cab50abad6e610ea19626cd249070` (ancestor of the reviewed commit) |
| Package | `proofs/contributions/agent-119/four-column-prefix/` |
| Reviewer worktree | `/home/claude/review119` (detached at the reviewed commit, unmodified: `git status --porcelain` is empty) |
| Reviewer scratch | `/tmp/claude-0/-home-claude/51fb4d3d-04fd-5232-a6d9-a2027d524e65/scratchpad/review119` |
| Date | 2026-10-15 |

I did not use the author's `check.py` or `generate_certificate.py`. I did not edit any author file, `/home/claude/w119` or `/home/claude/build119`. I made no git push or network git operation.

---

## 1. Toolchain (task 1)

* I downloaded `https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst` myself into an empty directory.
* Archive size: 343,842,845 bytes.
* **Archive SHA256:** `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`. This **matches** the value Agent #104 recorded as official.
* I extracted it with python `zstandard` 0.25.0 and `tarfile`, using my own script (`reviewer-sources/extract.py`).
* `lean --version` reports `Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`, as required.
* SHA256 of `bin/lean` is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. This matches the `/bin/lean` entry in Agent #104's `integration-verified/official-archive-member-pins.json`.

## 2. Dependency fidelity (task 2)

All nine reused sources at the reviewed commit are byte-identical to Agent #104's accepted pins. Each was checked against both `integration-verified/source-pins.json` and `integration-verified/independent-source-pins.json`:

| Module | SHA256 (= pin) |
|---|---|
| PrefixInverse | `0a93622752fa22cf6c8de2efc8500dc313498d59831bb0e5381b3b351e0ab03e` |
| FastInverse | `585cb4d197479714edbdbe147c2c1c489742fa0f8eb978571abdc602eada4eee` |
| ActualPrefix | `c136216ed9c4100a268643be9a471b6746320f63d0af2030b6418429e5551e76` |
| ShortBoundary | `a018a0b73bfc82f12bc6d866dd3b396bf6b217cae3e0448883be04e2c50e50c9` |
| PrefixCertificate | `2b125b95c61604da41821eee4e58ce9a50f4039a7e43117a42194e6560adfca9` |
| PalindromeBridge | `6c1de8cf02ec9381e80388e6b4915db6cfa4d1189d3e47c273400f0d37948093` |
| certificate/LongRowsBase | `6568c04797f1e4cf1388c08c6142c6566bbfce59ef3d41a0c8df95cd8b7d07aa` |
| certificate/FastRowsBase | `e6ae5bcf64ca61d4c3d5aba5f1e08a956f969a8c4b98a85bb2b62867064a1984` |
| research/continuation/LychrelDigitSums | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` (= required base pin) |

Other checks:

* **Branch diff.** `git diff --name-only eec3d5f 3bb721d` touches only files under `proofs/contributions/agent-119/` (28 files added). No reused module, pin file or base file is modified by the branch.
* **Generated files.** The author's `certificate/summary.json` lists SHA256 values for the 21 generated certificate files. All 21 match the files I compiled.
* **Import closure.** The closure of `FourColumnConclusion` has exactly 33 modules: the 9 reused modules plus 24 Agent #119 modules. Outside that set it imports only `Std` and `Init` from the official toolchain. There is no Mathlib.

## 3. Semantic review (task 3)

I read the exact statements and every definition they depend on. The elaborated statements below are printed by Lean in `logs/ReviewAudit.log`, using `pp.fullNames`.

A separate `run_cmd` (`reviewer-sources/ReviewOrigins.lean`, `logs/ReviewOrigins.log`) computed every non-`Init` constant reachable from the **types** of the seven headline theorems, following definition bodies. There are exactly **13**:

* **From `LychrelDigitSums` (base):** `Canonical`, `value`, `Palindrome`, `orbit`, `orbit.match_1`, `reverse10`, `reverseFuel`, `reverseFuel.match_1`, `step`.
* **From Agent #119:** `Starts3` and `PalindromeStarts3` (ThreeDigitBridge), `Starts2` (FourColumnConclusion), `table4` (Table4).

So the meaning of the headline statements depends on the base definitions, three short predicates and the table. It depends on nothing from the certificate machinery. No Agent #119 module declares a non-internal constant outside the `FourColumnKernel` namespace.

### (a) Statement fidelity: matches the intended mathematics

```
ancestry_bound : ∀ {a b c B}, (a,b,c,B) ∈ table4 →
  ∀ A P t, 0 < A → PalindromeStarts3 a b c P → Lychrel196.orbit A t = P → t ≤ B
no_196 : ∀ {a b c B}, (a,b,c,B) ∈ table4 → ∀ t, ¬ PalindromeStarts3 a b c (orbit 196 t)
no_196_listed_prefix : ∀ t, Palindrome (orbit 196 t) → ∀ a b c B, (a,b,c,B) ∈ table4 → ¬ Starts3 a b c (orbit 196 t)
ancestry_bound_33 : ∀ A P t, 0 < A → Palindrome P → Starts2 3 3 P → orbit A t = P → t ≤ 5
no_196_33 : ∀ t, ¬ (Palindrome (orbit 196 t) ∧ Starts2 3 3 (orbit 196 t))
sharp_33 : orbit 1109090 5 = 33266233 ∧ Palindrome (orbit 1109090 5) ∧ ∀ k < 5, ¬ Palindrome (orbit 1109090 k)
sharp_33_starts : Starts2 3 3 33266233
```

How the base definitions read:

* `orbit n 0 = n` and `orbit n (k+1) = step (orbit n k)`, with `step n = n + reverse10 n`.
* `reverse10` is decimal reversal that drops leading zeros (`reverse10 1200 = 21` is kernel-checked).
* `Palindrome n := reverse10 n = n`.
* The iteration does not stop at intermediate palindromes, as in the written source.

What the hypotheses are:

* `ancestry_bound` and `no_196` assume only membership in the concrete list `table4`.
* Every entry is discharged by the kernel-checked `table4_checked : table4.all (entryOK ranks4) = true`.
* Everything else (`allRows`, `shortDescent4`, `table4_checked`, `root33_checked`) is a closed, kernel-checked theorem. None is a hypothesis. There is no circularity.

The hypotheses are not vacuous:

* `table4_length = 229`.
* Concrete instances type-check in `reviewer-sources/ReviewExtra.lean`: prefix 310 with bound 13, and `no_196 (B := 14)` for prefix 561.
* Every one of the 229 prefixes has palindromes below 10^8 (control in section 7).
* `sharp_33` exhibits a real orbit that reaches the class at t = 5.

`no_196` is derived from `ancestry_bound` together with a bound ≤ 100. It uses Agent #104's `no_196_target_of_ancestry_bound` and the base `no_palindrome_through_100`, which is `decide` on `noPalindromeFor 101 196`.

Sharpness: `sharp_33` and `sharp_33_starts` together give H(33266233) ≥ 5, so the uniform bound 5 for class 33 is exact. No other optimality is claimed. Section 7 shows that 46 of the 229 bounds are not attained by any palindrome below 10^8, which is consistent with the package's "no optimality" disclaimer.

### (b) `Starts3` means "the canonical decimal numeral begins a, b, c"

`Starts3 a b c P := ∃ e W, Canonical P e W ∧ 3 ≤ W ∧ e (W-1) = a ∧ e (W-2) = b ∧ e (W-3) = c`

* `Canonical n d L := 0 < L ∧ (∀ i < L, d i ≤ 9) ∧ 0 < d (L-1) ∧ value d L = n`.
* `value d (L+1) = value d L + d L * 10^L`, so `d 0` is the units digit and `d (L-1)` is the nonzero leading digit.
* `PalindromeBridge.canonical_unique` proves that width and digits are unique. The existential therefore picks out the unique numeral, and positions W-1, W-2, W-3 are its three most significant digits.

Kernel-checked interpretation tests are in `reviewer-sources/ReviewInterp.lean` (`logs/ReviewInterp.log`, exit 0):

* `Starts3 1 2 0 1209` holds.
* `¬ Starts3 9 0 2 1209` (digits are not read from the units end).
* `¬ Starts3 3 3 3 33` (width 2 is excluded from `Starts3`).
* `Starts2 3 3 33` holds.

### (c) `table4` equals the written table restricted as described

I parsed section 6 of `proofs/chat-6acee928/originals/p196_four_column_obstruction.md` independently (`reviewer-sources/compare_table.py`, output `table-comparison.json`):

* 67 rows and 360 entries, max bound 14. The bound histogram equals the written one: {1:55, 2:53, 3:110, 4:69, 5:15, 6:17, 7:7, 8:13, 9:5, 10:4, 11:2, 12:7, 13:1, 14:2}.
* Removing all extensions of {10,20,32,40,41,60,64,65,76,80,81,82,83} (130 entries) and 620 (1 entry) leaves **229**.
* `Table4.lean` has 229 entries with distinct keys. None is missing, none is extra, and **no bound differs**.
* No growth prefix appears in the table.

The bundled program `code/p196_four_column_obstruction.py` is byte-identical to the program embedded in the written source (SHA256 `60bec352…4d0107`). Its output, restricted the same way, also equals `table4` exactly (section 7).

The bounds are re-derived by the kernel with the **unrestricted** inverse:

* `rootWords` contains all `[a,b,c,d]` for d = 0..9, plus `[a,b,a]` at width 3.
* `longPred 4` contains both the overflow and no-overflow branches.
* So the written "descending-prefix" lemma (first edge restricted to N when b < a), which has no Lean proof, is **not** used. The kernel nevertheless accepts the same bounds.

### (d) Leading-digit-1 handling: `GrowthPrefix` is exactly 110/111/121/122

`GrowthPrefix a b c := a = 1 ∧ ((b = 1 ∧ c ≤ 1) ∨ (b = 2 ∧ 1 ≤ c ∧ c ≤ 2))`.

* The reviewer theorem `growth_exact` (`decide +kernel`, no axioms) proves that, for all digits a, b, c < 10, `GrowthPrefix a b c ↔ 100a+10b+c ∈ {110, 111, 121, 122}`.
* `growth_not_in_table` proves that no `table4` entry is a growth prefix.

Why the exclusion is correct. `overflow_palindrome_prefix` is kernel-proved from the base exact overflow criterion (all pair sums 0 or 11, first = 11) and the carry equations of the two leading columns. It shows that an overflowing step onto a palindrome of width ≥ 3 has top digits 1, 1+e, e+e' with e, e' ∈ {0,1}, which is exactly the four patterns.

The remaining leading-1 classes (120, 13x, …, 19x) therefore get a carry-free final step. That step is handled by `canonical_last_step3`, a generalisation of Agent #104's `canonical_last_step`, which required a leading digit > 1.

Brute-force control over every n < 10^7: 1,456 overflow steps land on a palindrome of width ≥ 3, with prefixes exactly {110: 32, 111: 136, 121: 200, 122: 1088}. All four occur and no other prefix does.

### (e) Soundness of `actual_iterPairs_rank4` (short and long sources)

The theorem is kernel-checked. What I verified is that its hypotheses are adequate and that its case split covers every actual step.

The proof is by induction on t over the exact pair-sum states `iterPairs q L t`.

* **Coverage of the actual orbit.** `iterPairs_representation` shows these states are the actual pair words of `orbit A t`. Admissibility is preserved (`iterPairs_admissible`).
* **Width monotonicity.** Width never decreases and grows by at most 1 per step (`width_le_nextWidth`, `nextWidth_le_succ`). The split "source width < 4" versus "≥ 4" is therefore exhaustive, and a long source always has a long target.

**Short sources (widths 1–3, including the 3 → 4 crossing):**

* The target width is ≤ 4, so `project4` of the target is the complete exact word (`project4_short`, since `min L' 4 = L'`).
* By Agent #104's `nextWord_wordOf`, that word equals `nextWord (wordOf q L)`.
* `shortWords3_complete` puts the source word in the exact list of 207 admissible short words.
* `ShortDescent` (kernel-checked as `shortDescent4`) says: if the exact image has rank r, the source has rank k < r.

For the 3 → 4 overflow, the image is the full width-4 word, which uses the same key format as a long 4-prefix. Tree nodes of length 4 therefore serve both cases. The rows of short (length < 4) nodes are vacuous under `longPred 4` (= [] when the length ≠ 4). That is harmless, because only short sources can reach short targets, and those are all covered by `ShortDescent`.

**Long sources (width ≥ 4):**

* Agent #104's `actual_mem_prefixPredecessors` (hypotheses: 0 < 4 ≤ L only) puts the source 4-prefix in `prefixPredecessors` of the target 4-prefix.
* `checkedRows_closed` with `allRows` then gives a strictly smaller rank.

Overlap of the low prefix with the reflected high columns (L = 4..7) is handled inside that proved theorem. It uses the actual carries with no disjointness assumption, and k = L is covered.

`allRows` is checked over `fastLongPred 4` and transferred to `longPred 4` by `checkedRows_fast_to_long`. That transfer needs only fast ⊇ original, which is proved.

Robustness of the tree data:

* All semantics go through the deterministic `lookup`.
* A malformed pivot could only make a lookup return `none`, which never makes a `checkBelow`/`checkInitial` succeed. `shortDescentOK`'s `none → true` branch is never used for a word that `lookup` finds.
* Independently, `Rank4Data.lean` has 7,776 distinct words (2 / 1 / 30 / 7,743 of lengths 1 / 2 / 3 / 4), max rank 13, and every pivot equals `wordCode`.

Numeric control on the concrete tree: for A ≤ 300,000 and t ≤ 20, there are 47,349 events where `project4` of the actual pair word of T^t(A) is a tree node (3 / 5 / 155 / 47,186 by projection length). There are **0** violations of t ≤ rank, and 6,375 events with t = rank.

`time_bound_of_root` and `ancestry_bound_of_checks`:

* The last step uses `last_step_root`. It shows that L = W, there are no carries, and the low pair sums equal the target digits. By palindromic symmetry q0 = a, q1 = b, q2 = c, and q3 ≤ 9. At width 3 the projection is `[a,b,a]`, requiring c = a and an even center from admissibility, which matches `rootWords`.
* `checkInitial` bounds the root rank by B−1, so t ≤ B.

### (f) Class 33 covers width 2 (P = 33)

`ancestry_bound_33` splits on the canonical width W.

* **W ≥ 3:** e(W−3) < 10, and `table4_has_33` (`decide`) supplies `(3,3,c,5) ∈ table4` for every c < 10, so `ancestry_bound` applies.
* **W = 2:** this is exactly P = 33.
  * The final step uses Agent #104's `canonical_last_step`, since the leading digit is 3 > 1. It gives source width 2, no carries and pair word [3,3].
  * `root33_checked : checkInitial ranks4 4 [3,3] = true` (kernel) gives t ≤ 4 before the last step, so t ≤ 5 overall.
  * In the data, [3,3] has rank 2.

Exact check: H(33) = 3, from the chain 3 → 6 → 12 → 33.

The reviewer example `fun A t hA h => ancestry_bound_33 A 33 t hA (by decide) starts2_33 h` type-checks. `sharp_33` is verified by `decide`, with no axioms.

## 4. Independent clean rebuild (task 4)

* I created a new empty directory: `/tmp/claude-0/-home-claude/51fb4d3d-04fd-5232-a6d9-a2027d524e65/scratchpad/review119/build`.
* I copied the 33 closure sources into it in a flat layout (module = file stem). Their hashes are in `build-source-sha256.txt` and were re-verified unchanged after the build.
* I compiled with my own scheduler (`reviewer-sources/build.py`), which parses the `import` lines and runs `lean -j1 -o X.olean X.lean` with `LEAN_PATH=<build dir>`, at most 2 jobs at a time, in dependency order.
* **Result: all 33 modules exit 0** (`logs/build-summary.json`, `logs/build-driver.log`, one log per module).
* Total wall time 453.2 s. The author's own clean build was running at the same time, so timings are inflated.
* Peak RSS (VmHWM, sampled once per second) was 2,598,120 KiB (about 2.5 GiB), reached by `LychrelDigitSums` in 278.2 s.
* The only warnings are two unused-variable linter warnings in Agent #104's pinned `ShortBoundary.lean`, at lines 170 and 187.

| Module | exit | s | peak MiB |
|---|---|---|---|
| PrefixCertificate | 0 | 3.0 | 443 |
| PrefixInverse | 0 | 6.0 | 509 |
| FastInverse | 0 | 4.0 | 455 |
| LongRowsBase | 0 | 1.0 | n/a (exited before the 1 s sample) |
| FastRowsBase | 0 | 2.0 | 415 |
| Rank4Data | 0 | 68.2 | 930 |
| Rows4_000 … Rows4_015 | 0 (all 16) | 15.1 – 53.2 | 976 – 1394 |
| LychrelDigitSums | 0 | 278.2 | 2537 |
| ActualPrefix | 0 | 5.1 | 488 |
| PalindromeBridge | 0 | 2.0 | 442 |
| ShortBoundary | 0 | 6.0 | 495 |
| FourColumnAncestry | 0 | 2.0 | 456 |
| Short4 | 0 | 4.0 | 609 |
| Rows4_branches | 0 | 21.1 | 1585 |
| ThreeDigitBridge | 0 | 5.0 | 494 |
| AllRows4 | 0 | 2.0 | 433 |
| Table4 | 0 | 2.0 | 441 |
| FourColumnConclusion | 0 | 18.1 | 1406 |

`build-summary.json` has the full per-module rows.

## 5. Axiom audit (task 4)

`reviewer-sources/ReviewAudit.lean` imports `FourColumnConclusion` and runs a `run_cmd`. Output is in `logs/ReviewAudit.log`; status is **exit 0, 83.7 s**. The command:

* enumerates **every** constant whose defining module is one of the 33 closure modules: 25,579 constants, of which 2,541 are theorems;
* runs `Lean.collectAxioms`, the engine behind `#print axioms`, on **every theorem**;
* fails on any axiom outside {propext, Classical.choice, Quot.sound}, any safe `axiom` declaration, any `opaque`, any user-visible `unsafe`/`partial` definition, and any `implemented_by`/`extern`.

Results:

* **Axiom union over all 2,541 theorems:** {propext, Classical.choice, Quot.sound}.
* **Violations:** 0.
* No `sorryAx`, `Lean.ofReduceBool` or `Lean.ofReduceNat` occurs. Any use would have appeared in the union.
* **`FourColumnKernel` namespace:** all 1,124 theorem constants are audited, including the `_proof_N` auxiliaries from `decide +kernel` (547 have non-internal names). Axiom sets: [] ×1036, [propext, Quot.sound] ×65, [propext, Classical.choice, Quot.sound] ×15, [propext] ×8.
* **The other 1,417 closure theorems** (reused modules) also stay within the allowed set.

**Compiler auxiliaries.** My first, unclassified run is kept as `logs/ReviewAudit-v1-unclassified.log`. It flagged 22,168 unsafe `_cstage`/`_closed`/`_spec` definitions, 42 unsafe `axiom` stubs (`List.mapTR.loop._at.…._spec_N`) and 27 partial `_unsafe_rec` definitions. All of them have internal names generated by the code generator.

A control experiment (`reviewer-sources/Control*.lean`, `logs/control-compiler-aux.log`) settles what they are:

* A trivial `def roots := (List.range 10).map …` produces the same kind of unsafe axiom stub.
* The kernel rejects any safe declaration that mentions such a stub ("invalid declaration, it uses unsafe declaration") or an `_unsafe_rec` ("safe declaration must not contain partial declaration").

So these stubs cannot enter any theorem. The final audit counts them separately.

**Source scan.**

* The 24 Agent #119 sources contain no `sorry`, `admit`, `native_decide`, `axiom`, `opaque`, `unsafe`, `partial`, `implemented_by`, `extern`, `run_cmd`, `#eval`, `elab`, `macro`, `syntax` or `initialize`.
* The only `instance` is the derived `Decidable (GrowthPrefix a b c)` (ThreeDigitBridge.lean:46). It cannot affect soundness, because `decide` proofs are re-checked by the kernel.
* The only `set_option`s in the whole closure are `maxHeartbeats` and `maxRecDepth`.

**Headline theorems (explicit `#print axioms`):**

| Theorem | Axioms |
|---|---|
| Certificate.ancestry_bound / no_196 / no_196_listed_prefix | propext, Classical.choice, Quot.sound |
| Certificate.ancestry_bound_33 / no_196_33 | propext, Classical.choice, Quot.sound |
| Certificate.sharp_33 | none |
| Certificate.sharp_33_starts | propext |
| Certificate.table4_checked / table4_length / allRowsFast / root33_checked | none |
| Certificate.allRows | propext, Classical.choice, Quot.sound |
| Certificate.shortDescent4 / entry_sound / table4_has_33 | propext, Quot.sound |
| actual_iterPairs_rank4, overflow_palindrome_prefix, no_overflow_of_prefix, canonical_last_step3, last_step_root, time_bound_of_root, ancestry_bound_of_checks, no_196_of_checks | propext, Classical.choice, Quot.sound |
| shortWords3_complete, project4_congr | propext, Quot.sound |
| project4_short, project4_long | propext |
| shortDescentOK_sound | none |

## 6. Statement and definition printouts

`logs/ReviewAudit.log` (end of file) contains the elaborated `#check`s of the headline theorems. It also contains `#print`s of `Starts3`, `PalindromeStarts3`, `Starts2`, `GrowthPrefix`, `rootWords`, `project4`, `ShortDescent`, `shortDescentOK`, `shortWords3`, `entryOK`, `Canonical`, `value`, `orbit`, `step`, `Palindrome`, `reverse10`, `CheckedRows`, `checkRow`, `checkInitial`, `longPred` and `lookup`. They agree with the source text quoted in section 3.

## 7. Supplementary controls (task 5; evidence, not proof)

* **Original program.**
  * `proofs/chat-6acee928/code/p196_four_column_obstruction.py` ran under `python3 -I`: exit 0 in 7.0 s, printing "All certificates passed".
  * It produced 360 classes (max 14), coverage 198,702, prefix-33 layer counts [100, 346, 171, 107, 62, 0], and the sharp path 1109090 → … → 33266233.
  * Restricted as above, it gives **229 classes, equal to `table4` entry by entry** (`program-comparison.json`, `logs/original-program.*`).
* **Literal-integer control.** For every A in 1..2,000,000 and t ≤ 20:
  * 3,002,992 palindrome events, of which 111,548 have a listed prefix. All 229 prefixes are hit. **0 violations** of t ≤ B.
  * Class 33 (all widths ≥ 2): 9,395 hits, maximum t = 5, 0 violations.
  * Output: `controls/lit_a.*`, `controls/lit_b.*`.
* **Exact ancestry depth below 10^8** (stronger than the literal control).
  * Every predecessor of n is smaller than n, so one increasing pass computes H(P) = max{k : ∃ A ≥ 1, T^k(A) = P} **exactly** for every P < 10^8.
  * 5,078 listed-prefix palindromes (widths 3–8) were checked: **0 violations**, and all 229 prefixes are represented.
  * 183 of the 229 bounds are attained exactly. For the other 46 (e.g. 120: B = 7, max H below 10^8 = 1; 561: B = 14, max 8) no palindrome below 10^8 attains the bound. That does not contradict anything, since optimality is not claimed.
  * Class 33 max H by width: w2 = 3, w3 = 0, w4 = 5 (150 → 201 → 303 → 606 → 1212 → 3333), w5 = 4, w6 = w7 = w8 = 5.
  * H(33266233) = 5.
  * Output: `controls/exact_1e8.json`, `controls/exact_1e6.json`.
* **Rank-tree control:** see 3(e) (`controls/rank_tree.*`).
* **Overflow-prefix brute force:** see 3(d) (`controls/overflow_prefixes.json`).

## 8. Answers to the specific questions

| Check | Result |
|---|---|
| (a) statements match the intended mathematics; no hidden, vacuous or circular hypothesis | yes |
| (b) `Starts3` = canonical numeral begins a, b, c from the most significant end | yes |
| (c) `table4` = written table minus the 131 entries owned by others (229 entries, all bounds equal) | yes |
| (d) `GrowthPrefix` is exactly {110, 111, 121, 122}; leading digit 1 handled by a proved overflow criterion | yes |
| (e) `actual_iterPairs_rank4` covers every actual step: short sources including the 3 → 4 crossing via exact short descent; long sources including overlapping prefixes via the proved complete inverse | yes |
| (f) class 33 covers width 2 (P = 33) via `canonical_last_step` and root [3,3] | yes |

## 9. Defects and issues

**Blocking defects: none.**

Non-blocking documentation issues:

1. **`README.md` is stale.**
   * Lines 6–9 say "Status: WIP … theorems are *conditional* on explicit finite certificate checks that are not yet supplied. No prefix ancestry bound and no statement about the orbit of 196 is claimed yet." That contradicts `FourColumnConclusion.lean`, which proves both unconditionally.
   * The module table (lines 18–23) omits `FourColumnConclusion.lean` and `certificate/*`.
   * Line 33 still says the bounds are "to be confirmed by the kernel certificate"; they now are confirmed.
2. **`ThreeDigitBridge.lean` docstrings are imprecise.**
   * Lines 19–21 say `ancestry_bound_of_checks` "has no other premise" than the three finite checks.
   * The theorem (lines 246–250) also takes `hng : ¬ GrowthPrefix a b c`. The docstring at lines 243–245 also omits it.
   * The premise is discharged by `entryOK` and is mathematically necessary, so this is only a wording issue.
3. **Redundant option in `certificate/AllRows4.lean`.** Lines 20–21 set `maxRecDepth` twice (10000, then 100000). This is harmless.
4. **Commit and README labels say "WIP".** Commit `3bb721d` is titled `wip(agent-119)…`, and commit `836a0ad` says "clean rebuild, full audit and independent review pending". This review supplies the independent rebuild and audit. The author's own `check.py` run was not evaluated here.

## 10. Files

All files are under `/tmp/claude-0/-home-claude/51fb4d3d-04fd-5232-a6d9-a2027d524e65/scratchpad/review119/out/`:

* `REVIEW.md` and `review.json`.
* `table-comparison.json`, `program-comparison.json` and `build-source-sha256.txt`.
* `logs/`: build driver, `build-summary.json`, one log per module, `ReviewAudit.log` and `.status`, `ReviewAudit-v1-unclassified.log`, `ReviewOrigins.log`, `ReviewInterp.log` and `.status`, `ReviewExtra.log` and `.status`, `control-compiler-aux.log`, `original-program.stdout`/`.stderr`/`.status`.
* `controls/`: literal, exact-depth, rank-tree and overflow-prefix outputs, plus `audit_parsed.json`.
* `reviewer-sources/`: every reviewer script and Lean file used.

No `.olean` files were copied.
