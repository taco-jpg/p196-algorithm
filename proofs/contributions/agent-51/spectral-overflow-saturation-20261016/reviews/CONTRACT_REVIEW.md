# Independent semantic contract review

## Verdict and verification level

**PASS: the mathematical contract preserves the selected source claim.** The proposed explicit family is a valid specialization of the source construction, and its uniform threshold preserves both source parity thresholds. This review is independent of proof authorship. The reviewer did not author or modify `OverflowDigits.lean`, `OverflowWitness.lean`, `ResidueSums.lean`, or `Saturation.lean`.

This is a **source-semantic contract review**, not an assertion that the new modules compile or that their final declarations have passed axiom audit. Those checks remain pending. One administrative item remains: the contract should list the final exported theorem identifiers before final acceptance, as required by contract item I. This omission does not change the mathematics or block implementation.

## Reviewed evidence and exact pins

- Accepted task: `agent51-spectral-overflow-saturation-20261016`, owner Agent #51, accepted coordination commit `809f3db5d5837bc79be3624c5f3f485fdff2b069` and task blob `c6e10644a2398bdc19262a80bec7f06144b8f25d` as supplied by the coordinator. This review did not independently contact the remote service.
- Reviewed local task bytes: `/dev/shm/p196-agent51/evidence/task.json`, SHA-256 `b04f3916316aa5dc86d2b360ca7a931d6c7274e0d01484cb1dd3bb6d634100d8`.
- Pinned source snapshot: `54ac7c885e54ce74190b85ec82cceca2b23c2e38`.
- Original source: `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/astra_spectral_carry_quotient.md`, Theorem 3, overflow saturation paragraphs. The independently computed Git blob of the retained exact text is `eac5b8f61385a615d9cc3e7796a4d698c66b716b`; SHA-256 `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09`.
- Reused arithmetic source: `proofs/LychrelDigitSums__0810ace083af80c5.lean`; independently computed Git blob `8a865176625283648a8a20dd2411ed77670eb0a2`, SHA-256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.
- The full supplied dedicated-formalization role prompt was read. Ownership, exact-statement preservation, independent-review separation, foundational-axiom restrictions, and prohibition of bounded enumeration as a substitute for universal widths apply.

## Exact source claim and selected scope

The selected source paragraph asserts that, at every even input width L >= 18 and every odd input width L >= 19, each of the nine retained classes s has a canonical, nonpalindromic ordinary integer representative with actual terminal overflow h = 1 and palindromic next reverse-and-add output. The representative has s = (Q(1)/2) mod 9 and r = (Q(-1)/2) mod 11 = 0. The source chooses k in {1,...,9}, uses coefficient 11 in k symmetric pairs including the outer pair, and zero in all other positions, including the center when L is odd.

This task covers that overflow saturation statement, its explicit arithmetic witnesses, and the literal residue evaluations. It does not cover carry-free saturation, the full ideal equality or quotient-ring classification, the universal no-go consequence for arbitrary predicates, any orbit reachability assertion, or the all-time 196 conjecture.

## Quantifier and domain audit

The main existence statement must have the effective order

    for every natural L >= 18,
    for every natural s < 9,
    there exist n and decimal digits d such that all witness conclusions hold.

Equivalently, s may be quantified first because both are universal. The witness k may depend on s; n and d depend on L and k. The threshold is independent of s. The constructor theorem is stronger and should retain its unrestricted parameters k >= 1 and L >= 2*k, rather than silently specializing all construction lemmas to nine small values.

The nine-value modular choice is finite and may be proved by kernel-checkable finite reasoning. This is not a substitute for a universal width proof: L must remain an arbitrary natural throughout construction, canonicality, overflow, and palindrome arguments.

The uniform threshold L >= 18 covers exactly the union of the stated parity regimes: an odd natural L >= 18 is automatically at least 19, and an even natural in scope is at least 18. Explicit parity corollaries will make the source correspondence transparent.

The input domain is positive ordinary natural numbers in base ten. The fact that Q(-1) can be negative requires integer-valued evaluation; a truncated natural-number alternating sum would change the statement.

## Construction audit

With positions counted from the least significant end, take d(i) = 2 for i < k, d(i) = 9 for L-k <= i < L, and d(i) = 0 otherwise. Under 1 <= k and 2*k <= L, the two blocks are disjoint, each contains exactly k positions, and reflection exchanges them. The actual column sum is therefore 11 on those 2*k positions and zero elsewhere. In particular the outer column sum is 11.

The leading digit is 9 and the units digit is 2. Hence the input has a nonzero leading digit, is positive, and cannot be palindromic. The nonpalindromicity claim must use ordinary numeric reversal or the existing proved canonical-digit equivalence, not an unrelated string predicate.

At the boundary L = 2*k, the two blocks meet without overlap and leave no zero gap. For odd L, the minimum possible gap has length one and contains the central zero. Thus no pair is counted twice and the odd central coefficient remains even. The concrete smallest constructor boundary k = 1, L = 2 gives input 92 and next output 121, consistent with the universal formulation. This example is explanatory only and is not offered as proof evidence.

The choice of contiguous edge pairs is a valid specialization of the source's freedom to choose any k symmetric pairs containing the outer pair. It suffices for all nine classes; the source does not require surjectivity over all possible coefficient patterns.

## Arithmetic bridge and exact-width obligations

`DecimalDigits.columnSum d L` is the sum of actual reflected decimal digits. `DecimalDigits.carry q L` is the carry entering position L, which is exactly the source's carry leaving position L-1. This is the only indexing shift between the source h and the Lean terminal carry.

The following existing interfaces preserve the intended arithmetic semantics:

- `DecimalDigits.Canonical n d L` supplies positive width, bounded digits, a nonzero leading digit, and `value d L = n`.
- `DecimalDigits.reverse10_value` and `DecimalDigits.step_value` connect fixed-width digits with the independent ordinary natural-number reversal and reverse-add functions.
- `DecimalDigits.palindrome_value_iff` connects ordinary numeric palindromicity with symmetry of canonical digits.
- `DecimalDigits.overflow_palindrome_iff` derives terminal carry 1 and output digit symmetry from outer coefficient 11 and all coefficients in {0,11}.
- `DecimalDigits.step_palindrome_iff_overflow` converts the same actual coefficient criterion into `Lychrel196.Palindrome (Lychrel196.step n)` once actual overflow is established.
- `FoldedDecimal.canonical_next_overflow` proves that the step has canonical digits `extended q L` and exact width L+1.
- `DecimalQuantitativeMass.decimalLength_of_canonical` is an existing optional bridge to a numerical width equality. Canonicality itself already fixes width semantically; an explicit numerical width conclusion is useful for public coverage.

Actual overflow must be proved, not inferred merely from the word “overflow” in a definition or assumed as a hypothesis of the final existence theorem. The output canonicality or exact decimal-length result must include the new leading digit at position L.

Digits outside the interval [0,L) do not contribute to the numeral or its finite coefficient polynomial. Any total-function extension beyond this interval is acceptable provided every theorem uses the correct finite width and no out-of-range coefficient is inserted into the sum.

## Literal residues and division audit

Let q = columnSum d L and define the literal polynomial evaluation by

    Q(x) = sum over 0 <= i < L of (integer q(i)) * x^i.

A recursively defined helper is acceptable only with a proved correspondence to this exact finite sum, or a definition whose recursive equations transparently are that finite sum. In particular the final theorem must connect residue helpers to actual column sums, not simply define a residue to equal the desired answer.

There are 2*k coefficients equal to 11, so Q(1) = 22*k. Integer halving is exact and gives (Q(1)/2) mod 9 = (11*k) mod 9. If a natural sum is used for the evaluation at 1, its integer conversion must agree with the shared polynomial semantics.

For even L, the signs in each mirrored pair are opposite, so Q(-1) = 0. For odd L, the signs in each pair agree, so every pair contributes either 22 or -22 and Q(-1) is divisible by 22. In the chosen contiguous family, Q(-1) is in fact 0 or 22, but this extra simplification is not required by the source. Divisibility by 22 proves exact halving and then (Q(-1)/2) mod 11 = 0. No property of natural-number truncated subtraction may stand in for this argument.

The map k -> 11*k mod 9 permutes the nine residues for 1 <= k <= 9, because 11 is congruent to 2 modulo 9 and 2 is invertible modulo 9. The explicit sequence is 2,4,6,8,1,3,5,7,0. Choosing one of these nine k and using L >= 18 supplies 2*k <= L uniformly.

The even-width conclusion is about Q(-1), not about n mod 11. There is no general conclusion n mod 11 = 0 at even width, and the contract correctly excludes it. Likewise, these witnesses need not be reached by the orbit of 196 or by any designated earlier state.

## Final acceptance checklist

Before this review can advance from contract PASS to final source-semantic PASS, inspect the frozen declarations and verify:

1. Exact exported theorem names and source-to-theorem mapping are recorded.
2. Quantification is universal in all widths in scope, with no finite-width bound or hidden positivity/overflow premise added to the final existence result.
3. Canonicality, numeric nonpalindromicity, actual terminal carry, numeric next-step palindromicity, and exact input/output widths are conclusions for the same witnesses.
4. Both literal residue expressions evaluate the actual coefficient polynomial; division at 2 is exact and alternating sums use integers.
5. The source parity corollaries follow from the universal-width endpoint.
6. All local imports are freshly compiled and exported/transitive axiom results are actually inspected; no `sorry`, `admit`, `sorryAx`, `native_decide`, `Lean.ofReduceBool`, or new mathematical axioms are accepted.
7. Build evidence and final exact source hashes are retained separately from this source-only contract review.

No mathematical gap was found in the proposed construction or its correspondence to the selected original statement. No compilation or final-proof acceptance claim is made by this document.
