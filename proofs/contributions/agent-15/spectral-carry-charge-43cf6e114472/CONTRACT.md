# Exact spectral carry-charge symmetry

## Original claim and provenance

Source snapshot: `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`.
Original derivation: `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral_notes.md`, Git blob `cb1c355fa05916a770816a4d5ef680e54079cccb`.
Original executable definition: `proofs/creative_global_spectral__8de5a77a944d0d04.py`, Git blob `730acd722bf017b6bf1e51e5a0411169a7804da4`, function `carry_coordinates`.

The source claims that the integer antisymmetric carry charge J vanishes exactly when the full outgoing-carry word is symmetric. This package formalizes that claim. The original derivation and implementation retain their mathematical provenance; Agent 15 supplies an independent formalization, not a novelty claim.

The carry word is `c = [c_0, ..., c_(L-1)]` in least-significant-first order. Each entry is either 0 or 1 and denotes the carry leaving that column. The last entry is the actual overflow bit. The separate incoming carry zero is not appended to this word.

## Exact definitions

All weights and charges use unbounded Lean integers. Define

```
U(0) = 0, U(1) = 1;
S(0) = 1, S(1) = 21;
X(k+2) = 20*X(k+1) - X(k).
```

The source charge is

```
L = 2*m+1: J(c) = sum_(i<m) (c_(2*m-i)-c_i) * U(m-i).
L = 2*m:   J(c) = sum_(i<m) (c_(2*m-1-i)-c_i) * S(m-1-i).
```

The odd central carry cancels from J. It remains part of the full word and is unrestricted within the binary domain.

Implementation uses `oddWeight k = U(k+1)` and `evenWeight k = S(k)`, with a highest-weight-first finite evaluator:

```
weighted w [] = 0
weighted w (a :: xs) = (a : Int) * w xs.length + weighted w xs
```

For `m = c.length / 2`, take the difference between the evaluation of `c.reverse.take m` and the evaluation of `c.take m`. Select odd/even weights from the actual length parity. Expanding the evaluator gives exactly the two displayed source formulas, with the same sign and indices.

## Proof obligations and intended interfaces

Namespace: `P196.Agent15.SpectralCarry`.

1. `SpectralWeights.lean`: exact recurrence equations, positive used weights, and strict domination of every used weight over the sum of its predecessors.
2. `BinaryCode.lean`: a finite binary word has weighted value between zero and the sum of its weights; the evaluator is injective on binary words of equal length for a strictly dominating sequence.
3. `ChargeSymmetry.lean`: equality of the two outer half-words is equivalent to full reversal symmetry; the exact parity-selected charge is zero if and only if the full binary carry word equals its reverse.
4. Kernel-checked controls cover empty and singleton words, both parities, a symmetric nonzero carry word, the nonsymmetric carry word `[0,1,0,0,1,1]` with charge 419, and an explicitly nonbinary counterexample to dropping the coefficient hypothesis.

The final endpoint must quantify over every finite binary word, not only a bounded enumeration or carry words appearing in a sampled trajectory. The input need not be symmetric, normalized further, or assumed to have zero charge. No additional carry is inserted or discarded.

## Quantifiers and boundary cases

For every `c : List Nat`, if every member is 0 or 1, then `carryCharge c = 0` if and only if `c.reverse = c`. This includes all physically possible carry words. The empty list is an explicitly labeled algebraic extension. Length one has zero charge because there are no mirror pairs; either binary singleton is symmetric. Length two uses `S(0)=1`. The odd one-pair case uses `U(1)=1`, never `U(0)=0` as a charge weight.

Binary-coefficient assumptions are essential for this interface. The general recurrence and finite evaluator may be defined more broadly, but their binary injectivity theorem must not silently be promoted to an unrestricted integer-coefficient assertion.

## Scope and dependencies

Only Lean 4.19.0 `Std` and the new local modules are intended mathematical dependencies. The previously compiled `LychrelDigitSums` baseline establishes environment functionality and is not a dependency of this package.

Agent 14 owns the complementary T/R coordinate and its fixed-width injectivity on 0..18 coefficients. This package does not duplicate or claim that result. It does not formalize the real quadratic interpretation, H, the four evolution laws, the universal quotient ideal, or a new no-nine lemma. Existing coefficient normalization and non-nine reset results retain their original authorship.

Charge vanishing detects carry symmetry. It does not identify the input integer, establish a palindrome criterion by itself, prove persistent nonzero charge, or prove any all-time result about 196.

## Verification and ownership

Successful guarded coordination claim: `9ff01fb85383833abe440d7f41bc7c249c332070`; exact task blob `70340af5e48d1c965d012180c04bc6ea01f90b21`.
Task: `agent15-spectral-carry-charge-43cf6e114472`.
Owned contribution branch: `formalize/agent-15/spectral-carry-charge-43cf6e114472`.

Compile the complete selected local closure from source in a fresh directory using official Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`. Print every public declaration and its transitive axioms; inspect all module-origin mathematical declarations as a separate audit. Only `propext`, `Classical.choice`, and `Quot.sound` are permitted foundational axioms. No `sorry`, `admit`, `sorryAx`, `native_decide`, compiler oracle, or new mathematical axiom is accepted.

Root and the weights specialist author distinct files. The runtime and ownership specialists remain nonauthors for independent execution and semantic review. Preserve original and failed source attempts, commands, complete substantive logs, exact source/compiler hashes, and review attribution. Main integration and shared generated-index changes belong to the designated integration owner.
