# Agent #109 — Lean bridge for the complementary two-gap template

Task record: `proofs/coordination/tasks/agent109-template-step-bridge.json`
(branch `p196/coordination`). Contribution branch: `research/agent-109/s20261015`.

**Status: LEAN-CHECKED (local fresh build, Lean 4.19.0 commit `6caaee842e94`).
Not yet independently reviewed. No cycle, no safe orbit, no Lychrel witness and
nothing about 196 is claimed.**

## What this closes

[`2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`](../../../2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md)
states the actual whole-word identities (5) and (8) with written proofs only
("have not been formalized in Lean"). Agent #8's
[`PeriodObstructions.lean`](../../../2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean)
works with word-level `stepWord`/`template` and records that "the ordinary
whole-word exterior and width bridge is written, not yet integrated". The
`agent101-exterior-cap56` task lists the exterior projection formulas as "not
yet Lean-bridged". This package kernel-checks:

1. **Identity (5)** — `Agent109.norm_template`, `Agent109.normalize_template`:
   for every phase `c ∈ {1,…,17}∖{9}`, all blocks `B,A,C` with coefficients
   `≤ 18`, and all band lengths `g+1,h+1 ≥ 1`, the actual carry normalization of
   `template c B A C (g+1) (h+1)` (Agent #8's definition, verbatim) is the explicit
   digit word `digitWord` built from `N(B,0), N(A,k_c), N(C,k_d), N(rev A,k_d),
   N(rev B,k_c)` and `u_0…u_3`, followed by the overflow digit iff `γ ≠ 0`; and
   `γ ≤ 1` (`gamma_le`).
2. **Identity (8)** — `Agent109.stepWord_template`:
   `stepWord (template c B A C (g+2) (h+2)) =
    template (2 t_c) (Br …) (Ar …) (Cr …) (g+γ) (h+γ)` with `Br, Ar, Cr`
   exactly the blocks (6) (`γ = 0`) or (7) (`γ = 1`). Symmetry of `C`, even
   middle and a positive exterior are *not* needed at word level.
3. **Integer bridge** — with verbatim copies of the accepted
   `Lychrel196.reverse10/step/Palindrome/orbit`:
   * `pairWord_step : pairWord (step n) = stepWord (pairWord n)` for **every**
     natural `n`, where `pairWord n = pair (digits n)`;
   * `pairWord_orbit : pairWord (orbit n k) = orbitWord (pairWord n) k`;
   * `actual_template_step`: an integer whose pair word is a template steps to
     an integer whose pair word is the returned template;
   * `palindrome_iff`, `step_palindrome_iff`, `actual_template_palindrome_iff`:
     `step n` is a palindrome iff the normalized word (for templates: the
     explicit digit word (5) with overflow digit) is a list palindrome.
4. **Compatibility** (`Compat.lean`, importing the unmodified originals):
   the copies equal `Agent8.zipAdd/pair/normalize/stepWord/template/orbit` and
   `Lychrel196.reverseFuel/reverse10/step/Palindrome/orbit`; the bridge is
   restated with the original constants, and
   `Agent109.Compat.isLychrel_iff`:
   `Lychrel196.IsLychrel n ↔ ¬Palindrome n ∧ ∀ k, (Agent8.normalize
   (Agent8.orbit (pairWord n) k) 0).reverse ≠ Agent8.normalize (Agent8.orbit
   (pairWord n) k) 0`.
   So any word-level returned-template construction proved with Agent #8's
   definitions now transfers to ordinary reverse-and-add without a written step.

## What is not done here

* No search for, or claim of, a returned interface; no safety of any template
  orbit beyond the stated equivalences.
* Agent #8's `no_repeatable_six_step_template_return` still takes its
  `p/e/evolves/hWidth` premises; deriving them from `stepWord_template`
  (exterior coefficient of `Br` and the length bookkeeping `|step| = |w|+γ`) is
  a natural follow-up, not done in this checkpoint.
* Realizability of every admissible template by an integer is not re-proved here
  (the Python controls construct realizations; the accepted
  `Lychrel196Research` module has a separate constructive-realization result).

## Verification

`./build.sh <repo-root>` copies the unmodified `LychrelDigitSums.lean` and
`PeriodObstructions.lean` into a fresh temporary directory, compiles everything
from source (no reused `.olean`), prints all axiom reports and scans the
Agent #109 sources for `sorry/admit/native_decide/ofReduceBool/axiom`.
`build_log.txt` is the retained log (source SHA-256s, exit codes, axiom
reports). Every exported theorem depends only on `propext`, `Classical.choice`,
`Quot.sound` (some on fewer). The kernel sanity example in `Audit.lean` uses
ordinary `decide`.

`controls.py` is an independent Python implementation: 200,000 random admissible
templates (all 16 phases, `|B|,|A| ≤ 4`, symmetric `|C| ≤ 5`, `g,h ∈ 2..7`) are
realized by ordinary integers, stepped with Python big-integer `n+reverse(n)`,
and compared with formulas (5), (6)/(7), (8) and the palindrome criterion:
`controls_result.json` — PASS (104,097 overflow cases). This is a formula
control, not a search.
