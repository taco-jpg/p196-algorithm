# Agent #13 — original real safe-weight obstruction

Source: `proofs/research/main_existence_attempt/continuation_pass/finite_seed/FINITE_SEED_OBSTRUCTIONS.md`, section 3, at `c2b6977e43a79caa5ff3bb88801f3ba896986f38`. Task: `agent13-real-safe-weight-obstruction`, published through non-force expected-head update at `7d20cc08ec07d1db7b9441ab5fdbce91f29e5747`.

## Exact statements and quantifiers

Let `S n` mean `0 < n`, `not Lychrel196.Palindrome n`, and `not Lychrel196.Palindrome (Lychrel196.step n)`, using the unchanged actual decimal definitions. Let `w : Nat -> Real`. Assume only positivity on `S` and nonincrease on `S`: for any safe `n <= y`, `w y <= w n`. No sign or monotonicity assumptions outside `S` may silently strengthen this contract.

Define the full finite incoming sum `I(w,y) = sum_{n in S, step n = y} w(n)`. A finite range implementation must prove that it includes every actual positive predecessor; the chosen constructed family alone is not the definition of this sum.

For every such `w` and every natural `m >= 2`, prove

`I(w,y_m) / w(y_m) >= 9*10^(m-2)`,

where `y_m = 10^(2*m)+99*10^(m-1)-1`. Prove equivalently the multiplication form using positive `w(y_m)`. Then prove that for every real `C` there exists a safe `y` with `C*w(y) < I(w,y)`. Equivalently, no finite real uniform multiplier exists. This includes negative `C` without an unnecessary assumption `C >= 0`.

Separately prove the original strict quantitative lower bound

`(9/100)*Real.sqrt(10/11)*Real.sqrt(y_m) < I(w,y_m)/w(y_m)`.

Natural-to-real coercions and all constants must be exact, not floating-point. The width hypothesis `m>=2`, positivity of the division denominator, complete incoming fiber, and arbitrary real weights are part of semantic review.

## Dependencies and architecture

Reuse `Agent13SafeFamily.safe_predecessor_family`, `predecessor_complete`, and `safe_fibers_unbounded` from `8b1e5d15b94ea67bbb8a522b40ba6643c17ef5ee`; their 36 new declarations and shared Std-only decimal dependency already passed full transitive audits and a fresh local rebuild. The original decimal sources and standalone build remain unchanged.

The source statement genuinely quantifies over real numbers. Add an isolated Mathlib extension at commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`, whose toolchain is the same existing Lean 4.19.0. Preserve its exact dependency manifest. Official compiled-library cache retrieval is development infrastructure, not an independent source rebuild or theorem verification. Record imported source pins and transitive axioms and perform a clean contribution rebuild before accepting the new results.

## Acceptance and exclusions

Each endpoint must compile, preserve the exact contract, and have complete `#print axioms` output containing no axioms beyond `propext`, `Classical.choice`, and `Quot.sound`. Exclude `sorry`, `admit`, compiler-trusted evaluation, new mathematical axioms, hidden target premises, and abstract-only or rational-only replacements. Preserve all failed attempts and substantive logs outside accepted build targets.

This excludes one specified nonincreasing-weight method. It does not exclude arbitrary target-dependent weights or prove decimal Lychrel existence, a 196 orbit property, novelty, external peer review, or exhaustive source coverage. Independent review remains a separate requirement.
