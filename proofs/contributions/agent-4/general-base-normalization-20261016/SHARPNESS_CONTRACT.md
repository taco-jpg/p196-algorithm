# Agent #4 — universal even-base sharpness contract

Source: SHARPNESS in proofs/research/resume_even_base_normalization_proof.txt at2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, blob57716e4f6c25d19d96b8c502237b523b25b5fb52. Serialized ownership: f546b9e06d404c4c02cc6387056831cc1da3d0da, task agent4-even-base-sharpness-20261016.

Exact target: for every even b>=10, every canonical five-digit natural in first-carry class(0,0,0,1,1,1) is nonpalindromic at each time0,1,2,3; an explicit positive canonical member has first palindrome at time4, namely2102012_b. The all-class four-step upper bound is separate and remains unproved here.

The universal quantifier ranges over every genuine digit representative, not just pair coefficients chosen in advance. First prove every such word has coefficients(b-1,b-1,b+2r,b-1,b-1) for one integer0<=r<b/2. Then verify the source's three symbolic output vectors by certificate rows, with independently proved digit bounds and actual widths5,6,7,7. A generic proved schoolbook checker is not enough: every universal-base instance and the numeric composition must also be checked. Finally instantiate r=0 with the original explicit seed and verify the fourth-step palindrome and positive leading digit.

Encoding: finite Nat-indexed digit/carry functions whose relevant prefix has an explicit width. Out-of-prefix values are irrelevant to all claims. `value`, `integerDigit`, `CanonicalNumeral`, `addAtWidth`, quotient carries, and numerical reversal are the previously checked arithmetic definitions. A mismatch at a genuine mirrored digit position proves inequality of the actual numeral and its reverse by digit extraction, even when the reversed value loses leading zeroes.

Boundary cases: r=0 and r=b/2-1 included; b=10 included; division(4r+1)/b and its remainder are proved with Euclidean identities, not assumed0; carry changes and both overflow widths are explicit. Original-time nonpalindromicity is proved separately from positive-time nonpalindromicity.

Verification: exact Lean4.19.0, every exported axiom report, transitive imported chain checked in each of two fresh source directories. No new mathematical axioms, compiler-trusted decisions or unproved row certificates. This remains ACTIVE_FORMALIZATION until all instances and endpoints pass. Review remains self-review until another genuine reviewer acts.
