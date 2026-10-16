# Agent #109 — a complementary template step is never a palindrome

Task record: `proofs/coordination/tasks/agent109-template-step-safety.json`.

**Status: LEAN-CHECKED (fresh from-source build, Lean 4.19.0 `6caaee842e94`,
`build_log.txt`). Not independently reviewed. No infinite safe orbit, no Lychrel
witness, nothing about 196.**

## Statement

For the complementary two-gap template of
`2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`, with phase
`c ∈ {1,…,17}∖{9}` and blocks with coefficients at most 18:

* `Agent109.NoPal.not_stepPal`: the band-length-independent palindrome criterion
  `Agent109.Cert.StepPal c B A C` is **always false**.
* `template_step_not_palindrome`: if `pairWord n = template c B A C (g+2) (h+2)`,
  then `step n` is not a palindrome — for every ordinary integer `n` and all band
  lengths ≥ 2.
* `template_orbit_safe` (and `Agent109.NoPalCompat.lychrel_template_orbit_safe`
  with `Lychrel196.orbit`/`Lychrel196.Palindrome`/`Agent8.template`): if `n`
  realizes a template whose two bands are both at least `2k+2`, then the ordinary
  orbit has no palindrome at times `1, …, k+1`.

So within this family a palindrome can only appear after a band has shrunk below
two; long complementary bands give provably long palindrome-free stretches. This is
finite-time safety, not an all-time result. It also shows the non-palindrome
conjunct of `Agent109.Cert.check` is automatically satisfied: a return
certificate needs only exact closure and nonnegative gap gains.

## Proof idea

`StepPal` (proved exact and band-length independent in
`template-return-certificate/`) would force a mirrored equality of normalized
blocks. Normalization preserves digit sum plus carries modulo nine
(`norm_mod9`). Without overflow, the interface condition forces the outgoing
carries of `A` and of `rev A` to equal the complementary band carries, and then
`k_c ≡ k_d (mod 9)`, contradicting `k_c + k_d = 1`. With overflow, the exterior
condition forces `c ≡ 2k_c (mod 9)` and the interface condition
`2c − 18 ≡ 11(k_c − k_d) (mod 9)`; no phase satisfies both. Iterating the
exact step (`Agent109.actual_template_step`) with bounded successor blocks gives
the orbit statement (bands lose at most two per step).

## Evidence

* `build.sh <repo-root>` rebuilds from the unmodified sources in an empty
  directory; axioms `propext`, `Classical.choice`, `Quot.sound` only.
* `nopal_control.py`: 3,000 random realized templates with bands ≥ 2k+2
  (k ≤ 10), ordinary big-integer reverse-and-add, no palindrome at times
  1..k+1 (`control_result.json`). Also 300,000 random states and 12,000
  literal-integer comparisons in `../template-return-certificate/` never showed a
  palindromic step, consistent with the theorem.
