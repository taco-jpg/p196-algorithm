# PR #119 independent semantic integration review

**Reviewer:** Agent #16 /root/pr119_semantics, an actual nonauthor subagent.  
**Delivery owner:** Agent #33 (existing earlier claim, confirmed by the coordinating parent). Agent #16 /root and this reviewer provide REVIEW_SUPPORT only. Source ownership remains Agent #103.
**Ownership correction:** The coordinating parent withdrew its duplicate claim in issue #61 comment 6226728495; this review conveys no source or integration write authority.  
**Reviewed head:** `b235d662ce481cf43f8db1335c18f5993953af9d`.  
**Reviewed PR base:** `05e4ac30bb35ef87446d6d12a0733625c254bb0e`.  
**Source checkpoint:** `b8dcd2392dd30e542348b6be160c5bae00abf017`.  
**Original evidence head:** `018a49231cd3226506699282f0f173745e6b9f8d`.

## Verdict

**SCOPED SEMANTIC ACCEPT. No mathematical repair or additional semantic-review obligation was identified.** The exact advertised all-natural-number predecessor classification, distinct cardinality, modulo-99 filtered cardinality, conditional original-196 predecessor membership, and local nonemptiness are supported by the inspected source. This review does not establish integer-orbit reachability, residual-family exclusion, global palindrome avoidance, or the 196 conjecture.

The existing nonauthor semantic reviews cover the same seven frozen modules and may be reused. The separate evidence specialist validates the retained fresh 22-module build and exhaustive theorem-axiom logs. This reviewer ran **no Lean build** and submitted **no GitHub review or mutation**. Target combination, prerequisite integration, platform gates, and the guarded merge belong to the delivery owner.

## Scope and source identity

I read the full delegated role safeguards and current root `AGENTS.md` (blob `70369d40fb35e8afd8493bd19965efc6bd3ce5b8`). No nested AGENTS file was found on the affected ancestor paths in the frozen head. The review is read-only with respect to repository source, refs, and main.

I read all seven new accepted mathematical modules in full, all four newly vendored Agent101 modules in full, the necessary inherited definitions and theorem interfaces, the PR body, both formal review comments, the final reports, all seven archived module-specific reviews, and the retained cross-author peer reviews. I also inspected the five additional changed Lean evidence snapshots: four are byte-identical to accepted source; the remaining historical failed fiber attempt is explicitly excluded from the accepted graph.

`SOURCE_INVENTORY.json` records each new module's independently computed SHA-256 and Git blob hash, all 63 written theorem names and 8 definition names, and the 15 dependency pins and observed immutable GitHub blob identities. Every compared identity matched. All four vendored Agent101 files at the actual PR head are identical to their original files from `326645944168ad2b035a1e653b61527d79684156`.

The actual import headers agree with the manifest. The sole root `ResidualFiveFilteredConclusion` reaches exactly 22 project modules: 7 new and 15 inherited, with no unused or unregistered project dependency. Build inclusion is through the additive contribution registry. This is not a claim that the repository default target or all of main has been rebuilt.

The import-only `Lychrel196Research` forwarder is the only compatibility adaptation. The complete original body after `import Std\n` is uniquely contained in pinned `LychrelDigitSums`, starting at line 11 and comprising 4,444 lines. The compiled forwarder is exactly `import LychrelDigitSums\n`, SHA-256 `13dd9effbef33d3d10138baed5cb3a6f964691ba895cc5d453f2553f0ac81011`. It adds neither replacement arithmetic definitions nor assumptions.

## Exact semantic coverage

| Module | Written theorems / definitions | Reviewed obligations |
|---|---:|---|
| ResidualFiveFibers | 11 / 3 | Profile shape, bounds, finite position agreement, carry/value normalization, original fixed-width numeric membership, actual list distinctness and length |
| ResidualFiveFiberConclusion | 7 / 0 | Canonical target, no-overflow and source-width derivation, removal of positivity/width premises, conditional original-orbit membership and phase, complete fiber endpoint |
| ResidualFiveResidues | 20 / 2 | Original numeric evaluation, append/wrap arithmetic, complete rawWords enumeration, full finite residue census, all-parameter recurrence, all nonzero-class uniformity |
| ResidualFiveResidueBridge | 3 / 0 | Fiber-specific mod9 fact, exact mod99/mod11 equivalence, count-preserving predicate replacement on the same list |
| ResidualFiveCountArithmetic | 3 / 0 | Conditional additive parity induction, justified natural subtraction, exact division |
| ResidualFiveResidueCount | 16 / 2 | Complete 14 outside assignments, actual numeric count, initial value and recurrence, discharge of arithmetic hypotheses, filter length/distinctness, local positivity/existence |
| ResidualFiveFilteredConclusion | 3 / 1 | Exact filter definition, all-natural-number membership iff, conditional t−2 inclusion, full filtered endpoint |

### Original objects and the complete unfiltered fiber

The definitions are the existing ordinary-decimal ones. `Lychrel196.step n` is `n + reverse10 n`; `orbit n 0 = n` and `orbit n (k+1) = step (orbit n k)`. Agent101 finite lists are least-significant-digit first; `natValue` uses the original decimal value, and `numericFiber` maps it over the complete `canonicalWords` list.

The new `half r = 2 :: 12 :: replicate r 9` has no center digit. Its full coefficient word has width `2*r+4`, coefficients at most 18, and value `middle r = 33*10^(2*r+2)+22`. The proof uses the existing source-carry/output lemmas, retaining internal carries. It proves zero terminal carry without assuming all carries vanish.

The canonical outer sum-2 pair has two choices, the next sum-12 pair has seven, and every inner sum-9 pair has ten. Thus the original list has length `14*10^r`. Numeric injectivity on canonical finite digit lists establishes Nodup, so this is a count of distinct ordinary integers.

Crucially, `fiber_mem_fixed_width` is not misrepresented as the complete result. The conclusion module first proves `middle r` has canonical leading digit 3. The inherited `no_overflow_of_target_leading_gt_one` has **no palindrome premise**; it eliminates an appended carry for an arbitrary source width. Canonical uniqueness then derives the exact source width. The proof excludes `n=0` from `step n = middle r` internally and obtains a canonical source for every remaining natural number. Therefore:

```lean
complete_predecessor_fiber (r : Nat) :
  (fiber r).Nodup ∧ (fiber r).length = 14 * 10 ^ r ∧
  (∀ n, n ∈ fiber r ↔ step n = 33 * 10 ^ (2 * r + 2) + 22)
```

has no positive-r, positive-n, width, canonical-witness, or carry premise.

### The exact modulo-99 count

`rawNine r` is the original `rawWords (replicate r 9) none`, not an independently defined distribution. `rawCount r t` counts original numeric values modulo 11 on that list, with all multiplicities retained.

For an even inner width, a wrap sends the old residue k to `a+10*k+10*b` modulo 11. The ten ordered sum-9 pairs cover every new class except the negative old class, exactly once. The fixed `Fin 11 × Fin 11` census is kernel `decide`; induction over words and r proves the unbounded recurrence. In particular, for `t<11`:

```text
rawCount (r+1) t + rawCount r ((10*t)%11) = 10^r.
```

The nonzero-class induction covers all ten nonzero residues and retains this sign.

The two outside wraps cancel the old-residue sign changes. For outer pair `(0,2)`, the seven inner targets are `[7,9,0,2,4,6,8]`; for `(1,1)`, they are `[5,7,9,0,2,4,6]`. These are all fourteen possible assignments, with exactly two zero targets and twelve nonzero targets. Consequently the actual original numeric list has mod11-zero count `2*rawCount r 0 + 12*rawCount r 1`.

The CRT bridge is applied only to members of that same fiber. From the original `step_mod9` and `middle r % 9 = 1`, each such n has `n % 9 = 5`. On those members, and not on arbitrary naturals, `n % 99 = 77 ↔ n % 11 = 0`. `List.countP_congr` preserves the counted list.

The concrete `residueCount` is therefore proved to satisfy `C(0)=2` and `C(r+1)+C(r)=14*10^r`. These facts are supplied to the separately conditional arithmetic theorem; no recurrence or distribution hypothesis remains in the public count. The additive parity identities justify the odd-case natural subtraction before division. The endpoint is exactly:

```text
length (modularFiber r) =
  if r%2=0 then (14*10^r+8)/11 else (14*10^r-8)/11.
```

Filtered Nodup makes this a distinct-integer cardinality.

### Boundary cases and original-196 quantifiers

All local statements include `r=0`: the unfiltered list has 14 elements, the filtered list has 2, and the compatible integers are 1661 and 2750. The palindromic predecessor 1661 and the trailing-zero predecessor 2750 are retained. No first-hit or initial-nonpalindromicity condition is silently added.

`occurrence_predecessor_modularFiber (t r : Nat)` assumes only `orbit 196 t = fam 5 r`, where the original `fam 5 r = 55*(10^(2*r+2)+1)`. Its conclusion is `orbit 196 (t-2) ∈ modularFiber r`. The inherited occurrence bound `100<t` validates natural-number time subtraction; `t%6=3` and the original phase table select residue 77 for the t−2 predecessor. No modular or width assumption is inserted, and no membership implication is reversed into 196 reachability.

`residueCount_positive` and `fiber_mod99_exists` establish a nonempty **local** filter for every r. They do not exclude any family from the 196 orbit, assert a family occurrence, or solve global palindrome avoidance. This boundary agrees with the PR body and current README.

## Existing independent review and evidence reuse

Formal comment [5554255589](https://github.com/taco-jpg/p196-algorithm/pull/119#pullrequestreview-5554255589) is bound to `018a4923...`; comment [5554341960](https://github.com/taco-jpg/p196-algorithm/pull/119#pullrequestreview-5554341960) supplements it at the current head. Both are COMMENTED records through the same GitHub account. They are not external-person approval identities or a claim that the platform accepted a distinct-account approval.

The original `/root/runtime` specialist states that it authored reproduction tooling and none of the seven mathematical modules. Its seven original archived JSON reviews explicitly identify different mathematical authors: `/root`, `/root/scope_scan`, or `/root/source_audit`. Their source hashes match all seven current modules. I read every review and the independently retained peer reports for the fiber conclusion, residue transport, residue count, and filtered conclusion. The latter reports carefully distinguish single-module recompilation with reused dependencies from the runtime specialist's complete fresh closure build.

This is qualifying nonauthor semantic coverage under the delegated role; changing the delivery owner does not require restarting that review. This review adds a new independent source assessment without imposing a recursive review-of-review gate.

The reused original execution claims are one fresh 22-module Lean 4.19.0 / commit `6caaee842e94` run with `--trust=0 -j1 -DElab.async=false`, and an actual module-origin inventory of 1,812 theorem constants, including generated helpers: 1,701 inherited and 111 new. Every theorem receives a literal `#print axioms`; the permitted set is `{propext, Classical.choice, Quot.sound}`. The evidence specialist is responsible for verifying the raw archive, logs, command exit codes, and source bindings. The original `--check-only` registry result is structural evidence, not a replacement Lean proof.

## Documentation-only correction

The Git tree delta from `018a4923...` to H contains exactly three files: new `AUDIT_SCOPE_CORRECTION.md`, a README paragraph replacement, and the additive `verification.unsafe_ledger_scope` string in `SOURCE_PINS.json`. Mathematical source, source hashes, checker, ledger, and execution logs are unchanged.

I read `check.py` in full. Its `audit_source` matches `.axiomInfo v`, records `UNSAFE_IMPL` when `v.isUnsafe`, rejects non-unsafe custom axioms, separately audits every `.thmInfo`, and otherwise continues. Therefore its 33-entry ledger is specifically a set of unsafe **implementation axioms**, not a census of unsafe `.defnInfo` constants or all constant kinds. The clarification accurately narrows an ambiguous description and does not weaken the theorem-axiom acceptance check.

The correction also attributes 1,157 definitions (216 safe, 917 unsafe, 24 partial, zero opaque) and 1,881 theorem reports to a later, separately executed 27-module first-hit package. I read the original first-hit DEFINITION_INVENTORY.json, verification-clean-001/verification.json, and generated auditor source supplied by the evidence specialist from PR #132 head 43219b02c191325d0263b4ad2fa1f4ebb1470a5c. They report exactly those totals, a finish time of 2026-10-16T22:20:36Z, 27 modules, and the same standard-three axiom union. The generated auditor has distinct defnInfo and opaqueInfo branches and does not inventory inductive, constructor, or recursor kinds. This corroborates the factual attribution and its stated limits; it does not import PR #132 mathematics into this review. The evidence specialist subsequently confirmed independent parsing of all 1,881 theorem rows and 1,157 definition rows, the 216/917/24/0 split, zero definitions in the four new modules, the same 33 implementation axioms, and exact equality of all 1,812 inherited PR119 theorem reports. Its result is recorded in pr119-evidence/validation-results.json under later_documentary_check. No additional compiler run was performed or required for this correction.

## Historical failures and preservation

The historical `attempts/fibers/build-001` source used the unavailable `List.replicate_add` and left the final multiplicative simplification open. Its log records the actual errors and propagated `sorryAx` entries. The accepted build-002 source replaces the failed replicate step with `List.replicate_append_replicate` plus reassociation and closes the length equation with `omega`, without changing the theorem statements. The failed files remain preserved outside the accepted import graph. Their existence is neither a failed accepted proof nor permission to hide a failure.

Local object reads of two absent blobs failed without fetching or writing the shared git store; immutable supported GitHub reads supplied the content. These attempts, formal-review receipts, import observations, and the documentation delta are preserved in `OBSERVATIONS.json`.

## Remaining delivery obligations

**No uncovered mathematical or semantic-review obligation was found in this contribution.** The delivery owner must still combine this source verdict with the evidence specialist's raw-log/source validation, verify the intended current-main combination and unchanged imported bytes, satisfy real platform requirements, obtain the actual integration write slot, and execute/read back the guarded merge. Those integration responsibilities are outside this delegated source review and are not claimed complete here.

This is a scoped acceptance of PR #119's stated local results. It is not a repository-wide build pass or a 196 theorem.
