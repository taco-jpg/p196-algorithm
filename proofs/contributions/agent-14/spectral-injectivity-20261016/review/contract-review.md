# Independent semantic review: fixed-width spectral coordinate injectivity

## Review identity and status

- Reviewer: Agent #14 / `spectral_semantics`, independently assigned by the author/coordinator.
- Role: nonauthor semantic reviewer. No candidate proof source was authored or compiled during this review.
- Review status: `SEMANTIC_CONTRACT_ACCEPTABLE_WITH_EXPLICIT_SCOPE`.
- Repository snapshot: `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5` on `main`.
- Remote writes, task ownership, and issue #61 publication remain with the root coordinator. This file is a local review artifact for attributed relay and later Git preservation.
- Reviewed repository instructions: root `AGENTS.md`. A tracked-file search found no additional `AGENTS.md` under the affected tree.

This review approves a precise mathematical contract for the integer recurrence coordinate and its injectivity at a fixed ambient width. It does not certify a Lean proof, a build, real evaluation at beta, carry evolution, a palindrome criterion, or any conclusion about the 196 orbit.

## Pinned source evidence

The working copies were compared byte-for-byte with `git show <snapshot>:<path>`; both match the pinned snapshot.

| Source | SHA-256 | Git blob |
| --- | --- | --- |
| `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral_notes.md` | `e4a1e6b61848f473693c36d91d2a453b1dc82b26a347fa76b2a0b9a7e1228e27` | `cb1c355fa05916a770816a4d5ef680e54079cccb` |
| `proofs/creative_global_spectral__8de5a77a944d0d04.py` | `393545516c13d41c0416e560ec37bab6b1c1655357ae351b0f960dea76ff7448` | `730acd722bf017b6bf1e51e5a0411169a7804da4` |

The source-tree path preserves historical provenance `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`; the bytes actually reviewed were pinned through current `main` as above. The historical original commit was not separately rebuilt or otherwise audited here.

Relevant original-source locations:

- Notes lines 6–9: positive-integer pair-sum word, symmetry, coefficient order, and outgoing-carry convention.
- Notes lines 23–33: beta interpretation, integer recurrence seeds, and coordinate formulas.
- Notes lines 35–38: fixed-length injectivity and the dominance justification.
- Notes lines 58–66: separate neutral-nine and carry-coordinate claims.
- Notes lines 82–86: later use of injectivity on `q` and `11c`.
- Notes lines 88–99: explicit unresolved-orbit and verification limitations.
- Python lines 15–18: `rec(a,b,count)` returns exactly the requested prefix of the recurrence with coefficient 20.
- Python lines 20–26: `coordinate(q)` implements exactly the two displayed coordinate formulas.
- Python lines 46–53 and 55–69: verification assertions and sampling restrictions; these are not an injectivity proof.

## Exact definitions and indexing

Use integer-valued sequences, with subtraction interpreted in the integers:

\[
T_0=2,\quad T_1=20,\quad T_{k+2}=20T_{k+1}-T_k,
\]

\[
R_0=1,\quad R_1=19,\quad R_{k+2}=20R_{k+1}-R_k.
\]

For a finite word `q` of ambient width `L`, with index zero at the least significant end:

\[
A_{2m+1}(q)=q_m+\sum_{0\le i<m}q_iT_{m-i},
\qquad
A_{2m}(q)=\sum_{0\le i<m}q_iR_{m-1-i}.
\]

These match the Python implementation term for term. In particular:

- The odd center has weight **1**, not `T_0 = 2`.
- In an odd width, the outermost independent coefficient has weight `T_m`, and the innermost noncentral coefficient has weight `T_1 = 20`.
- In an even width, the outermost independent coefficient has weight `R_(m-1)`, and the innermost pair has weight `R_0 = 1`.
- The displayed subtraction `m-1-i` is used only under `i < m`. A Lean implementation using natural-number subtraction should keep that guard explicit in all index arguments.
- If the implementation reverses to center-out coefficient order, the odd coefficients are `a_k = q_(m-k)` for `0 <= k <= m`, with weights `W_0=1` and `W_k=T_k` for `k>=1`. The even coefficients are `a_k=q_(m-1-k)` for `k<m`, with weights `R_k`. Reindexing must itself be justified if the exported definition differs from the source sum.

The first weights are:

| Family | Weights in increasing order |
| --- | --- |
| Odd coordinate | `1, 20, 398, 7940, ...` |
| Even coordinate | `1, 19, 379, 7561, ...` |

## Minimal statements supplying the selected source claim

The natural generic domain is integer coefficient words satisfying, at the selected width:

\[
\forall i<L,\quad 0\le q_i\le18,
\qquad
\forall i<L,\quad q_i=q_{L-1-i}.
\]

For every fixed natural width `L`, and every two such words `q,r`, the required conclusion is

\[
A_L(q)=A_L(r)\quad\Longrightarrow\quad
\forall i<L,\ q_i=r_i.
\]

The parity-specific forms are equally adequate when exported together:

1. For every `m >= 0`, two bounded words symmetric at width `2*m+1` and having equal odd coordinate agree at every index below `2*m+1`.
2. For every `m >= 0`, two bounded words symmetric at width `2*m` and having equal even coordinate agree at every index below `2*m`.

The zero-width case of the second statement is an explicitly labeled algebraic extension. Restricting the source-facing corollary to positive width would also match the source domain.

If the word is represented by a total function `Nat -> Int`, the conclusion is equality **within the finite width**. Equality of the total functions is false without a condition on their values beyond that width. If the domain is `Fin L`, ordinary function equality is appropriate. List equality is also appropriate when both list lengths are established as exactly `L`.

The exact weight-dominance statements sufficient for this contract are:

\[
T_k > 18\left(1+\sum_{1\le j<k}T_j\right)\quad(k\ge1),
\]

\[
R_k > 18\sum_{0\le j<k}R_j\quad(k\ge0).
\]

Equivalently, the odd weight family `W_0=1`, `W_k=T_k` for positive `k` satisfies `W_k > 18 * sum_(j<k) W_j` for all `k`.

**Do not include `T_0=2` in the odd lower-weight sum.** That changes the intended central weight and already yields the false base inequality `20 > 18*2` at `k=1`.

For a generic bounded weighted-sum helper, positivity and the dominance property must be proved for these exact weights and used to prove finite coefficient equality. They must not merely be restated as an unproved premise of the final spectral result.

## Hypothesis review

| Condition | Role in the selected injectivity result |
| --- | --- |
| Coefficients are integers, or natural numbers | Essential to the bounded-digit argument: a nonzero coefficient difference has absolute value at least 1. Arbitrary real coefficients in the same interval do not satisfy this injectivity claim. |
| Each independent coefficient lies in `[0,18]` | Supplies the difference bound of 18. Bounds on all entries match the source and make the full-word statement direct. |
| Equal finite width | Required by the stated source claim. `A` alone is not a globally length-tagged encoding. |
| Symmetry within that width | Required to recover the entire word from the independent half used by `coordinate`. The weighted half-word injectivity helper itself does not need symmetry. |
| Positive leading coefficient | Present for actual positive-integer pair-sum words, but unnecessary for this integer injectivity theorem. Omitting it gives a valid strengthening. |
| Even center at odd width | Present for actual pair sums, but unnecessary for injectivity. Omitting it gives a valid strengthening and is useful for the source's later `11c` application. |
| Absence of coefficient 9 | Unnecessary. It is used only in distinct claims about carries and `J`; it must not be added to this theorem. |
| Decimal seed realizability | Unnecessary for injectivity of already given bounded symmetric words. Its connection to digit semantics is a separate bridge. |
| Carry bits, overflow, trajectories, stopping at a palindrome | Not part of this static theorem. |

The source begins with actual positive-integer pair-sum words, whereas the proposed generic theorem admits a larger class. The documentation should label this as a stronger bounded-word lemma covering the source's injectivity subclaim, not silently redefine the source's entire dynamical state space.

Allowing a zero outer coefficient also means that `L` is an **ambient word width**. The associated polynomial need not have degree exactly `L-1`; that source phrase relies on positivity and must not be imported into the generalized static contract.

## Boundary cases and adversarial checks

| Width | Coordinate | Exact recovery condition |
| --- | --- | --- |
| `L=0`, `m=0` | Empty even sum, hence `0` | Finite equality is vacuous, or equality of the unique `Fin 0` word. This is outside the source's positive-integer domain. |
| `L=1`, `m=0` | `q_0` | Coordinate equality is coefficient equality. Actual decimal pair sums are positive and even, but these facts are unnecessary. |
| `L=2`, `m=1` | `q_0 * R_0 = q_0` | Equality recovers `q_0`; symmetry gives `q_1=q_0`. |
| `L=3`, `m=1` | `20*q_0 + q_1` | Dominance is `20 > 18`; symmetry recovers `q_2`. |
| `L=4`, `m=2` | `19*q_0 + q_1` | Dominance is `19 > 18`; symmetry recovers the other two entries. |

The Python `coordinate(())` returns zero because the loop and sum are empty. The separate `verify(())` is not valid: it evaluates `q[0]` while checking positive leading coefficient. Therefore no claim that the original verifier accepts the empty word is justified.

Simple counterexamples identify prohibited overstatements:

- Without symmetry, width-two words `(1,0)` and `(1,1)` have the same coordinate.
- With total-function inputs, changing `q_L` while keeping all entries below `L` fixed preserves the coordinate and disproves total-function equality.
- Without a width tag, the valid words `(2)` and `(2,2)` both have integer coordinate `2`.
- The recovered object is the pair-sum word, not the original integer: decimal integers `12` and `21` both give pair-sum word `(3,3)` and coordinate `3`.
- Removing the coefficient bound invalidates the conclusion: reciprocal width-three words `(2,0,2)` and `(1,20,1)` both have coordinate `40`.

## Source caveats and exact remaining coverage

1. **Later use on `11c`.** Notes lines 82–84 call `q` and `11c` admissible symmetric coefficient words. A symmetric carry word can have central carry 1, making the center of `11c` equal to 11. Thus `11c` need not satisfy the even-center condition of a realizable odd-width pair-sum word. The generic bounded-symmetric-word theorem avoids that gap. Here “admissible” should be read as bounded and symmetric, not as full decimal realizability.
2. **Real interpretation remains separate.** A proof about the explicit integer recurrence sum does not prove that it equals `Q(beta)/beta^((L-1)/2)` in odd width or that the latter equals `sqrt(22)*A` in even width. It is exact coverage of the source's integer-coordinate injectivity subclaim only.
3. **Carry results remain separate.** The `H,J` decompositions, reflection behavior, four evolution identities, neutral-nine support, and `J=0` characterization are not consequences supplied by this static injectivity proof.
4. **Palindrome and orbit results remain separate.** In particular, the one-step algebraic palindrome criteria require additional bridges; an orbit invariant excluding the targets remains explicitly unresolved in the source.
5. **Code evidence is limited.** `verify(q)` checks evolution and carry support, not a pairwise collision-free assertion or a dominance theorem. The reported 85,447 cases therefore provide no substitute for the universal injectivity proof. This review inspected the source code; it did not rerun its full test suite.
6. **Number `187088`.** In notes line 69, `n=187088` denotes an integer orbit state, consistently with the Python variables `n` and `k`; it must not be misreported as an iteration count.

## Existing Lean interface inspection

At the pinned snapshot, a targeted search of current nonarchive `.lean` sources for spectral, Chebyshev, superincreasing, and dominant-weight terminology found no direct matching spectral declaration. This is limited evidence, not an exhaustive semantic deduplication or ownership claim.

The inspected `proofs/SignedDigitUniqueness__4e5556743a19b5f4.lean` and `proofs/SignedDigitUniqueness__68e74b603e8b47aa.lean` use `Std` and integer arithmetic. Their `SignedDigitUniqueness.eval` is Horner evaluation at a fixed integer base, and `all_zero_of_eval_zero_open` relies on that base-multiple structure. Those statements do not directly apply to the second-order `T` and `R` weight families. They provide a compatible arithmetic style but do not already cover this source claim.

No existing imported dependency, source module, accepted build, or axiom report is certified by this read-only interface inspection. The separate coverage specialist remains responsible for ownership and broader semantic overlap checks.

## Required later acceptance checks

The independent authored-source review should verify all of the following before raising the status beyond a semantic contract review:

1. Exact `T` and `R` seeds, integer recurrence, odd central weight, source index order, and any reindexing bridge.
2. Both dominance families, including their stated base cases.
3. Full finite-width word equality under only boundedness, symmetry, and coordinate equality; no conclusion is hidden in a premise.
4. Boundary cases `L=0,1,2`, and explicit treatment of parity selection in a unified-width wrapper if one is exported.
5. Axiom output for every exported result, with no `sorry`, `admit`, `sorryAx`, unproved mathematical axioms, or `native_decide` in the accepted dependency chain.
6. Actual compilation of the intended module, its inclusion in the intended build target, and an independent clean rebuild using the pinned toolchain and imports.
7. Claim-inventory wording that closes only the recurrence-weight dominance and fixed-width integer-coordinate injectivity obligations, leaving beta evaluation, dynamics, palindrome bridges, and 196 open.

The proposed target is semantically sound under these explicit definitions and boundaries. No proof implementation or build success is asserted by this report.
