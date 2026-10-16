# PR #110 independent integration review

## Identity, scope, and current conclusion

Reviewer: the genuine nonauthor `review110` subagent assigned by Agent #13 in session `6124a6476634`. This reviewer did not author or modify either proposed Lean module, the eight prerequisite modules, the original verification scripts, or the remote PR. This is independent work by a separate reasoning subagent within the same assistant session. It is not external peer review or a claim to a separate GitHub account.

**PASS: the stated finite mathematics, the exact ten-module source closure, and the complete logical type/axiom audit passed independent review and execution. Execution is a fresh source closure with recorded resource recovery; the initial disk-full failure remains explicitly preserved.**

The reviewed identities are:

| Input | Exact identity |
|---|---|
| PR | `taco-jpg/p196-algorithm#110` |
| Head H | `624cc122e39e4d1f30b5c17890e7aac17c40a1e9` |
| Checked accepted base B | `1ee9123344dbe17e9bda224ff8af5b1cbb2b64e4` |
| Intended combined tree T | `23ef1e89374822bf559a1cf0760878f941a9dc56` |
| Core root SHA-256 | `190778311fe86b4c48ae617b2946d78876b13772c6dfeee8cba4f2a7cc0ba1a4` |
| Numeric root SHA-256 | `14abe8bbdc4320c3ec72d97eacb403c481b154d8baf8f1dac041d3af79cc13c4` |

The independent snapshot procedure read all ten source files from T, compared them byte for byte with H, and checked each registry SHA-256 and Git blob. Both new modules are absent from B; all eight prerequisites are present and byte-identical in B, H, and T. The root Git blobs are `7d997797e5d680f931f3f19e26113edfcb05b4f2` and `ae8dea5ca30698560987a56d3ca88961311b666b`. Full identities and local source paths are recorded in `snapshot-receipt.json`. The clone's administrative checkout HEAD was not used as a substitute for those explicit Git objects.

This review covers the two complete new modules, their exact ten-module closure, the definitions and bridges that give their statements ordinary decimal meaning, and the retained evidence relevant to those claims. Agent #13's parent separately owns the full incoming-tree preservation check, current platform state, remote publication, and any guarded integration. This document does not assert that all of main was rebuilt or that any platform gate has passed.

## The mathematical claim actually proved

The fixed original component is `DelayedOverlapGate.component r 1 10 6`, with component width `2*r+6`. Its whole word is `DelayedOverlapGate.initial r 1 10 6`, with width `2*r+7`. Original `initial_is_overlap` identifies the initial whole word with `shiftOne` of the component. The new `first_domain` supplies the original Group III parameter domain for every `r>=1`; it does not postulate a return or a numerical realization.

For every `r>=1`, `time_four_overlap_iff` proves

```lean
OverlapAt r 4 ↔ 2 ≤ r
```

For every `r>=2`, `two_genuine_repairs` proves all four terms

```lean
¬ OverlapAt r 1 ∧ OverlapAt r 2 ∧
¬ OverlapAt r 3 ∧ OverlapAt r 4
```

The component return is exactly `sixWord r 16 8 5 9`, namely the low-to-high pair-sum word

`16, 0^(r-1), 8, 5, 9, 9, 5, 8, 0^(r-1), 16`.

These are pair-sum coefficients, which can exceed nine. They are not individual decimal digits. The result agrees with the `(10,6)` row of the original written construction, blob `d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2`, section 3. That exact original blob is retained in `reference/constructive-STATUS-d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2.md`. Other rows and later-time statements in that document are not promoted by this PR review.

## Carry arithmetic, width, and the finite-prefix interpretation

I read both new source files in full, the original `Agent1GroupIII` and `Agent1GroupIIINumeric` in full, the imported bridge modules, and the required original digit, carry, palindrome, realizability, and iteration definitions. The new explicit states and carry certificates have the following meanings:

| State being normalized | Component/pair-word description | Nonzero incoming carries |
|---|---|---|
| Component at time 2 | `sixWord r 4 2 1 7` | None |
| Whole at time 2 | `shiftOne (sixWord r 4 2 1 7)` | Exactly `r+4` |
| Component at time 3 | `sixWord r 8 4 2 14` | Exactly `r+3`, `r+4` |
| Whole at time 3, `r>=2` | The explicit additive `wholeThree r` | Exactly `r+3`, `r+5` |

The profiles are proved against the original recursive carry equation, starting with carry zero. The terminal-carry lemmas establish the no-overflow branch for each continuation under its actual parameter bound. In particular, the whole time-three carry profile requires `r>=2`; the proof does not apply that profile at the excluded shortest spacer. The component's normalized six central digits are `(4,2,4,5,3,4)`, whose reflected pair sums give `(8,5,9,9,5,8)`.

The code defines `wholeThree` by adding exterior and central contributions. This matters at `r=1`, where the supports touch: an `if` chain that overwrote one contribution would have changed the boundary. The supplied expression preserves the addition.

`continue_no_overflow` uses the original `no_overflow_next_congr` to continue an actual `iterPairs` state from equality only on the represented prefix. It neither assumes equality of unused function tails nor replaces the state with a fixed-width surrogate. The component width is proved constant through time four for `r>=1`; the whole width is proved constant through time four for `r>=2`.

`finiteComponent r t` truncates the component at the width actually returned by `iterPairs` at time t and extends with zeros beyond that width. `OverlapAt` requires both the actual width relation and equality on every represented whole-word position. The same definition is used for both departures and both repairs. This removes a possible false overlap caused by arbitrary values of a `Nat → Nat` representation outside its finite word.

The first departure is reduced to the accepted original Group III finite-component departure. The third departure has a direct witness at column `r+3`: `wholeThree` equals 8 there, whereas the independently shifted component equals 28. The time-two restoration reuses the original proven first gate; the time-four restoration is obtained from the new full carry and column identities. No recurrence premise is assumed.

## Exact treatment of r = 1

The five boundary theorems refer to the original actual iterates, not to a substituted guessed family. At time four the component has width eight and columns

`[16,8,5,9,9,5,8,16]`.

The whole has width nine. The exact signed difference between the whole and the zero-extended shifted actual component is

`[1,-20,1,0,0,0,1,-20,1]`.

Subtraction takes place in `Int`, so the negative entries are retained. Every list lookup is restricted by `i<9`; there is no reliance on an out-of-range default. The finite quantifiers are discharged with ordinary kernel `decide`. The theorem stating failure of actual overlap witnesses a differing finite column. The all-parameter iff handles `r>=2` using the positive theorem and reduces the remaining `r>=1` case to this exact r=1 failure. There is no assertion about r=0.

For interpretation, the retained diagnostic whole word is `[17,4,14,14,18,14,14,4,17]`, while the shifted component is `[16,24,13,14,18,14,13,24,16]`. The nine signed differences agree entry by entry. The formal boundary proof, rather than the diagnostic list, supports acceptance.

## Ordinary integers, positivity, and quantifiers

The numeric module retains the original meanings:

- `reverse10` is decimal natural-number reversal, related to the terminating recursive reversal algorithm by `reverseFuel_correct`.
- `step n = n + reverse10 n`, and `orbit n t` applies exactly t steps.
- `Palindrome n` means `reverse10 n = n`.
- `Canonical n d L` requires positive width, every represented digit at most nine, a strictly positive leading digit, and exact positional value n.
- `columnSum` adds a represented digit to its reflected digit; each actual column is at most 18.
- `representation_next` covers both actual terminal-carry branches, and `iterPairs_representation` iterates that exact arithmetic bridge.

Canonical leading positivity establishes `n>0`; zero and leading-zero padding cannot satisfy the hypotheses. Trailing zeros and values of d outside the represented width are permitted, as they should be. Positive ordinary outputs follow from the canonical successor bridge or from the original positivity-preservation results.

`numeric_time_four` is universal in n, d, and r subject to the explicit initial canonical representation and finite pair-word agreement. It proves existence of canonical digits for `orbit n 4` with width `2*r+7` and the full pair word `shiftOne (componentFour r)`. There is no assumed symbolic-to-integer lifting hypothesis.

`numeric_time_four_iff` establishes the same exact r threshold for that canonical ordinary time-four conclusion. At r=1, the proposed overlap has column 24 at index one; this contradicts the original bound 18 for any pair of canonical decimal digits. Its exclusion is therefore about genuine canonical output representations.

`numeric_four_step_safety` proves `¬ Palindrome (orbit n t)` for every `1<=t<=4`, for every permitted canonical realization. Outputs one and two reuse the original first-gate safety result. Outputs three and four use the pair words at times two and three, respectively. The original `palindrome_iff_bad` says that a predecessor produces a palindrome exactly when all its columns are at most nine, or its outer column is 11 and all its columns lie in `{0,11}`. `wholeTwo` has a column 14 and outer column 4; `wholeThree` has a column 17 and outer column 8. Both exact predecessor patterns are excluded. The step indices are correct.

`numeric_safe_handoff` combines the universal safety statement with the exact canonical return. `realized_safe_handoff` discharges nonemptiness separately: for each `r>=2` there exist n and d with `n>0`, the required original representation, all four safety conclusions, and the canonical time-four return. It invokes the original proven `realized_safe_gate`, whose `valid_word_realizable` construction uses `realizingDigit` and proves bounded digits, positive leading digit, and every required column equation.

The quantifier order is thus **for every permitted spacer, a positive finite seed exists**, together with a statement for every canonical realization of that spacer's initial pair word. It does not produce one fixed seed with an arbitrarily long safe orbit.

## Fresh execution and audit

The independent runner is `/workspace/scratch/6124a6476634/review110/run_clean_review.py`; its source is retained. It was inspected before execution, and is separate from the untouched original verifier. Its masker and module-origin enumeration are openly adapted from the retained repository verifier and the retained previous independent runner. Independent execution is claimed; independently invented verification infrastructure is not.

One new complete ten-module build was started in the previously nonexistent directory `/workspace/scratch/6124a6476634/review110/evidence/clean-001/source`. All project objects were absent before the build, and only newly compiled objects in that directory enter `LEAN_PATH`. The official Lean/Std distribution supplies the standard library. No author or earlier reviewer project object is reused.

The compiler is official Lean 4.19.0, commit `6caaee842e94`, executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Every module and the separate audit harness use explicit `--trust=0 -j1 -DElab.async=false`. Commands, environment, exit statuses, durations, source hashes, compiler/library hashes, and unabridged compiler logs are retained in `clean-001/receipt.json`, `clean-001/source/`, and `clean-001/logs/`. The exact module closure comes from `Agent1GroupIIIHandoff.registry.json`, rooted at `Agent1GroupIIIHandoffNumeric`; actual source imports are compared with the registry and independently traversed.

The new audit enumerates declarations by their actual imported module of origin. It checks every theorem and safe definition, safe opaque declaration, constructor, recursor, and inductive declaration belonging to the ten project modules. It records the type and transitive `Lean.collectAxioms` set for each audited declaration, plus literal `#check` and `#print axioms` for all 43 new public theorems and all seven new public definitions. Unsafe compiler implementation declarations are recorded separately and cannot enter any accepted logical axiom set. The only permitted logical axioms are `propext`, `Classical.choice`, and `Quot.sound`.

The initial `clean-001` remains recorded as FAIL. Six prerequisite modules produced complete objects. Although GroupIII returned exit 0, its object was truncated to 11,710,464 bytes instead of 39,668,192 bytes when disk space was exhausted. The next Handoff invocation exited -11 after 0.064393 seconds with an empty module log. Writing failure records then raised ENOSPC, and a subsequent read-only command could not create its sandbox mount marker. The unabridged returned traceback is preserved in `disk-incident-build-terminal-output.log`, and the corrupted object identity/removal record is retained. This was not a proof counterexample, and a successful complete closure was not inferred from the isolated zero exit.

The authorized recovery uses `/dev/shm/p196-agent13-session6124-20261016/review110/evidence/recovery-001`, with a new independent receipt. It verifies and copies only the six intact objects produced by this reviewer in clean-001, recompiles GroupIII and the three remaining modules, checks each completed object hash, and then executes the same complete audit obligation. No original source, verifier, or failed log is changed. Recovery completed successfully. All four affected/remaining modules and the audit exited zero, and every rebuilt object matched its complete expected hash. The entire ten-module closure therefore derives from this reviewer's new source compilation. It is a fresh closure with recorded recovery, not one uninterrupted successful run.


### Completed audit result

The final raw audit contains **2,746 logical constant records and 2,746 corresponding type records**: **2,547 theorem constants**, **185 safe definitions**, **four inductive declarations**, **six constructors**, and **four recursors**. There are no project safe opaque or quotient declarations. All **43 new public theorem endpoints and seven new public definitions** have literal type and axiom prints. The new modules account for 565 theorem constants, including generated auxiliaries, plus seven safe definitions. Declaration counts are audit metadata, not counts of independent major results.

| Module | Theorem constants | Safe definitions |
|---|---:|---:|
| LychrelDigitSums | 986 | 131 |
| SafeDelay | 24 | 10 |
| DecimalSafeRuns | 42 | 3 |
| DecimalDelayBridge | 41 | 7 |
| PairDelayBridge | 26 | 6 |
| DelayedOverlapGate | 392 | 14 |
| Agent1GroupIII | 466 | 7 |
| Agent1GroupIIIHandoff | 554 | 7 |
| Agent1GroupIIINumeric | 5 | 0 |
| Agent1GroupIIIHandoffNumeric | 11 | 0 |

The transitive logical axiom union is exactly {propext, Classical.choice, Quot.sound}. All five r=1 boundary theorem axiom sets are empty. The audit separately records 14 unsafe compiler implementation axioms from unchanged prerequisite modules and 846 non-safe implementation definitions. None of those 14 axioms originates in either new root, and no unsupported implementation axiom occurs in any audited logical dependency set. Source scanning found no forbidden proof-bypass token.

The raw audit log is 3,589,174 bytes, SHA-256 65dcb4b65113c0b52b10de622fc7308b900aac55cc45098b60df51f4c5f4994f. Complete source, command, exit-code, compiler, and object identities are in recovery-001/receipt.json. The successful new Handoff compile has one unused-parameter warning; its numeric companion has no compiler diagnostics. No original proof was repaired or weakened.

The original runner's line-oriented JSON stored only the first line of 837 wrapped axiom-list summaries. This did not affect the Lean-side checks, constant census, or complete raw output. That JSON remains unchanged. The additional inspected parse_complete_audit.py parsed the full multiline log without rerunning Lean or modifying proof sources. The canonical structured table is recovery-001/constant-audit-complete.json, containing all 2,746 full types and full axiom arrays. Its receipt is postprocess-receipt.json. The complete JSON SHA-256 is 65cfb9d073aa62a3f1a9ed78f35b1bc3162e9113085a9d474a1bc639f1870ad2.

## Retained evidence and remaining scope

All 99 files of the PR's handoff contribution package have been retained locally without loss. I examined the author execution scripts, source freeze/result, attempt-003 failure log and its correction, boundary-specialist records, prior independent review and clean-run record, the finite diagnostic program and result, and the parent's publication-source receipt. The parent integration agent separately checks every incoming contribution-package manifest and current-base preservation obligation.

The author's attempt-003 failed due to a tactic after the goal had already closed and an unsupported `by_contra` tactic. The retained diff to attempt-004 replaces those proof-script details without changing theorem statements or hypotheses. The failure, original source, and log remain available. The author explicitly identifies reuse of already compiled prerequisite objects; that run is not treated as a fresh dependency build. Earlier WIP and source-only review records retain their original labels.

The prior finite diagnostics cover 34 spacers (`1..32,64,128`) and 102 realization checks, with no assertion that the three choices per spacer are distinct. I inspected this evidence; I did not rerun it or relabel it as a new experiment. Its finite scope does not replace the universal Lean proofs. A minor archival wording difference is recorded for the parent's preservation review: the boundary README says object files were retained, while the final package inventory explicitly lists generated `.olean` files as excluded. Those reproducible objects are exempt under the accepted publication policy; source, commands, hashes, and logs are retained.

No source/proof repair was implemented by this reviewer. No mathematical weakening, custom axiom, native proof oracle, or unresolved semantic objection was identified in the reviewed roots. This review makes no time-six, later-cycle, infinite-safety, Lychrel-existence, 196, first-hit classification, or repository-wide acceptance claim. Source or dependency changes would require reassessing the affected evidence. The parent must still apply fresh platform and integration guards to the exact head and current base before any remote action.
