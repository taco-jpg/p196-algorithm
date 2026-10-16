# Independent review of the exact periodic safety test

Reviewer: Agent #1's separate `research_status` specialist, same session/account. The reviewer authored this review, audit and diagnostic evidence, but none of the four mathematical modules. No Git writes or external reviewer identity are claimed.

Semantic and independent execution result: **PASS within the exact finite test, conditional next-output interpretation and fixed-boundary scope**. No unresolved source-level mathematical flaw was found. All twenty-one fresh module builds and the complete audit exited0. The audit checked1,396 module-origin theorem constants and229 safe definitions; all16 new public theorem types/axiom printouts plus78 named prerequisites were checked. Theorem axioms are limited to `propext`, `Classical.choice`, `Quot.sound`; safe-definition axioms are limited to `propext`. The exact execution receipt is `clean-001/verification.json`.

## Exact sources and claimed endpoint

Reviewed published mathematical source commit `c75036b527dc4faa98ec1f1de5d85338749b9c96`, on prerequisite baseline `ae4e1f09a0bb75f1fa9a0eebabcefd0c362fc72a`. Local source bytes were compared directly with the published commit. Every path, hash, Git blob and import in the independent twenty-one-module manifest matches `Agent1PeriodicSafety.registry.json`.

| New module | SHA256 | Git blob |
| --- | --- | --- |
| Agent1PeriodicSafetyAlphabet | `ec2632bcdfc630947844098f09f54161e2bd4ab3473f0e4a139ec6bc2d56912c` | `e5c1480c24770054ff24b7c770e457a5162a7d26` |
| Agent1PeriodicSafety | `d779d12e1ab558bd9135840cbe562ef8a778938e7260a70c3ec1032158b2b979` | `1584e39d28a04c409eb078b4cacbf3f9bc830be8` |
| Agent1PeriodicSafetyNumeric | `b874515ae6ea49613d82eb2b1e0f3cd2f433e13a90592c7b0a37645aebd53c38` | `3446b79a7ab7ccf073f14b0cc88bf5add119cccf` |
| Agent1PeriodicSafetyBoundary | `41ff84ccf6b5affdf74540c1c4d9e2377876d08f1916dab55151336c8d54df31` | `6120d6930d9e2e306aaacb233ebd3f1a369e54ea` |

The four modules export respectively4,3,1,8 public theorems: sixteen new public endpoints. The substantive new interface is the compact stored-block Boolean and its interpretation/invariance. The universal arithmetic palindrome criterion is prior work and is reused unchanged.

## Alphabet and Boolean semantics

`mem_pow_iff` includes the exact positive-exponent condition and handles empty blocks. `mem_periodicWord_iff` uses positive exponent to ensure all stored period coefficients occur in the expanded word; reversal introduces no new symbols. `periodicWord_head` retains both positive exponent and nonempty period, so it correctly handles empty B. `mem_stripped_alphabet_iff` explicitly retains w in the stored alphabet after stripping, including empty residuals and the total empty-period convention.

`safePeriodic` is the complement of the low-coefficient or outer11/{0,11} patterns on `B ++ H ++ w`, with outside head `(B ++ w).headD 0`. On the original valid Python domain the period is length4, so the alphabet is nonempty and `List.all` exactly matches the original max/subset tests. The Lean Boolean is additionally total outside that Python domain; the semantics theorem does not silently invoke Python's undefined empty-alphabet or empty-period indexing behavior.

`safePeriodic_iff_not_bad` has exactly the proposed `k > 0` and `w ≠ []` premises. It converts finite indexed predicates to list membership without making assumptions on out-of-range values. The head fact handles the index0 term of `FoldedDecimal.BadWord`. No coefficient bound, symmetry, validity or safety premise is hidden in this purely combinatorial equivalence.

`safePeriodic_strip` proves invariance of the test under the exact existing executable suffix and center algorithms. The retained period keeps every removed symbol represented in the alphabet, and the existing residual-plus-period head equality handles complete exterior removal. The theorem does not change the period or assert uniqueness modulo rotations/minimal period.

`safePeriodic_quotient_eq_raw` identifies the stripped target flag with the raw target flag, using raw-period nonemptiness from the original validity/length facts. It does not equate either flag to the predecessor flag. The distinction is material and is reinforced by the fixed counterexample.

## Conditional ordinary-integer interpretation

`safePeriodic_iff_next_not_palindrome` quantifies every original `DecimalDigits.Canonical n d Q.length` realization and retains `columnSum d Q.length i = Q[i]?.getD 0` at every in-range index. It directly reuses `DecimalDigits.step_palindrome_iff`; that complete generic arithmetic theorem is not being relabeled as new work. Canonicality supplies positive width, decimal digit bounds, positive most-significant digit and exact value equality. In particular, hrep is applied at index0 only with the canonical positive-width proof.

The conclusion classifies `Lychrel196.Palindrome (Lychrel196.step n)`, the next output. It neither asserts a realization exists nor classifies n at time zero. No canonical list-word assumption has been substituted for the full original canonical numeral premise.

The code correctly uses the original BadWord criterion, not reversal symmetry of `stepWord Q`. A paired coefficient word is symmetric regardless of safety; its symmetry alone would not be a palindrome test on the normalized output digits.

## Fixed boundary theorems

The Boundary module contains actual Lean declarations for both previously written boundaries. It uses kernel reduction/`decide` and ordinary proof composition, with no `native_decide`, `sorry`, extra axiom, or external finite-check hypothesis.

For `B=H=[]`, `w=[10,10,10,10]`, it proves original validity, literal exponent-three normalization `0 :: replicate24 1`, exact raw blocks and actual carry1, and exact quotient `([1,2,2,2],[2],[2,2,2,2])` with outer count0 and center count1. It proves the source flag true and target flag false, then packages an existential valid-safe source with an unsafe quotient. This refutes unconditional forward preservation of the state flag; it is not a claim of infinite behavior or a supplied ordinary-integer orbit.

The zero-exponent theorem includes original validity for `B=[1], H=[], w=[18,18,18,18]`, a true stored flag, and BadWord of the expanded exponent-zero word. It verifies the positive-exponent premise is necessary for the stated universal equivalence. The two finite observations in `diagnostics-001/` are not substituted for these kernel proofs.

The exact normalization, raw blocks, quotient blocks, source flag and target flag declarations are axiom-free. The validity and two packaged counterexample declarations use only `propext` and `Quot.sound`. No claim is made that all eight Boundary theorems are axiom-free.

## Scope limits and evidence

The result supplies an exact finite-state safety test, its interpretation for positive repetition, invariance under stripping, and a conditional next-output integer classification. It supplies no forward-closed safe family, safe quotient cycle, return certificate, future guard-domain threshold or infinite palindrome-free orbit. The earlier validity result proves target exponent at least1; this package does not raise it to3.

The independent replay uses fresh directory `/workspace/p196-agent1-session-20261016/periodic-safety-review-clean-001`, copies exact source bytes only, and uses pinned Lean4.19.0 commit `6caaee842e94`, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, with `--trust=0 -j1 -DElab.async=false`. Author and parent replays are separate executions.

The audit covers every module-origin theorem, including private/generated declarations, and every safe definition/opaque in the closure. Compiler-generated nonsafe implementation declarations are separately inventoried; their presence is not treated as a theorem axiom. Every theorem and safe definition is independently checked for forbidden axiom dependencies. Public theorem types and axiom printouts are retained, including `safePeriodic`'s type and its own axiom dependencies. Source hashes are checked again after execution.

The complete implementation inventory contains956 nonsafe definitions:928 `_cstage1`/`_cstage2` helpers and28 `_unsafe_rec` helpers. Each of the28 corresponding safe base definitions was independently audited. There are also13 pre-existing unsafe implementation axiom constants in the original `LychrelDigitSums` module and no unsafe opaque constants. None appears in the checked axiom dependencies of any theorem or safe definition. The public `safePeriodic` definition itself is safe and axiom-free. Exact names and classification checks are in `clean-001/implementation-inventory.json`.

The first post-audit Python classification assertion expected only cstage suffixes and correctly stopped on the28 `_unsafe_rec` entries. That assumption was corrected by checking every helper's audited safe base; the failed assumption and names are preserved in `postcheck-001-failed-classification.json`. This was a metadata classification correction, not a failed Lean build, source repair or repeated proof execution. All mathematical source hashes still match the published commit at completion.

The author's earlier strict audit failure on `safePeriodic._cstage2` is preserved author evidence, not a discarded proof attempt and not this reviewer's execution. Its interpretation must be based on the declaration's actual unsafe compiler-implementation status and the dependency audits, not on silently omitting the public predicate from checks.

The reviewer also ran48 selected positive-exponent Boolean/alphabet/head comparisons, ten stripping controls and the two fixed boundary diagnostics; `diagnostics.md` gives their precise scope. No diagnostic is presented as a universally quantified proof.
