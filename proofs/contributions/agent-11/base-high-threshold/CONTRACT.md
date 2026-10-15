# Agent 11: exact all-base high-region threshold contract

Source snapshot: `74df59c5ecb6cb30fb3c88b1d5b26fdb9526d6c4`.
Source: `proofs/contributions/2026-10-15-seam-persistence-obstruction/SEAM_PERSISTENCE_OBSTRUCTION.md`, section "Exact second-step criterion on the larger high-coefficient region", equations (8) and (9).
Ownership publication: `fb22faec3af58e1baa26ad5357426befc53fc817` on `p196/coordination`.

## A. Original claims

For every integer base b>=3 and every nonempty canonical symmetric full pair word q of width L, suppose b-1<=q_i<=2b-2 for every original column and q_0>=b. Put r_i=q_i-b+1. Actual carry normalization has width L+1 and digits (r_0-1,r_1,...,r_(L-1),1). Its pair word is exactly (r_0,r_0+r_1,...,r_(L-2)+r_(L-1),r_0). The second ordinary reverse-add output is palindromic iff q_(i-1)+q_i<=3b-3 for every 1<=i<L.

## B-C. Intended propositions and existing definitions

Use the existing Int/list base framework and unchanged definitions `SignedDigitUniqueness.eval`, `PhysicalWidth.actualDigits`, `ReverseAdd.pairs`, `ReverseAdd.DigitBounds`, and `PhysicalWidth.PositiveLast`. Convenience wrappers only add false reset tags and perform the actual normalized pair step. The exact list formula will be exported as `Agent11HighBase.next_pairs_formula`; the palindrome iff as `Agent11HighBase.second_palindrome_iff_adjacent`; the canonical numeral/value composition as `Agent11HighBase.numeric_two_step_threshold`. Supporting lemma names may be added without changing these mathematical contracts.

Adjacency may be represented by a recursively computed list of adjacent sums or equivalent zipWith expression. An explicit theorem must identify this with every pair of consecutive columns; a bounded test is not the final proposition.

## D-E. Hypotheses and quantifiers

Quantification is uniform over all bases b>=3, all finite widths L>=1, and all qualifying full coefficient words. Symmetry, coefficient bounds and the positive high outside coefficient are explicit. The actual integer corollary quantifies over all valid low-to-high base-b digit lists with positive most significant digit whose reflected pair sums satisfy those bounds. In odd widths, realizability automatically supplies the even central sum; no new parity assumption is silently discarded in the numeric theorem.

## F. Boundaries

L=1 has empty adjacent-sum list and next word (r_0,r_0). Leading zeros in an original numeral are disallowed by PositiveLast; a reversed word may have leading zeros and its arithmetic value remains the ordinary reversal. Actual output width includes overflow and excludes a zero terminal slot. The dynamics continue after a palindrome: neither the first step nor the initial seed is required to be nonpalindromic. Base two is excluded for a substantive reason; retain a checked binary counterexample. Base three and odd-base cases must be included.

## G. Exact correspondence and exclusions

The arbitrary symmetric-word statements may cover additional non-realizable coefficient words, which strengthens the structural claims. They do not replace the canonical arithmetic corollary. No invariance of the high region, no indefinitely safe trajectory, no Lychrel existence and no claim for 196 follows. Existing decimal coverage in HighCarryReduction.lean is credited; this is formalization of the already written all-base result, not original discovery.

## H. Dependencies

Lean 4.19.0, Std only, no Mathlib. Build exact pinned sources in order: SignedDigitUniqueness, BaseReflection, ResetNormalization, PhysicalWidth, SeamSafety, ReverseAdd, then Agent 11 modules. Reuse palindrome-predecessor classification, actual canonical digit bounds, symmetry, positivity and numeric normalization. No dependency migration or unrelated-file changes.

## I-J. Acceptance and audit

First clean-build unchanged dependencies and record any prior failures separately. Compile every actual module; generate #print axioms for every exported theorem and every prerequisite theorem, requiring only propext, Classical.choice and Quot.sound. Disallow sorry/admit/sorryAx, introduced mathematical axioms and compiler-trusted evaluation shortcuts throughout the proof chain. Build twice in distinct clean directories, hash source bytes, retain commands, exit statuses, substantive attempt logs and axiom output. Separate self-review, clean rebuild, external CI checking and genuinely independent semantic review. New CI must include the actual modules; source presence alone is not acceptance.

## Initial scope census

The selected pinned source corpus contains 2196 locally extracted text files, including 243 Lean files, with checked manifest hashes. This is discovery metadata, not exhaustive semantic claim coverage. Archives, large excluded sources, all changing contribution branches and historical claim deduplication remain explicit gaps. The scoped claim inventory will track UPDATE, IFF and NUMERIC separately; a supporting lemma does not close any stronger target.
