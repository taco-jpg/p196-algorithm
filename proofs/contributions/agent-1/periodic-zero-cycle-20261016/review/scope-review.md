# Adversarial source review: periodic realization and zero-period cycles

Agent #1 specialist `/root/research_status`, 2026-10-16. This is source and statement inspection, not a new theorem or a Lean execution result. No mathematical source or Git state was changed for this report. Initial proposal was issue61 comment [6225746264](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225746264); the exact zero-cycle proposal is [6225781689](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225781689). During inspection, parent reported successful claim publication `d5786f691f77c606f7343b1182cc67643f058a8f` and opened `/workspace/p196-agent1-zero-cycle-20261016`. This report reviews the proposed obligations; it does not certify the still-being-authored new modules.

## Assessment

The pointwise realization proposal has the right contract: retain all seven original `ValidPeriodic` fields, require `0 < k`, assemble original indexed `FoldedDecimal.Admissible`, and immediately apply original `FoldedDecimal.valid_word_realizable`. The generic positive canonical realizer already exists. The additional period-specific middle-parity transport is the only property omitted by existing `periodicWord_canonical`'s `Agent8.CanonicalPair` conclusion.

No semantic contradiction was found in the proposed zero-period obstruction. Its crucial unfinished link is **full list/index actual-step representation**, not decimal width alone. The cycle argument must construct one fixed positive ordinary integer whose every actual iterate has the displayed quotient pair word. Choosing a different realization at each time does not establish an orbit. The existing mass-unboundedness theorem needs no safety or nonpalindromicity assumption, so the claimed omission of safety is appropriate if the full correspondence and exponent guards are proved.

## Exact existing results to reuse

All line numbers in this section refer to `proofs/LychrelDigitSums__75febdc48f0ca802.lean` unless otherwise stated.

* `DecimalDigits.Canonical` (907) means positive width, all in-range digits at most nine, strictly positive most significant digit `d (L-1)`, and `value d L = n`. It must remain the numeric contract; a coefficient-list length alone is insufficient.
* `FoldedDecimal.valid_word_realizable` (1469) takes positive width, positive outside coefficient, coefficient bound eighteen, reflection equality and even fixed middle coefficient. It returns `∃ n d, 0 < n ∧ Canonical n d L ∧ ∀ i < L, columnSum d L i = q i`. The implementation already uses `realizingDigit`; no new generic decoder is needed.
* `FoldedDecimal.Admissible` (1518) packages those five exact indexed conditions. Entries outside the first `L` positions are irrelevant.
* `FoldedDecimal.representation_next` (1568) carries a canonical realization through the original `Lychrel196.step`, preserving every in-range pair sum for `nextColumns q L` at `nextWidth q L`.
* `OverflowCarryNormalization.iterPairs_representation` (2400) carries **one fixed initial** canonical realization along the entire ordinary orbit, at the exact changing width.
* `DecimalMass.wordSum_columns` (4555), `digitSum_value` (4563) and `DecimalUnboundedMass.iterPairs_wordSum` (5143) already provide the necessary factor-two mass identity. The latter concludes
  `wordSum (iterPairs q L t).2 (iterPairs q L t).1 = 2 * digitSum (Lychrel196.orbit n t)`
  under original Canonical and initial in-range representation hypotheses.
* `DecimalUnboundedMass.digitSum_unbounded_after` (5255) has only `0 < n` as an arithmetic hypothesis. `not_eventually_bounded_digitSum` (5264) is a convenient direct contradiction endpoint. Neither theorem requires safety or stopping before a palindrome.

The already-reviewed period-specific chain is `periodicWord_canonical`, `middle_append_eq`, `quotient_valid`, `quotient_step_bounded`, `quotient_exponent_accounting` and `quotient_width_balance`. The last two retain signed exponent increments explicitly; no replacement arithmetic is needed.

## Proof obligations that must not be silently omitted

1. **Exact cycle object.** A positive-length cycle must return the full stored tuple `(B,H,w)` under the exact executable quotient, not merely its phase, length, exterior projection, rotated period, or an observation. Require positive cycle length. Either retain `ValidPeriodic` at every vertex or derive it explicitly from initial validity using `quotient_valid`.
2. **Zero period is a theorem, not a phase convention.** Establish literal `rawPeriod B H [0,0,0,0] = [0,0,0,0]` under the actual bounded-input hypotheses, with the original carry and raw slices. Existing constant-phase template theorems use `Agent109.Phase` (`1 ≤ c`, `c ≤ 17`, `c ≠ 9`) and therefore do not cover `c=0`. The first-block carry transient must remain in the guard; no assumption of zero incoming carry throughout the word is permitted.
3. **Leading-zero exclusion.** With zero period, original `outside_positive` forces a nonempty positive-headed exterior. The tuple with all empty/zero data is not valid. Do not weaken to bounds and symmetry or use a coefficient list's apparent length as ordinary numeral width. Empty center is allowed. Empty exterior is allowed by general realizability only when the actual period supplies a positive outside coefficient; it is unavailable in the zero-period case.
4. **Pointwise realization.** `k > 0` is essential because positivity is about `B ++ w`. `CanonicalPair` does not supply odd-middle parity. Use equal exterior lengths plus `middle_append_eq` to transport `ValidPeriodic.center_even`; do not assume the displayed band shape alone implies realizability. The resulting witness may depend on `k`; the assertion is not one integer realizing every exponent.
5. **Every prefix guard.** The initial proposed route sums the exact width identity around a full state cycle, yielding `8 * sum(delta) = sum(rawGamma)` and nonnegative total shift. That alone does not guarantee each intermediate `k ≥ 3`; a signed-prefix argument would still be needed, without discarding negative increments through `delta.toNat`. Parent subsequently proposed a simpler, sound source-level route: obtain a finite bound `I(t) = 2*|B(t)|+|H(t)| ≤ M`, choose `k(0)=M+3`, and induct on `W(t)=I(t)+8*k(t) ≥ M+24`. The bound on `I(t)` yields the current guard `k(t)≥3` **before** using quotient accounting; the exact width balance then gives `W(t+1)=W(t)+gamma(t)≥W(t)`, closing induction. Thus no cycle-total-shift lemma or signed-prefix minimum is necessary. Keep the literal natural recursion `(k-2)+u+v` and convert the existing signed identity only after obtaining the current guard. There is no assumption that the exponent returns with the tuple.
6. **Full list/index bridge.** For a bounded actual coefficient list `W`, the needed correspondence is both `(Agent8.stepWord W).length = FoldedDecimal.nextWidth (fun i => (W[i]?).getD 0) W.length` and equality of its indexed coefficients with `FoldedDecimal.nextColumns` throughout that output width. `Agent1PeriodicNumeric.actual_step_canonical_width` calls `representation_next` but discards the returned pair-sum equality; its conclusion is insufficient to iterate the proposed argument. `terminalCarry_eq_carryIn` and `carryIn_zero_eq_carry` already supply the terminal-carry part. The digit/output-index and reflected-pair portions must also be justified, including overflow at the new final index.
7. **One fixed orbit and exact mass.** Realize one initial guarded word once. Preserve that same seed's canonical representation at every step using the full bridge. Prove the finite indexed sum/list sum equality and the zero-band sum identity. Finite cycle interfaces then give a uniform mass bound independent of the changing exponent; transfer it with the existing factor-two identity. A list coefficient sum is not automatically an ordinary digit sum. Bounds must cover all actual times, including intermediate vertices, not only cycle multiples.

An alternative to item6 is to establish genuine initial `Agent109.pairWord n = W` and invoke existing `Agent109.Compat.pairWord_orbit` (`Compat__a87d4fe51356e8b5.lean:73`). That equality is stronger than the pointwise Canonical/hrep witness and needs its own bridge. Importing the older list-numeral closure is a choice, not permission to assume equality. The direct indexed route already has the original realizer and mass theorem in the current dependency closure.

## Overlap and attribution boundaries

This review read the local coordination snapshot `2c53e20391c669ac876d94c27138ad29286e9086` and the two actual issue comments above; parent separately performed the fresh claim/race check and reported the later claim receipt. Absence of an endpoint in this limited inspection is not an assertion about every unpublished workspace.

* Agent104's exact zero-gap/mass task is `REVIEWED` and provides quantitative finite-prefix mass escape. The proposed obstruction should call the existing unconditional unboundedness theorem, not rediscover its zero-run propagation or quantitative growth proof.
* Agent4's active zero-gap departure task assumes separately canonical components and compares a different auxiliary recursion with the actual concatenated word. The proposed full tuple has arbitrary valid exterior `B`, which need not itself be symmetric; Agent4's theorem cannot simply be applied to it. Preserve that ownership.
* Agent110's current task is exact two-step nonreturn for original Agent6 exterior phase six. Earlier scalar/radix observable obstructions are also different state maps. None inspected supplies the literal period-zero full quotient no-cycle endpoint.
* Agent105's reviewed affine-dynamics scope includes eventual affine-run representations and uniform positive safe return time. Do not claim a new general affine-return theorem or its ordinary predecessor decoder. The zero-period proof is an exact obstruction for this already-defined quotient and may reuse existing orbit compatibility.
* Historical `periodic_interface_followup` is still the recorded owner of subsequent finite-interface/lift work; the earlier preserved periodic-bulk note explicitly pointed there. Its absent source path does not release it. Parent's narrow public proposal and claim exclude a general finite-interface search or return-lift takeover.
* The generic realizer, list-digit realizers and mirror parity results are preexisting work. The symbolic-scope report `/workspace/p196-agent1-session-20261016/periodic-realizability-scope.md` records the broader exact ownership census; this review checks its proposed mathematical interface rather than repeating that census. Its Agent3 `NormalizedSafety.lean` pin was confirmed by that author via exact GitHub contents API blob `94fdd08052afd20bea4a662c6505af2862ecf313`; that remote object is not present in the new local worktree database, so local `git show` failure is not evidence against the citation.

## Source identities inspected

The existing source bytes in the new worktree matched the safety evidence base `c74c9d1ca1fef5463738abac348a5d12eaab4a01`; newly authored files were not treated as frozen or verified here.

| File in `proofs/` | Git blob | SHA256 |
|---|---|---|
| `LychrelDigitSums__75febdc48f0ca802.lean` | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `Agent1PeriodicGuard.lean` | `7c62748625cecbc277ddd5e01ffb17671e4db7a8` | `4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91` |
| `Agent1PeriodicQuotient.lean` | `63bd5f4319f6a79924b7292db3eb82e0d027b26c` | `562ad271c282a8a246de344b5fa9ea7e96bd64f74098c3799c839853e792a9a4` |
| `Agent1PeriodicValidity.lean` | `3c5673981d4c9a73a0ade71552f5867d8f73dd69` | `4652df468f38ed9696f5b68616f5bfd9225ab6f377a4d449289d8c2ad65b0e52` |
| `Agent1PeriodicPositivity.lean` | `bc392c470c3bf3389f4ae0166cf67dcaf2462e89` | `481768dfb0d8884d61c038a886d5fc05131fc085286869c32190f80691e0b3d6` |
| `Agent1PeriodicParity.lean` | `c5a2bfb004aa8421110403195abf9951572e7b4b` | `8eb97092e0c402f24e8163b51ed902f7e83f39b3c2a663698b08375147f2e129` |
| `Agent1PeriodicNumeric.lean` | `710e899d559514f48e409569268929803dde3ce9` | `d3142b2a44bbe471df559e74bba993a9a663592b3bf04ce973e1ef94251873f7` |
| `Compat__a87d4fe51356e8b5.lean` | `0279661cd41c62e8b1e8f7fe53d005a80f79dd71` | `73dca78232b0c2c048da4d1d182f84b31c0e95bab283fad603fd342bf38616e6` |
| `TemplateStep__8873883b39064515.lean` | `75326d41c3f3d568cc32e86bc9aa5cdeb5f3e49d` | `76ad132fec23f9da8733f72a6baf22c3dbfe68d402a8165766bd8d163549d2ed` |

## Review boundary

No new proof or computation is certified by this report. Finite controls and a source-pinned complete fresh closure build remain later review work once authors freeze the exact modules. The proposed conclusion excludes only positive-length exact valid quotient cycles with zero period. It does not establish termination, a palindrome, safe closure, absence of nonzero-period cycles, a general finite-interface theorem, or a conclusion about196.
