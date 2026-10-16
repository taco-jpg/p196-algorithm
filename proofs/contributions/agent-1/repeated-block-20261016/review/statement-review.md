# Independent semantic review: repeated-block normalization

Reviewer: genuine Agent #1 specialist `research_status`, 2026-10-16. This is an independent source/statement review of the core written by specialist `symbolic_scope` and the context module written by the parent. The reviewer edited neither core nor context and performed no Git mutation. After the source review, the parent assigned the reviewer to author `Agent1RepeatedBlockBoundary.lean` and independently rebuild the eight-module closure with `--trust=0`. The boundary witnesses therefore have reviewer authorship; independence applies to the core/context review and execution, not to semantic review of the reviewer’s own witnesses. Execution results are recorded below.

**Verdict at the recorded source snapshot: semantic PASS for the stated normalization, carry, and list-length identities.** No counterexample or missing hypothesis was found in those statements. This is not a review approval of the full preserved guard-period quotient, which remains outside the declarations reviewed here. The exact source identities, including five unchanged prior modules and the three new modules, are in `source-identity.json`; a source change requires the snapshot and affected review to be refreshed.

Base: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`. Parent reported coordination claim `2cb89418916f1d0a22813028d5fea623e80900ad`, issue 61 receipt `6224749698`. This review does not independently infer ownership transfer or recipient acknowledgment from that report.

## Original definitions and attribution

All arithmetic remains in the original namespaces. `Agent8.normalize` in `PeriodObstructions__70ce034b31b5b218.lean:24` scans the list from its head, outputs `(x+e)%10`, passes `(x+e)/10`, and appends a single nonzero terminal carry. `Agent8.fixedDigits` and `terminalCarry` in `ActualWordBridge__7f032d27940694a8.lean:6` and `:10` use that same scan; they neither reverse nor trim the word. `Bounded w 18` is a pointwise membership condition, not a hidden symmetry or canonicality hypothesis.

`Agent1.RepeatedBlock.pow` only concatenates copies. `terminalCarry_eq_carryIn` connects the original list carry to `IncomingCarry.carryIn (fun i => (w[i]?).getD 0) e w.length`. The interval length is precisely `w.length`, so the zero default beyond the list does not introduce an extra column. The empty case is the identity on the incoming carry. The successor proof removes the first actual coefficient and passes its actual outgoing carry; there is no independently chosen interior carry.

`terminalCarry_idempotent` explicitly reuses the prior `IncomingCarry.carryIn_transfer_trichotomy` (`IncomingCarry__13645dd30c0ce73b.lean:141`): constant zero, identity on bits, or constant one. It then restricts `e` to the two cases supplied by `e ≤ 1`. The fixed-digit append identity comes from the existing `Agent8.fixedDigits_append` in `PrefixSemantics__3798a605dd95d8c6.lean:34`, rather than a new copy. The original append, decomposition, length, and bit-carry bounds are also reused unchanged.

## Declaration checks

All declarations below belong to `Agent1.RepeatedBlock`.

| Declaration | Semantic check |
|---|---|
| `terminalCarry_eq_carryIn` | Equality for arbitrary natural coefficients and carry; correct finite interval and orientation. |
| `terminalCarry_idempotent` | Idempotence of the same block's transfer on bit carries; does not assert independence from the incoming carry. |
| `terminalCarry_pow_succ` | Every positive number of copies has the first copy's outgoing carry. The induction preserves the bit bound before reusing the block. |
| `fixedDigits_pow_succ` | Keeps `fixedDigits w e` as the first, possibly transient block; only later copies use `fixedDigits w (terminalCarry w e)`. |
| `normalize_pow_succ` | Appends the single actual stabilized terminal carry once, after all fixed digits. It does not concatenate individually normalized blocks and their overflow digits. |
| `pow_length`, `bounded_pow` | Structural list facts valid also for zero copies and an empty block. |
| `normalize_context` | Prefix carry is computed from `B`; bounded `B` ensures it is a bit. The final suffix is evaluated with the stabilized carry and may be arbitrary. |
| `terminalCarry_context` | Same terminal carry for any positive copy count; no claim that this carry is a bit when the suffix is unbounded. |
| `terminalCarry_two_bands` | Both counts may vary independently. Bounded middle `H` is used to deliver a bit carry to the second repeated band. Final suffix `T` need not be bounded for this equality. |
| `terminalCarry_symmetric_bands` | Correct specialization to `v = w.reverse`, `T = B.reverse`, and equal counts. Reversal preserves the coefficient bound. No palindromicity of `H` is assumed or inferred. |
| `normalize_context_length` | All of `B,w,H` are bounded, so terminal carry is 0 or 1 and the appended carry contributes exactly its value to list length. |
| `normalize_symmetric_bands_length` | The bounds cover both reversed bands and contexts. Its list-length formula uses the single-copy carry and permits empty blocks; it claims no numeral canonicality. |

## Edge cases and necessity of bounds

The examples in this section were first obtained by direct evaluation of the inspected definitions. Each is now stated as an exact closed theorem in the reviewer-authored `Agent1RepeatedBlockBoundary.lean`, with proofs using kernel `decide` only and an explicit axiom print for every theorem. Their execution status is recorded below; there was no mathematical search.

- **Empty block:** `pow [] n = []`, `fixedDigits [] e = []`, and `terminalCarry [] e = e`. In particular, `normalize [] 1 = [1]`. The statements remain true and do not silently delete the incoming carry.
- **All-nine block:** on either bit input, its carry transfer is the identity. At incoming carry 0 every nine remains nine; at incoming carry 1 every nine becomes zero and the carry remains 1. The formula preserves this dependence. The two bands are not assigned a common independent carry.
- **First transient:** for `w=[10]`, `e=0`, the first fixed-digit block is `[0]` while the stabilized block is `[1]`. Two copies normalize to `[0,1,1]`, including the one final carry. Thus the first-copy distinction in the theorem is substantive.
- **Positive count:** at zero copies the carry is `e`; for `w=[10]`, `e=0`, one copy instead has carry 1. The `k+1` restriction is essential to the advertised stabilization.
- **Coefficient bound:** if `w=[19]` and `e=0`, the first block produces carry 1 and the second produces carry 2, so idempotence already fails one above the permitted maximum.
- **Incoming bound:** if `w=[8]` and `e=2`, the first carry is 1 and the next is 0. A bound on coefficients alone is insufficient.
- **Prefix bound:** with `B=[100]`, `w=[0]`, `H=[]`, `e=0`, one copy exits with carry 1 and two copies with carry 0. Bounded `B` is a sufficient, correctly supplied condition for the first repeated band to receive a bit.
- **Middle bound:** choose `B=[]`, `w=[]`, `H=[100]`, `v=[0]`, `T=[]`, `e=0` in the two-band shape. One versus two copies of `v` again exits with 1 versus 0. The `hH` premise cannot simply be dropped.
- **Arbitrary final suffix:** equality of the suffix input suffices for exact list/carry equality, even without a bound. It does not ensure that the output is a decimal digit list: `normalize [100] 0 = [0,10]`. In particular, the terminal carry cannot be interpreted as an overflow bit or as the number of appended digits without the extra bound used in the length theorem.

## Meaningful application and preserved guard-period boundary

The reviewed exact normalization formula supplies the first-transient/stable-period decomposition missing from the existing pairwise locality theorem `IncomingCarry.actual_repeated_block_output_locality` (which requires a preceding non-nine). It applies to arbitrary block length and includes the all-nine and empty cases. This is more than an append identity, while preserving the prior carry-transfer classification's attribution.

For fixed bounded `B,w,H`, the two-band endpoint proves that the actual scan carry of

`B ++ pow w (k+1) ++ H ++ pow w.reverse (k+1) ++ B.reverse`

is independent of the positive count. This is exactly the carry-independence subargument in the first paragraph of the guard-period proof in preserved `periodic_bulk_followup/METHOD_AND_PROOF.md`, section 4. The source file is `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/METHOD_AND_PROOF.md`.

A compact useful application is the symmetric list-width formula

`2 * B.length + 2 * (k+1) * w.length + H.length + gamma`,

where `gamma = terminalCarry (B ++ w ++ H ++ w.reverse ++ B.reverse) e`. The reviewed carry theorem, boundedness, and existing `Agent8.normalize_length` imply that formula; `Agent8.pair_length` gives the same output width after taking mirrored sums when `e=0`. This application fixes overflow independently of the exponent without claiming the full guarded image is known. The parent subsequently added this exact endpoint as `normalize_symmetric_bands_length`; its statement and proof were reviewed at the final context source hash. It uses only the existing normalization length formula, the new carry invariance, structural lengths, and the explicit bounds.

The rest of the guard-period statement remains separate: pair the normalized digits with their reversed list; account for the one-column reflected displacement when overflow is 1; identify `B_raw,H_raw,w'` from the transition at exponent 3; prove exact raw guard widths and the image identity at every exponent at least 3; and verify quotient stripping and exponent change. These obligations do not follow merely from knowing the terminal carry or total list length. No safe cycle, persistent safe family, or ordinary integer infinite orbit is supplied here. The preserved Python controls at exponents `(3,4,7,31)` were inspected as source only and were not rerun.

## Interpretation limits and execution status

These statements concern list normalization and list length. The normalizer retains leading zeros: a list of zero coefficients remains a list of zeros, whose length can exceed the canonical decimal width of the represented integer. Symmetric band shape alone does not enforce that `H` is a palindrome, that the outer coefficient is positive, or that an odd center coefficient is even. For the intended ordinary whole-word application, specialize to the relevant canonical hypotheses and `e=0`; the prior `Agent8.terminalCarry_eq_actual_overflow` in `PrefixSemantics__3798a605dd95d8c6.lean` explicitly supplies the outer-overflow interpretation under `CanonicalPair`.

All five prior dependency blobs match both the author's pins and the checked-out base, as recorded in `source-identity.json`. The author baseline result file reports successful compilation of those five prior modules; the reviewer inspected that receipt but did not execute it. The reviewer independently executed all eight modules in the fresh directory `/workspace/p196-agent1-session-20261016/repeated-review-clean-001`, with `LEAN_PATH` restricted to that directory and no reused project `.olean` files. Every compile used `--trust=0 -j1 -DElab.async=false` and exited 0. Lean was `4.19.0`, compiler commit `6caaee842e94`, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

The separate `ReviewAudit.lean` also exited 0. It enumerated every theorem constant in the selected eight-module closure: **1,236 theorems**, with transitive axiom union exactly `Classical.choice`, `Quot.sound`, and `propext`. It rejected custom safe axioms, disallowed transitive axioms, and missing audited modules; generated unsafe implementation declarations were recorded separately and were not accepted as theorem dependencies. All **23 new theorem** axiom prints are present. All **10 boundary witnesses** depend on **no axioms**. New source contains no `sorry`, `admit`, `native_decide`, `sorryAx`, or `Lean.ofReduceBool`.

The complete commands, exit codes, runtime measurements, source snapshots, compiler fingerprint, audit source, logs and log hashes are in `clean-001/`; the result is `clean-001/verification.json`. All source hashes were rechecked against the working files after the audit. There were no failed attempts in this reviewer replay. This is a scoped result for these eight modules, not a repository-wide pass. Parent/author results are separate receipts.


## Final reviewed source hashes

| Module | SHA-256 |
|---|---|
| `Agent1RepeatedBlock` | `4dc552677e5b7f1484fa2c765378bae02236033a4c5d42858f84b258a9f30d12` |
| `Agent1RepeatedBlockContext` | `d73d6825fbae0da63595073d82ee32e7cdf7dad1a8c6aa4efa8e29cf99911eb3` |
| `Agent1RepeatedBlockBoundary` | `fd1dd6626cc6acba656d8d34fddc327bf7cfa6d8b5dd826b262117e1562628d5` |

No unresolved statement defect was found in the reviewed core/context endpoints. The explicit canonicality and guard-extraction boundaries above remain essential interpretation limits, not compile blockers.
