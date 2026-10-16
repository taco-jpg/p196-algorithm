# Agent #112: Exact unit-digit image of a decimal-adic cylinder

**Status: WIP for Lean acceptance.** The elementary argument below is a written proof; the proposed `CylinderImage.lean` is **not compiled** in this execution environment. The finite Python controls are not a proof of a universal theorem. No statement here resolves P196 or produces a positive Lychrel seed.

## Exact target and interpretation

Let `R(m)` reverse the ordinary base-ten digits of a **positive finite integer** `m`, dropping any leading zeroes in the reversed output. Define `T(m)=m+R(m)`. For `k>=1` and `0<=a<10^k`, let

`C(k,a) = {m in positive integers : m mod 10^k = a}`.

The proposed complete Nat theorem is

`{T(m) mod 10 : m in C(k,a)} = {(a+c) mod 10 : 1<=c<=9}`.

There are exactly nine residues in this image, namely all of `0,1,...,9` **except** `a mod 10`.

## Elementary proof for a future kernel formalization

**Necessity:** If `m>0`, let `c` be the first (most significant) digit of its ordinary decimal representation. Then `1<=c<=9`, and the last digit of `R(m)` is `c`. Since `k>=1`, the congruence `m mod 10^k=a` forces `m mod 10=a mod 10`. Thus `T(m) mod10=(a+c) mod10`.

**Sufficiency:** For each digit `c` from 1 through 9, take the explicit positive witness `m=c*10^k+a`. The assumption `a<10^k` makes this an ordinary `(k+1)`-digit integer with first digit `c`; its last `k` digits are exactly the zero-padded `k`-digit representation of `a`. Therefore `m mod10^k=a`, `R(m) mod10=c`, and `T(m) mod10=(a+c) mod10`. Addition by fixed `a` is a bijection modulo 10, and the nine distinct choices `1<=c<=9` give nine distinct output residues, omitting exactly `a mod10`.

**Topological implication (written, not a Lean topology theorem):** Every basic cylinder in the 10-adic completion contains positive finite integers with nine distinct `T`-outputs modulo 10. Consequently there is no point of that completion at which a function agreeing with `T` on all positive natural integers can be continuous. At any proposed continuity point, continuity to a fixed output residue modulo 10 would require a sufficiently small input cylinder to have constant output residue, contradicting the nine-way image.

This strengthens the earlier preserved written observation of discontinuity *at each finite positive integer* to a uniform statement applying to **every** decimal-adic point. The mathematical mechanism and predecessor paper are not new; the exact nine-residue classification and its proposed Lean endpoint are this task's separate scope, subject to formal checking.

## Boundary conditions and caveats

- The restriction `k>=1` is essential. For `k=0`, all positive inputs lie in the same residue class modulo 1 and outputs divisible by 10 exist, e.g. `T(19)=110`.
- The restriction `a<10^k` is essential because a raw remainder can never equal a larger integer.
- The witness `c*10^k+a` remains canonical when `a=0` or its padded suffix has leading zeros. Do not silently use a truncated suffix representation to change the actual input width.
- The claim is **not** about the existence or nonexistence of palindromes in an orbit. It rules out an unaugmented 10-adic continuity argument and is consistent with adding extra leading-digit or two-sided symbolic state.

## Dependencies and source pins

- `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/astra_modular_fixed_modulus_theorem.md`, section 4, records the old explicit perturbation `n+c*10^j` and discontinuity at natural points.
- `proofs/astra_lean_modular__af14192db66453cd.lean` includes the existing canonical lemma `reverse10_mod10` and ordinary `Lychrel196.step` semantics in the original module namespace.
- `proofs/LeadingWitness__02bd58af5fbf790b.lean` provides reusable exact-width constructors `canonical_of_pow_bounds`, `canonical_lead_of_interval`; it already handles two distinct leading digits modulo a fixed modulus. This contribution depends on that source and is not a claim to have invented digit perturbations.

## Reproduction and acceptance gates

Run `python3 verify_cylinder.py` from this directory and compare exact JSON with `verification/finite-controls.json`. It verifies 800,000 forward modular instances, independently compares decimal arithmetic with string reversal for 200,000 inputs, and tests 14,202 constructed canonical witnesses. It cannot validate quantifiers over all naturals.

To upgrade `CylinderImage.lean`, first restore the pinned original-layout module imports as required by the project's migration/replay policy, compile with official Lean 4.19.0 and `--trust=0`, inspect each `#print axioms` output, and obtain independent semantic plus clean-build review. Until that succeeds, **all Lean endpoints are proposals**, not checked results.