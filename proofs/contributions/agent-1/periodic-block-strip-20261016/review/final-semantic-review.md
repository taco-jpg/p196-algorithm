# Independent semantic review of the finite periodic quotient

Reviewer: Agent #1's separate `research_status` specialist, in the same session/account as the authors. The reviewer authored no mathematical module in this contribution, made no Git writes, and does not represent an external approval. Review and finite diagnostic scripts are reviewer-authored evidence.

Semantic result: **PASS for the stated finite list-algorithm and one-step quotient scope**. No unresolved source-level mathematical flaw was found. Independent fresh execution also **PASS**: all fourteen source modules and the complete audit exited 0; all 1,343 module-origin theorem constants use only `propext`, `Classical.choice`, and `Quot.sound`. All 26 new named theorems, 28 prior periodic theorems, and 13 repeated-block prerequisites have checked axiom printouts. Exact execution receipts are under `clean-001/`, including `verification.json`.

## Exact reviewed sources

The unchanged prerequisite source baseline is PR95 commit `95a17ceeaba51b7d2c14645401df5159a3d483d1`. The complete independent manifest is `final-source-identity.json`; all fourteen module entries were compared with the new scoped registry, including paths, hashes, Git blobs and imports.

| New source | SHA256 | Git blob |
| --- | --- | --- |
| `proofs/Agent1PeriodicOuterStrip.lean` | `734a8d8f639e5eac254e76de6eb8d9a41e377c6e87e0574be4478a3669cfb85c` | `9e35c06bf3dd393f33dfd2af965a1ea2d4305bc7` |
| `proofs/Agent1PeriodicCenterStrip.lean` | `566c7c5eac1fa54b98a9150a21f7ac61c403d8b0391b7aa92c1dbdea51c300c3` | `bfcfd913cfd7b4063c9b632f2b0461aafd9ca437` |
| `proofs/Agent1PeriodicQuotient.lean` | `562ad271c282a8a246de344b5fa9ea7e96bd64f74098c3799c839853e792a9a4` | `63bd5f4319f6a79924b7292db3eb82e0d027b26c` |

The new modules have respectively 6, 12 and 8 named theorem declarations. Generic list lemmas strengthen the period-four application to arbitrary nonempty period words where their statements say so. This is not an extension of the decimal coefficient model.

## Faithfulness to the preserved loops

The target is the two literal loops in `proofs/periodic_word_quotient__8404d0a63dd1fa13.py:51–52`, source SHA256 `122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425`. The period is the exact `rawPeriod` extracted from the original actual `Agent8.stepWord` image at exponent three. The source does not replace the carry computation or select a new phase.

`stripPeriodSuffixAux` checks nonempty period, sufficient suffix length, and equality of the entire suffix to the period. It recurs on the preceding prefix without reversing the remainder. Each removal increments the count once. `stripPeriodSuffixAux_spec` proves both reconstruction and no remaining full period suffix whenever the input length does not exceed the fuel; the public function supplies exactly that amount of fuel. Thus the maximum stopping claim is not conditional on an unexplained computational cutoff.

`stripPeriodCenterAux` compares the input to `w ++ stripPeriodMiddle w H ++ w.reverse`. `stripPeriodCenter_test_iff` proves this is exactly the length-at-least-two-periods, complete-prefix, reversed-complete-suffix condition used by the original loop. The length condition prevents overlapping removal. `stripPeriodMiddle_wrap` identifies the retained middle, and `stripPeriodMiddle_length_lt` justifies sufficient input-length fuel. The final decomposition and maximality concern complete period words, preserving order and the number of copies removed from each side.

Both public algorithms return the original input and count zero for an empty period. The center auxiliary alone may count empty wraps when supplied arbitrary fuel, but the public empty-period branch bypasses it; maximality is stated only for nonempty periods. No false empty-period maximality is exported. Actual raw periods have length four, discharged from the checked `raw_block_lengths` theorem.

Empty residual outer/center words are allowed. Constant, all-nine, palindromic and nonprimitive periods are not excluded. Complete length-four removal is not scalar single-letter trimming: residual runs shorter than four are retained. The claim is maximality relative to the exact supplied period, not a unique representation modulo rotations or changes of fundamental period.

The center's new boundedness and symmetry consequences are valid consequences of exact mirrored decomposition; they do not silently add the missing odd-middle parity or positive exterior conditions of `ValidPeriodic`.

## The composed theorem is the actual finite endpoint

`periodicWord_absorb` proves the needed identity for arbitrary words and natural exponents, including zero. Reversal of the exterior correctly places the removed copies on the opposite end; `pow_append` combines copies of the same word only. It does not commute different words.

`raw_guard_of_stripped` and `stripped_width_balance` expose explicit conditional decomposition interfaces. The public `quotient_step_bounded` then supplies those premises from the **executable** suffix and center algorithms. It assumes exactly the existing input coefficient bounds, input period length four, and `3 ≤ k`; no stripping equality, symmetry, realizability, safety or selected-carry hypothesis remains hidden in the endpoint.

The result is

```
stepWord (periodicWord B H w k)
  = periodicWord (quotientOuter B H w) (quotientCenter B H w)
      (rawPeriod B H w)
      ((k-2) + outerPeriods B H w + centerPeriods B H w).
```

`quotient_irreducible` supplies both exact stopping conditions. `quotient_width_balance` is the written one-step list-length identity with all terms cast to `Int`, and `exponentDelta` is the signed value `u+v-2`. `quotient_exponent_accounting` proves both that the natural target exponent is at least one and that its integer cast is `k + exponentDelta`. No negative shift is truncated to a natural number.

The width balance does not need an exponent premise because its two raw length equations are computed at the fixed exponent-three sample. The actual step identity does retain `k ≥ 3`. These are different, appropriate domains.

## Preserved limits

This formalizes the finite normalization subsection of the preserved periodic quotient, following the already checked raw guard. It establishes neither an accepted finite-interface cycle nor an infinite lift. The historical `periodic_interface_followup/` lane remains excluded; exact source and claim distinctions are retained in `ownership-source-scout.md` and the parent's scope documents.

In particular, this contribution does not prove:

* `ValidPeriodic` of the output, including its positive exterior and odd-center parity;
* safety or nonpalindromicity of the input/output, or an ordinary-numeral realization theorem;
* that the output exponent remains at least three, or an iterated guard-domain invariant;
* a return certificate, state cycle, cap-four obstruction, or infinite palindrome-free orbit.

The algebraic endpoint applies to bounded coefficient lists beyond the original valid-and-safe Python transition domain. That is an explicit strengthening of a finite identity, not an assertion that such inputs are canonical numbers. The list-length balance is not silently interpreted as ordinary decimal width.

## Independent evidence and reproduction

`replay.py` builds the exact fourteen-module import closure in a new empty directory using pinned Lean 4.19.0 commit `6caaee842e94`, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, with `--trust=0 -j1 -DElab.async=false`. It copies source bytes only, no project `.olean` files. Numeric is not imported by these roots and is correctly outside this closure; its prior independent audit is not counted as a new run.

The audit enumerates every theorem whose defining module is in that closure and checks its complete axiom set. It rejects nonstandard theorem axioms and safe custom axiom declarations, and requires every selected module to contribute audited theorems. Named theorem printouts are also checked, and source hashes are rechecked after the build. Logs, compiler identity, exact command results, source snapshots and the complete audit are preserved under `clean-001/`.

This reviewer used fresh directory `/workspace/p196-agent1-session-20261016/periodic-strip-review-clean-001`. No reviewer compile attempt failed, and every source hash still matched at completion. Author builds and the parent's canonical replay are separate executions and are not counted as this independent run.

The separate `diagnostics.md` and `diagnostics-001/` record the single successful Python control run: twelve targeted generic cases and fourteen actual raw inputs at five exponents each, covering both carry values. These finite controls are not substituted for the kernel proof and are not presented as formally proved counterexamples. No source or evidence from failed author attempts was removed.
