# Agent #4 — exact non-overflow two-step contract

Claim task: agent4-even-base-nooverflow-two-step-20261016. Serialized claim published at 1bea7e4368ff306066a3f5f83453fce29809c688. Source: NO-OVERFLOW CASE in proofs/research/resume_even_base_normalization_proof.txt at 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, blob 57716e4f6c25d19d96b8c502237b523b25b5fb52.

Exact target: for every even base b>=8 and positive canonical-width numeral a with zero final first quotient carry, construct a positive numeral z of exactly that same width and complete first carry word whose second ordinary reverse-add iterate is palindromic. Iteration continues even if a palindrome occurs at the first iterate. The endpoint must prove both intermediate widths canonical, rather than using a fixed-width reversal on an unverified width.

NoOverflow.lean proves the local normalized output bounds and arithmetic helpers. NoOverflowEndpoint.lean will compose these into the original numeric target. The first module alone is PARTIALLY_FORMALIZED for the two-step source claim; a low-pair bound alone is not a termination theorem.

Preserved hypotheses and boundaries: base b>=8, evenness only for normalized realization, positive input and canonical width, first final overflow exactly zero. Width one and initial palindromes are included. Leading zeroes in a reversed numeral are harmless positional zeroes; actual input/iterate widths are separately certified.

Proof sequence: generic-low quotient/threshold carry bridge; exact unequal-carry neutral output sum; low/low<=6 and high/high<=2; global reflected-pair bound; actual no-overflow output width; low-pair arithmetic palindrome; two-step composition; integer representative with all required carry equalities. No desired palindrome condition appears as a hypothesis.

Verification: pinned Lean4.19.0 and manifest-driven fresh source chain, twice; every exported theorem axiom report inspected; only propext/Classical.choice/Quot.sound allowed; all errors rejected. Self-verification is not independent review. Full overflowing four-step theorem and sharpness remain separate targets.
