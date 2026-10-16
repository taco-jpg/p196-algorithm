# Independent semantic review: exact period-four raw guard

Reviewer: genuine Agent #1 specialist `research_status`, 2026-10-16. This reviewer authored no periodic mathematical module, changed no author source, and performed no Git writes. The core guard and facts are specialist `symbolic_scope` work; Digits/Slices are parent work; Numeric is specialist `cap4_existing_theorems` work. The earlier `periodic-digits-review.md` records the preliminary incremental check; the final execution described here uses a separate fresh source/build directory.

**Semantic verdict: PASS for the exact raw one-transition extraction, the stated output-block facts, and the conditional ordinary-successor width interfaces.** No unresolved statement flaw was found. The full package's compilation/audit result is recorded below; this review does not assert quotient stripping, state-cycle existence, safety closure, or any infinite ordinary orbit.

## Exact endpoint and source identity

`Agent1.Periodic.raw_guard_bounded` proves, for bounded `B,H,w`, `w.length=4`, and every `k≥3`,

`Agent8.stepWord (periodicWord B H w k) = periodicWord (rawOuter B H w) (rawCenter B H w) (rawPeriod B H w) (k-2)`.

Every operation is the original `Agent8` normalizer/pair/carry or a structural list definition. `rawGamma` is the actual terminal carry of `periodicWord B H w 3`, starting at carry 0. `rawOuter`, `rawPeriod`, and `rawCenter` are literal slices of that single actual `stepWord` output:

| Block | Start | Width |
|---|---:|---:|
| `rawOuter` | 0 | `B.length+4` |
| `rawPeriod` | `B.length+4` | 4 |
| `rawCenter` | `B.length+8` | `H.length+8+rawGamma` |

These match the preserved `periodic_word_quotient.py` `transition` implementation, including the center offset after both the exterior guard and the retained output period. The theorem does not assume an output decomposition or choose arbitrary existential blocks.

All twelve source pins, Git blob identities, and import lists are in `final-source-identity.json`. The five newly reviewed module SHA-256 values are:

| Module | SHA-256 |
|---|---|
| `Agent1PeriodicDigits` | `dc6cc1dadb74c4927f0635107fdc1eb62cebac3038dea4e97ad4229fc8703eab` |
| `Agent1PeriodicSlices` | `8c1afe94c85fcfc3d7318a651cfd236f7d833aa257972c73815110dfe9003e43` |
| `Agent1PeriodicNumeric` | `d3142b2a44bbe471df559e74bba993a9a663592b3bf04ce973e1ef94251873f7` |
| `Agent1PeriodicGuard` | `4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91` |
| `Agent1PeriodicGuardFacts` | `106cd4c4f3454fbe6ac5304691951b8292ef8477f0901424f323fb2fa4f366c9` |

The seven prerequisites are the unchanged five original modules and two checked repeated-block modules. The source map only restores their logical import filenames in the isolated build; no arithmetic adapter or source rewrite is used.

## Proof interpretation

**Actual digit scan.** `normalize_periodicWord` supplies `A ++ U^(n+2) ++ C ++ V^(n+2) ++ Z` for source exponent `n+3`. Its two first-copy transients are separate; each stable period receives the actual carry computed through the preceding blocks. `Z` includes the final carry once. `scan_block_lengths` gives lengths `b+4,4,h+4,4,b+gamma` when `w.length=4`; `scan_carry_le_one` gives `gamma≤1`. The review of the complete five-export Digits module is preserved separately.

**Structural zipper.** `pair_periodic_digits` permits arbitrary natural-number lists with those lengths and a displacement `g≤4`. It does not posit decimal semantics. Let `t=V.take g` and `d=V.drop g`. Its proof decomposes the digit list as equally long exteriors

`l=A ++ U^(n+1)`, `r=d ++ V^(n+1) ++ Z`,

around `m=U ++ C ++ t`. The lengths are explicitly proved equal using `g≤4`; natural subtraction is therefore justified. Reversing `r` and applying `pow_rotate_append` gives

`r.reverse = (Z.reverse ++ d.reverse) ++ (t.reverse ++ d.reverse)^(n+1)`.

The two exact zip lengths then identify the exterior and repeated output period. `pair_three_parts` pairs the middle with itself and obtains the reflected right output from commutativity of coefficient addition. The shift is therefore encoded by the **first `g` entries of the forward right period**, not by an incorrectly selected prefix of its reversal. Actual application uses the computed `g=rawGamma≤1`; the generic allowance through 4 introduces no extra actual carry choice.

**Literal slices.** `zipper_block_lengths` proves the exact three output widths. `stepWord_periodic_form` composes the actual digit theorem with the generic zipper. `raw_blocks_eq_zipper` specializes this form to exponent 3 and uses the four Slices theorems to identify the literal output slices with the same zipper blocks used for every larger exponent. Exact lengths are proved before the `take`/`drop` identification, avoiding a truncated-slice assumption. `raw_guard_bounded` substitutes `n=k-3`; its explicit `3≤k` proves both `k-3+3=k` and `k-3+1=k-2`.

**Output facts.** `raw_block_lengths` transfers the exact zipper lengths to the literal slices. `raw_center_symmetric` applies original `pair_symmetric` to the identified zipper center, so it does not require a symmetric input center. `raw_blocks_bounded` uses original `normalized_digits_bounded` and `pair_bounded` on the actual full output, then restricts membership to each slice. This last fact correctly needs no period-length premise: truncated slices are still bounded. The three facts do not assert preservation of the entire valid-state predicate.

## Original domain and explicit strengthening

`ValidPeriodic` retains all original `valid(s)` conditions: bounds on `B,H,w`; length-four `w`; symmetric `H`; even center coefficient when `H.length` is odd; and `0 < (B ++ w).headD 0`. Since `w.length=4`, the last field is precisely the original conditional positive-head requirement: use the head of nonempty `B`, otherwise the head of `w`. When `H` has odd length, its center index is in range, so the optional-index default does not erase the parity condition.

`raw_guard` is the exact wrapper on that original domain. `raw_guard_bounded` explicitly strengthens the algebraic result by dropping symmetry, center parity, and positive-head assumptions. This is legitimate in the inspected proof: the forward normalizer needs coefficient/carry bounds, and its final `pair` is symmetric for any digit list. The proof does not infer realizability from the stronger domain or from `Agent8.CanonicalPair`, whose fields lack the odd-center parity condition.

The original Python discovery transition also asserts input safety before using the raw formula. Safety is not required by the written raw guard lemma and is not claimed as preserved by these new theorems. Their stronger algebraic scope must not be reported as a closed safe family.

## Boundary conditions

- **Exponent three:** `n=0` produces exactly one output period. This is the actual sliced base output, not a sampled approximation.
- **Empty exterior/center:** `B=[]` and `H=[]` are permitted. The exterior still has its four-column guard; the raw center still has width `8+gamma` when `H=[]`.
- **Appended carry with empty exterior:** the right guard is `normalize [] rightCarry`; it retains `[1]` when that carry is 1. The proof never drops this entry.
- **All-nine period:** idempotence includes the identity carry transfer. The two actual band-entry bits may differ; the digit decomposition preserves them. No non-nine reset is assumed.
- **First-copy transient:** each first normalized period is retained in a guard; subsequent periods use the stabilized carry. The old checked boundary witness showing distinct first/later digits remains applicable.
- **Both actual carry values:** carry 0 uses `t=[]`; carry 1 moves one right-period digit into the middle and rotates the reflected period accordingly. The proof handles these uniformly through the exact computed displacement and length bound.
- **Period length:** the guard theorem requires a four-entry block, not a block of minimal period four. Constant phases are included. Empty `w` is allowed only in the more general Digits/Numeric interfaces, not in the raw guard endpoint.

## Numeric bridge: hypotheses retained

The six Numeric exports use original `DecimalDigits.Canonical`, `DecimalDigits.columnSum`, `DecimalDigits.carry`, `FoldedDecimal.representation_next`, `Lychrel196.step`, and `DecimalQuantitativeMass.decimalLength`.

`terminalCarry_eq_actual_carry` identifies the list scan with the finite indexed column-sum carry under explicit in-range coefficient agreement. It does not require irrelevant infinite-tail equality. `actual_step_canonical_width` applies existing `representation_next` to a supplied canonical predecessor, then identifies `nextWidth` with old width plus the actual list carry using its bit bound. `actual_step_decimalLength_normalize` applies existing `decimalLength_of_canonical`; it does not infer integer width from list length alone.

`periodic_actual_carry` specializes carry independence to every positive repetition count. `periodic_actual_step_canonical_width` and `periodic_actual_step_decimalLength` give the exact width

`2*B.length + 2*(k*w.length) + H.length + terminalCarry (periodicWord B H w 3) 0`

under **explicit original canonical predecessor and finite column-sum representation premises**, plus bounds and `k>0`. They do not assert that arbitrary bounded repeated bands admit such a predecessor. In particular, this package contains no new theorem deriving an ordinary realization from `ValidPeriodic` alone. The original `Canonical` predicate includes positive width and a nonzero leading digit, excluding empty/zero numerals; the existing `decimalLength 0 = 0` convention therefore causes no mismatch here.

This bridge reuses the existing finite-index canonical successor theorem rather than rebranding Agent #3's generic digit-list canonicality theorem. Its new connection is the original list terminal carry to that finite-index representation.

## Execution status

**Final independent execution: PASS.** All twelve exact source modules were copied into the initially empty `/workspace/p196-agent1-session-20261016/periodic-guard-review-clean-001` and compiled sequentially with Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`, with `LEAN_PATH` restricted to that directory. No previous project `.olean` was copied or reused. All twelve compile commands and the separate `ReviewAudit.lean` command exited 0.

The complete audit imported both `Agent1PeriodicGuardFacts` and `Agent1PeriodicNumeric`, selected all twelve project modules by actual module origin, and checked **1,298 theorem constants**. The transitive axiom union was exactly `Classical.choice`, `Quot.sound`, and `propext`. It rejected custom safe axioms, any disallowed theorem dependency, and any module omitted from the theorem enumeration. Generated unsafe implementation declarations were recorded separately, not accepted as proof dependencies. All **34 periodic public theorem** axiom prints and **13 repeated-block prerequisite** prints were present. The checked new sources contain no `sorry`, `admit`, `native_decide`, custom axiom, or `Lean.ofReduceBool` token.

The compiler binary SHA-256 was `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, version commit `6caaee842e94`. All twelve working source hashes were checked again after the audit and matched the compiled snapshot. There were no failed attempts in this reviewer run. Exact source snapshots, commands, compiler fingerprint, exit codes, runtimes, full logs, audit source and hashes are retained in `clean-001/`; the final receipt is `clean-001/verification.json`. `replay.py` reproduces this reviewer run from the pinned manifest into new directories.

Author eleven-module results, numeric-author nine-module results, and the earlier Digits incremental result are separate runs and are not counted as this execution. This is a twelve-module project result, not a repository-wide verification.

## Scope conclusion

The package proves the preserved literal all-exponent **raw one-step image** and supplies the stated block facts and conditional numeric width. Normalizing/stripping the quotient state, computing or telescoping exponent changes, finding a finite-interface return, preserving safety through iterations, and producing an infinite ordinary orbit remain outside the result and the historical finite-interface/lift owner's lane remains untouched.
