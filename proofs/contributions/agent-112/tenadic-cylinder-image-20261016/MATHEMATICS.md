# Agent #112: Exact unit-digit image of a decimal-adic cylinder

**Status: LEAN-CHECKED for the original four named unit-digit endpoints.** Official Lean 4.19.0, `--trust=0`, compiled the original pinned proof sources and `CylinderImage.lean` at source commit `5ae76379f06ea958e209856c26722468068502d2`; see [Actions run 38972297131](https://github.com/taco-jpg/p196-algorithm/actions/runs/38972297131). All four audited endpoints use only `propext`, `Classical.choice`, `Quot.sound`. The initial WIP revision was uncompiled; its actual three failing CI revisions and corrections are preserved in branch history. Independent semantic review and shared accepted-build integration are still pending. Python finite controls alone do not prove a universal theorem. No statement here resolves P196 or produces a positive Lychrel seed.

## Exact target and interpretation

Let `R(m)` reverse the ordinary base-ten digits of a **positive finite integer** `m`, dropping any leading zeroes in the reversed output. Define `T(m)=m+R(m)`. For `k>=1` and `0<=a<10^k`, let

`C(k,a) = {m in positive integers : m mod 10^k = a}`.

The established, kernel-checked Nat theorem is

`{T(m) mod 10 : m in C(k,a)} = {(a+c) mod 10 : 1<=c<=9}`.

There are exactly nine residues in this image, namely all of `0,1,...,9` **except** `a mod 10`.

## Elementary proof and correspondence with the kernel formalization

**Necessity:** If `m>0`, let `c` be the first (most significant) digit of its ordinary decimal representation. Then `1<=c<=9`, and the last digit of `R(m)` is `c`. Since `k>=1`, the congruence `m mod 10^k=a` forces `m mod 10=a mod 10`. Thus `T(m) mod10=(a+c) mod10`.

**Sufficiency:** For each digit `c` from 1 through 9, take the explicit positive witness `m=c*10^k+a`. The assumption `a<10^k` makes this an ordinary `(k+1)`-digit integer with first digit `c`; its last `k` digits are exactly the zero-padded `k`-digit representation of `a`. Therefore `m mod10^k=a`, `R(m) mod10=c`, and `T(m) mod10=(a+c) mod10`. Addition by fixed `a` is a bijection modulo 10, and the nine distinct choices `1<=c<=9` give nine distinct output residues, omitting exactly `a mod10`.

**Topological implication (written, not a Lean topology theorem):** Every basic cylinder in the 10-adic completion contains positive finite integers with nine distinct `T`-outputs modulo 10. Consequently there is no point of that completion at which a function agreeing with `T` on all positive natural integers can be continuous. At any proposed continuity point, continuity to a fixed output residue modulo 10 would require a sufficiently small input cylinder to have constant output residue, contradicting the nine-way image.

This strengthens the earlier preserved written observation of discontinuity *at each finite positive integer* to a uniform statement applying to **every** decimal-adic point. The mathematical mechanism and predecessor paper are not new; the exact nine-residue classification and its Lean-checked endpoint are this task's separate scope, subject to formal checking.

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

The official CI verifier in `.github/workflows/agent112-cylinder-image.yml` restores archived original module imports, checks source blob identities, builds using the authenticated Lean 4.19.0 official release with `--trust=0`, and records all exported endpoint axiom dependencies. The first successful run for the four original endpoints is [38972297131](https://github.com/taco-jpg/p196-algorithm/actions/runs/38972297131); the corresponding original Lean source blob was `e87e83d024d6a408cde25a2532cb214edeee4a7a`. Subsequent editorial changes must be rechecked at their own source hashes. The four original endpoints are **LEAN-CHECKED**, not independently reviewed or integrated; the separate `CylinderNoContinuity.lean` consequence is WIP until its own run passes.
